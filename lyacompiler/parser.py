# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lyaparser.py
# Parser and AST builder for the Lya scripting language.
#
# ------------------------------------------------------------

# from .lyalexer import LyaLexer


class LyaParser(object):
    # Parsing rules

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

    # dictionary of names
    names = {}

    def p_program(self, p):
        """program :            statement_list"""

        p[0] = ("program",)

    ##
    def p_statement_list_rec(self, p):
        """statement_list:      statement_list statement"""

    def p_statement_list(self, p):
        """statement_list:      statement"""

    def p_statement(self, p):
        """statement:           declaration_statement
                    |           synonym_statement
                    |           newmode_statement
                    |           procedure_statement
                    |           action_statement"""

    def p_declaration_statement(self, p):
        """declaration_statement:   DCL declaration_list"""

    ##
    def p_declaration_list_rec(self, p):
        # the first line might need to be reversed depending on the parsing rules
        """declaration_list:    declaration_list COMMA declaration"""

    def p_declaration_list(self, p):
        """declaration_list:    declaration"""

    def p_declaration_init(self, p):
        """declaration:         identifier_list mode initialization"""

    def p_declaration(self, p):
        """declaration:         identifier_list mode"""

    def p_initialization(self, p):
        """initialization:      assignment_symbol expression"""

    ##
    def p_identifier_list_rec(self, p):
        # the first line might need to be reversed depending on the parsing rules
        """identifier_list:     identifier_list COMMA identifier"""

    def p_identifier_list(self, p):
        """identifier_list:     identifier"""

    def p_identifier(self, p):
        """identifier:          ID"""

    def p_synonym_statement(self, p):
        """synonym_statement:   SYN synonym_list"""

    ##
    def p_synonym_list_rec(self, p):
        # the first line might need to be reversed depending on the parsing rules
        """synonym_list:    synonym_list COMMA synonym_definition"""

    def p_synonym_list(self, p):
        """synonym_list:    synonym_definition"""

    ##
    def p_synonym_definition_mode(self, p):
        """synonym_definition:      identifier_list mode EQUALS constant_expression"""

    def p_synonym_definition(self, p):
        """synonym_definition:      identifier_list EQUALS constant_expression"""

    def p_constant_expression(self, p):
        """constant_expression:     expression"""

    def p_newmode_statement(self, p):
        """newmode_statement:   TYPE newmode_list"""

    ##
    def p_newmode_list_rec(self, p):
        # the first line might need to be reversed depending on the parsing rules
        """newmode_list:        newmode_list COMMA mode_definition"""

    def p_newmode_list(self, p):
        """newmode_list:        mode_definition"""

    def p_mode_definition(self, p):
        """mode_definition:     identifier_list EQUALS mode"""

    def p_mode(self, p):
        """mode:                mode_name
                    |           discrete_mode
                    |           reference_mode
                    |           composite_mode"""

    def p_discrete_mode(self, p):
        """discrete_mode        integer_mode
                    |           boolean_mode
                    |           character_mode
                    |           discrete_range_mode"""

    def p_integer_mode(self, p):
        """integer_mode:        INT"""

    def p_boolean_mode(self, p):
        """boolean_mode:        BOOL"""

    def p_character_mode(self, p):
        """character_mode:      CHAR"""

    def p_discrete_range_mode(self, p):
        """discrete_range_mode:     discrete_mode_name  LPAREN literal_range RPAREN
                    |               discrete_mode LPAREN literal_range RPAREN"""

    def p_mode_name(self, p):
        """mode_name:           identifier"""

    def p_discrete_mode_name(self, p):
        """discrete_mode_name:  identifier"""

    def p_literal_range(self, p):
        """literal_range:       lower_bound COLON upper_bound"""

    def p_lower_bound(self, p):
        """lower_bound:         expression"""

    def p_upper_bound(self, p):
        """upper_bound:         expression"""

    def p_reference_mode(self, p):
        """reference_mode:      REF mode"""

    def p_composite_mode(self, p):
        """composite_mode:      string_mode
                    |           array_mode"""

    def p_string_mode(self, p):
        """string_mode:         CHARS LBRACK string_length RBRACK"""

    def p_string_length(self, p):
        """string_length:       integer_literal"""

    def p_array_mode(self, p):
        """array_mode:          ARRAY LBRACK index_mode_list RBRACK"""

    ##
    def p_index_mode_list_rec(self, p):
        # the first line might need to be reversed depending on the parsing rules
        """index_mode_list:     intex_mode_list COMMA index_mode"""

    def p_index_mode_list(self, p):
        """index_mode_list:     index_mode"""

    def p_index_mode(self, p):
        """index_mode:          discrete_mode
                    |           literal_range"""

    def p_element_mode(self, p):
        """element_mode:        mode"""

    def p_location(self, p):
        """location:            location_name
                    |           dereferenced_reference
                    |           string_element
                    |           string_slice
                    |           array_element
                    |           array_slice
                    |           call_action"""

    # T0D0 CHECK ARROW
    def p_dereferenced_reference(self, p):
        """dereferenced_reference:      primitive_value ARROW"""

    def p_string_element(self, p):
        """string_element:      string_location LBRACK start_element RBRACK"""

    def p_start_element(self, p):
        """start_element:       integer_expression"""

    def p_string_slice(self, p):
        """string_slice:        string_location LBRACK left_element COLON right_element RBRACK"""

    def p_string_location(self, p):
        """string_location:     identifier"""

    def p_left_element(self, p):
        """left_element:        integer_expression"""

    def p_right_element(self, p):
        """right_element:       integer_expression"""

    def p_array_element(self, p):
        """array_element:       array_location LBRACK expression_list RBRACK"""

    ##
    def p_expression_list_rec(self, p):
        # the first line might need to be reversed depending on the parsing rules
        """expression_list:     expression_list COMMA expression"""

    def p_expression_list(self, p):
        """expression_list:     expression"""

    def p_array_slice(self, p):
        """array_slice:         array_location LBRACK lower_bound COLON upper_bound RBRACK"""

    def p_array_location(self, p):
        """array_location:      location"""

    # def p_lower_element(self,p):
    #     """lower_element:       expression"""
    #
    # def p_upper_element(self,p):
    #     """upper_element:       expression"""

    def p_primitive_value(self, p):
        """primitive_value:     literal
                    |           value_array_element
                    |           value_array_slice
                    |           parenthesized_expression"""
        p[0] = p[1]

    def p_literal(self, p):
        """literal:             integer_literal
                    |           boolean_literal
                    |           character_literal
                    |           empty_literal
                    |           character_string_literal"""
        p[0] = p[1]

    ###########################################################
    # T0D0: find out what ICONST is
    def p_integer_literal(self, p):
        """integer_literal:     ICONST"""

    ###########################################################

    def p_boolean_literal(self, p):
        """boolean_literal:     FALSE | TRUE"""

    ###########################################################
    # T0D0: check the meaning of this rule
    def p_character_literal(self, p):
        """character_literal:   CCONST """

    ###########################################################

    def p_empty_literal(self, p):
        """empty_literal:       NULL"""
        p[0] = p[1]

    ##
    def p_character_string_literal_char(self, p):
        """character_string_literal;    DOUBLEQUO character_list DOUBLEQUO"""

    def p_character_string_literal(self, p):
        """character_string_literal;    DOUBLEQUO DOUBLEQUO"""

    def p_character_list_rec(self, p):
        """character_list:      character_list character"""

    def p_character_list_rec(self, p):
        """character_list:      character"""

    def p_value_array_element(self, p):
        """value_array_element:         array_primitive_value LBRACK expression_list RBRACK"""

    def p_value_array_slice(self, p):
        """value_array_slice:   array_primitive_value LBRACK lower_element COLON upper_element RBRACK"""

    def p_array_primitive_value(self, p):
        """array_primitive_value:       primitive_value"""

    def p_parenthesized_expression(self, p):
        """parenthesized_expression:    LPAREN expression RPAREN"""

    def p_expression(self, p):
        """expression:          operand0 | conditional_expression"""

    def p_conditional_expression(self, p):
        """conditional_expression:  IF boolean_expression then_expression else_expression FI"""

    def p_conditional_expression_elsif(self, p):
        """conditional_expression:  IF boolean_expression then_expression elsif_expression else_expression FI"""

    def p_boolean_expression(self, p):
        """boolean_expression:  expression"""

    def p_then_expression(self, p):
        """then_expression:     THEN expression"""

    def p_else_expression(self, p):
        """else_expression:     ELSE expression"""

    # this rule might have to be changed with the next one depending on the parsing rules
    def p_elsif_expression_elsif(self, p):
        """elsif_expression:    elsif_expression ELSIF boolean_expression then_expression"""

    def p_elsif_expression(self, p):
        """elsif_expression:    ELSIF boolean_expression then_expression"""

    def p_operand0(self, p):
        """operand0:            operand1"""

    def p_operand0_op1(self, p):
        """operand0:            operand0 operator1 operand1"""

    def p_operator1(self, p):
        """operator1:           relational_operator | membership_operator"""

    def p_relational_operator(self, p):
        """relational_operator:     DBL_AMPERSAND | DBL_STRSLASH | DBLEQUAL | DIF | GTR | GEQ | LSS | LEQ"""

    def p_membership_operator(self, p):
        """membership_operator:     IN"""

    def p_operand1(self, p):
        """operand1:            operand2"""

    def p_operand1_op2(self, p):
        """operand1:            operand1 operator2 operand2"""

    def p_operator2(self, p):
        """operator2:           arithmetic_additive_operator
                    |           string_concatenation_operator"""

    def p_arithmetic_additive_operator(self, p):
        """arithmetic_additive_operator:        PLUS | MINUS"""

    def p_string_concatenation_operator(self, p):
        """string_concatenation_operator:       AMPERSAND"""

    def p_operand2(self, p):
        """operand2:            operand3"""

    def p_operand2_op3(self, p):
        """operand2:            operand2 arithmetic_multiplicative_operator operand3"""

    def p_arithmetic_multiplicative_operator(self, p):
        """arithmetic_multiplicative_operator:      TIMES | DIVIDE | PERC"""

    def p_operand3_monadic(self, p):
        """operand3:            monadic_operator operand4"""

    def p_operand3(self, p):
        """operand3:            operand4
                    |           integer_literal"""

    def p_monadic_operator(self, p):
        """monadic_operator:    MINUS | EXCLAMMARK"""

    def p_operand4(self, p):
        """operand4:            location | referenced_location | primitive_value"""

    def p_referenced_location(self, p):
        """referenced_location:         ARROW location"""

    def p_action_statement_id(self, p):
        """action_statement:    label_id COLON action SEMICOL"""
        p[0] = ("action_statement_label", p[3], p[1])

    def p_action_statement(self, p):
        """action_statement:    action SEMICOL"""
        p[0] = ("action_statement", p[1])

    def p_label_id(self, p):
        """label_id:            identifier"""

    def p_action(self, p):
        """action:              bracketed_action
                    |           assignment_action
                    |           call_action
                    |           exit_action
                    |           return_action
                    |           result_action"""

    def p_bracketed_action(self, p):
        """bracketed_action:    if_action | do_action"""

    def p_assignment_action(self, p):
        """assignment_action:   location assigning_operator expression"""

    def p_assigning_operator(self, p):
        """assigning_operator:  closed_dyadic_operator assignment_symbol"""

    def p_closed_dyadic_operator(self, p):
        """closed_dyadic_operator:      arithmetic_additive_operator
                    |                   arithmetic_multiplicative_operator
                    |                   string_concatenation_operator"""

    def p_assignment_symbol(self, p):
        """assignment_symbol:   EQUALS"""

    def p_if_action_else(self, p):
        """if_action:           IF boolean_expression then_clause else_clause FI"""

    def p_if_action(self, p):
        """if_action:           IF boolean_expression then_clause FI"""

    def p_then_clause_action(self, p):
        """then_clause:         THEN action_statement_list"""

    def p_then_clause(self, p):
        """then_clause:         THEN """

    def p_else_clause_elsif_else(self, p):
        """else_clause:         ELSIF boolean_expression then_clause else_clause"""

    def p_else_clause_elsif(self, p):
        """else_clause:         ELSIF boolean_expression then_clause"""

    def p_else_clause_action(self, p):
        """else_clause:         ELSE action_statement_list"""

    def p_else_clause(self, p):
        """else_clause:         ELSE"""

    def p_do_action_control(self, p):
        """do_action:           DO control_part SEMICOL action_statement_list OD"""

    def p_do_action_control_zero(self, p):
        """do_action:           DO control_part SEMICOL OD"""

    def p_do_action(self, p):
        """do_action:           DO action_statement_list OD"""

    def p_do_action_zero(self, p):
        """do_action:           DO OD"""

    def p_control_part_forwhile(self, p):
        """control_part:        for_control while_control"""

    def p_control_part(self, p):
        """control_part:        for_control
                    |           while_control"""

    def p_for_control(self, p):
        """for_control:         FOR iteration"""

    def p_iteration(self, p):
        """iteration:           step_enumeration | range_enumeration"""

    def p_step_enumeration_stepvalue_down(self, p):
        """step_enumeration:    loop_counter assignment_symbol start_value step_value DOWN end_value"""

    def p_step_enumeration_stepvalue(self, p):
        """step_enumeration:    loop_counter assignment_symbol start_value step_value end_value"""

    def p_step_enumeration_down(self, p):
        """step_enumeration:    loop_counter assignment_symbol start_value DOWN end_value"""

    def p_step_enumeration(self, p):
        """step_enumeration:    loop_counter assignment_symbol start_value end_value"""

    def p_loop_counter(self, p):
        """loop_counter:        identifier"""

    def p_start_value(self, p):
        """start_value:         discrete_expression"""

    def p_step_value(self, p):
        """step_value:          BY integer_expression"""

    def p_end_value(self, p):
        """end_value:           TO discrete_expression"""

    def p_discrete_expression(self, p):
        """discrete_expression:     expression"""

    def p_range_enumeration_down(self, p):
        """range_enumeration:       loop_counter DOWN IN discrete_mode_name"""

    def p_range_enumeration(self, p):
        """range_enumeration:       loop_counter IN discrete_mode_name"""

    def p_while_control(self, p):
        """while_control:       WHILE boolean_expression"""
        p[0] = ("while_control", p[2])

    def p_call_action(self, p):
        """call_action:         procedure_call | builtin_call"""
        p[0] = ("call_action", p[1])

    def p_procedure_call_parameter(self, p):
        """procedure_call:      procedure_name LPAREN parameter_list RPAREN"""
        p[0] = ("procedure_call_param", p[1], p[3])

    def p_procedure_call(self, p):
        """procedure_call:      procedure_name LPAREN RPAREN"""
        p[0] = ("procedure_call", p[1])

    def p_parameter_list_rec(self, p):
        # the first line might need to be reversed depending on the parsing rules
        """parameter_list:      parameter_list COMMA parameter"""
        p[0] = p[1] + (p[3],)

    def p_parameter_list(self, p):
        """parameter_list:      parameter"""
        p[0] = p[1]

    def p_parameter(self, p):
        """parameter:           expression"""
        p[0] = p[1]

    def p_procedure_name(self, p):
        """procedure_name:      ID"""
        p[0] = p[1]

    def p_exit_action(self, p):
        """exit_action:         EXIT label_id"""
        p[0] = ("exit_action", p[2])

    def p_return_action_result(self, p):
        """return_action:       RETURN result"""
        p[0] = ("return_action_result", p[2])

    def p_return_action(self, p):
        """return_action:       RETURN"""
        p[0] = ("return_action",)

    def p_result_action_result(self, p):
        """result_action:       RESULT result"""
        p[0] = ("result_action", p[2])

    def p_result(self, p):
        """result:              expression"""
        p[0] = p[1]

    def p_builtin_call_parameter(self, p):
        """builtin_call:        builtin_name LPAREN parameter_list RPAREN"""
        p[0] = ("builtin_call_param", p[1], p[3])

    def p_builtin_call(self, p):
        """builtin_call:        builtin_name LPAREN RPAREN"""
        p[0] = ("builtin_call", p[1])

    def p_builtin_name(self, p):
        """builtin_name:        NUM | PRED | SUCC | UPPER | LOWER | LENGTH | READ | PRINT"""
        p[0] = ("builtin_name", p[1])

    def p_procedure_statement(self, p):
        """procedure_statement:     label_id COLON procedure_definition SEMICOL"""
        p[0] = ("procedure_statement", p[1], p[3])

    def p_action_statement_list_rec(self, p):
        """action_statement_list:   action_statement_list action_statement"""
        p[0] = p[1] + (p[2],)

    def p_action_statement_list(self, p):
        """action_statement_list:   action_statement"""
        p[0] = p[1]

    ###
    def p_procedure_definition_parameter_result_statement(self, p):
        """procedure_definition:    PROC LPAREN formal_parameter_list RPAREN result_spec SEMICOL statement_list END"""
        p[0] = ("proc_param_rslt_sttm", p[3], p[5], p[7])

    def p_procedure_definition_parameter_statement(self, p):
        """procedure_definition:    PROC LPAREN formal_parameter_list RPAREN SEMICOL statement_list END"""
        p[0] = ("proc_param_sttm", p[3], p[6])

    def p_procedure_definition_result_statement(self, p):
        """procedure_definition:    PROC LPAREN RPAREN result_spec SEMICOL statement_list END"""
        p[0] = ("proc_rslt_sttm", p[4], p[6])

    def p_procedure_definition_statement(self, p):
        """procedure_definition:    PROC LPAREN RPAREN SEMICOL statement_list END"""
        p[0] = ("proc_sttm", p[5])

    def p_procedure_definition_parameter_result(self, p):
        """procedure_definition:    PROC LPAREN formal_parameter_list RPAREN result_spec SEMICOL END"""
        p[0] = ("proc_param_rslt", p[3], p[5])

    def p_procedure_definition_parameter(self, p):
        """procedure_definition:    PROC LPAREN formal_parameter_list RPAREN SEMICOL END"""
        p[0] = ("proc_param", p[3])

    def p_procedure_definition_result(self, p):
        """procedure_definition:    PROC LPAREN RPAREN result_spec SEMICOL END"""
        p[0] = ("proc_rslt", p[4])

    def p_procedure_definition(self, p):
        """procedure_definition:    PROC LPAREN RPAREN SEMICOL END"""
        p[0] = ("proc",)

    def p_formal_parameter_list_rec(self, p):
        """formal_parameter_list:   formal_parameter_list COMMA formal_parameter"""
        p[0] = p[1] + (p[3],)

    def p_formal_parameter_list(self, p):
        """formal_parameter_list:   formal_parameter"""
        p[0] = p[1]

    def p_formal_parameter(self, p):
        """formal_parameter:        identifier_list parameter_spec"""
        p[0] = ("formal_parameter", p[1], p[2])

    def p_parameter_spec_attr(self, p):
        """parameter_spec:          mode parameter_attribute"""
        p[0] = ("parameter_spec_att", p[1], p[2])

    def p_parameter_spec(self, p):
        """parameter_spec:          mode"""
        p[0] = ("parameter_spec", p[1])

    def p_parameter_attribute(self, p):
        """parameter_attribute:     LOC"""
        p[0] = ("loc",)

    def p_result_spec_attr(self, p):
        """result_spec:             RETURNS LPAREN mode result_attribute RPAREN"""
        p[0] = ("returns_mode_att", p[3], p[4])

    def p_result_spec(self, p):
        """result_spec:             RETURNS LPAREN mode RPAREN"""
        p[0] = ("returns_mode", p[3])

    def p_result_attribute(self, p):
        """result_attribute:        LOC"""
        p[0] = ("loc",)

    # T0D0: create the functions
    ##########################################################################
    def p_expression_name(self, p):
        'expression : ID'
        try:
            p[0] = names[p[1]]
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0

    def p_error(self, p):
        print("Syntax error at '%s'" % p.value)

    import ply.yacc as yacc
    parser = yacc.yacc()

    while True:
        try:
            s = input('calc > ')  # Use raw_input on Python 2
        except EOFError:
            break
        parser.parse(s)
