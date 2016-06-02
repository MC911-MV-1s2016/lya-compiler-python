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


__all__ = [
    'LTF',
    'LyaTypeFactory',
    'LyaType',
    'IntType',
    'BoolType',
    'CharType',
    'StringType',
    'ArrayType',
    'VoidType',
    'RefType'
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

    @property
    def name(self) -> str:
        return self._name

    @property
    def memory_size(self) -> int:
        return None


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

    def memory_size(self):
        return 1


class LyaVoidType(LyaBaseType):
    """Class that represents a void type in lya.
    """

    _name = "void"

    _instance = None

    def memory_size(self):
        return 0


class LyaIntType(LyaBaseType):
    """Class that represents an integer type in lya.
    """

    _name = "int"
    _unary_ops = {'+', '-'}
    _binary_ops = {'+', '-', '*', '/', '%'}
    _rel_ops = {'==', '!=', '>', '>=', '<', '<='}
    _unary_opcodes = {}
    _binary_opcodes = {}
    _rel_opcodes = {}

    _instance = None


class LyaBoolType(LyaBaseType):
    """Class that represents a boolean type in lya.
    """

    _name = "bool"
    _unary_ops = {'!'}
    _binary_ops = {}
    _rel_ops = {'==', '!='}
    _unary_opcodes = {}
    _binary_opcodes = {}
    _rel_opcodes = {}

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

    _name = "ref",
    _unary_ops = {"->"}
    _binary_ops = {}
    _rel_ops = {"==", "!="}
    _unary_opcodes = {"->": "ldr"}
    _binary_opcodes = {},
    _rel_opcodes = {"==": "equ", "!=": "neq"}

    def __init__(self, referenced_type: LyaType):
        super().__init__()
        # TODO: Bloquear referenced_types não permitidos (como outro Ref)
        self.referenced_type = referenced_type

    # TODO: Can assign <- other

    def name(self):
        return "{0} {1}".format(self._name, self.referenced_type.name)

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
        self.length = index_range[0] - index_range[1] + 1
        self._memory_size = self.length * self.referenced_type.memory_size

    def memory_size(self):
        return self._memory_size


class LyaStringType(LyaArrayType):
    """Lya Type that represents a string.
    """

    _name = "chars"
    _unary_ops = {}
    _binary_ops = {'+'}
    _rel_ops = {'==', '!='}
    _unary_opcodes = {}
    _binary_opcodes = {}
    _rel_opcodes = {}

    def __init__(self, length):
        super().__init__(LyaCharType.get_instance())
        self.length = length

    def memory_size(self):
        return self.length * self.referenced_type.memory_size


class LyaTypeFactory(object):
    """Lya Types Factory.
    """

    @staticmethod
    def void_type():
        return LyaVoidType.get_instance()

    @staticmethod
    def int_type():
        return LyaIntType.get_instance()

    @staticmethod
    def bool_type():
        return LyaBoolType.get_instance()

    @staticmethod
    def char_type():
        return LyaCharType.get_instance()

    @staticmethod
    def ref_type(referenced_type: LyaType):
        return LyaRefType(referenced_type)

    @staticmethod
    def array_type(referenced_type: LyaType, index_ranges):
        return LyaArrayType(referenced_type, index_ranges)

    @staticmethod
    def string_type(length):
        return LyaStringType(length)

LTF = LyaTypeFactory
