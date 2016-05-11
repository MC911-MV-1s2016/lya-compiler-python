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

from lyacompiler.symboltable import SymbolTable
from lyacompiler.lyabuiltins import IntType, CharType, StringType, BoolType

# from symboltable import SymbolTable
# from lyabuiltins import IntType, CharType, StringType, BoolType


class Environment(object):
    def __init__(self):
        self.stack = []
        self.root = SymbolTable()
        self.stack.append(self.root)
        self.root.update({
            "int": IntType,
            "char": CharType,
            "string": StringType,
            "bool": BoolType
        })

    def push(self, enclosure):
        self.stack.append(SymbolTable(decl=enclosure))

    def pop(self):
        self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def scope_level(self):
        return len(self.stack)

    def add_local(self, name, value):
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
