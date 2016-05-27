# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lyaenvironment.py
# Lya environment.
#
# ------------------------------------------------------------

from .symboltable import SymbolTable
from .lyabuiltins import *


class Environment(object):
    def __init__(self):
        self.stack = []
        self.root = SymbolTable()
        self.stack.append(self.root)
        self.root.update({
            "int": IntType,
            "char": CharType,
            "string": StringType,
            "bool": BoolType,
            "array": ArrayType
        })

    # TODO: Allow new type declarations. Add to root or create new var

    def raw_type(self, name):
        # TODO: Lookup on new types as well.
        t = self.root.get(name, None)
        return t

    def push(self, enclosure):
        self.stack.append(SymbolTable(decl=enclosure))

    def pop(self):
        self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def scope_level(self):
        return len(self.stack) - 2

    def add_local(self, name, value):
        if self.peek().lookup(name) is not None:
            raise Exception
        self.peek().add(name, value)

    def add_root(self, name, value):
        self.root.add(name, value)

    def lookup(self, name):
        for scope in reversed(self.stack):
            hit = scope.lookup(name)
            if hit is not None:
                return hit
        return None

    def find(self, name):
        if name in self.stack[-1]:
            return True
        else:
            return False
