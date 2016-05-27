#!/usr/bin/env python3
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


from typing import Tuple

__all__ = [
    'LyaType',
    'IntType',
    'BoolType',
    'CharType',
    'StringType',
    'ArrayType',
    'VoidType'
]


# Types
class LyaType(object):
    """Base class that represents a Lya builtin type.

    Attributes:
        name -- The LyaType name.
        default -- The type default value.
        binops -- The group of supported binary operation symbols.
        unops -- The group of
    """
    def __init__(self, name: str, default, binops: Tuple[str, ...], unops: Tuple[str, ...]):
        self.name = name
        self.default = default
        self.binops = binops
        self.unops = unops

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name


int_binops = tuple(['+', '-', '*', '/', '%', '==', '!=', '>', '>=', '<', '<='])
int_unops = tuple(['+', '-'])
IntType = LyaType("int", 0, int_binops, int_unops)

bool_binops = tuple(['==', '!='])
bool_unops = tuple('!')
BoolType = LyaType("bool", False, bool_binops, bool_unops)

char_binops = tuple(['==', '!=', '>', '>=', '<', '<='])
char_unops = tuple()
CharType = LyaType("char", '', char_binops, char_unops)

string_binops = tuple(['+', '==', '!='])
string_unops = tuple()
StringType = LyaType("string", "", string_binops, string_unops)

array_binops = tuple()
array_unops = tuple()
ArrayType = LyaType("array", list(), array_binops, array_unops)

VoidType = LyaType("void", None, tuple(), tuple())

# Functions

# TODO: Builtin funcions
