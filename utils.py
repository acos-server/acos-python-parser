import ast, json, sys, re, os
from ast import Load,Store, For, If, While, Call, Add, Sub
from os import path
from webbrowser import get
from tqdm import tqdm
import pandas as pd
from ply.lex import lex
from version import __developer__

# These nodes will be ignored and are not added to the node list.
#
# For example, the operators are skipped b  ecause the actual operator
# will be added to the list instead of the operator family.
nodesToSkip = {'Store', 'Load', 'Name', 'Expr', 'arg', 'arguments','Subscript', 'BoolOp', 'BinOp', 'Compare', 'UnaryOp'} ## we skip these because this data can be parsed with other nodes
tokensToSkip = {}
associated_py_concepts = json.load(open(path.join(path.dirname(__file__), './static/py_keyword_functions.json'))) ## function keywords associated concepts
op_py_concepts = json.load(open(path.join(path.dirname(__file__), './static/py_ops.json')))


# *****************************************************************************
# Special handlers for some nodes

def handleNameConstant(node, line):
    """ Converts the NameConstant node to represent the type of the value (True, False, None). """
    return str(node.value)

def handleNum(node, line):
    """ Converts the Num node to represent the type of the value (Int, Float). """
    return node.n.__class__.__name__.capitalize()

handlers = {'Num' : handleNum, 'NameConstant' : handleNameConstant}

def get_name_from_ast_object(node,type_name):
    if type_name == 'Name':

        name = node.__dict__['id'] if 'id' in node.__dict__ else \
            ','.join([x.__dict__['id'] for x in node.__dict__['elts']]) if 'elts' in node.__dict__ else ''

        if name.endswith('Error'): return 'Exception-Types'
        
        if name in associated_py_concepts: return associated_py_concepts[name].capitalize()
        if type(node.__dict__['ctx']) == Store: return 'Variable-decl-or-assign'
        if type(node.__dict__['ctx']) == Load: return "Variable-usage"
    
    if type_name == 'Attribute':
        # pass
        name = node.__dict__['attr']
        if name.endswith('Try') or name.endswith('ExceptHandler'): return 'Exception-Handler'
        if name in associated_py_concepts: return associated_py_concepts[name].capitalize()
        return name

    if type_name == 'Call':
        
        CallObjectDict = node.__dict__['func'].__dict__
        CallObjectNode = node.__dict__['func']

        lineno = CallObjectDict['lineno']
        
        if False: print(CallObjectNode.__class__.name,
            CallObjectDict,
            CallObjectDict['id'] if 'id' in CallObjectDict['id'] else CallObjectDict['value'],
            CallObjectDict['ctx']
        )

        if 'id' in CallObjectDict:
            return f"{associated_py_concepts[CallObjectDict['id']].capitalize()}" if CallObjectDict['id'] in associated_py_concepts else 'Class-Obj-Instantiate'

        elif 'attr' in CallObjectDict:
            return f"{associated_py_concepts[CallObjectDict['attr']].capitalize()}" if CallObjectDict['attr'] in associated_py_concepts else 'ClassMethod-or-Function-Call'
        
        else: f"Parsed Concept {type_name}: this should not happen -- email {__developer__}"

    else:
        
        if type_name in op_py_concepts:
            # print(type)
            return op_py_concepts[type_name].capitalize()
    
    return type_name.capitalize()


def handle_nested_if(node_dict_body_or_else,name):
    if len(node_dict_body_or_else) == 0:  return name


    if len(node_dict_body_or_else) > 0:
        count_expr = 0
        for elements in node_dict_body_or_else: 
            if type(elements) == If: return f'Nested-{name}'
            if not(type(elements) == If): count_expr += 1
        if count_expr == len(node_dict_body_or_else): return 'if-else'
        



# *****************************************************************************

