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
    # precedence = (
    #     ('left', 'PLUS', 'MINUS'),
    #     ('left', 'TIMES', 'DIVIDE'),
    #     ('right', 'UMINUS'),
    # )

    # Grammar productions

    def p_program(self, p):
        """program : statement_list"""
        p[0] = ('program', p[1])

    #### Statement

    def p_statement_list(self, p):
        """statement_list : statement_list statement
                          | statement"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            # print(len(p[1][2]))
            # print(p[1][2])
            # p[0] = ('statement-list', () + p[1] + (p[2]))
            p[0] = p[1] + (p[2])

    def p_statement(self, p):
        """statement : declaration_statement"""
        # | synonym_statement
        # | newmode_statement
        # | procedure_statement
        # | action_statement"""
        p[0] = ('statement', p[1])

    def p_declaration_statement(self, p):
        """declaration_statement : DCL declaration_list SEMICOL"""
        p[0] = ('declaration-statement', () + ('declaration-list',) + (p[2],))

    #### Declaration

    def p_declaration_list(self, p):
        """declaration_list : declaration_list COMMA declaration
                            | declaration"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + (p[3])

    def p_declaration(self, p):
        """declaration : identifier_list mode"""
        p[0] = ('declaration', p[1], p[2])

    def p_declaration_initialization(self, p):
        """declaration : identifier_list mode initialization"""
        p[0] = ('declaration_initialization', (p[1], p[2], p[3]))

    def p_initialization(self, p):
        """initialization : ASSIGN expression"""
        p[0] = ('initialization', p[2])

    #### Identifier

    def p_identifier_list(self, p):
        """identifier_list : identifier
                           | identifier_list COMMA identifier"""
        if len(p) == 2:
            p[0] = ('identifier-list', ('identifier', p[1]))
        else:
            p[0] = p[1] + (('identifier', p[3]),)

    def p_identifier(self, p):
        """identifier : ID"""
        p[0] = ('identifier', p[1])

    ##### Mode

    def p_newmode_statement(self, p):
        """newmode_statement : TYPE newmode_list"""

    def p_newmode_list(self, p):
        """newmode_list : newmode_list COMMA mode_definition
                        | mode_definition"""

    def p_mode_definition(self, p):
        """mode_definition : identifier_list EQUALS mode"""

    def p_mode(self, p):
        """mode : mode_name
                | discrete_mode"""
        # | reference_mode
        # | composite_mode"""
        p[0] = ('mode', p[1])

    def p_discrete_mode(self, p):
        """discrete_mode : integer_mode
                         | boolean_mode
                         | character_mode"""
        # | discrete_range_mode"""
        p[0] = ('discrete-mode', p[1])

    def p_integer_mode(self, p):
        """integer_mode : INT"""
        p[0] = p[1]

    def p_boolean_mode(self, p):
        """boolean_mode : BOOL"""
        p[0] = p[1]

    def p_character_mode(self, p):
        """character_mode : CHAR"""
        p[0] = p[1]

    # def p_discrete_range_mode(self, p):
    #     """discrete_range_mode : discrete_mode_name  LPAREN literal_range RPAREN
    #                            | discrete_mode LPAREN literal_range RPAREN"""

    def p_mode_name(self, p):
        """mode_name : identifier"""
        p[0] = ('mode-name', p[1])

    def p_discrete_mode_name(self, p):
        """discrete_mode_name : identifier"""
        p[0] = ('discrete-mode-name', p[1])

    # def p_literal_range(self, p):
    #     """literal_range : lower_bound COLON upper_bound"""
    #
    # def p_lower_bound(self, p):
    #     """lower_bound : expression"""
    #
    # def p_upper_bound(self, p):
    #     """upper_bound : expression"""
    #
    # def p_reference_mode(self, p):
    #     """reference_mode : REF mode"""
    #
    # def p_composite_mode(self, p):
    #     """composite_mode : string_mode
    #                       | array_mode"""
    #
    # def p_string_mode(self, p):
    #     """string_mode : CHARS LBRACK string_length RBRACK"""
    #
    # def p_string_length(self, p):
    #     """string_length : integer_literal"""
    #
    # def p_array_mode(self, p):
    #     """array_mode : ARRAY LBRACK index_mode_list RBRACK"""
    #
    # def p_index_mode_list_rec(self, p):
    #     # the first line might need to be reversed depending on the parsing rules
    #     """index_mode_list : intex_mode_list COMMA index_mode"""
    #
    # def p_index_mode_list(self, p):
    #     """index_mode_list : index_mode"""
    #
    # def p_index_mode(self, p):
    #     """index_mode : discrete_mode
    #                  | literal_range"""
    #
    # def p_element_mode(self, p):
    #     """element_mode : mode"""


    def p_expression(self, p):
        """expression :          operand0"""  # | conditional_expression"""
        p[0] = ("expression", p[1])

    # def p_conditional_expression(self, p):
    #     """conditional_expression:  IF boolean_expression then_expression else_expression FI"""
    #     p[0] = ("conditional_expression", p[2], p[3], p[4])
    # 
    # def p_conditional_expression_elsif(self, p):
    #     """conditional_expression:  IF boolean_expression then_expression elsif_expression else_expression FI"""
    #     p[0] = ("conditional_expression", p[2], p[3], p[4], p[5])
    # 
    # def p_boolean_expression(self, p):
    #     """boolean_expression:  expression"""
    #     p[0] = ("boolean_expression", p[1])
    # 
    # def p_then_expression(self, p):
    #     """then_expression:     THEN expression"""
    #     p[0] = ("then_expression", p[2])
    # 
    # def p_else_expression(self, p):
    #     """else_expression:     ELSE expression"""
    #     p[0] = ("else_expression", p[2])
    #
    # def p_elsif_expression_elsif(self, p):
    #     """elsif_expression:    elsif_expression ELSIF boolean_expression then_expression"""
    #     p[0] = ("elsif_expression", p[1], p[3], p[4])
    #
    # def p_elsif_expression(self, p):
    #     """elsif_expression:    ELSIF boolean_expression then_expression"""
    #     p[0] = ("elsif_expression", p[2], p[3])

    def p_operand0(self, p):
        """operand0 :            operand1"""
        p[0] = ("operand0", p[1])

    def p_operand0_op1(self, p):
        """operand0 :            operand0 operator1 operand1"""
        p[0] = ("operand0", p[1], p[2], p[3])

    def p_operator1(self, p):
        """operator1 :           relational_operator
                    | membership_operator"""
        p[0] = ("operator1", p[1])

    def p_relational_operator(self, p):
        """relational_operator :     AND
                                | OR
                                | EQUALS
                                | DIF
                                | GTR
                                | GEQ
                                | LSS
                                | LEQ"""
        p[0] = ("relational_operator", p[1])

    def p_membership_operator(self, p):
        """membership_operator :     IN"""
        p[0] = ("membership_operator", p[1])

    def p_operand1(self, p):
        """operand1 :            operand2"""
        p[0] = ("operand1", p[1])

    def p_operand1_op2(self, p):
        """operand1 :            operand1 operator2 operand2"""
        p[0] = ("operand1", p[1], p[2], p[3])

    def p_operator2(self, p):
        """operator2 :           arithmetic_additive_operator"""
        #             |           string_concatenation_operator"""
        p[0] = ("operator2", p[1])

    def p_arithmetic_additive_operator(self, p):
        """arithmetic_additive_operator :        PLUS
                                        | MINUS"""
        p[0] = ("arithmetic_additive_operator", p[1])

    # def p_string_concatenation_operator(self, p):
    #     """string_concatenation_operator:       CONCAT"""
    #     p[0] = ("string_concatenation_operator", p[1])

    def p_operand2(self, p):
        """operand2 :            operand3"""
        p[0] = ("operand2", p[1])

    def p_operand2_op3(self, p):
        """operand2 :            operand2 arithmetic_multiplicative_operator operand3"""
        p[0] = ("operand2", p[1], p[2], p[3])

    def p_arithmetic_multiplicative_operator(self, p):
        """arithmetic_multiplicative_operator :      TIMES
                                                | DIVIDE
                                                | PERC"""
        p[0] = ("arithmetic_multiplicative_operator", p[1])

    def p_operand3_monadic(self, p):
        """operand3 :            monadic_operator operand4"""
        p[0] = ("operand3", p[1], p[2])

    def p_operand3(self, p):
        """operand3 :            operand4"""
                    # |           integer_literal"""
        p[0] = ("operand3", p[1])

    def p_monadic_operator(self, p):
        """monadic_operator :    MINUS
                            | NOT"""
        p[0] = ("monadic_operator", p[1])

    def p_operand4(self, p):
        """operand4 : ICONST"""
        # """operand4:            location | referenced_location | primitive_value"""
        p[0] = ("operand4", p[1])

    # def p_referenced_location(self, p):
    #     """referenced_location:         ARROW location"""
    #     p[0] = ("referenced_location", p[2])

    # ####### Expression (Fake)
    # def p_expression_plus(self, p):
    #     'expression : expression PLUS term'
    #     p[0] = ('plus-expression', p[1], p[3])
    #
    # def p_expression_minus(self, p):
    #     'expression : expression MINUS term'
    #     p[0] = ('minus-expression', p[1], p[3])
    #
    # def p_expression_term(self, p):
    #     'expression : term'
    #     p[0] = ('term-expression', p[1])
    #
    # def p_term_times(self, p):
    #     'term : term TIMES factor'
    #     p[0] = ('times-term', p[1], p[3])
    #
    # def p_term_div(self, p):
    #     'term : term DIVIDE factor'
    #     p[0] = ('divide-term', p[1], p[3])
    #
    # def p_term_factor(self, p):
    #     'term : factor'
    #     p[0] = ('factor-term', p[1])
    #
    # def p_factor_num(self, p):
    #     'factor : ICONST'
    #     p[0] = ('num-factor', p[1])
    #
    # def p_factor_expr(self, p):
    #     'factor : LPAREN expression RPAREN'
    #     p[0] = ('expr-factor', p[2])

    # def p_empty(self, p):
    #     'empty : '
    #     p[0] = None

    def p_error(self, p):
        try:
            print("Syntax error at '%s'" % p.value)
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
                    "gen_prime.lya",
                    "int_stack.lya"
                    ]

    lyaparser = LyaParser()

    file_name = lya_examples[1]
    file_path = "./lyaexamples/" + file_name
    # file = open(file_name)
    # lya_source = file.read()

    lya_source = """dcl var1 int=3+5-7*7/9%3; dcl var2 int = 2 in 3;"""  # ;\ndcl var2, varx char;\ndcl var3, var4 int = 10;"""#\ndcl var5 = 10;"""# + 5 * (10 - 20);"""

    print(lya_source)

    AST = lyaparser.parse(lya_source)
    pprint.pprint(AST, indent=4)
