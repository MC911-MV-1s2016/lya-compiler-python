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

from .lya_ast import Identifier
from .lya_scope import *
from .lya_builtins import *


class Environment(object):
    """
    :type current_scope: LyaScope
    """
    def __init__(self):
        self.current_scope = LyaScope()
        self.current_scope.level = -1
        self._define_builtins()

    def _define_builtins(self):
        self.current_scope.add_new_type(self._identifier_from_type(IntType), IntType)
        self.current_scope.add_new_type(self._identifier_from_type(CharType), CharType)
        self.current_scope.add_new_type(self._identifier_from_type(StringType), StringType)
        self.current_scope.add_new_type(self._identifier_from_type(BoolType), BoolType)
        self.current_scope.add_new_type(self._identifier_from_type(ArrayType), ArrayType)
        self.current_scope.add_new_type(self._identifier_from_type(VoidType), VoidType)
        self.current_scope.add_new_type(self._identifier_from_type(RefType), RefType)

    @staticmethod
    def _identifier_from_type(raw_type: LyaType):
        type_id = Identifier(raw_type.name)
        type_id.raw_type = raw_type
        return type_id

    def start_new_scope(self, enclosure):
        self.current_scope = LyaScope(enclosure, self.current_scope)
        enclosure.environment = self
        enclosure.scope = self.current_scope

    def end_current_scope(self):
        self.current_scope.enclosure.offset = self.current_scope.locals_displacement
        self.current_scope = self.current_scope.parent

    @property
    def current_scope_level(self):
        return self.current_scope.level