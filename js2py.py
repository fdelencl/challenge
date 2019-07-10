from .jsInterpreter import interprete, parse

from ast import AST, Module
from typing import Dict, Any


def transform(js: str) -> AST:
    parse_tree = parse(js)
    node = interprete(parse_tree)
    return Module(node)

def js2py(js: str, context: Dict[str, Any]) -> Dict[str, Any]:
    ast = transform(js)
    
    code = compile(ast, filename='<ast>', mode='exec')
    exec(code, context)
    del context['__builtins__']
    return context
