from arpeggio import *
from arpeggio import RegExMatch as _
from typing import List, Any

# PEG Grammar for Arpeggio (Python version)
# https://github.com/textX/Arpeggio/blob/master/docs/grammars.md
def integer():       	return _(r'[+|-]?\d+')
def floatingpoint(): 	return _(r'[+|-]?\d*\.\d*')
def string():        	return _(r'".*?"|\'.*?\'')
def nameconstant():  	return _(r'true|false')
def literal():       	return [nameconstant, integer, floatingpoint, string]
def name():          	return _(r'[a-z|A-Z]\w*')
def attribute():     	return _(r'[a-z|A-Z]\w*')
def subscript():     	return [(name, OneOrMore([("[", [integer, string, name], "]"), (".", attribute)]))]
def termoperator():  	return _(r'\+|\-')
def factoroperator():	return _(r'\*|\/')
def booloperator():  	return _(r'&&|\|\|')
def cmpoperator():   	return [_(r'==|!=|<=|>=|<|>')]
def boolop():        	return [OneOrMore([cmpop]), literal, subscript, name], booloperator, [expression]
def termop():        	return [OneOrMore(factorop), literal, subscript, name], termoperator, [expression]
def factorop():      	return [literal, subscript, name], factoroperator, [factorop, literal, subscript, name]
def cmpop():         	return [literal, subscript, name], cmpoperator, [cmpop, literal, subscript, name]
def assignation():   	return [subscript, name], _(r'\='), [expression]
def expression():    	return [boolop, cmpop, factorop, termop, assignation, literal, subscript, name]
def ifstatement():   	return "if", "(", expression, ")", block, Optional("else", block)
def statement():     	return [ifstatement, expression]
def block():         	return "{", ZeroOrMore(statement), "}"
def javascript():    	return OneOrMore(statement, _(r';?'))

# Parser initialization
# https://github.com/textX/Arpeggio/blob/master/docs/configuration.md
# To visualize the parse tree result:
# https://github.com/textX/Arpeggio/blob/master/docs/debugging.md#visualization
js_parser = ParserPython(javascript, debug=False, reduce_tree=False)

def parse(js: str) -> List:
    if not len(js):
        return []
    return js_parser.parse(js)
