# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lya_environment.py
# Lya environment.
#
# ------------------------------------------------------------

from .symboltable import SymbolTable
from .lya_ast import Identifier, ProcedureStatement
from .lya_builtins import *
from .lya_errors import *


class Environment(object):
    """
    """
    def __init__(self):
        self.scope_stack = []
        self.procedure_stack = []
        self.typedef_stack = []
        builtin_types = SymbolTable()
        builtin_types.update({
            "int": IntType,
            "char": CharType,
            "string": StringType,
            "bool": BoolType,
            "array": ArrayType,
            "void": VoidType,
            "ref": RefType
        })
        self.typedef_stack.append(builtin_types)

    def start_new_level(self, enclosure):
        # Scope
        self.scope_stack.append(SymbolTable(enclosure))
        enclosure.environment = self
        enclosure.symbol_table = self.current_scope
        self.current_scope.locals_count = 0
        # Procedure
        self.procedure_stack.append(SymbolTable(enclosure))
        self.current_procedures.parameters_count = 0
        # Types
        self.typedef_stack.append(SymbolTable(enclosure))

    def end_current_level(self):
        self.scope_stack.pop()
        self.procedure_stack.pop()
        self.typedef_stack.pop()

    @property
    def current_types(self):
        return self.typedef_stack[-1]

    @property
    def current_procedures(self):
        return self.procedure_stack[-1]

    @property
    def current_scope(self):
        return self.scope_stack[-1]

    @property
    def current_scope_level(self):
        return len(self.scope_stack) - 1

    def declare_label(self, identifier: Identifier):
        self._add_identifier(identifier)

    def declare_formal_parameter(self, identifier: Identifier):
        self._add_identifier(identifier)
        identifier.displacement = self.current_scope.locals_count - 3
        self.current_procedures.parameters_count -= identifier.memory_size

    def declare_local(self, identifier: Identifier):
        self._add_identifier(identifier)
        identifier.displacement = self.current_scope.locals_count
        self.current_scope.locals_count += identifier.memory_size

    def _add_identifier(self, identifier: Identifier):
        prev_id = self.current_scope.lookup(identifier.name)
        if prev_id is not None:
            raise LyaNameError(identifier.lineno, identifier.name, prev_id.lineno)
        self.current_scope.add(identifier.name, identifier)
        identifier.scope = self.current_scope_level

    def declare_procedure(self, procedure: ProcedureStatement):
        self.declare_label(procedure.label)
        self.current_procedures.add(procedure.label.name, procedure)

    def define_type(self, name, identifier, raw_type):
        pass

    def raw_type(self, name):
        # TODO: Lookup on new types as well.
        t = self.root.get(name, None)
        return t

    def lookup_scope(self, name):
        return self._lookup()

    def lookup_type(self, name):
        pass

    def _lookup(self, stack, name):
        for table in reversed(stack):
            hit = table.lookup(name)
            if hit is not None:
                return hit
        return None

    def _defined_in_current_scope(self, name):
        if name in self.current_scope:
            return True
        else:
            return False
