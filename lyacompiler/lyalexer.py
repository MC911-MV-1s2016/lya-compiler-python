# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lyalexer.py
# Tokenizer for the Lya scripting language.
#
# ------------------------------------------------------------
import ply.lex as lex
from ply.lex import TOKEN


class LyaLexer(object):

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # def reset_lineno(self):
    #     """ Resets the internal line number counter of the lexer.
    #     """
    #     self.lexer.lineno = 1

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token

    def find_tok_column(self, token):
        """ Find the column of the token in its line.
        """
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        return token.lexpos - last_cr

    # Test
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

    # PRIVATE

    reserved = {

        # RESERVED WORDS
        'array': 'ARRAY',
        'by': 'BY',
        'chars': 'CHARS',
        'dcl': 'DCL',
        'do': 'DO',
        'down': 'DOWN',
        'else': 'ELSE',
        'elsif': 'ELSIF',
        'end': 'END',
        'exit': 'EXIT',
        'fi': 'FI',
        'for': 'FOR',
        'if': 'IF',
        'in': 'IN', 'loc': 'LOC',
        'od': 'OD',
        'proc': 'PROC',
        'ref': 'REF',
        'result': 'RESULT',
        'returns': 'RETURNS',
        'return': 'RETURN',
        'sys': 'SYS',
        'then': 'THEN',
        'to': 'TO',
        'type': 'TYPE',
        'while': 'WHILE',

        # PREDEFINED WORDS
        'bool': 'BOOL',
        'char': 'CHAR',
        'false': 'FALSE',
        'int': 'INT',
        'length': 'LENGTH',
        'lower': 'LOWER',
        'null': 'NULL',
        'num': 'NUM',
        'pred': 'PRED',
        'print': 'PRINT',
        'read': 'READ',
        'succ': 'SUCC',
        'true': 'TRUE',
        'upper': 'UPPER',
    }

    # Tokens
    tokens = [

        # SYMBOLS
        'DBLSLASH', 'LPAREN', 'RPAREN', 'LCURL', 'RCURL', 'LBRACK', 'RBRACK', 'SEMICOL', 'ASSIGN',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'PERC', 'COMMA', 'COLON', 'SINGQUO',
        'DBLQUO', 'CIRCUMF', 'AND', 'OR', 'EQUALS', 'DIF',
        'GTR', 'GEQ', 'LSS', 'LEQ', 'CONCAT', 'NOT', 'ARROW',

        'ID', 'ICONST', 'CCONST', 'SCONST'

    ] + list(reserved.values())


    # Token Regexes

    end_of_line = r'\n'

    # Comment
    bracketed_comment = r'/\*(.|\n)*?\*/'
    line_end_comment = r'//(.*?)' + end_of_line
    comment = bracketed_comment + '|' + line_end_comment

    integer_digits = r'\d'
    ascii_character = r'[\x00-\x7F]'

    iconst = '\d+'
    cconst = "'" + ascii_character + "'"
    sconst = '"' + ascii_character + '+"'
    identifier = r'[a-zA-Z_][a-zA-Z_0-9]*'

    # Ignores
    t_ignore = " \t"

    # Newlines
    @TOKEN(end_of_line)
    def t_NEWLINE(self, t):
        t.lexer.lineno += len(t.value)
        pass

    # Comments
    @TOKEN(comment)
    def t_COMMENT(self, t):
        newlines_count = t.value.count('\n')
        t.lexer.lineno += newlines_count
        pass

    # Regular expression rules for simple tokens
    t_DBLSLASH          = r'//'
    t_LPAREN            = r'\('
    t_RPAREN            = r'\)'
    t_LCURL             = r'\{'
    t_RCURL             = r'}'
    t_LBRACK            = r'\['
    t_RBRACK            = r'\]'
    t_SEMICOL           = r';'
    t_PLUS              = r'\+'
    t_MINUS             = r'-'
    t_TIMES             = r'\*'
    t_DIVIDE            = r'/'
    t_PERC              = r'%'
    t_ASSIGN            = r'='
    t_COMMA             = r','
    t_COLON             = r':'
    t_SINGQUO           = r'\''
    t_DBLQUO            = r'"'
    t_CIRCUMF           = r'\^'
    t_AND               = r'&&'
    t_OR                = r'\|\|'
    t_EQUALS            = r'=='
    t_DIF               = r'!='
    t_GTR               = r'>'
    t_GEQ               = r'>='
    t_LSS               = r'<'
    t_LEQ               = r'<='
    t_CONCAT            = r'&'
    t_NOT               = r'!'
    t_ARROW             = r'->'

    # Regular expression rule with some action code

    @TOKEN(iconst)
    def t_ICONST(self, t):
        return t

    @TOKEN(cconst)
    def t_CCONST(self, t):
        return t

    @TOKEN(sconst)
    def t_SCONST(self, t):
        return t


    @TOKEN(identifier)
    def t_ID(self, t):
        t.type = self.reserved.get(t.value, 'ID')
        return t

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


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

if __name__ == '__main__':

    # Build the lexer
    lyalexer = LyaLexer()
    lyalexer.build()

    file_name = "./lyaexamples/" + lya_examples[1]
    file = open(file_name)
    lya_source = file.read()

    print(lya_source)

    lyalexer.test(lya_source)

