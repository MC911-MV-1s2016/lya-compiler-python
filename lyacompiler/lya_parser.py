#!/usr/bin/env python3
# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lya_parser.py
# Parser and AST builder for the Lya scripting language.
#
# ------------------------------------------------------------

from .ply import yacc

from .lya_lexer import LyaLexer
from .lya_errors import LyaSyntaxError
from .lya_ast import *


class LyaParser(object):
    def __init__(self):
        """ Create a new LyaParser.
        """
        self.lex = LyaLexer()
        self.lex.build()
        self.tokens = self.lex.tokens

        self.parser = yacc.yacc(module=self)

        # Keeps track of the last token given to yacc
        self._last_yielded_token = None

    def parse(self, text):
        """ Parses Lya code and returns an AST.
        """
        self.lex.reset_lineno()
        self._last_yielded_token = None
        ret = self.parser.parse(input=text, lexer=self.lex)
        return ret

    # Private

    # Precedence
    precedence = (
        ('left', 'ASSIGN'),
        # ('left', 'LOR'),
        # ('left', 'LAND'),
        ('left', 'OR'),
        # ('left', 'XOR'),
        ('left', 'AND'),
        ('left', 'EQUALS', 'DIF'),
        ('left', 'GTR', 'GEQ', 'LSS', 'LEQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'PERC'),
        ('right', 'UMINUS'),  # Unary minus operator
    )

    # Grammar productions

    def p_program(self, p):
        """program : statement_list"""
        p[0] = Program(p[1])

    # Statement ------------------------------------------------------

    def p_statement_list(self, p):
        """statement_list : statement_list statement
                          | statement"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        """statement : declaration_statement
                     | synonym_statement
                     | newmode_statement
                     | procedure_statement
                     | action_statement"""
        p[0] = p[1]

    def p_declaration_statement(self, p):
        """declaration_statement : DCL declaration_list SEMICOL"""
        p[0] = DeclarationStatement(p[2])

    def p_synonym_statement(self, p):
        """synonym_statement : SYN synonym_list SEMICOL"""
        p[0] = SynonymStatement(p[2])

    def p_newmode_statement(self, p):
        """newmode_statement : TYPE newmode_list SEMICOL"""
        p[0] = NewModeStatement(p[2])

    def p_procedure_statement(self, p):
        """procedure_statement : label_id COLON procedure_definition SEMICOL"""
        p[0] = ProcedureStatement(p[1], p[3])

    def p_action_statement_label(self, p):
        """action_statement : label_id COLON action SEMICOL"""
        p[0] = LabeledAction(p[1], p[3])

    def p_action_statement(self, p):
        """action_statement : action SEMICOL"""
        p[0] = p[1]

    # Declaration --------------------------------------------------

    def p_declaration_list(self, p):
        """declaration_list : declaration_list COMMA declaration
                            | declaration"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_declaration(self, p):
        """declaration : identifier_list mode initialization
                       | identifier_list mode"""
        if len(p) == 3:
            p[0] = Declaration(p[1], p[2], None)
        else:
            p[0] = Declaration(p[1], p[2], p[3])

    def p_initialization(self, p):
        """initialization : ASSIGN expression"""
        p[0] = p[2]

    # Synonym -------------------------------------------------------

    def p_synonym_list(self, p):
        """synonym_list : synonym_list COMMA synonym_definition
                        | synonym_definition"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_synonym_definition_mode(self, p):
        """synonym_definition : identifier_list mode ASSIGN constant_expression
                              | identifier_list ASSIGN constant_expression"""
        if len(p) == 4:
            p[0] = SynonymDefinition(p[1], None, p[3])
        else:
            p[0] = SynonymDefinition(p[1], p[2], p[4])

    def p_constant_expression(self, p):
        """constant_expression : expression"""
        p[0] = p[1]

    # Mode ------------------------------------------------------------

    def p_newmode_list(self, p):
        """newmode_list : newmode_list COMMA mode_definition
                        | mode_definition"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_mode_definition(self, p):
        """mode_definition : identifier_list ASSIGN mode"""
        p[0] = ModeDefinition(p[1], p[3])

    def p_mode(self, p):
        """mode : mode_name
                | discrete_mode
                | reference_mode
                | composite_mode"""
        p[0] = Mode(p[1])

    def p_discrete_mode(self, p):
        """discrete_mode : integer_mode
                         | boolean_mode
                         | character_mode
                         | discrete_range_mode"""
        if isinstance(p[1], DiscreteRangeMode):
            p[0] = p[1]
        else:
            p[0] = DiscreteMode(p[1])

    def p_integer_mode(self, p):
        """integer_mode : INT"""
        p[0] = p[1]

    def p_boolean_mode(self, p):
        """boolean_mode : BOOL"""
        p[0] = p[1]

    def p_character_mode(self, p):
        """character_mode : CHAR"""
        p[0] = p[1]

    def p_discrete_range_mode(self, p):
        """discrete_range_mode : identifier  LPAREN literal_range RPAREN
                               | discrete_mode LPAREN literal_range RPAREN"""
        # TODO: identifier case, check like loc if defined
        p[0] = DiscreteRangeMode(p[1], p[3])

    def p_mode_name(self, p):
        """mode_name : identifier"""
        p[0] = p[1]

    def p_literal_range(self, p):
        """literal_range : lower_bound COLON upper_bound"""
        p[0] = LiteralRange(p[1], p[3])

    def p_lower_bound(self, p):
        """lower_bound : expression"""
        p[0] = p[1]

    def p_upper_bound(self, p):
        """upper_bound : expression"""
        p[0] = p[1]

    def p_reference_mode(self, p):
        """reference_mode : REF mode"""
        # TODO: check if mode_name is defined
        p[0] = ReferenceMode(p[2])

    def p_composite_mode(self, p):
        """composite_mode : string_mode
                          | array_mode"""
        p[0] = p[1]

    def p_string_mode(self, p):
        """string_mode : CHARS LBRACK string_length RBRACK"""
        p[0] = StringMode(p[3])

    def p_string_length(self, p):
        """string_length : integer_literal"""
        p[0] = p[1]

    def p_array_mode(self, p):
        """array_mode : ARRAY LBRACK index_mode_list RBRACK element_mode"""
        p[0] = ArrayMode(p[3], p[5], lineno=p.lineno(1))

    # To support array[10], add new rule ARRAY LBRACK integer_literal

    def p_index_mode_list(self, p):
        """index_mode_list : index_mode_list COMMA index_mode
                           | index_mode"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_index_mode(self, p):
        """index_mode : literal_range"""
        # """index_mode : discrete_mode
        #               | literal_range"""
        p[0] = p[1]
        # Só aceitar literal_range com const_exp e iconst

    def p_element_mode(self, p):
        """element_mode : mode"""
        p[0] = p[1]

    # Identifier ----------------------------------------------------

    def p_identifier_list(self, p):
        """identifier_list : identifier
                           | identifier_list COMMA identifier"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_identifier(self, p):
        """identifier : ID"""
        p[0] = Identifier(p[1], lineno=p.lineno(1))

    # Location ------------------------------------------------------

    def p_location(self, p):
        """location : location_name
                    | dereferenced_reference
                    | string_element
                    | string_slice
                    | array_element
                    | array_slice
                    | call_action"""
        p[0] = Location(p[1])

    def p_location_name(self, p):
        """location_name : identifier"""
        p[0] = p[1]

    def p_dereferenced_reference(self, p):
        """dereferenced_reference : location ARROW"""
        p[0] = DereferencedReference(p[1])
        # TODO: check if location is RefType

    def p_string_element(self, p):
        """string_element : identifier LBRACK start_element RBRACK"""
        # TODO: Check identifier as location if defined
        p[0] = StringElement(p[1], p[3])

    def p_start_element(self, p):
        """start_element : integer_expression"""
        p[0] = StartElement(p[1])

    def p_string_slice(self, p):
        """string_slice : identifier LBRACK left_element COLON right_element RBRACK"""
        # TODO: Check identifier as location if defined
        p[0] = StringSlice(p[1], p[3], p[5])

    def p_left_element(self, p):
        """left_element : integer_expression"""
        p[0] = p[1]

    def p_right_element(self, p):
        """right_element : integer_expression"""
        p[0] = p[1]

    def p_array_element(self, p):
        """array_element : array_location LBRACK expression_list RBRACK"""
        p[0] = ArrayElement(p[1], p[3])

    def p_array_slice(self, p):
        """array_slice : array_location LBRACK lower_bound COLON upper_bound RBRACK"""
        p[0] = ArraySlice(p[1], p[3], p[5])

    def p_array_location(self, p):
        """array_location : location"""
        p[0] = p[1]

    # Primitive Values ----------------------------------------------

    def p_primitive_value(self, p):
        """primitive_value : literal
                           | value_array_element
                           | value_array_slice
                           | parenthesized_expression"""
        p[0] = p[1]

    def p_literal(self, p):
        """literal : integer_literal
                   | boolean_literal
                   | character_literal
                   | empty_literal
                   | character_string_literal"""
        p[0] = p[1]

    def p_integer_literal(self, p):
        """integer_literal : ICONST"""
        p[0] = IntegerConstant(p[1])

    def p_boolean_literal(self, p):
        """boolean_literal : FALSE
                           | TRUE"""
        p[0] = BooleanConstant(p[1])

    def p_character_literal(self, p):
        """character_literal : CCONST """
        p[0] = CharacterConstant(p[1][1:-1])      # Removing ''

    def p_empty_literal(self, p):
        """empty_literal : NULL"""
        p[0] = EmptyConstant(p[1])

    def p_character_string_literal_char(self, p):
        """character_string_literal : SCONST"""
        p[0] = StringConstant(p[1][1:-1])   # Removing ""

    # Array

    def p_value_array_element(self, p):
        """value_array_element : array_primitive_value LBRACK expression_list RBRACK"""
        p[0] = ValueArrayElement(p[1], p[3])

    def p_value_array_slice(self, p):
        """value_array_slice : array_primitive_value LBRACK lower_bound COLON upper_bound RBRACK"""
        p[0] = ValueArraySlice(p[1], p[3], p[5])

    def p_array_primitive_value(self, p):
        """array_primitive_value : primitive_value"""
        p[0] = p[1]

    # Expression

    def p_parenthesized_expression(self, p):
        """parenthesized_expression : LPAREN expression RPAREN"""
        p[0] = p[2]

    def p_expression_list(self, p):
        """expression_list : expression_list COMMA expression
                           | expression"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expression(self, p):
        """expression : operand0
                      | conditional_expression"""
        p[0] = Expression(p[1])

    def p_conditional_expression(self, p):
        """conditional_expression : IF boolean_expression then_expression else_expression FI"""
        p[0] = ConditionalExpression(p[2], p[3], None, p[4])

    def p_conditional_expression_elsif(self, p):
        """conditional_expression : IF boolean_expression then_expression elsif_expression else_expression FI"""
        p[0] = ConditionalExpression(p[2], p[3], p[4], p[5])

    def p_integer_expression(self, p):
        """integer_expression : expression"""
        p[0] = IntegerExpression(p[1])

    def p_boolean_expression(self, p):
        """boolean_expression : expression"""
        p[0] = BooleanExpression(p[1])

    def p_then_expression(self, p):
        """then_expression : THEN expression"""
        p[0] = ThenExpression(p[2])

    def p_else_expression(self, p):
        """else_expression : ELSE expression"""
        p[0] = ElseExpression(p[2])

    def p_elsif_expression_elsif(self, p):
        """elsif_expression : elsif_expression ELSIF boolean_expression then_expression"""
        p[0] = ElsifExpression(p[1], p[3], p[4])

    def p_elsif_expression(self, p):
        """elsif_expression : ELSIF boolean_expression then_expression"""
        p[0] = ElsifExpression(None, p[2], p[3])

    def p_operand0_operand1(self, p):
        """operand0 : operand1"""
        p[0] = p[1]

    def p_operand0_relational_exp(self, p):
        """operand0 : operand0 relational_operator operand1"""
        p[0] = RelationalExpression(p[1], p[2], p[3])

    def p_operand0_membership_exp(self, p):
        """operand0 : operand0 membership_operator operand1"""
        p[0] = MembershipExpression(p[1], p[2], p[3])

    def p_relational_operator(self, p):
        """relational_operator : AND
                               | OR
                               | EQUALS
                               | DIF
                               | GTR
                               | GEQ
                               | LSS
                               | LEQ"""
        p[0] = p[1]

    def p_membership_operator(self, p):
        """membership_operator : IN"""
        p[0] = p[1]

    def p_operand1_operand2(self, p):
        """operand1 : operand2"""
        p[0] = p[1]

    def p_operand1_op2(self, p):
        """operand1 : operand1 operator2 operand2"""
        p[0] = BinaryExpression(p[1], p[2], p[3])

    def p_operator2(self, p):
        """operator2 : arithmetic_additive_operator
                     | string_concatenation_operator"""
        p[0] = p[1]

    def p_arithmetic_additive_operator(self, p):
        """arithmetic_additive_operator : PLUS
                                        | MINUS"""
        p[0] = p[1]

    def p_string_concatenation_operator(self, p):
        """string_concatenation_operator : CONCAT"""
        p[0] = p[1]

    def p_operand2_operand3(self, p):
        """operand2 : operand3"""
        p[0] = p[1]

    def p_operand2_op3(self, p):
        """operand2 : operand2 arithmetic_multiplicative_operator operand3"""
        p[0] = BinaryExpression(p[1], p[2], p[3])

    def p_arithmetic_multiplicative_operator(self, p):
        """arithmetic_multiplicative_operator : TIMES
                                              | DIVIDE
                                              | PERC"""
        p[0] = p[1]

    def p_operand3_uminus(self, p):
        """operand3 : MINUS operand4 %prec UMINUS"""
        p[0] = UnaryExpression(p[1], p[2])

    def p_operand3_monadic(self, p):
        """operand3 : NOT operand4"""
        p[0] = UnaryExpression(p[1], p[2])

    def p_operand3(self, p):
        """operand3 : operand4"""
        p[0] = p[1]

    def p_operand4(self, p):
        """operand4 : location
                    | referenced_location
                    | primitive_value"""
        p[0] = p[1]

    def p_referenced_location(self, p):
        """referenced_location : ARROW location"""
        p[0] = ReferencedLocation(p[2])

    # Action Statement ---------------------------------------------------

    def p_action_statement_list(self, p):
        """action_statement_list : action_statement_list action_statement
                                 | action_statement"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_label_id(self, p):
        """label_id : identifier"""
        p[0] = p[1]

    def p_action(self, p):
        """action : bracketed_action
                  | assignment_action
                  | call_action
                  | exit_action
                  | return_action
                  | result_action"""
        p[0] = Action(p[1])

    def p_bracketed_action(self, p):
        """bracketed_action : if_action
                             | do_action"""
        p[0] = BracketedAction(p[1])

    def p_assignment_action(self, p):
        """assignment_action : location assigning_operator expression"""
        # names[p[1]]=p[3]
        p[0] = Assignment(p[1], p[2], p[3])

    def p_assigning_operator(self, p):
        """assigning_operator : ASSIGN
                              | PLUSASSIGN
                              | MINUSASSIGN
                              | TIMESASSIGN
                              | DIVIDEASSIGN
                              | PERCASSIGN
                              | CONCATASSIGN"""
        p[0] = p[1]

    # if-then-else ------------------------------------------------------

    def p_if_action_else(self, p):
        """if_action : IF boolean_expression then_clause else_clause FI"""
        p[0] = IfAction(p[2], p[3], p[4])

    def p_if_action(self, p):
        """if_action : IF boolean_expression then_clause FI"""
        p[0] = IfAction(p[2], p[3], None)

    def p_then_clause(self, p):
        """then_clause : THEN action_statement_list"""
        p[0] = ThenClause(p[2])

    def p_then_clause_empty(self, p):
        """then_clause : THEN empty"""
        p[0] = ThenClause(None)

    def p_else_clause(self, p):
        """else_clause : ELSE action_statement_list"""
        p[0] = ElseClause(p[2])

    def p_else_clause_empty(self, p):
        """else_clause : ELSE empty"""
        p[0] = ElseClause(None)

    def p_else_clause_if_else(self, p):
        """else_clause : ELSIF boolean_expression then_clause else_clause"""
        p[0] = ElsifClause(p[2], p[3], p[4])

    def p_else_clause_if(self, p):
        """else_clause : ELSIF boolean_expression then_clause"""
        p[0] = ElsifClause(p[2], p[3], None)

    def p_do_action_control_action(self, p):
        """do_action : DO control_part SEMICOL action_statement_list OD"""
        p[0] = DoAction(p[2], p[4])

    def p_do_action_control(self, p):
        """do_action : DO control_part SEMICOL OD"""
        p[0] = DoAction(p[2], None)

    def p_do_action(self, p):
        """do_action : DO action_statement_list OD"""
        p[0] = DoAction(None, p[2])

    def p_do_action_zero(self, p):
        """do_action : DO OD"""
        p[0] = DoAction(None, None)

    def p_control_part_forwhile(self, p):
        """control_part : for_control while_control"""
        p[0] = DoControl(p[1], p[2])

    def p_control_part_for(self, p):
        """control_part : for_control"""
        p[0] = DoControl(p[1], None)

    def p_control_part_while(self, p):
        """control_part : while_control"""
        p[0] = DoControl(None, p[1])

    def p_for_control(self, p):
        """for_control : FOR iteration"""
        p[0] = ForControl(p[2])

    def p_iteration(self, p):
        """iteration : range_enumeration
                     | step_enumeration"""
        p[0] = p[1]

    def p_step_enumeration_stepvalue_down(self, p):
        """step_enumeration : loop_counter ASSIGN start_value step_value DOWN end_value"""
        p[0] = StepEnumeration(p[1], p[3], p[4], True, p[6], lineno=p.lineno(2))

    def p_step_enumeration_stepvalue(self, p):
        """step_enumeration : loop_counter ASSIGN start_value step_value end_value"""
        p[0] = StepEnumeration(p[1], p[3], p[4], False, p[5], lineno=p.lineno(2))

    def p_step_enumeration_down(self, p):
        """step_enumeration : loop_counter ASSIGN start_value DOWN end_value"""
        p[0] = StepEnumeration(p[1], p[3], None, True, p[5], lineno=p.lineno(2))

    def p_step_enumeration(self, p):
        """step_enumeration : loop_counter ASSIGN start_value end_value"""
        p[0] = StepEnumeration(p[1], p[3], None, False, p[4], lineno=p.lineno(2))

    def p_loop_counter(self, p):
        """loop_counter : identifier"""
        p[0] = p[1]

    def p_start_value(self, p):
        """start_value : discrete_expression"""
        p[0] = p[1]

    def p_step_value(self, p):
        """step_value : BY integer_expression"""
        p[0] = p[2]

    def p_end_value(self, p):
        """end_value : TO discrete_expression"""
        p[0] = p[2]

    def p_discrete_expression(self, p):
        """discrete_expression : expression"""
        p[0] = p[1]

    def p_range_enumeration_down(self, p):
        """range_enumeration : loop_counter DOWN IN discrete_mode"""
        p[0] = RangeEnumeration(p[1], True, p[4])

    def p_range_enumeration(self, p):
        """range_enumeration : loop_counter IN discrete_mode"""
        p[0] = RangeEnumeration(p[1], False, p[3])

    def p_while_control(self, p):
        """while_control : WHILE boolean_expression"""
        p[0] = WhileControl(p[2], lineno=p.lineno(1))

    # Actions ------------------------------------------------------------

    def p_call_action(self, p):
        """call_action : procedure_call
                       | builtin_call"""
        p[0] = CallAction(p[1])

    def p_procedure_call_parameter(self, p):
        """procedure_call : procedure_name LPAREN parameter_list RPAREN"""
        p[0] = ProcedureCall(p[1], p[3], lineno=p.lineno(2))

    def p_procedure_call(self, p):
        """procedure_call : procedure_name LPAREN RPAREN"""
        # TODO: Check if name defined as procedure
        p[0] = ProcedureCall(p[1], list(), lineno=p.lineno(2))

    def p_parameter_list(self, p):
        """parameter_list : parameter_list COMMA parameter
                          | parameter"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_parameter(self, p):
        """parameter : expression"""
        p[0] = p[1]

    def p_procedure_name(self, p):
        """procedure_name : identifier"""
        p[0] = p[1]

    def p_exit_action(self, p):
        """exit_action : EXIT label_id"""
        # TODO: Check if defined as label
        p[0] = ExitAction(p[2])

    def p_return_action_result(self, p):
        """return_action : RETURN result"""
        p[0] = ReturnAction(p[2], lineno=p.lineno(1))

    def p_return_action(self, p):
        """return_action : RETURN"""
        p[0] = ReturnAction(None, lineno=p.lineno(1))

    def p_result_action(self, p):
        """result_action : RESULT result"""
        p[0] = ResultAction(p[2], lineno=p.lineno(1))

    def p_result(self, p):
        """result : expression"""
        p[0] = p[1]

    def p_builtin_call_parameter(self, p):
        """builtin_call : builtin_name LPAREN parameter_list RPAREN"""
        p[0] = BuiltinCall(p[1], p[3])

    def p_builtin_call(self, p):
        """builtin_call : builtin_name LPAREN RPAREN"""
        p[0] = BuiltinCall(p[1], None)

    def p_builtin_name(self, p):
        """builtin_name : NUM
                        | PRED
                        | SUCC
                        | UPPER
                        | LOWER
                        | LENGTH
                        | READ
                        | PRINT"""
        p[0] = p[1]

    # Procedure -----------------------------------------------------------------

    def p_procedure_definition_prs(self, p):
        """procedure_definition : PROC LPAREN formal_parameter_list RPAREN result_spec SEMICOL statement_list END"""
        p[0] = ProcedureDefinition(p[3], p[5], p[7])

    def p_procedure_definition_pr(self, p):
        """procedure_definition : PROC LPAREN formal_parameter_list RPAREN result_spec SEMICOL END"""
        p[0] = ProcedureDefinition(p[3], p[5], None)

    def p_procedure_definition_ps(self, p):
        """procedure_definition : PROC LPAREN formal_parameter_list RPAREN SEMICOL statement_list END"""
        p[0] = ProcedureDefinition(p[3], None, p[6])

    def p_procedure_definition_rs(self, p):
        """procedure_definition : PROC LPAREN RPAREN result_spec SEMICOL statement_list END"""
        p[0] = ProcedureDefinition(None, p[4], p[6])

    def p_procedure_definition_p(self, p):
        """procedure_definition : PROC LPAREN formal_parameter_list RPAREN SEMICOL END"""
        p[0] = ProcedureDefinition(p[3], None, None)

    def p_procedure_definition_r(self, p):
        """procedure_definition : PROC LPAREN RPAREN result_spec SEMICOL END"""
        p[0] = ProcedureDefinition(None, p[4], None)

    def p_procedure_definition_s(self, p):
        """procedure_definition : PROC LPAREN RPAREN SEMICOL statement_list END"""
        p[0] = ProcedureDefinition(None, None, p[5])

    def p_procedure_definition(self, p):
        """procedure_definition : PROC LPAREN RPAREN SEMICOL END"""
        p[0] = ProcedureDefinition(None, None, None)

    def p_formal_parameter_list(self, p):
        """formal_parameter_list : formal_parameter_list COMMA formal_parameter
                                 | formal_parameter"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_formal_parameter(self, p):
        """formal_parameter : identifier_list parameter_spec"""
        p[0] = FormalParameter(p[1],  p[2])

    def p_parameter_spec(self, p):
        """parameter_spec : mode LOC
                          | mode"""
        if len(p) == 2:
            p[0] = ParameterSpec(p[1], QualifierType.none)
        else:
            p[0] = ParameterSpec(p[1], QualifierType.location)

    def p_result_spec_attr(self, p):
        """result_spec : RETURNS LPAREN mode LOC RPAREN"""
        p[0] = ResultSpec(p[3], QualifierType.location)

    def p_result_spec(self, p):
        """result_spec : RETURNS LPAREN mode RPAREN"""
        p[0] = ResultSpec(p[3], QualifierType.none)

    # Empty

    def p_empty(self, p):
        """empty :"""
        pass

    # Error

    def p_error(self, p):
        try:
            print("\n" + LyaColor.WARNING + str(LyaSyntaxError(p.lineno, p.value)) + LyaColor.ENDC)
        except Exception as err:
            print("\n" + LyaColor.WARNING + str(LyaSyntaxError(None, p)) + LyaColor.ENDC)
        finally:
            exit()
