#
#
# # -----------------------------------------------------------------------------
# # lyacompiler.py
# #
# # Compiler for the scripting language Lya.
# # -----------------------------------------------------------------------------
#
# tokens = (
#     # RESERVED WORDS
#     'ARRAY', 'BY', 'CHARS', 'DCL', 'DO', 'DOWN', 'ELSE', 'ELSIF', 'END', 'EXIT',
#     'FI', 'FOR', 'IF', 'IN', 'LOC', 'TYPE', 'OD', 'PROC', 'REF', 'RESULT', 'RETURNS',
#     'RETURN', 'SYS', 'THEN', 'TO', 'TYPE', 'WHILE',
#
#     # PREDEFINED WORDS
#     'BOOL', 'CHAR', 'FALSE', 'INT', 'LENGTH', 'LOWER', 'NULL', 'NUM', 'PRED',
#     'PRINT', 'READ', 'SUCC', 'TRUE', 'UPPER',
#
#     # SYMBOLS
#     'DBLSLASH', 'LPAREN', 'RPAREN', 'LCURL', 'RCURL', 'LBRACK', 'RBRACK', 'SEMICOL', 'ASSIGN',
#     'PLUS','MINUS','TIMES','DIVIDE', 'PERC', 'COMMA', 'COLON', 'SINGQUO',
#     'DBLQUO', 'CIRCUMF', 'AND', 'OR', 'EQUALS', 'DIF',
#     'GTR', 'GEQ', 'LSS', 'LEQ', 'CONCAT', 'NOT', 'ARROW',
#
#     'BGN_COMMENT', 'END_COMMENT',
#
#     'NAME', 'INTEGER', 'FLOAT',
#     )
# # Tokens
#
# # RESERVED WORDS
# t_ARRAY     = r'array'
# t_BY        = r'by'
# t_CHARS     = r'chars'
# t_DCL       = r'dcl'
# t_DO        = r'do'
# t_DOWN      = r'down'
# t_ELSE      = r'else'
# t_ELSIF     = r'elsif'
# t_END       = r'end'
# t_EXIT      = r'exit'
# t_FI        = r'fi'
# t_FOR       = r'for'
# t_IF        = r'if'
# t_IN        = r'in'
# t_LOC       = r'loc'
# t_TYPE      = r'type'
# t_OD        = r'od'
# t_PROC      = r'proc'
# t_REF       = r'ref'
# t_RESULT    = r'result'
# t_RETURNS   = r'returns'
# t_RETURN    = r'return'
# t_SYN       = r'syn'
# t_THEN      = r'then'
# t_TYPE      = r'type'
# t_TO        = r'to'
# t_WHILE     = r'while'
#
# # PREDEFINED WORDS
# t_BOOL      = r'bool'
# t_CHAR      = r'char'
# t_FALSE     = r'false'
# t_INT       = r'int'
# t_LENGTH    = r'length'
# t_LOWER     = r'lower'
# t_NULL      = r'null'
# t_NUM       = r'num'
# t_PRED      = r'pred'
# t_PRINT     = r'print'
# t_READ      = r'read'
# t_SUCC      = r'succ'
# t_TRUE      = r'true'
# t_UPPER     = r'upper'
#
# # SYMBOLS
# t_DBLSLASH  = r'//'
# t_LPAREN    = r'\('
# t_RPAREN    = r'\)'
# t_LCURL     = r'\{'
# t_RCURL     = r'}'
# t_LBRACK    = r'\['
# t_RBRACK    = r']'
# t_SEMICOL   = r';'
# t_PLUS      = r'\+'
# t_MINUS     = r'-'
# t_TIMES     = r'\*'
# t_DIVIDE    = r'/'
# t_PERC      = r'%'
# t_ASSIGN    = r'='
# t_COMMA     = r','
# t_COLON     = r':'
# t_SINGQUO   = r'\''
# t_DBLQUO = r'"'
# t_CIRCUMF   = r'\^'
# t_AND  = r'&&'
# t_OR  = r'\|\|'
# t_EQUALS  = r'=='
# t_DIF       = r'!='
# t_GTR       = r'>'
# t_GEQ       = r'>='
# t_LSS       = r'<'
# t_LEQ       = r'<='
# t_CONCAT    = r'&'
# t_NOT    = r'!'
# t_ARROW     = r'->'
# t_BGN_COMMENT   = r'/\*'
# t_END_COMMENT   = r'\*/'
#
# # VARIABLES AND IDENTIFIERS
# t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
#
# def t_ICONST(self, t):
#     r'\d+'
#     try:
#         t.value = int(t.value)
#     except ValueError:
#         print("Integer value too large %d", t.value)
#         t.value = 0
#     return t
#
# # Ignored characters
# t_ignore = " \t"
#
# def t_newline(self, t):
#     r'\n+'
#     t.lexer.lineno += t.value.count("\n")
#
# def t_error(self, t):
#     print("Illegal character '%s'" % t.value[0])
#     t.lexer.skip(1)
#
# # Build the lexer
# import ply.lex as lex
# lexer = lex.lex()
#
#
# # i dunno what's this
# #precedence = (
# #    ('left','PLUS','MINUS'),
# #    ('left','TIMES','DIVIDE'),
# #    ('right','UMINUS'),
# #    )
#
# # dictionary of names
# names = { }
#
# def p_program(self, t):
#     """program :            statement_list"""
#
# ##
# def p_statement_list_rec(self, t):
#     """statement_list:      statement_list statement"""
#
# def p_statement_list(self, t):
#     """statement_list:      statement"""
#
#
# def p_statement(self, t):
#     """statement:           declaration_statement
#                 |           synonym_statement
#                 |           newmode_statement
#                 |           procedure_statement
#                 |           action_statement"""
#
# def p_declaration_statement(self, t):
#     """declaration_statement:   DCL declaration_list"""
#
# ##
# def p_declaration_list_rec(self, t):
#     #the first line might need to be reversed depending on the parsing rules
#     """declaration_list:    declaration_list COMMA declaration"""
#
# def p_declaration_list(self, t):
#     """declaration_list:    declaration"""
#
#
# def p_declaration_init(self, t):
#     """declaration:         identifier_list mode initialization"""
#
# def p_declaration(self, t):
#     """declaration:         identifier_list mode"""
#
#
# def p_initialization(self, t):
#     """initialization:      assignment_symbol expression"""
#
# ##
# def p_identifier_list_rec(self, t):
#     #the first line might need to be reversed depending on the parsing rules
#     """identifier_list:     identifier_list COMMA identifier"""
#
# def p_identifier_list(self, t):
#     """identifier_list:     identifier"""
#
#
# def p_identifier(self, t):
#     """identifier:          NAME"""
#
# def p_synonym_statement(self, t):
#     """synonym_statement:   SYN synonym_list"""
#
# ##
# def p_synonym_list_rec(self, t):
#     #the first line might need to be reversed depending on the parsing rules
#     """synonym_list:    synonym_list COMMA synonym_definition"""
#
# def p_synonym_list(self, t):
#     """synonym_list:    synonym_definition"""
#
# ##
# def p_synonym_definition_mode(self, t):
#     """synonym_definition:      identifier_list mode ASSIGN constant_expression"""
#
# def p_synonym_definition(self, t):
#     """synonym_definition:      identifier_list ASSIGN constant_expression"""
#
#
# def p_constant_expression(self, t):
#     """constant_expression:     expression"""
#
# def p_newmode_statement(self, t):
#     """newmode_statement:   TYPE newmode_list"""
#
# ##
# def p_newmode_list_rec(self, t):
#     #the first line might need to be reversed depending on the parsing rules
#     """newmode_list:        newmode_list COMMA mode_definition"""
#
# def p_newmode_list(self, t):
#     """newmode_list:        mode_definition"""
#
#
# def p_mode_definition(self, t):
#     """mode_definition:     identifier_list ASSIGN mode"""
#
# def p_mode(self, t):
#     """mode:                mode_name
#                 |           discrete_mode
#                 |           reference_mode
#                 |           composite_mode"""
#
# def p_discrete_mode(self, t):
#     """discrete_mode        integer_mode
#                 |           boolean_mode
#                 |           character_mode
#                 |           discrete_range_mode"""
#
# def p_integer_mode(self, t):
#     """integer_mode:        INT"""
#
# def p_boolean_mode(self, t):
#     """boolean_mode:        BOOL"""
#
# def p_character_mode(self, t):
#     """character_mode:      CHAR"""
#
# def p_discrete_range_mode(self, t):
#     """discrete_range_mode:     discrete_mode_name  LPAREN literal_range RPAREN
#                 |               discrete_mode LPAREN literal_range RPAREN"""
#
# def p_mode_name(self, t):
#     """mode_name:           identifier"""
#
# def p_discrete_mode_name(self, t):
#     """discrete_mode_name:  identifier"""
#
# def p_literal_range(self, t):
#     """literal_range:       lower_bound COLON upper_bound"""
#
# def p_lower_bound(self, t):
#     """lower_bound:         integer_literal"""
#
# def p_upper_bound(self, t):
#     """upper_bound:         integer_literal"""
#
# def p_reference_mode(self, t):
#     """reference_mode:      REF mode"""
#
# def p_composite_mode(self, t):
#     """composite_mode:      string_mode
#                 |           array_mode"""
#
# def p_string_mode(self, t):
#     """string_mode:         CHARS LBRACK string_length RBRACK"""
#
# def p_string_length(self, t):
#     """string_length:       integer_literal"""
#
# def p_array_mode(self, t):
#     """array_mode:          ARRAY LBRACK index_mode_list RBRACK"""
#
# ##
# def p_index_mode_list_rec(self, t):
#     #the first line might need to be reversed depending on the parsing rules
#     """index_mode_list:     intex_mode_list COMMA index_mode"""
#
# def p_index_mode_list(self, t):
#     """index_mode_list:     index_mode"""
#
#
# def p_index_mode(self, t):
#     """index_mode:          discrete_mode
#                 |           literal_range"""
#
# def p_element_mode(self, t):
#     """element_mode:        mode"""
#
# def p_location(self, t):
#     """location:            location_name
#                 |           dereferenced_reference
#                 |           string_element
#                 |           string_slice
#                 |           array_element
#                 |           array_slice
#                 |           call_action"""
#
# #TODO CHECK ARROW
# def p_dereferenced_reference(self, t):
#     """dereferenced_reference:      primitive_value ARROW"""
#
# def p_string_element(self, t):
#     """string_element:      string_location LBRACK start_element RBRACK"""
#
# def p_start_element(self, t):
#     """start_element:       integer_expression"""
#
# def p_string_slice(self, t):
#     """string_slice:        string_location LBRACK left_element COLON right_element RBRACK"""
#
# def p_string_location(self, t):
#     """string_location:     identifier"""
#
# def p_left_element(self, t):
#     """left_element:        integer_expression"""
#
# def p_right_element(self, t):
#     """right_element:       integer_expression"""
#
# def p_array_element(self, t):
#     """array_element:       array_location LBRACK expression_list RBRACK"""
#
# ##
# def p_expression_list_rec(self, t):
#     #the first line might need to be reversed depending on the parsing rules
#     """expression_list:     expression_list COMMA expression"""
#
# def p_expression_list(self, t):
#     """expression_list:     expression"""
#
#
# def p_array_slice(self, t):
#     """array_slice:         array_location LBRACK lower_element COLON upper_element RBRACK"""
#
# def p_array_location(self, t):
#     """array_location:      location"""
#
# def p_lower_element(self, t):
#     """lower_element:       expression"""
#
# def p_upper_element(self, t):
#     """upper_element:       expression"""
#
# def p_primitive_value(self, t):
#     """primitive_value:     literal
#                 |           value_array_element
#                 |           value_array_slice
#                 |           parenthesized_expression"""
#
# def p_literal(self, t):
#     """literal:             integer_literal
#                 |           boolean_literal
#                 |           character_literal
#                 |           empty_literal
#                 |           character_string_literal"""
#
# ###########################################################
# #TODO: find out what ICONST is
# def p_integer_literal(self, t):
#     """integer_literal:     ICONST"""
# ###########################################################
#
# def p_boolean_literal(self, t):
#     """boolean_literal:     FALSE | TRUE"""
#
# ###########################################################
# #TODO: check the meaning of this rule
# def p_character_literal(self, t):
#     """character_literal:   SINGQUO character SINGQUO
#                 |           SINGQUO CIRCUMF LPAREN integer_literal RPAREN SINGQUO """
# ###########################################################
#
# def p_empty_literal(self, t):
#     """empty_literal:       NULL"""
#
# ##
# def p_character_string_literal_char(self, t):
#     """character_string_literal;    DBLQUO character_list DBLQUO"""
#
# def p_character_string_literal(self, t):
#     """character_string_literal;    DBLQUO DBLQUO"""
#
# def p_character_list_rec(self, t):
#     """character_list:      character_list character"""
#
# def p_character_list_rec(self, t):
#     """character_list:      character"""
#
#
# def p_value_array_element(self, t):
#     """value_array_element:         array_primitive_value LBRACK expression_list RBRACK"""
#
# def p_value_array_slice(self, t):
#     """value_array_slice:   array_primitive_value LBRACK lower_element COLON upper_element RBRACK"""
#
# def p_array_primitive_value(self, t):
#     """array_primitive_value:       primitive_value"""
#
# def p_parenthesized_expression(self, t):
#     """parenthesized_expression:    LPAREN expression RPAREN"""
#
# def p_expression(self, t):
#     """expression:          operand0 | conditional_expression"""
#
# def p_conditional_expression(self, t):
#     """conditional_expression:  IF boolean_expression then_expression else_expression FI"""
#
# def p_conditional_expression_elsif(self, t):
#     """conditional_expression:  IF boolean_expression then_expression elsif_expression else_expression FI"""
#
# def p_boolean_expression(self, t):
#     """boolean_expression:  expression"""
#
# def p_then_expression(self, t):
#     """then_expression:     THEN expression"""
#
# def p_else_expression(self, t):
#     """else_expression:     ELSE expression"""
#
# #this rule might have to be changed with the next one depending on the parsing rules
# def p_elsif_expression_elsif(self, t):
#     """elsif_expression:    elsif_expression ELSIF boolean_expression then_expression"""
#
# def p_elsif_expression(self, t):
#     """elsif_expression:    ELSIF boolean_expression then_expression"""
#
# def p_operand0(self, t):
#     """operand0:            operand1"""
#
# def p_operand0_op1(self, t):
#     """operand0:            operand0 operator1 operand1"""
#
# def p_operator1(self, t):
#     """operator1:           relational_operator | membership_operator"""
#
# def p_relational_operator(self, t):
#     """relational_operator:     AND | OR | EQUALS | DIF | GTR | GEQ | LSS | LEQ"""
#
# def p_membership_operator(self, t):
#     """membership_operator:     IN"""
#
# def p_operand1(self, t):
#     """operand1:            operand2"""
#
# def p_operand1_op2(self, t):
#     """operand1:            operand1 operator2 operand2"""
#
# def p_operator2(self, t):
#     """operator2:           arithmetic_additive_operator
#                 |           string_concatenation_operator"""
#
# def p_arithmetic_additive_operator(self, t):
#     """arithmetic_additive_operator:        PLUS | MINUS"""
#
# def p_string_concatenation_operator(self, t):
#     """string_concatenation_operator:       CONCAT"""
#
# def p_operand2(self, t):
#     """operand2:            operand3"""
#
# def p_operand2_op3(self, t):
#     """operand2:            operand2 arithmetic_multiplicative_operator operand3"""
#
# def p_arithmetic_multiplicative_operator(self, t):
#     """arithmetic_multiplicative_operator:      TIMES | DIVIDE | PERC"""
#
# def p_operand3_monadic(self, t):
#     """operand3:            monadic_operator operand4"""
#
# def p_operand3(self, t):
#     """operand3:            operand4
#                 |           integer_literal"""
#
# def p_monadic_operator(self, t):
#     """monadic_operator:    MINUS | NOT"""
#
# def p_operand4(self, t):
#     """operand4:            location | referenced_location | primitive_value"""
#
# def p_referenced_location(self, t):
#     """referenced_location:         ARROW location"""
#
# def p_action_statement_id(self, t):
#     """action_statement:    label_id COLON action SEMICOL"""
#
# def p_action_statement(self, t):
#     """action_statement:    action SEMICOL"""
#
# def p_label_id(self, t):
#     """label_id:            identifier"""
#
# def p_action(self, t):
#     """action:              bracketed_action
#                 |           assignment_action
#                 |           call_action
#                 |           exit_action
#                 |           return_action
#                 |           result_action"""
#
# def p_bracketed_action(self, t):
#     """bracketed_action:    if_action | do_action"""
#
# def p_assignment_action(self, t):
#     """assignment_action:   location assigning_operator expression"""
#
# def p_assigning_operator(self, t):
#     """assigning_operator:  closed_dyadic_operator assignment_symbol"""
#
# def p_closed_dyadic_operator(self, t):
#     """closed_dyadic_operator:      arithmetic_additive_operator
#                 |                   arithmetic_multiplicative_operator
#                 |                   string_concatenation_operator"""
#
# def p_assignment_symbol(self, t):
#     """assignment_symbol:   ASSIGN"""
#
# def p_if_action_else(self, t):
#     """if_action:           IF boolean_expression then_clause else_clause FI"""
#
# def p_if_action(self, t):
#     """if_action:           IF boolean_expression then_clause FI"""
#
# def p_then_clause(self, t):
#     """then_clause:         THEN action_statement_list"""
#
# def p_else_clause_elsif_else(self, t):
#     """else_clause:         ELSIF boolean_expression then_clause else_clause"""
#
# def p_else_clause_elsif(self, t):
#     """else_clause:         ELSIF boolean_expression then_clause"""
#
# def p_else_clause(self, t):
#     """else_clause:         ELSE action_statement_list"""
#
# def p_do_action_control(self, t):
#     """do_action:           DO control_part SEMICOL action_statement_list OD"""
#
# def p_do_action(self, t):
#     """do_action:           DO action_statement_list OD"""
#
# def p_control_part_forwhile(self, t):
#     """control_part:        for_control while_control"""
#
# def p_control_part(self, t):
#     """control_part:        for_control
#                 |           while_control"""
#
# def p_for_control(self, t):
#     """for_control:         FOR iteration"""
#
# def p_iteration(self, t):
#     """iteration:           step_enumeration | range_enumeration"""
#
# def p_step_enumeration_stepvalue_down(self, t):
#     """step_enumeration:    loop_counter assignment_symbol start_value step_value DOWN end_value"""
# def p_step_enumeration_stepvalue(self, t):
#     """step_enumeration:    loop_counter assignment_symbol start_value step_value end_value"""
# def p_step_enumeration_down(self, t):
#     """step_enumeration:    loop_counter assignment_symbol start_value DOWN end_value"""
# def p_step_enumeration(self, t):
#     """step_enumeration:    loop_counter assignment_symbol start_value end_value"""
#
# def p_loop_counter(self, t):
#     """loop_counter:        identifier"""
#
# def p_start_value(self, t):
#     """start_value:         discrete_expression"""
#
# def p_step_value(self, t):
#     """step_value:          BY integer_expression"""
#
# def p_end_value(self, t):
#     """end_value:           TO discrete_expression"""
#
# def p_discrete_expression(self, t):
#     """discrete_expression:     expression"""
#
# def p_range_enumeration_down(self, t):
#     """range_enumeration:       loop_counter DOWN IN discrete_mode_name"""
#
# def p_range_enumeration(self, t):
#     """range_enumeration:       loop_counter IN discrete_mode_name"""
#
# def p_while_control(self, t):
#     """while_control:       WHILE boolean_expression"""
#
# def p_call_action(self, t):
#     """call_action:         procedure_call | builtin_call"""
#
# def p_procedure_call_parameter(self, t):
#     """procedure_call:      procedure_name LPAREN parameter_list RPAREN"""
#
# def p_procedure_call(self, t):
#     """procedure_call:      procedure_name LPAREN RPAREN"""
#
# def p_parameter_list_rec(self, t):
#     #the first line might need to be reversed depending on the parsing rules
#     """parameter_list:      parameter_list COMMA parameter"""
#
# def p_parameter_list(self, t):
#     """parameter_list:      parameter"""
#
# def p_parameter(self, t):
#     """parameter:           expression"""
#
# def p_procedure_name(self, t):
#     """procedure_name:      identifier"""
#
# def p_exit_action(self, t):
#     """exit_action:         EXIT label_id"""
#
# def p_return_action_result(self, t):
#     """return_action:       RETURN result"""
#
# def p_return_action(self, t):
#     """return_action:       RETURN"""
#
# def p_result_action(self, t):
#     """result_action:       RESULT result"""
#
# def p_result(self, t):
#     """result:              expression"""
#
# def p_builtin_call_parameter(self, t):
#     """builtin_call:        builtin_name LPAREN parameter_list RPAREN"""
#
# def p_builtin_call(self, t):
#     """builtin_call:        builtin_name LPAREN RPAREN"""
#
# def p_builtin_name(self, t):
#     """builtin_name:        NUM | PRED | SUCC | UPPER | LOWER | LENGTH | READ | PRINT"""
#
# def p_procedure_statement(self, t):
#     """procedure_statement:     label_id COLON produre_definition SEMICOL"""
#
# def p_action_statement_list_rec(self, t):
#     """action_statement_list:   action_statement_list action_statement"""
#
# def p_action_statement_list(self, t):
#     """action_statement_list:   action_statement"""
#
#
# ###
# def p_procedure_definition_parameter_result_action(self, t):
#     """procedure_definition:    PORC LPAREN formal_parameter_list RPAREN result_spec SEMICOL action_statement_list END"""
#
# def p_procedure_definition_parameter_action(self, t):
#     """procedure_definition:    PORC LPAREN formal_parameter_list RPAREN SEMICOL action_statement_list END"""
#
# def p_procedure_definition_result_action(self, t):
#     """procedure_definition:    PORC LPAREN RPAREN result_spec SEMICOL action_statement_list END"""
#
# def p_procedure_definition_action(self, t):
#     """procedure_definition:    PORC LPAREN RPAREN SEMICOL action_statement_list END"""
#
#
# def p_procedure_definition_parameter_result(self, t):
#     """procedure_definition:    PORC LPAREN formal_parameter_list RPAREN result_spec SEMICOL END"""
#
# def p_procedure_definition_parameter(self, t):
#     """procedure_definition:    PORC LPAREN formal_parameter_list RPAREN SEMICOL END"""
#
# def p_procedure_definition_result(self, t):
#     """procedure_definition:    PORC LPAREN RPAREN result_spec SEMICOL END"""
#
# def p_procedure_definition(self, t):
#     """procedure_definition:    PORC LPAREN RPAREN SEMICOL END"""
#
#
#
# def p_formal_parameter_list_rec(self, t):
#     """formal_parameter_list:   formal_parameter_list COMMA formal_parameter"""
#
# def p_formal_parameter_list(self, t):
#     """formal_parameter_list:   formal_parameter"""
#
# def p_formal_parameter(self, t):
#     """formal_parameter:        identifier_list parameter_spec"""
#
# def p_parameter_spec_attr(self, t):
#     """parameter_spec:          mode parameter_attribute"""
#
# def p_parameter_spec(self, t):
#     """parameter_spec:          mode"""
#
# def p_parameter_attribute(self, t):
#     """parameter_attribute:     LOC"""
#
# def p_result_spec_attr(self, t):
#     """result_spec:             RETURNS LPAREN mode result_attribute RPAREN"""
#
# def p_result_spec(self, t):
#     """result_spec:             RETURNS LPAREN mode RPAREN"""
#
# def p_result_attribute(self, t):
#     """result_attribute:        LOC"""
#
#
# def p_comment(self, t):
#     """comment:                 bracketed_comment | line_end_comment"""
#
# def p_bracketed_comment(self, t):
#     """bracketed_comment:       BGN_COMMENT character_string END_COMMENT"""
#
# def p_line_end_comment(self, t):
#     """line_end_comment:        DBLSLASH character_string newline"""
#
# def p_character_string_list(self, t):
#     """character_string:        character_string character"""
#
# def p_character_string(self, t):
#     """character_string:        character"""
#
# def p_character_string_null(self, t):
#     """character_string:"""
#
#
# #TODO: create the functions
# ##########################################################################
# def p_expression_name(self, t):
#     'expression : NAME'
#     try:
#         t[0] = names[t[1]]
#     except LookupError:
#         print("Undefined name '%s'" % t[1])
#         t[0] = 0
#
# def p_error(self, t):
#     print("Syntax error at '%s'" % t.value)
#
# import ply.yacc as yacc
# parser = yacc.yacc()
#
# while True:
#     try:
#         s = input('calc > ')   # Use raw_input on Python 2
#     except EOFError:
#         break
#     parser.parse(s)
#
