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
from .lya_errors import *


class Environment(object):
    """
    :type current_scope: LyaScope
    """
    def __init__(self):
        self.current_scope = LyaScope()
        self.current_scope.level = -1
        self._define_builtins()
        self.string_constant_heap = list()
        self._labels_map = {}
        self._current_label = 0

    def _define_builtins(self):
        # self.current_scope.add_new_type(self._identifier_from_type(IntType), IntType)
        # self.current_scope.add_new_type(self._identifier_from_type(CharType), CharType)
        # self.current_scope.add_new_type(self._identifier_from_type(StringType), StringType)
        # self.current_scope.add_new_type(self._identifier_from_type(BoolType), BoolType)
        # self.current_scope.add_new_type(self._identifier_from_type(ArrayType), ArrayType)
        # self.current_scope.add_new_type(self._identifier_from_type(VoidType), VoidType)
        # self.current_scope.add_new_type(self._identifier_from_type(RefType), RefType)
        pass

    @staticmethod
    def _identifier_from_type(raw_type: LyaType):
        type_id = Identifier(raw_type.name)
        type_id.raw_type = raw_type
        return type_id

    @property
    def current_scope_level(self):
        return self.current_scope.level

    def start_new_scope(self, enclosure):
        self.current_scope = LyaScope(enclosure, self.current_scope)
        enclosure.environment = self
        enclosure.scope = self.current_scope

    def end_current_scope(self):
        if self.current_scope.ret is not None and self.current_scope.ret.raw_type != LTF.void_type():
            if self.current_scope.result is None:
                raise LyaGenericError(-1, self.current_scope.enclosure, "Exiting scope without return.")

        self.current_scope.enclosure.offset = self.current_scope.locals_displacement
        self.current_scope = self.current_scope.parent

    def store_string_constant(self, string_constant) -> int:
        prev_sconst_pos = len(self.string_constant_heap)
        try:
            prev_sconst_pos = self.string_constant_heap.index(string_constant)
        except ValueError as err:
            self.string_constant_heap.append(string_constant)
            prev_sconst_pos = self.string_constant_heap.index(string_constant)
        finally:
            return prev_sconst_pos

    def add_label(self, name):
        label = self.generate_label()
        self._labels_map[name] = label
        return label

    def lookup_label(self, name):
        return self._labels_map.get(name, None)

    def generate_label(self):
        self._current_label += 1
        return self._current_label
