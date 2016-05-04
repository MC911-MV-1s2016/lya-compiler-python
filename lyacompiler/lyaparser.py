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

from ply import yacc

from lyalexer import LyaLexer
from lya_ast import *


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
            p[0] = (p[1],)
        else:
            p[0] = p[1] + (p[2],)

    def p_statement(self, p):
        """statement : declaration_statement
                     | synonym_statement
                     | newmode_statement
                     | procedure_statement
                     | action_statement"""
        p[0] = p[1]

    def p_declaration_statement(self, p):
        """declaration_statement : DCL declaration_list SEMICOL"""
        #p[0] = ('DeclarationStatement (at line {0})'.format(p.lineno(1)), p[2])
        p[0] = DeclarationStatement(p[2])

    def p_synonym_statement(self, p):
        """synonym_statement : SYN synonym_list SEMICOL"""
        # p[0] = ('SynonymStatement (at line {0})'.format(p.lineno(1)), p[2])
        p[0] = SynonymStatement(p[2])

    def p_newmode_statement(self, p):
        """newmode_statement : TYPE newmode_list SEMICOL"""
        # p[0] = ('NewmodeStatement (at line {0})'.format(p.lineno(1)), p[2])
        p[0] = NewModeStatement(p[2])

    def p_procedure_statement(self, p):
        """procedure_statement : label_id COLON procedure_definition SEMICOL"""
        # p[0] = ('ProcedureStatement (at line {0})'.format(p.lineno(2)), p[2])
        p[0] = ProcedureStatement(p[1], p[3])

    def p_action_statement_label(self, p):
        """action_statement : label_id COLON action SEMICOL"""
        p[0] = ActionStatement(p[1], p[3])

    def p_action_statement(self, p):
        """action_statement : action SEMICOL"""
        p[0] = ActionStatement(None, p[1])

    # Declaration --------------------------------------------------

    def p_declaration_list(self, p):
        """declaration_list : declaration_list COMMA declaration
                            | declaration"""
        if len(p) == 2:
            p[0] = ((p[1]),)
        else:
            p[0] = p[1] + (p[3],)

    def p_declaration(self, p):
        """declaration : identifier_list mode initialization
                       | identifier_list mode"""
        if len(p) == 3:
            p[0] = ('Declaration', p[1], p[2])
        else:
            p[0] = ('Declaration', (p[1], p[2], p[3]))

    def p_initialization(self, p):
        """initialization : ASSIGN expression"""
        p[0] = p[2]

    # Synonym -------------------------------------------------------

    def p_synonym_list(self, p):
        """synonym_list : synonym_list COMMA synonym_definition
                        | synonym_definition"""
        if len(p) == 2:
            p[0] = ((p[1]),)
        else:
            p[0] = p[1] + (p[3],)

    def p_synonym_definition_mode(self, p):
        """synonym_definition : identifier_list mode ASSIGN constant_expression
                              | identifier_list ASSIGN constant_expression"""
        if len(p) == 4:
            p[0] = ('SynonymDefinition', p[1], p[3])
        else:
            p[0] = ('SynonymDefinition', p[1], p[2], p[4])

    def p_constant_expression(self, p):
        """constant_expression : expression"""
        p[0] = p[1]

    # Mode ------------------------------------------------------------

    def p_newmode_list(self, p):
        """newmode_list : newmode_list COMMA mode_definition
                        | mode_definition"""
        if len(p) == 2:
            p[0] = ((p[1]),)
        else:
            p[0] = p[1] + (p[3],)

    def p_mode_definition(self, p):
        """mode_definition : identifier_list ASSIGN mode"""
        p[0] = ('ModeDefinition', p[1], p[3])

    def p_mode(self, p):
        """mode : mode_name
                | discrete_mode
                | reference_mode
                | composite_mode"""
        p[0] = ('Mode', p[1])

    def p_discrete_mode(self, p):
        """discrete_mode : integer_mode
                         | boolean_mode
                         | character_mode
                         | discrete_range_mode"""
        p[0] = ('DiscreteMode', p[1])

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
        p[0] = ('DiscreteRangeMode', p[1], p[3])

    def p_mode_name(self, p):
        """mode_name : identifier"""
        p[0] = p[1]
    #
    # def p_discrete_mode_name(self, p):
    #     """discrete_mode_name : identifier"""
    #     p[0] = p[1]

    def p_literal_range(self, p):
        """literal_range : lower_bound COLON upper_bound"""
        p[0] = ('LiteralRange', (p[1], p[3]))

    def p_lower_bound(self, p):
        """lower_bound : expression"""
        p[0] = p[1]

    def p_upper_bound(self, p):
        """upper_bound : expression"""
        p[0] = p[1]

    def p_reference_mode(self, p):
        """reference_mode : REF mode"""
        p[0] = ('ReferenceMode', p[2])

    def p_composite_mode_string(self, p):
        """composite_mode : string_mode
                          | array_mode"""
        p[0] = ('CompositeMode', p[1])

    def p_string_mode(self, p):
        """string_mode : CHARS LBRACK string_length RBRACK"""
        p[0] = ('StringMode', p[3])

    def p_string_length(self, p):
        """string_length : integer_literal"""
        p[0] = ('Length', p[1])

    def p_array_mode(self, p):
        """array_mode : ARRAY LBRACK index_mode_list RBRACK element_mode"""
        p[0] = ('ArrayMode', p[3], p[5])

    def p_index_mode_list(self, p):
        """index_mode_list : index_mode_list COMMA index_mode
                           | index_mode"""
        if len(p) == 2:
            p[0] = ((p[1]),)
        else:
            p[0] = p[1] + (p[3],)

    def p_index_mode(self, p):
        """index_mode : discrete_mode
                      | literal_range"""
        p[0] = ('IndexMode', p[1])

    def p_element_mode(self, p):
        """element_mode : mode"""
        p[0] = ('ElementMode', p[1])

    # Identifier ----------------------------------------------------

    def p_identifier_list(self, p):
        """identifier_list : identifier
                           | identifier_list COMMA identifier"""
        if len(p) == 2:
            p[0] = (p[1],)
        else:
            p[0] = p[1] + (p[3],)

    def p_identifier(self, p):
        """identifier : ID"""
        p[0] = ('Identifier', p[1])

    # Location ------------------------------------------------------

    def p_location(self, p):
        """location : location_name
                    | dereferenced_reference
                    | string_element
                    | string_slice
                    | array_element
                    | array_slice
                    | call_action"""
        p[0] = ('Location', p[1])

    def p_location_name(self, p):
        """location_name : identifier"""
        p[0] = p[1]

    def p_dereferenced_reference(self, p):
        """dereferenced_reference : location ARROW"""
        p[0] = (p[1], p[2])

    def p_string_element(self, p):
        """string_element : identifier LBRACK start_element RBRACK"""
        p[0] = ("StringElement", p[1], p[3])

    def p_start_element(self, p):
        """start_element : integer_expression"""
        p[0] = ("StartElement", p[1])

    def p_string_slice(self, p):
        """string_slice : identifier LBRACK left_element COLON right_element RBRACK"""
        p[0] = ("StringSlice", p[1], (p[3], p[5]))

    # def p_string_location(self, p):
    #     """string_location : identifier"""
    #     p[0] = p[1]

    def p_left_element(self, p):
        """left_element : integer_expression"""
        p[0] = p[1]

    def p_right_element(self, p):
        """right_element : integer_expression"""
        p[0] = p[1]

    def p_array_element(self, p):
        """array_element : array_location LBRACK expression_list RBRACK"""
        p[0] = ("ArrayElement", p[1], p[3])

    def p_array_slice(self, p):
        """array_slice : array_location LBRACK lower_bound COLON upper_bound RBRACK"""
        p[0] = ("ArraySlice", p[1], (p[3], p[5]))

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
        p[0] = ('IntegerConstant', p[1])

    def p_boolean_literal(self, p):
        """boolean_literal : FALSE
                           | TRUE"""
        p[0] = ("BooleanConstant", p[1])

    def p_character_literal(self, p):
        """character_literal : CCONST """
        p[0] = ("CharacterConstant", p[1])

    def p_empty_literal(self, p):
        """empty_literal : NULL"""
        p[0] = ("EmptyConstant", p[1])

    def p_character_string_literal_char(self, p):
        """character_string_literal : SCONST"""
        p[0] = ("StringConstant", p[1])

    # Array

    def p_value_array_element(self, p):
        """value_array_element : array_primitive_value LBRACK expression_list RBRACK"""
        p[0] = ("ValueArrayElement", p[1], p[3])

    def p_value_array_slice(self, p):
        """value_array_slice : array_primitive_value LBRACK lower_bound COLON upper_bound RBRACK"""
        p[0] = ("ValueArraySlice", p[1], (p[3], p[5]))

    def p_array_primitive_value(self, p):
        """array_primitive_value : primitive_value"""
        p[0] = p[1]

    # Expression

    def p_parenthesized_expression(self, p):
        """parenthesized_expression : LPAREN expression RPAREN"""
        p[0] = ("ParenthesizedExpression", p[2])

    def p_expression_list(self, p):
        """expression_list : expression_list COMMA expression
                           | expression"""
        if len(p) == 2:
            p[0] = ((p[1]),)
        else:
            p[0] = p[1] + (p[3],)

    def p_expression(self, p):
        """expression : operand0
                      | conditional_expression"""
        p[0] = ("Expression", p[1])

    def p_conditional_expression(self, p):
        """conditional_expression : IF boolean_expression then_expression else_expression FI"""
        p[0] = ("ConditionalExpression", p[2], p[3], p[4])

    def p_conditional_expression_elsif(self, p):
        """conditional_expression : IF boolean_expression then_expression elsif_expression else_expression FI"""
        p[0] = ("ConditionalExpression", p[2], p[3], p[4], p[5])

    def p_integer_expression(self, p):
        """integer_expression : expression"""
        p[0] = ('IntegerExpression', p[1])

    def p_boolean_expression(self, p):
        """boolean_expression : expression"""
        p[0] = ('BooleanExpression', p[1])

    def p_then_expression(self, p):
        """then_expression :     THEN expression"""
        p[0] = ("then_expression", p[2])

    def p_else_expression(self, p):
        """else_expression :     ELSE expression"""
        p[0] = ("ElseExpression", p[2])

    def p_elsif_expression_elsif(self, p):
        """elsif_expression :    elsif_expression ELSIF boolean_expression then_expression"""
        p[0] = ("ElsifExpression", p[1], p[3], p[4])

    def p_elsif_expression(self, p):
        """elsif_expression :    ELSIF boolean_expression then_expression"""
        p[0] = ("ElsifExpression", p[2], p[3])

    def p_operand0(self, p):
        """operand0 : operand1"""
        p[0] = p[1]

    def p_operand0_op1(self, p):
        """operand0 : operand0 operator1 operand1"""
        p[0] = (p[1], p[2], p[3])

    def p_operator1(self, p):
        """operator1 : relational_operator
                     | membership_operator"""
        p[0] = p[1]

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

    def p_operand1(self, p):
        """operand1 : operand2"""
        p[0] = p[1]

    def p_operand1_op2(self, p):
        """operand1 : operand1 operator2 operand2"""
        p[0] = (p[1], p[2], p[3])

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

    def p_operand2(self, p):
        """operand2 : operand3"""
        p[0] = p[1]

    def p_operand2_op3(self, p):
        """operand2 : operand2 arithmetic_multiplicative_operator operand3"""
        p[0] = (p[1], p[2], p[3])

    def p_arithmetic_multiplicative_operator(self, p):
        """arithmetic_multiplicative_operator : TIMES
                                              | DIVIDE
                                              | PERC"""
        p[0] = p[1]

    def p_operand3_uminus(self, p):
        """operand3 : MINUS operand4 %prec UMINUS"""
        p[0] = (p[1], p[2])

    def p_operand3_monadic(self, p):
        """operand3 : NOT operand4"""
        p[0] = (p[1], p[2])

    def p_operand3(self, p):
        """operand3 : operand4"""
                    # "| integer_literal"""
        p[0] = p[1]

    def p_operand4(self, p):
        """operand4 : location
                    | referenced_location
                    | primitive_value"""
        p[0] = p[1]

    def p_referenced_location(self, p):
        """referenced_location : ARROW location"""
        p[0] = p[2]

    # Action Statement ---------------------------------------------------

    def p_action_statement_list(self, p):
        """action_statement_list : action_statement_list action_statement
                                 | action_statement"""
        if len(p) == 2:
            p[0] = (p[1],)
        else:
            p[0] = p[1] + (p[2],)

    def p_label_id(self, p):
        """label_id : identifier"""
        p[0] = ('Label', p[1])

    def p_action(self, p):
        """action : bracketed_action
                  | assignment_action
                  | call_action
                  | exit_action
                  | return_action
                  | result_action"""
        p[0] = ("Action", p[1])

    def p_bracketed_action(self, p):
        """bracketed_action : if_action
                             | do_action"""
        p[0] = ("BracketedAction", p[1])

    def p_assignment_action(self, p):
        """assignment_action : location assigning_operator expression"""
        # names[p[1]]=p[3]
        p[0] = ("Assignment", p[1], p[2], p[3])

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
        p[0] = ("IfAction", p[2], p[3], p[4])

    def p_if_action(self, p):
        """if_action : IF boolean_expression then_clause FI"""
        p[0] = ("IfAction", p[2], p[3])

    def p_then_clause(self, p):
        """then_clause : THEN action_statement_list"""
        p[0] = ("ThenClause", p[2])

    def p_then_clause_empty(self, p):
        """then_clause : THEN empty"""
        p[0] = ("ThenClause",)

    def p_else_clause(self, p):
        """else_clause : ELSE action_statement_list"""
        p[0] = ('ElseClause', p[2])

    def p_else_clause_empty(self, p):
        """else_clause : ELSE empty"""
        p[0] = ('ElseClause',)

    def p_else_clause_if_else(self, p):
        """else_clause : ELSIF boolean_expression then_clause else_clause"""
        p[0] = ("ElseClause", p[2], p[3], p[4])

    def p_else_clause_if(self, p):
        """else_clause : ELSIF boolean_expression then_clause"""
        p[0] = ("ElseClause", p[2], p[3])

    def p_do_action_control_action(self, p):
        """do_action :           DO control_part SEMICOL action_statement_list OD"""
        p[0] = ("DoAction", p[2], p[4])

    def p_do_action_control(self, p):
        """do_action :           DO control_part SEMICOL OD"""
        p[0] = ("DoAction", p[2])

    def p_do_action(self, p):
        """do_action :           DO action_statement_list OD"""
        p[0] = ("DoAction", p[2])

    def p_do_action_zero(self, p):
        """do_action :           DO OD"""
        p[0] = ("DoAction", None)

    def p_control_part_forwhile(self, p):
        """control_part :        for_control while_control"""
        p[0] = ("DoControl", p[1], p[2])

    def p_control_part(self, p):
        """control_part :        while_control
                    |           for_control"""
        p[0] = ("DoControl", p[1])

    def p_for_control(self, p):
        """for_control :         FOR iteration"""
        p[0] = ("For", p[2])

    def p_iteration(self, p):
        """iteration :          range_enumeration
                    |          step_enumeration"""
        p[0] = p[1]

    def p_step_enumeration_stepvalue_down(self, p):
        """step_enumeration :    loop_counter ASSIGN start_value step_value DOWN end_value"""
        p[0] = ("StepIteration", p[1], p[3], p[4], p[6])

    def p_step_enumeration_stepvalue(self, p):
        """step_enumeration :    loop_counter ASSIGN start_value step_value end_value"""
        p[0] = ("StepIteration", p[1], p[3], p[4], p[5])

    def p_step_enumeration_down(self, p):
        """step_enumeration :    loop_counter ASSIGN start_value DOWN end_value"""
        p[0] = ("StepIteration", p[1], p[3], ("StepValue", None), p[5])

    def p_step_enumeration(self, p):
        """step_enumeration :    loop_counter ASSIGN start_value end_value"""
        p[0] = ("StepIteration", p[1], p[3], ("StepValue", None), p[4])

    def p_loop_counter(self, p):
        """loop_counter :        identifier"""
        p[0] = p[1]

    def p_start_value(self, p):
        """start_value :         discrete_expression"""
        p[0] = p[1]

    def p_step_value(self, p):
        """step_value :          BY integer_expression"""
        p[0] = ("StepValue", p[2])

    def p_end_value(self, p):
        """end_value :           TO discrete_expression"""
        p[0] = p[2]

    def p_discrete_expression(self, p):
        """discrete_expression :     expression"""
        p[0] = p[1]

    def p_range_enumeration_down(self, p):
        """range_enumeration :       loop_counter DOWN IN discrete_mode"""
        p[0] = ("RangeEnumeration", p[1], p[4])

    def p_range_enumeration(self, p):
        """range_enumeration :       loop_counter IN discrete_mode"""
        p[0] = ("RangeEnumeration", p[1], p[3])

    def p_while_control(self, p):
        """while_control :       WHILE boolean_expression"""
        p[0] = ("While", p[2])

    # Actions ------------------------------------------------------------

    def p_call_action(self, p):
        """call_action : procedure_call
                       | builtin_call"""
        p[0] = p[1]

    def p_procedure_call_parameter(self, p):
        """procedure_call : procedure_name LPAREN parameter_list RPAREN"""
        p[0] = ("ProcCall", p[1], p[3])

    def p_procedure_call(self, p):
        """procedure_call : procedure_name LPAREN RPAREN"""
        p[0] = ("ProcCall", p[1], None)

    def p_parameter_list(self, p):
        """parameter_list : parameter_list COMMA parameter
                          | parameter"""
        if len(p) == 2:
            p[0] = (p[1],)
        else:
            p[0] = p[1] + (p[3],)

    def p_parameter(self, p):
        """parameter : expression"""
        p[0] = ("Parameter", p[1])

    def p_procedure_name(self, p):
        """procedure_name : identifier"""
        p[0] = p[1]

    def p_exit_action(self, p):
        """exit_action : EXIT label_id"""
        p[0] = ("Exit", p[2])

    def p_return_action_result(self, p):
        """return_action : RETURN result"""
        p[0] = ("Return", p[2])

    def p_return_action(self, p):
        """return_action : RETURN"""
        p[0] = ("Return", None)

    def p_result_action(self, p):
        """result_action : RESULT result"""
        p[0] = p[2]

    def p_result(self, p):
        """result : expression"""
        p[0] = p[1]

    def p_builtin_call_parameter(self, p):
        """builtin_call : builtin_name LPAREN parameter_list RPAREN"""
        p[0] = ("BuiltinCall", p[1], p[3])

    def p_builtin_call(self, p):
        """builtin_call : builtin_name LPAREN RPAREN"""
        p[0] = ("BuiltinCall", p[1])

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
        p[0] = ('ProcedureDefinition', p[3], p[5], p[7])

    def p_procedure_definition_pr(self, p):
        """procedure_definition : PROC LPAREN formal_parameter_list RPAREN result_spec SEMICOL END"""
        p[0] = ('ProcedureDefinition', p[3], p[5])

    def p_procedure_definition_ps(self, p):
        """procedure_definition : PROC LPAREN formal_parameter_list RPAREN SEMICOL statement_list END"""
        p[0] = ('ProcedureDefinition', p[3], p[6])

    def p_procedure_definition_rs(self, p):
        """procedure_definition : PROC LPAREN RPAREN result_spec SEMICOL statement_list END"""
        p[0] = ('ProcedureDefinition', p[4], p[6])

    def p_procedure_definition_p(self, p):
        """procedure_definition : PROC LPAREN formal_parameter_list RPAREN SEMICOL END"""
        p[0] = ('ProcedureDefinition', p[3])

    def p_procedure_definition_r(self, p):
        """procedure_definition : PROC LPAREN RPAREN result_spec SEMICOL END"""
        p[0] = ('ProcedureDefinition', p[4])

    def p_procedure_definition_s(self, p):
        """procedure_definition : PROC LPAREN RPAREN SEMICOL statement_list END"""
        p[0] = ('ProcedureDefinition', p[5])

    def p_procedure_definition(self, p):
        """procedure_definition : PROC LPAREN RPAREN SEMICOL END"""
        p[0] = ('ProcedureDefinition',)

    def p_formal_parameter_list(self, p):
        """formal_parameter_list : formal_parameter_list COMMA formal_parameter
                                 | formal_parameter"""
        if len(p) == 2:
            p[0] = ((p[1]),)
        else:
            p[0] = p[1] + (p[3],)

    def p_formal_parameter(self, p):
        """formal_parameter : identifier_list parameter_spec"""
        p[0] = ('FormalParameter', p[1],  p[2])

    def p_parameter_spec(self, p):
        """parameter_spec : mode parameter_attribute
                          | mode"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1], p[2])

    def p_parameter_attribute(self, p):
        """parameter_attribute : LOC"""
        p[0] = ('ParameterAttribute', p[1])

    def p_result_spec_attr(self, p):
        """result_spec : RETURNS LPAREN mode result_attribute RPAREN"""
        p[0] = ('Returns', p[3] + p[4])

    def p_result_spec(self, p):
        """result_spec : RETURNS LPAREN mode RPAREN"""
        p[0] = ('Returns', p[3])

    def p_result_attribute(self, p):
        """result_attribute : LOC"""
        p[0] = ("ResultAttribute", p[1])

    # Empty

    def p_empty(self, p):
        """empty :"""
        pass

    # Error

    def p_error(self, p):
        try:
            print("Syntax error at '%s'" % p.value)
            print("Line: %d" % p.lineno)
        except:
            print("Syntax error")

# ------------------------------------------------------------

if __name__ == "__main__":
    import pprint

    lya_examples = ["example1.lya",
                    "example2.lya",
                    "example3.lya",
                    "example4.lya",
                    "factorial.lya",
                    "fibonacci.lya",
                    "gcd.lya",
                    "palindrome.lya",
                    "bubble_sort.lya",
                    "armstrong_number.lya",
                    "gen_primes.lya",
                    "int_stack.lya"
                    ]

    lyaparser = LyaParser()

    lya_source_dcl = """
    dcl dcl1 int;
    dcl dcl2, dcl3, dcl4, dcl5 char;
    dcl dcl6, dcl7 int, dcl8 bool;
    dcl dcl9 int = 5;
    dcl dcl10, dcl11 int = 6;
    dcl dcl12 int, dcl13, dcl14 int = 10;
    dcl dcl15 int (2:5);
    dcl dcl16 char (0:10);
    dcl dcl17 bool(10:11);
    dcl dcl18 dcl17 (1:2);
    dcl dcl19 int (0:1) (1:2);
    """

    lya_source_syn = """
    syn syn1 = 1;
    syn syn2, syn3, syn4 = 3;
    syn syn5 int = 2;
    syn syn6, syn7 int = 3;
    syn syn8 = 10, syn9 = 12;
    syn syn10, syn11 int = 13, syn12 = 20;"""

    lya_source_type = """
    type type1 = int;
    type type2 = char;
    type type3 = bool;
    type type4 = type3;
    type type7, type8 = int;
    type type9, type10, type11 = char;
    type type12 = bool, type13 = type9;
    type type14 = int, type15, type16 = char, type17, type18, type19 = char;
    type type20 = ref int;
    type type21 = ref ref type20;
    type type22 = chars[20];
    type type23 = array [int] char;
    type type24 = array[1:2] bool;
    """

    lya_source_composite_mode = """
    dcl cms1 chars [10];
    dcl cma1 array [int] bool;
    dcl cma2 array [bool, int] char;
    """

    lya_source_procedure1 = """
    power: proc (n int, r int) returns (int);
        dcl c int;
        type t = bool;
    end;
    """

    lya_source_procedure2 = """
    power: proc (n int, r int) returns (int);
    end;
    """

    lya_source_procedure3 = """
    power: proc (n int, r int);
        dcl c int;
        type t = bool;
    end;
    """

    lya_source_procedure4 = """
    power: proc () returns (int);
        dcl c int;
        type t = bool;
    end;
    """

    lya_source_procedure5 = """
    power: proc (n int, r int);
    end;
    """

    lya_source_procedure6 = """
    power: proc () returns (int);
    end;
    """

    lya_source_procedure7 = """
    power: proc ();
        dcl c int;
    end;
    """

    lya_source_procedure8 = """
    power: proc ();
    end;
    """

    lya_source_procedure9 = """
    power: proc (n int loc, r, z int) returns (int loc);
        dcl c, d int = 1;
        type t = bool;
    end;
    """

    lya_source_if1 = """
    label: if 1+2 then
        exit label1;
    else
        exit label2;
    fi;
    """

    lya_source_if2 = """
    if 1+2 then
        exit label1;
        exit label2;
    fi;
    """

    lya_source_if3 = """
    if 1+2 then
    else
        exit label2;
        exit label3;
    fi;
    """

    lya_source_if4 = """
    if 1+2 then
    else
    fi;
    """

    lya_source_if5 = """
    if 1+2 then
        exit label1;
    elsif 1+2 then
        exit label2;
        exit label22;
    else
        exit lable3;
    fi;
    """

    lya_source_if6 = """
    if 1+2 then
        exit label1;
    elsif 1+2 then
        exit label2;
        exit label22;
    fi;
    """

    lya_source_if7 = """
    if 1+2 then
        if 1+3 then
            exit label1;
        fi;
    elsif 1+2 then
        exit label2;
        if 2+5 then
        else
            exit label22;
        fi;
    else
        if 2+5 then
            exit a1;
        elsif 1+2 then
            exit label22;
        fi;
    fi;
    """

    lya_source_action1 = """
    label1: ac1 = 10 + 10;
    ac2 += 2;
    ac3 -= 10;
    ac4 *= 55;
    ac5 /= 1;
    ac5 %= 20;
    ac6 &= 2;
    """

    lya_source_expression = """dcl var1 int=3+5-7*7/9%3;
                        dcl var2 int = 2 in 3;
                        dcl var3 bool = 5 && 3 || 1 == 2 & 2;
                        dcl var4 bool = if 2 then 3 else 5 fi;
                        dcl var2 int = var1 + 3;"""

    lya_source_action2 = """
    exit label1;
    result 1 + 2;
    return;
    return 2 + 1;
    """

    lya_source_call1 = """
    function();
    function(1);
    function(1, 2);
    function(1+2, 2);
    function(1,2,3/2);
    """

    lya_source_call2 = """
    num(1);
    pred();
    succ(1,2);
    upper(1/2);
    lower(2/3);
    length();
    read(100);
    print(var2+2);
    """


    lya_source_do = """dcl var int = 3;
                    do od;
                    do var = 2; od;
                    do while 1; od;
                    do while 3; var = 32; od;
                    do for counter in mode_name; od;
                    do for counter in mode_name; var3 = 12; od;
                    do for counter down in mode_name; od;
                    do for counter in mode_name while 3; var = 32; od;
                    do for counter = 3 to 8; od;
                    do for counter = 3 down to 8; od;
                    do for counter = 3 by 5 to 8; od;
                    do for counter = 3 by 5 down to 8; od;
                    """

    file_name = lya_examples[9]
    file_path = "./lyaexamples/test.lya"# + file_name
    file = open(file_path)
    lya_source = file.read()

    # source = lya_source
    source = "dcl var int = 3;"
    # TODO: Test Location
    # TODO: Test Primitive

    # lya_source = """dcl var1 int=3+5-7*7/9%3; dcl var2 int = 2 in 3;"""  # ;\ndcl var2, varx char;\ndcl var3, var4 int = 10;"""#\ndcl var5 = 10;"""# + 5 * (10 - 20);"""

    # print(source)

#     lyaparser.lex.test("""if n == sum then
#   print(n, " is an Armstrong number.\n");
# else
#   print(n, " is not an Armstrong number.\n");
# fi;""")

    ast = lyaparser.parse(source)
    # pprint.pprint(AST, indent=2)
    print(ast)
