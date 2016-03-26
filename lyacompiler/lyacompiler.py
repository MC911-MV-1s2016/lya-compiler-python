

# -----------------------------------------------------------------------------
# lyacompiler.py
#
# Compiler for the scripting language Lya.
# -----------------------------------------------------------------------------

# T0D0: multiple relational/logical/concatenation/monadic operators
tokens = (
    # RESERVED WORDS
    'ARRAY', 'BY', 'CHARS', 'DCL', 'DO', 'DOWN', 'ELSE', 'ELSIF', 'END', 'EXIT',
    'FI', 'FOR', 'IF', 'IN', 'LOC', 'TYPE', 'OD', 'PROC', 'REF', 'RESULT', 'RETURNS',
    'RETURN', 'SYS', 'THEN', 'TO', 'TYPE', 'WHILE',

    # PREDEFINED WORDS
    'BOOL', 'CHAR', 'FALSE', 'INT', 'LENGTH', 'LOWER', 'NULL', 'NUM', 'PRED',
    'PRINT', 'READ', 'SUCC', 'TRUE', 'UPPER',

    # SYMBOLS
    'LPAREN', 'RPAREN', 'LCURL', 'RCURL', 'SEMICOL', 'EQUALS',
    'PLUS','MINUS','TIMES','DIVIDE',

    'NAME', 'NUMBER',
    )

# Tokens

# RESERVED WORDS
t_ARRAY     = r'ARRAY'
t_BY        = r'BY'
t_CHARS     = r'CHARS'
t_DCL       = r'DCL'
t_DO        = r'DO'
t_DOWN      = r'DOWN'
t_ELSE      = r'ELSE'
t_ELSIF     = r'ELSIF'
t_END       = r'END'
t_EXIT      = r'EXIT'
t_FI        = r'FI'
t_FOR       = r'FOR'
t_IF        = r'IF'
t_IN        = r'IN'
t_LOC       = r'LOC'
t_TYPE      = r'TYPE'
t_OD        = r'OD'
t_PROC      = r'PROC'
t_REF       = r'REF'
t_RESULT    = r'RESULT'
t_RETURNS   = r'RETURNS'
t_RETURN    = r'RETURN'
t_SYN       = r'SYN'
t_THEN      = r'THEN'
t_TYPE      = r'TYPE'
t_TO        = r'TO'
t_WHILE     = r'WHILE'

# PREDEFINED WORDS
t_BOOL      = r'BOOL'
t_CHAR      = r'CHAR'
t_FALSE     = r'FALSE'
t_INT       = r'INT'
t_LENGTH    = r'LENGTH'
t_LOWER     = r'LOWER'
t_NULL      = r'NULL'
t_NUM       = r'NUM'
t_PRED      = r'PRED'
t_PRINT     = r'PRINT'
t_READ      = r'READ'
t_SUCC      = r'SUCC'
t_TRUE      = r'TRUE'
t_UPPER     = r'UPPER'

# SYMBOLS
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURL     = r'\{'
t_RCURL     = r'\}'
t_SEMICOL   = r';'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='

# VARIABLES AND IDENTIFIERS
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# T0D0
# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)

