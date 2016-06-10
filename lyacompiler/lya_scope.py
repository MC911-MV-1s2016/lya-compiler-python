# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lya_scope.py
# Lya scope.
#
# ------------------------------------------------------------

from enum import Enum, unique

from .symboltable import SymbolTable
from .lya_ast import ASTNode, Identifier, ProcedureStatement, \
    Declaration, SynonymDefinition, FormalParameter
from .lya_builtins import *
from .lya_errors import *

__all__ = [
    'SymbolType',
    'SymbolEntry',
    'LyaScope'
]


@unique
class SymbolType(Enum):
    declaration = 0
    parameter = 1
    synonym = 2
    type_definition = 3
    procedure = 4
    ret = 5
    label = 6

    @classmethod
    def as_string(cls, t):
        if t == cls.declaration:
            return "declaration"
        if t == cls.parameter:
            return "parameter"
        if t == cls.synonym:
            return "synonym"
        if t == cls.type_definition:
            return "type definition"
        if t == cls.procedure:
            return "procedure"
        if t == cls.ret:
            return "_ret"
        if t == cls.label:
            return "label"


class SymbolEntry(object):
    """
    :type symbol_type: SymbolType
    :type identifier: Identifier
    :type scope: LyaScope
    """

    @classmethod
    def declaration(cls, identifier: Identifier, scope):
        return cls(SymbolType.declaration, identifier, scope)

    @classmethod
    def parameter(cls, identifier: Identifier, scope):
        return cls(SymbolType.parameter, identifier, scope)

    @classmethod
    def synonym(cls, identifier: Identifier, scope):
        return cls(SymbolType.synonym, identifier, scope)

    @classmethod
    def type_definition(cls, identifier: Identifier, scope):
        return cls(SymbolType.type_definition, identifier, scope)

    @classmethod
    def procedure(cls, identifier: Identifier, scope):
        return cls(SymbolType.procedure, identifier, scope)

    @classmethod
    def label(cls, identifier: Identifier, scope):
        return cls(SymbolType.label, identifier, scope)

    def __init__(self, symbol_type: SymbolType, identifier: Identifier, scope):
        self.symbol_type = symbol_type
        self.identifier = identifier
        self.scope = scope

    def __str__(self):
        return "{0} (at line:{1})".format()

    @property
    def raw_type(self):
        return self.identifier.raw_type

    @property
    def lineno(self):
        return self.identifier.lineno


class LyaScope(object):
    """
    :type enclosure: ASTNode
    :type parent: LyaScope
    :type level: int
    :type children: list[LyaScope]
    :type symbols: dict(str:SymbolEntry)
    :type declarations: dict(str:Declaration)
    :type synonyms: (str:SynonymDefinition)
    :type type_definitions: (str:LyaType)
    :type procedures: dict(str:ProcedureStatement)
    :type labels: dict(str:Identifier)
    :type locals_displacement: int
    :type parameters_displacement: int
    :type tables: dict(SymbolType:SymbolTable)
    :type ret: Identifier
    """
    def __init__(self, enclosure=None, parent=None):
        self.enclosure = enclosure
        self.parent = parent
        self.level = 0
        if parent is not None:
            self.level = parent.level + 1
        self.children = []
        self.symbols = SymbolTable(enclosure)
        self.declarations = SymbolTable(enclosure)
        self.parameters = SymbolTable(enclosure)
        self.synonyms = SymbolTable(enclosure)
        self.type_definitions = SymbolTable(enclosure)
        self.procedures = SymbolTable(enclosure)
        self.labels = SymbolTable(enclosure)
        self.locals_displacement = 0
        self.parameters_displacement = -3
        self.tables = {
            SymbolType.declaration: self.declarations,
            SymbolType.parameter: self.parameters,
            SymbolType.synonym: self.synonyms,
            SymbolType.type_definition: self.type_definitions,
            SymbolType.procedure: self.procedures,
            SymbolType.label: self.labels
        }
        self.ret = None
        self.result = None #holds a node of the return call

    def add_child(self, scope):
        scope.parent = self
        self.children.append(scope)

    def _add_symbol(self, name, entry: SymbolEntry):
        prev_entry = self.symbols.lookup(name)
        if prev_entry is not None:
            raise LyaNameError(entry.lineno, name, prev_entry)
        self.symbols.add(name, entry)
        entry.identifier.scope_level = self.level

    # Declarations

    def add_declaration(self, identifier: Identifier, declaration: Declaration):
        self._add_symbol(identifier.name, SymbolEntry.declaration(identifier, self))
        self.declarations.add(identifier.name, declaration)
        identifier.displacement = self.locals_displacement
        self.locals_displacement += identifier.memory_size

    # Parameter

    def add_parameter(self, identifier: Identifier, parameter: FormalParameter):
        self._add_symbol(identifier.name, SymbolEntry.parameter(identifier, self))
        self.parameters.add(identifier.name, parameter)
        identifier.displacement = self.parameters_displacement
        self.parameters_displacement -= identifier.memory_size

    # Synonyms
    # Evaluated constant (int, char, bool, chars) (Array?)
    def add_synonym(self, identifier: Identifier, synonym: SynonymDefinition):
        self._add_symbol(identifier.name, SymbolEntry.synonym(identifier, self))
        self.synonyms.add(identifier.name, synonym)

    # Types
    # TODO: Improve new types management.
    def add_new_type(self, identifier: Identifier, raw_type: LyaType):
        self._add_symbol(identifier.name, SymbolEntry.type_definition(identifier, self))
        self.type_definitions.add(identifier.name, raw_type)

    # Procedures

    def add_procedure(self, identifier: Identifier, procedure: ProcedureStatement):
        self._add_symbol(identifier.name, SymbolEntry.procedure(identifier, self))
        self.procedures.add(identifier.name, procedure)

    # Procedure return

    def add_return(self, identifier: Identifier):
        self._add_symbol(identifier.name, SymbolEntry(SymbolType.ret, identifier, self))
        self.ret = identifier

    def add_result(self, res: ASTNode):
        self.result = res

        if self.ret.raw_type != res.raw_type:
            raise LyaTypeError(res.lineno, res.result.raw_type, self.ret.raw_type)


    # Label

    def add_label(self, identifier: Identifier):
        self._add_symbol(identifier.name, SymbolEntry.procedure(identifier, self))
        self.labels.add(identifier.name, identifier)

    # Lookup

    def entry_lookup(self, name):
        entry = self.symbols.get(name)
        if entry is not None:
            return entry
        if self.parent is not None:
            return self.parent.entry_lookup(name)
        return None

    def identifier_lookup(self, name):
        entry = self.entry_lookup(name)
        if entry is not None:
            return entry.identifier
        return None

    def type_lookup(self, name):
        entry = self.entry_lookup(name)
        if entry is not None:
            return entry.raw_type
        return None

    def procedure_lookup(self, name, lineno: int):
        entry = self.entry_lookup(name)
        if entry is not None:
            if entry.symbol_type != SymbolType.procedure:
                raise LyaProcedureCallError(lineno, name, entry.symbol_type) #wrong type
            return entry.scope.procedures.lookup(name)
        return None

    # def _lookup(self, identifier: Identifier, entry: SymbolEntry):
    #     table = self.tables.get(entry.symbol_type)
    #     if table is None:
    #         raise LyaUnknownError(identifier.lineno, identifier)
    #
    #     for table in reversed(stack):
    #         hit = table.lookup(name)
    #         if hit is not None:
    #             return hit
    #     return None
