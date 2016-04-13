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

    def p_statement_list(self, p):
        """statement_list : statement_list statement
                          | statement"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            # print(len(p[1][2]))
            # print(p[1][2])
            #p[0] = ('statement-list', () + p[1] + (p[2]))
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

    def p_declaration_list(self, p):
        """declaration_list : declaration_list COMMA declaration
                            | declaration"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + (p[3])

    def p_declaration(self, p):
        """declaration : identifier_list"""
        p[0] = ('declaration', p[1])

    def p_declaration_initialization(self, p):
        """declaration : identifier_list initialization"""
        p[0] = ('declaration_initialization', (p[1], p[2]))

    def p_initialization(self, p):
        """initialization : ASSIGN expression"""
        p[0] = ('initialization', p[2])

    def p_identifier_list(self, p):
        """identifier_list : ID
                           | identifier_list COMMA ID"""
        if len(p) == 2:
            p[0] = ('identifier-list', ('identifier', p[1]))
        else:
            p[0] = p[1] + (('identifier', p[3]),)

    def p_expression_plus(self, p):
        'expression : expression PLUS term'
        p[0] = ('plus-expression', p[1], p[3])

    def p_expression_minus(self, p):
        'expression : expression MINUS term'
        p[0] = ('minus-expression', p[1], p[3])

    def p_expression_term(self, p):
        'expression : term'
        p[0] = ('term-expression', p[1])

    def p_term_times(self, p):
        'term : term TIMES factor'
        p[0] = ('times-term', p[1], p[3])

    def p_term_div(self, p):
        'term : term DIVIDE factor'
        p[0] = ('divide-term', p[1], p[3])

    def p_term_factor(self, p):
        'term : factor'
        p[0] = ('factor-term', p[1])

    def p_factor_num(self, p):
        'factor : ICONST'
        p[0] = ('num-factor', p[1])

    def p_factor_expr(self, p):
        'factor : LPAREN expression RPAREN'
        p[0] = ('expr-factor', p[2])

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

    lya_source = """dcl var1; dcl var2, varx;\ndcl var3, var4 = 3;\ndcl var5 = 10;"""# + 5 * (10 - 20);"""

    print(lya_source)

    AST = lyaparser.parse(lya_source)
    pprint.pprint(AST, indent=4)
