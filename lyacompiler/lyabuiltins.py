# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lyabuiltins.py
# Lya builtins.
#
# ------------------------------------------------------------


# Types

class ExprType(object):
    def __init__(self, decl, default, binops, unops):
        self.decl = decl
        self.default = default
        self.binops = binops
        self.unops = unops

int_binops = ('+', '-', '*', '/', '%', '==', '!=', '>', '>=', '<', '<=')
int_unops = ('+', '-')
IntType = ExprType("int", 0, int_binops, int_unops)

bool_binops = ('==', '!=')
bool_unops = ('!')
BoolType = ExprType("bool", False, bool_binops, bool_unops)

char_binops = ('==', '!=', '>', '>=', '<', '<=')
char_unops = tuple()
CharType = ExprType("char", '', char_binops, char_unops)

string_binops = ('+', '==', '!=')
string_unops = tuple()
StringType = ExprType("string", "", string_binops, string_unops)

array_binops = ()
array_unops = ()
ArrayType = ExprType("array", list(), array_binops, array_unops)

# Functions

# TODO: Builtin funcions
