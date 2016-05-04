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
    """ A lexer for the Lya scripting language. After building it,
        set the input text with input(), and call token()
        to get new tokens.
    """
    def __init__(self):
        """ Create a new Lexer.
        """
        self.lexer = None
        # Keeps track of the last token returned from self.token()
        self.last_token = None

    def build(self, **kwargs):
        """ Builds the lexer from the specification. Must be
            called after the lexer object is created.
            This method exists separately, because the PLY
            manual warns against calling lex.lex inside
            __init__
        """
        self.lexer = lex.lex(object=self, **kwargs)

    def reset_lineno(self):
        """ Resets the internal line number counter of the lexer.
        """
        self.lexer.lineno = 1

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
        """ Runs the lexer on a Lya code test input data.
        :param data: The Lya code test input data.
        """
        self.input(data)
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
        'in': 'IN',
        'loc': 'LOC',
        'od': 'OD',
        'proc': 'PROC',
        'ref': 'REF',
        'result': 'RESULT',
        'returns': 'RETURNS',
        'return': 'RETURN',
        'syn': 'SYN',
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
        'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK', 'SEMICOL', 'ASSIGN',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'PERC', 'COMMA', 'COLON',
        'AND', 'OR', 'EQUALS', 'DIF',
        'GTR', 'GEQ', 'LSS', 'LEQ', 'CONCAT', 'NOT', 'ARROW',

        'ID', 'ICONST', 'CCONST', 'SCONST',

        'PLUSASSIGN', 'MINUSASSIGN', 'TIMESASSIGN', 'DIVIDEASSIGN', 'CONCATASSIGN', 'PERCASSIGN'

    ] + list(reserved.values())

    # 'RCURL', 'CIRCUMF', DBLQUO', 'DBLSLASH', 'SINGQUO', 'LCURL',

    # Token Regexes

    # Misc
    end_of_line = r'\n'
    reg_or = r'|'

    # Integer constant
    int_digits = r'\d+'
    iconst = int_digits

    # Character constants
    sing_quo = r"'"
    double_quo = r'"'

    ascii_character = r'[\x00-\x7F]'
    char_cconst = sing_quo + ascii_character + sing_quo
    int_cconst = r"'\^\(\d+\)'"
    cconst = char_cconst + reg_or + int_cconst

    # String literal
    character_string = ascii_character + r'*'
    # sconst = double_quo + character_string + r'[^"]' + double_quo
    sconst = r'"((?!\/)|[^"])*"'

    unterminated_string = double_quo + character_string #+ reg_or + character_string + double_quo

    # Identifier
    identifier = r'[a-zA-Z_][a-zA-Z_0-9]*'

    # Comment
    comt_start = r'/\*'
    comt_end = r'\*/'
    bracketed_comment = r'/\*(\*(?!\/)|[^*])*\*/'
    line_end_comment = r'//(.*?)' + end_of_line
    # bracketed_comment = comt_start + character_string + comt_end
    # line_end_comment = r'//' + character_string + end_of_line
    comment = bracketed_comment + reg_or + line_end_comment

    unterminated_comment = comt_start + character_string #+ reg_or + r'(?!\n)' + character_string + comt_end

    # Ignores
    t_ignore = ' \t'

    # Regular expression rules for simple tokens
    #t_DBLSLASH          = r'//'
    t_LPAREN            = r'\('
    t_RPAREN            = r'\)'
    # t_LCURL             = r'\{'
    # t_RCURL             = r'}'
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
    # t_SINGQUO           = r'\''
    # t_DBLQUO            = r'"'
    # t_CIRCUMF           = r'\^'
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
    t_PLUSASSIGN        = r'\+='
    t_MINUSASSIGN       = r'-='
    t_TIMESASSIGN       = r'\*='
    t_DIVIDEASSIGN      = r'/='
    t_CONCATASSIGN      = r'&='
    t_PERCASSIGN        = r'%='

    # Regular expression rule with some action code

    # Comments
    @TOKEN(comment)
    def t_COMMENT(self, t):
        newlines_count = t.value.count('\n')
        t.lexer.lineno += newlines_count
        pass

    # Newlines
    @TOKEN(end_of_line)
    def t_NEWLINE(self, t):
        t.lexer.lineno += len(t.value)
        pass

    @TOKEN(iconst)
    def t_ICONST(self, t):
        t.value = int(t.value)
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

    @TOKEN(unterminated_comment)
    def t_UNTERMINATED_COMMENT(self, t):
        msg = "%d: Unterminated comment" % t.lineno
        print(msg)
        pass

    @TOKEN(unterminated_string)
    def t_UNTERMINATED_STRING(self, t):
        msg = "%d: Unterminated string" % t.lineno
        print(msg)
        pass

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

    lyalexer.test("""dcl var1 int; dcl var2, varx char;\ndcl var3, var4 bool = true;""")#lya_source)