def simpleTraverse(node, line, nodes,prev_node = None):

    name = node.__class__.__name__
    lineno = node.__dict__['lineno'] if 'lineno' in node.__dict__ else 0#node.__dict__[''].__dict__['lineno']
    # if name == 'Constant': print(re.split(r'[<,\s,>,\']',str(type(node.__dict__['value']))))
    # if name == 'Call': print(node.__dict__['func'].__dict__['id'])
    # print(prev_node)
    name = 'if-elif' if name.lower() == 'if' and not(prev_node == None) and type(prev_node) == If else name

    prev_node = node.__dict__['orelse'][0] if name.lower() == 'if' and \
                len(node.__dict__['orelse']) > 0 and\
                 type(node.__dict__['orelse'][0]) == If \
                else node if prev_node == None else prev_node
    
    if name.lower() == 'if' or name.lower() == 'if-elif': 
        # print(node.__dict__)
        name1 = f"{handle_nested_if(node.__dict__['body'],name.lower())}"
        name2 = f"{handle_nested_if(node.__dict__['orelse'], name.lower())}"
        name = name1 if name1.startswith("Nested") else name2


    if (name.lower() =='for' or  name.lower() == 'while'):
        name = name
        # print(node.__dict__)
        if name.lower() == 'while' and len(node.__dict__['orelse']) > 0: name = f'{name}-else'.capitalize()
        if name.lower() == 'while': f"{name}-{get_name_from_ast_object(node.__dict__['test'],'')}".capitalize()
        if name.lower() == 'for' and type(node.__dict__['iter']) == Call: name = f"{name}-{get_name_from_ast_object(node.__dict__['iter'],'Call')}-{get_name_from_ast_object(node.__dict__['target'],'Name')}".capitalize()

        for elements in node.__dict__['body']:
            if type(elements) == For or type(elements) == While: name = f'Nested-{name}'.capitalize()
    
            # if type(elements) == Expr:
                # print(elements)
                # simpleTraverse(elements,node.__dict__['lineno'],nodes)

    if name.lower() == 'keyword':
        name = f"keyword-args:{node.__dict__['arg']}"

    if name.lower() == 'augassign':
        if type(node.__dict__['op']) == Add: name = "Assignment-with-Add"
        if type(node.__dict__['op']) == Sub: name = "Assignment-with-Sub"

    if name == 'Name':
        # print(name,node.__dict__)
        # print(name, prev_node.__dict__)
        
        name = get_name_from_ast_object(node,'Name')
            

    if name == 'Attribute':
        # print(name, node.__dict__['attr'].capitalize(), node.__dict__['value'].__dict__['id'],prev_node.__dict__)
        
        name = get_name_from_ast_object(node,'Attribute')


    if name == 'Constant':
        # print(name, node.__dict__)
        name = re.split(r'[<,\s,>,\']',str(type(node.__dict__['value'])))[3].capitalize()
        

    if name == 'Call':  

        name = get_name_from_ast_object(node,'Call')

    else:
        if name not in nodesToSkip:
            
            name = get_name_from_ast_object(node,name)
        

    if name not in nodesToSkip:
        if line not in nodes['lines']:
            nodes['lines'][line] = set()
        if name not in handlers:
            
            nodes['lines'][line].add(name)
        else:
            nodes['lines'][line].add(handlers[name](node, line))

    for child in ast.iter_child_nodes(node):
        simpleTraverse(child, line, nodes, prev_node)

def complexTraverse(node, line, nodes):

    name = node.__class__.__name__

    # Only some nodes contain line number
    if hasattr(node, 'lineno'):
        line = node.lineno

    endLine = line

    current = {'name': name, 'startLine': line}

    if name not in nodesToSkip:
        if line not in nodes['lines']:
            nodes['lines'][line] = []
        if name not in handlers:
            nodes['lines'][line].append(current)
        else:
            current['name'] = handlers[name](node, line)
            nodes['lines'][line].append(current)

    maxLine = endLine
    for child in ast.iter_child_nodes(node):
        maxLine = max(maxLine, complexTraverse(child, line, nodes))

    if maxLine != line:
        current['endLine'] = maxLine

    return maxLine

def hierarchicalTraverse(node, line, currentNode):

    name = node.__class__.__name__

    # Only some nodes contain line number
    if hasattr(node, 'lineno'):
        line = node.lineno

    endLine = line

    current = {'name': name, 'startLine': line, 'children': []}

    if name not in nodesToSkip:
        if name not in handlers:
            currentNode['children'].append(current)
        else:
            current['name'] = handlers[name](node, line)
            currentNode['children'].append(current)
    else:
        current = currentNode

    maxLine = endLine
    for child in ast.iter_child_nodes(node):
        maxLine = max(maxLine, hierarchicalTraverse(child, line, current))

    if maxLine != line:
        current['endLine'] = maxLine

    return maxLine


def read_input_files(local=True,filename='./py-files/chap2/sec_2_1.py',format="simple"):
    if not(local):
        data = input()
        parsed = json.loads(data)
        code = parsed['code']
        mode = parsed.get('mode', 'simple')
        return code,mode

    if local:
        with open(filename) as f:
            code = f.read()
            codelines = code.split('\n')
            return code,codelines, format

def merge_lines_nodes(nodes):
    conceptset = []
    for lineno,conceptlist in nodes['lines'].items():
        conceptset.extend(set(conceptlist))
    return set(conceptset)


def lexer_tokens(code):
    tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    )

    # Tokens

    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_EQUALS  = r'='
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

    lexer = lex()

    # Parsing rules

    precedence = (
        ('left','PLUS','MINUS'),
        ('left','TIMES','DIVIDE'),
        ('right','UMINUS'),
        )
    
    lexer.input(code)
    ret_tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        
        if not(tok in tokensToSkip):
            ret_tokens.append(tok)
    
    return set(ret_tokens)

