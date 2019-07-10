from ast import *
from arpeggio import visit_parse_tree, PTNodeVisitor
from .parser import js_parser

binoperator = {
	"+": Add,
	"-": Sub,
	"*": Mult,
	"/": Div
}

booloperator = {
	"||": Or,
	"&&": And
}

cmpoperator = {
	'==': Eq,
	'!=': NotEq,
	'<': Lt,
	'<=': LtE,
	'>': Gt,
	'>=': GtE
}

# converting parse tree to AST nodes
# AST node documentation:                     https://docs.python.org/2/library/ast.html#abstract-grammar
# Arpeggio parse_tree visitors documentation: https://github.com/textX/Arpeggio/blob/master/docs/semantics.md
class JsParseTreeVisitor(PTNodeVisitor):
	def visit_integer(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		return Num(n=int(node.value), lineno=line, col_offset=col)

	def visit_floatingpoint(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		return Num(n=float(node.value), lineno=line, col_offset=col)

	def visit_string(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		return Str(s=node.value[1:-1], lineno=line, col_offset=col)

	def visit_nameconstant(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		v = True if (node.value == "true") else False
		return NameConstant(value=v, lineno=line, col_offset=col)

	def visit_literal(self, node, children):
		return children[0]
		
	def visit_name(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		return Name(id=node.value, ctx=Load(), lineno=line, col_offset=col)

	def visit_attribute(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		return Str(s=node.value, lineno=line, col_offset=col)

	def visit_subscript(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		node = children[0]
		for child in children[1:]:
			s = Index(value=child, ctx=Load(), lineno=line, col_offset=col)
			node = Subscript(value=node, slice=s, ctx=Load(), lineno=line, col_offset=col)
		return node

	def visit_termoperator(self, node, children):
		return node.value

	def visit_factoroperator(self, node, children):
		return node.value

	def visit_booloperator(self, node, children):
		return node.value

	def visit_cmpoperator(self, node, children):
		return node.value

	def visit_termop(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		op = binoperator[children[1]]()
		return BinOp(left=children[0], op=op, right=children[2], lineno=line, col_offset=col)

	def visit_factorop(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		op = binoperator[children[1]]()
		return BinOp(left=children[0], op=op, right=children[2], lineno=line, col_offset=col)

	def visit_boolop(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		op = booloperator[children[1]]()
		return BoolOp(values=[children[0], children[2]], op=op, lineno=line, col_offset=col)

	def visit_cmpop(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		ops = [cmpoperator[children[1]]()]
		return Compare(left=children[0], ops=ops, comparators=[children[2]], lineno=line, col_offset=col)

	def visit_assignation(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		children[0].ctx = Store()
		return Assign(targets=[children[0]], value=children[2], lineno=line, col_offset=col)

	def visit_expression(self, node, children):
		return children[0]

	def visit_ifstatement(self, node, children):
		line, col = js_parser.pos_to_linecol(node.position)
		t = children[0]
		b = children[1]
		o = [] if len(children) == 2 else children[2]
		return If(test=t, body=b, orelse=o, lineno=line, col_offset=col)

	def visit_statement(self, node, children):
		return children[0]

	def visit_block(self, node, children):
		return children

	def visit_javascript(self, node, children):
		return children


def interprete(parse_tree) -> AST:
	if not len(parse_tree):
		return []
	result = visit_parse_tree(parse_tree, JsParseTreeVisitor(debug=False))
	return result