# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lya_builtins.py
# Lya builtins.
#
# ------------------------------------------------------------

from .lya_errors import *
from .lya_lvminstruction import *

__all__ = [
    'LTF',
    'LyaTypeFactory',
    'LyaType',
    'LyaIntType',
    'LyaBoolType',
    'LyaCharType',
    'LyaStringType',
    'LyaArrayType',
    'LyaVoidType',
    'LyaRefType'
]


# Types
class LyaType(object):
    """Base class that represents a Lya builtin type.
    """

    _name = None
    _unary_ops = None
    _binary_ops = None
    _rel_ops = None
    _unary_opcodes = None
    _binary_opcodes = None
    _rel_opcodes = None

    def __init__(self):
        pass

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, LyaType):
            return False
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other

    def get_unary_instruction(self, op):
        instruction = self._unary_opcodes.get(op, None)

        if instruction is None:
            raise LyaGenericError(-1, None, "Unary operation error")

        return instruction()

    def get_binary_instruction(self, op):
        instruction = self._binary_opcodes.get(op, None)

        if instruction is None:
            raise LyaGenericError(-1, None, "Binary operation error")

        return instruction()

    def get_relational_instruction(self, op):
        instruction = self._rel_opcodes.get(op, None)

        if instruction is None:
            raise LyaGenericError(-1, None, "Relational operation error")

        return instruction()

    @property
    def name(self) -> str:
        return self._name

    @property
    def memory_size(self) -> int:
        return None

    @property
    def binary_ops(self):
        return self._binary_ops

    @property
    def relational_ops(self):
        return self._rel_ops

    @property
    def unary_ops(self):
        return self._unary_ops


class LyaBaseType(LyaType):
    """Class that represents a lya base type.

    Meant to be used as singleton via 'get_instance' method.
    """

    _instance = None

    @classmethod
    def get_instance(cls) -> 'LyaBaseType':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def memory_size(self):
        return 1


class LyaVoidType(LyaBaseType):
    """Class that represents a void type in lya.
    """

    _name = "void"

    _instance = None

    @property
    def memory_size(self):
        return 0


class LyaIntType(LyaBaseType):
    """Class that represents an integer type in lya.
    """

    _name = "int"
    _unary_ops = {'+', '-'}
    _binary_ops = {'+', '-', '*', '/', '%'}
    _rel_ops = {'==', '!=', '>', '>=', '<', '<='}
    _unary_opcodes = {
        '-': NEG,
        '+': NOP
    }
    _binary_opcodes = {
        '+': ADD,
        '-': SUB,
        '*': MUL,
        '/': DIV,
        '%': MOD
    }
    _rel_opcodes = {
        '==': EQU,
        '!=': NEQ,
        '<': LES,
        '<=': LEQ,
        '>': GRT,
        '>=': GRE
    }

    _instance = None


class LyaBoolType(LyaBaseType):
    """Class that represents a boolean type in lya.
    """

    _name = "bool"
    _unary_ops = {'!'}
    _binary_ops = {}
    _rel_ops = {'&&', '||', '==', '!=', '<', '<=', '>', '>='}
    _unary_opcodes = {
        '!': NOT
    }
    _binary_opcodes = {}
    _rel_opcodes = {
        '&&': AND,
        '||': LOR,
        '==': EQU,
        '!=': NEQ,
        '<': LES,
        '<=': LEQ,
        '>': GRT,
        '>=': GRE
    }

    _instance = None


class LyaCharType(LyaBaseType):
    """Class that represents a character type in lya.
    """

    _name = "char"
    _unary_ops = {}
    _binary_ops = {}
    _rel_ops = {'==', '!=', '>', '>=', '<', '<='}
    _unary_opcodes = {}
    _binary_opcodes = {}
    _rel_opcodes = {}

    _instance = None


class LyaRefType(LyaType):
    """Lya Type that references another LyaType.
    """

    _name = "ref"
    _unary_ops = {"->"}
    _binary_ops = {}
    _rel_ops = {"==", "!="}
    _unary_opcodes = {"->": "ldr"}
    _binary_opcodes = {}
    _rel_opcodes = {"==": "equ",
                    "!=": "neq"}

    def __init__(self, referenced_type: LyaType):
        super().__init__()
        # TODO: Bloquear referenced_types não permitidos (como outro Ref)
        self.referenced_type = referenced_type  # type : LyaType

    # TODO: Can assign <- other

    @property
    def name(self):
        return "{0} {1}".format(self._name, self.referenced_type.name)

    @property
    def memory_size(self):
        return self.referenced_type.memory_size


class LyaArrayType(LyaRefType):
    """Lya Type that represents an array.
    """

    _name = "array"
    _unary_ops = {}
    _binary_ops = {}
    _rel_ops = {}
    _unary_opcodes = {}
    _binary_opcodes = {}
    _rel_opcodes = {}

    # index_ranges = [(lower, upper)]
    def __init__(self, reference_type: LyaType, index_ranges: list):
        element_type = reference_type
        index_range = index_ranges[0]
        if len(index_ranges) > 1:
            element_type = LyaArrayType(reference_type, index_ranges[1:])
            index_range = index_ranges[0]
        super().__init__(element_type)
        self.index_range = index_range
        self.length = index_range[1] - index_range[0] + 1
        self._memory_size = self.length * self.referenced_type.memory_size
        pass

    @property
    def memory_size(self):
        return self._memory_size

    def get_referenced_type(self, depth) -> LyaType:
        if depth == 1:
            return self.referenced_type
        if not isinstance(self.referenced_type, LyaArrayType):
            return None
        else:
            return self.referenced_type.get_referenced_type(depth-1)

class LyaStringType(LyaType):
    """Lya Type that represents a string.
    """

    _name = "chars"
    _unary_ops = {}
    _binary_ops = {'+'}
    _rel_ops = {'==', '!='}
    _unary_opcodes = {}
    _binary_opcodes = {}
    _rel_opcodes = {}

    def __init__(self, length: int):
        super().__init__()
        self.length = length

    @property
    def memory_size(self):
        return self.length


class LyaTypeFactory(object):
    """Lya Types Factory.
    """

    @staticmethod
    def void_type() -> LyaVoidType:
        return LyaVoidType.get_instance()

    @staticmethod
    def int_type() -> LyaIntType:
        return LyaIntType.get_instance()

    @staticmethod
    def bool_type() -> LyaBoolType:
        return LyaBoolType.get_instance()

    @staticmethod
    def char_type() -> LyaCharType:
        return LyaCharType.get_instance()

    @staticmethod
    def ref_type(referenced_type: LyaType) -> LyaRefType:
        return LyaRefType(referenced_type)

    @staticmethod
    def array_type(referenced_type: LyaType, index_ranges) -> LyaArrayType:
        return LyaArrayType(referenced_type, index_ranges)

    @staticmethod
    def string_type(length) -> LyaStringType:
        return LyaStringType(length)

    @staticmethod
    def base_type_from_string(name: str) -> LyaBaseType:
        if name == LTF.int_type().name:
            return LTF.int_type()
        if name == LTF.bool_type().name:
            return LTF.bool_type()
        if name == LTF.char_type().name:
            return LTF.char_type()
        return None

LTF = LyaTypeFactory

# 6 - Visitar Exps
# 10 - Visitar Locs
# 11 - Visitar Assigns
# 12 - Visitar Slices