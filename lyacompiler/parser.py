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

    def p_error(self, p):
        print("Syntax error at '%s'" % p.value)

# ------------------------------------------------------------
if __name__ == "__main__":

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

    lya_source = "3 + 5 * (10 - 20)"

    print(lya_source)

    AST = lyaparser.parse(lya_source)
    print(AST)
