

# -----------------------------------------------------------------------------
# lyacompiler.py
#
# Compiler for the scripting language Lya.
# -----------------------------------------------------------------------------

tokens = (
    # RESERVED WORDS
    'ARRAY', 'BY', 'CHARS', 'DCL', 'DO', 'DOWN', 'ELSE', 'ELSIF', 'END', 'EXIT',
    'FI', 'FOR', 'IF', 'IN', 'LOC', 'TYPE', 'OD', 'PROC', 'REF', 'RESULT', 'RETURNS',
    'RETURN', 'SYS', 'THEN', 'TO', 'TYPE', 'WHILE',

    # PREDEFINED WORDS
    'BOOL', 'CHAR', 'FALSE', 'INT', 'LENGTH', 'LOWER', 'NULL', 'NUM', 'PRED',
    'PRINT', 'READ', 'SUCC', 'TRUE', 'UPPER',

    # SYMBOLS
    'DBLSLASH', 'LPAREN', 'RPAREN', 'LCURL', 'RCURL', 'LBRACK', 'RBRACK', 'SEMICOL', 'EQUALS',
    'PLUS','MINUS','TIMES','DIVIDE', 'PERC', 'COMMA', 'COLON', 'SINGQUO',
    'DOUBLEQUO', 'CIRCUMF', 'DBL_AMPERSAND', 'DBL_STRSLASH', 'DBLEQUAL', 'DIF',
    'GTR', 'GEQ', 'LSS', 'LEQ', 'AMPERSAND', 'EXCLAMMARK', 'ARROW',

    'BGN_COMMENT', 'END_COMMENT',

    'NAME', 'INTEGER', 'FLOAT',
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
t_DBLSLASH  = r'//'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURL     = r'\{'
t_RCURL     = r'}'
t_LBRACK    = r'\['
t_RBRACK    = r']'
t_SEMICOL   = r';'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_PERC      = r'%'
t_EQUALS    = r'='
t_COMMA     = r','
t_COLON     = r':'
t_SINGQUO   = r'\''
t_DOUBLEQUO = r'"'
t_CIRCUMF   = r'\^'
t_DBL_AMPERSAND  = r'&&'
t_DBL_STRSLASH  = r'\|\|'
t_DBLEQUAL  = r'=='
t_DIF       = r'!='
t_GTR       = r'>'
t_GEQ       = r'>='
t_LSS       = r'<'
t_LEQ       = r'<='
t_AMPERSAND    = r'&'
t_EXCLAMMARK    = r'!'
t_ARROW     = r'->'
t_BGN_COMMENT   = r'/\*'
t_END_COMMENT   = r'\*/'

# VARIABLES AND IDENTIFIERS
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_FLOAT(t):
    r'-?\d+\.\d*(e-?\d+)?'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'-?\d+'
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

# i dunno what's this
#precedence = (
#    ('left','PLUS','MINUS'),
#    ('left','TIMES','DIVIDE'),
#    ('right','UMINUS'),
#    )

# dictionary of names
names = { }

def p_program(t):
    '''program :            statement_list'''

##
def p_statement_list_rec(t):
    '''statement_list:      statement_list statement'''

def p_statement_list(t):
    '''statement_list:      statement'''


def p_statement(t):
    '''statement:           declaration_statement
                |           synonym_statement
                |           newmode_statement
                |           procedure_statement
                |           action_statement'''

def p_declaration_statement(t):
    '''declaration_statement:   DCL declaration_list'''

##
def p_declaration_list_rec(t):
    #the first line might need to be reversed depending on the parsing rules
    '''declaration_list:    declaration_list COMMA declaration'''

def p_declaration_list(t):
    '''declaration_list:    declaration'''


def p_declaration_init(t):
    '''declaration:         identifier_list mode initialization'''

def p_declaration(t):
    '''declaration:         identifier_list mode'''


def p_initialization(t):
    '''initialization:      assignment_symbol expression'''

##
def p_identifier_list_rec(t):
    #the first line might need to be reversed depending on the parsing rules
    '''identifier_list:     identifier_list COMMA identifier'''

def p_identifier_list(t):
    '''identifier_list:     identifier'''


def p_identifier(t):
    '''identifier:          NAME'''

def p_synonym_statement(t):
    '''synonym_statement:   SYN synonym_list'''

##
def p_synonym_list_rec(t):
    #the first line might need to be reversed depending on the parsing rules
    '''synonym_list:    synonym_list COMMA synonym_definition'''

def p_synonym_list(t):
    '''synonym_list:    synonym_definition'''

##
def p_synonym_definition_mode(t):
    '''synonym_definition:      identifier_list mode EQUALS constant_expression'''

def p_synonym_definition(t):
    '''synonym_definition:      identifier_list EQUALS constant_expression'''


def p_constant_expression(t):
    '''constant_expression:     expression'''

def p_newmode_statement(t):
    '''newmode_statement:   TYPE newmode_list'''

##
def p_newmode_list_rec(t):
    #the first line might need to be reversed depending on the parsing rules
    '''newmode_list:        newmode_list COMMA mode_definition'''

def p_newmode_list(t):
    '''newmode_list:        mode_definition'''


def p_mode_definition(t):
    '''mode_definition:     identifier_list EQUALS mode'''

def p_mode(t):
    '''mode:                mode_name
                |           discrete_mode
                |           reference_mode
                |           composite_mode'''

def p_discrete_mode(t):
    '''discrete_mode        integer_mode
                |           boolean_mode
                |           character_mode
                |           discrete_range_mode'''

def p_integer_mode(t):
    '''integer_mode:        INT'''

def p_boolean_mode(t):
    '''boolean_mode:        BOOL'''

def p_character_mode(t):
    '''character_mode:      CHAR'''

def p_discrete_range_mode(t):
    '''discrete_range_mode:     discrete_mode_name  LPAREN literal_range RPAREN
                |               discrete_mode LPAREN literal_range RPAREN'''

def p_mode_name(t):
    '''mode_name:           identifier'''

def p_discrete_mode_name(t):
    '''discrete_mode_name:  identifier'''

def p_literal_range(t):
    '''literal_range:       lower_bound COLON upper_bound'''

def p_lower_bound(t):
    '''lower_bound:         integer_literal'''

def p_upper_bound(t):
    '''upper_bound:         integer_literal'''

def p_reference_mode(t):
    '''reference_mode:      REF mode'''

def p_composite_mode(t):
    '''composite_mode:      string_mode
                |           array_mode'''

def p_string_mode(t):
    '''string_mode:         CHARS LBRACK string_length RBRACK'''

def p_string_length(t):
    '''string_length:       integer_literal'''

def p_array_mode(t):
    '''array_mode:          ARRAY LBRACK index_mode_list RBRACK'''

##
def p_index_mode_list_rec(t):
    #the first line might need to be reversed depending on the parsing rules
    '''index_mode_list:     intex_mode_list COMMA index_mode'''

def p_index_mode_list(t):
    '''index_mode_list:     index_mode'''


def p_index_mode(t):
    '''index_mode:          discrete_mode
                |           literal_range'''

def p_element_mode(t):
    '''element_mode:        mode'''

def p_location(t):
    '''location:            location_name
                |           dereferenced_reference
                |           string_element
                |           string_slice
                |           array_element
                |           array_slice
                |           call_action'''

#T0D0 CHECK ARROW
def p_dereferenced_reference(t):
    '''dereferenced_reference:      primitive_value ARROW'''

def p_string_element(t):
    '''string_element:      string_location LBRACK start_element RBRACK'''

def p_start_element(t):
    '''start_element:       integer_expression'''

def p_string_slice(t):
    '''string_slice:        string_location LBRACK left_element COLON right_element RBRACK'''

def p_string_location(t):
    '''string_location:     identifier'''

def p_left_element(t):
    '''left_element:        integer_expression'''

def p_right_element(t):
    '''right_element:       integer_expression'''

def p_array_element(t):
    '''array_element:       array_location LBRACK expression_list RBRACK'''

##
def p_expression_list_rec(t):
    #the first line might need to be reversed depending on the parsing rules
    '''expression_list:     expression_list COMMA expression'''

def p_expression_list(t):
    '''expression_list:     expression'''


def p_array_slice(t):
    '''array_slice:         array_location LBRACK lower_element COLON upper_element RBRACK'''

def p_array_location(t):
    '''array_location:      location'''

def p_lower_element(t):
    '''lower_element:       expression'''

def p_upper_element(t):
    '''upper_element:       expression'''

def p_primitive_value(t):
    '''primitive_value:     literal
                |           value_array_element
                |           value_array_slice
                |           parenthesized_expression'''

def p_literal(t):
    '''literal:             integer_literal
                |           boolean_literal
                |           character_literal
                |           empty_literal
                |           character_string_literal'''

###########################################################
#T0D0: find out what ICONST is
def p_integer_literal(t):
    '''integer_literal:     ICONST'''
###########################################################

def p_boolean_literal(t):
    '''boolean_literal:     FALSE | TRUE'''

###########################################################
#T0D0: check the meaning of this rule
def p_character_literal(t):
    '''character_literal:   SINGQUO character SINGQUO
                |           SINGQUO CIRCUMF LPAREN integer_literal RPAREN SINGQUO '''
###########################################################

def p_empty_literal(t):
    '''empty_literal:       NULL'''

##
def p_character_string_literal_char(t):
    '''character_string_literal;    DOUBLEQUO character_list DOUBLEQUO'''

def p_character_string_literal(t):
    '''character_string_literal;    DOUBLEQUO DOUBLEQUO'''

def p_character_list_rec(t):
    '''character_list:      character_list character'''

def p_character_list_rec(t):
    '''character_list:      character'''


def p_value_array_element(t):
    '''value_array_element:         array_primitive_value LBRACK expression_list RBRACK'''

def p_value_array_slice(t):
    '''value_array_slice:   array_primitive_value LBRACK lower_element COLON upper_element RBRACK'''

def p_array_primitive_value(t):
    '''array_primitive_value:       primitive_value'''

def p_parenthesized_expression(t):
    '''parenthesized_expression:    LPAREN expression RPAREN'''

def p_expression(t):
    '''expression:          operand0 | conditional_expression'''

def p_conditional_expression(t):
    '''conditional_expression:  IF boolean_expression then_expression else_expression FI'''

def p_conditional_expression_elsif(t):
    '''conditional_expression:  IF boolean_expression then_expression elsif_expression else_expression FI'''

def p_boolean_expression(t):
    '''boolean_expression:  expression'''

def p_then_expression(t):
    '''then_expression:     THEN expression'''

def p_else_expression(t):
    '''else_expression:     ELSE expression'''

#this rule might have to be changed with the next one depending on the parsing rules
def p_elsif_expression_elsif(t):
    '''elsif_expression:    elsif_expression ELSIF boolean_expression then_expression'''

def p_elsif_expression(t):
    '''elsif_expression:    ELSIF boolean_expression then_expression'''

def p_operand0(t):
    '''operand0:            operand1'''

def p_operand0_op1(t):
    '''operand0:            operand0 operator1 operand1'''

def p_operator1(t):
    '''operator1:           relational_operator | membership_operator'''

def p_relational_operator(t):
    '''relational_operator:     DBL_AMPERSAND | DBL_STRSLASH | DBLEQUAL | DIF | GTR | GEQ | LSS | LEQ'''

def p_membership_operator(t):
    '''membership_operator:     IN'''

def p_operand1(t):
    '''operand1:            operand2'''

def p_operand1_op2(t):
    '''operand1:            operand1 operator2 operand2'''

def p_operator2(t):
    '''operator2:           arithmetic_additive_operator
                |           string_concatenation_operator'''

def p_arithmetic_additive_operator(t):
    '''arithmetic_additive_operator:        PLUS | MINUS'''

def p_string_concatenation_operator(t):
    '''string_concatenation_operator:       AMPERSAND'''

def p_operand2(t):
    '''operand2:            operand3'''

def p_operand2_op3(t):
    '''operand2:            operand2 arithmetic_multiplicative_operator operand3'''

def p_arithmetic_multiplicative_operator(t):
    '''arithmetic_multiplicative_operator:      TIMES | DIVIDE | PERC'''

def p_operand3_monadic(t):
    '''operand3:            monadic_operator operand4'''

def p_operand3(t):
    '''operand3:            operand4
                |           integer_literal'''

def p_monadic_operator(t):
    '''monadic_operator:    MINUS | EXCLAMMARK'''

def p_operand4(t):
    '''operand4:            location | referenced_location | primitive_value'''

def p_referenced_location(t):
    '''referenced_location:         ARROW location'''

def p_action_statement_id(t):
    '''action_statement:    label_id COLON action SEMICOL'''

def p_action_statement(t):
    '''action_statement:    action SEMICOL'''

def p_label_id(t):
    '''label_id:            identifier'''

def p_action(t):
    '''action:              bracketed_action
                |           assignment_action
                |           call_action
                |           exit_action
                |           return_action
                |           result_action'''

def p_bracketed_action(t):
    '''bracketed_action:    if_action | do_action'''

def p_assignment_action(t):
    '''assignment_action:   location assigning_operator expression'''

def p_assigning_operator(t):
    '''assigning_operator:  closed_dyadic_operator assignment_symbol'''

def p_closed_dyadic_operator(t):
    '''closed_dyadic_operator:      arithmetic_additive_operator
                |                   arithmetic_multiplicative_operator
                |                   string_concatenation_operator'''

def p_assignment_symbol(t):
    '''assignment_symbol:   EQUALS'''

def p_if_action_else(t):
    '''if_action:           IF boolean_expression then_clause else_clause FI'''

def p_if_action(t):
    '''if_action:           IF boolean_expression then_clause FI'''

def p_then_clause(t):
    '''then_clause:         THEN action_statement_list'''

def p_else_clause_elsif_else(t):
    '''else_clause:         ELSIF boolean_expression then_clause else_clause'''

def p_else_clause_elsif(t):
    '''else_clause:         ELSIF boolean_expression then_clause'''

def p_else_clause(t):
    '''else_clause:         ELSE action_statement_list'''

def p_do_action_control(t):
    '''do_action:           DO control_part SEMICOL action_statement_list OD'''

def p_do_action(t):
    '''do_action:           DO action_statement_list OD'''

def p_control_part_forwhile(t):
    '''control_part:        for_control while_control'''

def p_control_part(t):
    '''control_part:        for_control
                |           while_control'''

def p_for_control(t):
    '''for_control:         FOR iteration'''

def p_iteration(t):
    '''iteration:           step_enumeration | range_enumeration'''

def p_step_enumeration_stepvalue_down(t):
    '''step_enumeration:    loop_counter assignment_symbol start_value step_value DOWN end_value'''
def p_step_enumeration_stepvalue(t):
    '''step_enumeration:    loop_counter assignment_symbol start_value step_value end_value'''
def p_step_enumeration_down(t):
    '''step_enumeration:    loop_counter assignment_symbol start_value DOWN end_value'''
def p_step_enumeration(t):
    '''step_enumeration:    loop_counter assignment_symbol start_value end_value'''

def p_loop_counter(t):
    '''loop_counter:        identifier'''

def p_start_value(t):
    '''start_value:         discrete_expression'''

def p_step_value(t):
    '''step_value:          BY integer_expression'''

def p_end_value(t):
    '''end_value:           TO discrete_expression'''

def p_discrete_expression(t):
    '''discrete_expression:     expression'''

def p_range_enumeration_down(t):
    '''range_enumeration:       loop_counter DOWN IN discrete_mode_name'''

def p_range_enumeration(t):
    '''range_enumeration:       loop_counter IN discrete_mode_name'''

def p_while_control(t):
    '''while_control:       WHILE boolean_expression'''

def p_call_action(t):
    '''call_action:         procedure_call | builtin_call'''

def p_procedure_call_parameter(t):
    '''procedure_call:      procedure_name LPAREN parameter_list RPAREN'''

def p_procedure_call(t):
    '''procedure_call:      procedure_name LPAREN RPAREN'''

def p_parameter_list_rec(t):
    #the first line might need to be reversed depending on the parsing rules
    '''parameter_list:      parameter_list COMMA parameter'''

def p_parameter_list(t):
    '''parameter_list:      parameter'''

def p_parameter(t):
    '''parameter:           expression'''

def p_procedure_name(t):
    '''procedure_name:      identifier'''

def p_exit_action(t):
    '''exit_action:         EXIT label_id'''

def p_return_action_result(t):
    '''return_action:       RETURN result'''

def p_return_action(t):
    '''return_action:       RETURN'''

def p_result_action(t):
    '''result_action:       RESULT result'''

def p_result(t):
    '''result:              expression'''

def p_builtin_call_parameter(t):
    '''builtin_call:        builtin_name LPAREN parameter_list RPAREN'''

def p_builtin_call(t):
    '''builtin_call:        builtin_name LPAREN RPAREN'''

def p_builtin_name(t):
    '''builtin_name:        NUM | PRED | SUCC | UPPER | LOWER | LENGTH | READ | PRINT'''

def p_procedure_statement(t):
    '''procedure_statement:     label_id COLON produre_definition SEMICOL'''

def p_action_statement_list_rec(t):
    '''action_statement_list:   action_statement_list action_statement'''

def p_action_statement_list(t):
    '''action_statement_list:   action_statement'''


###
def p_procedure_definition_parameter_result_action(t):
    '''procedure_definition:    PORC LPAREN formal_parameter_list RPAREN result_spec SEMICOL action_statement_list END'''

def p_procedure_definition_parameter_action(t):
    '''procedure_definition:    PORC LPAREN formal_parameter_list RPAREN SEMICOL action_statement_list END'''

def p_procedure_definition_result_action(t):
    '''procedure_definition:    PORC LPAREN RPAREN result_spec SEMICOL action_statement_list END'''

def p_procedure_definition_action(t):
    '''procedure_definition:    PORC LPAREN RPAREN SEMICOL action_statement_list END'''


def p_procedure_definition_parameter_result(t):
    '''procedure_definition:    PORC LPAREN formal_parameter_list RPAREN result_spec SEMICOL END'''

def p_procedure_definition_parameter(t):
    '''procedure_definition:    PORC LPAREN formal_parameter_list RPAREN SEMICOL END'''

def p_procedure_definition_result(t):
    '''procedure_definition:    PORC LPAREN RPAREN result_spec SEMICOL END'''

def p_procedure_definition(t):
    '''procedure_definition:    PORC LPAREN RPAREN SEMICOL END'''



def p_formal_parameter_list_rec(t):
    '''formal_parameter_list:   formal_parameter_list COMMA formal_parameter'''

def p_formal_parameter_list(t):
    '''formal_parameter_list:   formal_parameter'''

def p_formal_parameter(t):
    '''formal_parameter:        identifier_list parameter_spec'''

def p_parameter_spec_attr(t):
    '''parameter_spec:          mode parameter_attribute'''

def p_parameter_spec(t):
    '''parameter_spec:          mode'''

def p_parameter_attribute(t):
    '''parameter_attribute:     LOC'''

def p_result_spec_attr(t):
    '''result_spec:             RETURNS LPAREN mode result_attribute RPAREN'''

def p_result_spec(t):
    '''result_spec:             RETURNS LPAREN mode RPAREN'''

def p_result_attribute(t):
    '''result_attribute:        LOC'''


def p_comment(t):
    '''comment:                 bracketed_comment | line_end_comment'''

def p_bracketed_comment(t):
    '''bracketed_comment:       BGN_COMMENT character_string END_COMMENT'''

def p_line_end_comment(t):
    '''line_end_comment:        DBLSLASH character_string newline'''

def p_character_string_list(t):
    '''character_string:        character_string character'''

def p_character_string(t):
    '''character_string:        character'''

def p_character_string_null(t):
    '''character_string:'''


#T0D0: create the functions
##########################################################################
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

