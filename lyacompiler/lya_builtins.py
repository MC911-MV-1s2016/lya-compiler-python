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

    Attributes:
        name -- The LyaType name.
        unary_ops -- The group of
        binary_ops -- The group of supported binary operation symbols.
        rel_ops --
        unary_opcodes --
        binary_opcodes --
        rel_opcodes --
    """

    def __init__(self, name, unary_ops, binary_ops,
                 rel_ops, unary_opcodes, binary_opcodes, rel_opcodes):
        self.name = name
        self.unary_ops = unary_ops
        self.binary_ops = binary_ops
        self.rel_ops = rel_ops
        self.unary_opcodes = unary_opcodes
        self.binary_opcodes = binary_opcodes
        self.rel_opcodes = rel_opcodes
        self.memory_size = 1

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, LyaType.__class__):
            return False
        return self.name == other.name

    def __ne__(self, other):
        return not (self == other)


class LyaCompositeType(LyaType):
    def __init__(self, name, unary_ops, binary_ops,
                 rel_ops, unary_opcodes, binary_opcodes, rel_opcodes):
        super().__init__(name, unary_ops, binary_ops,
                         rel_ops, unary_opcodes, binary_opcodes, rel_opcodes)
        self.name = name
        self.unary_ops = unary_ops
        self.binary_ops = binary_ops
        self.rel_ops = rel_ops
        self.unary_opcodes = unary_opcodes
        self.binary_opcodes = binary_opcodes
        self.rel_opcodes = rel_opcodes
        self.memory_size = 1

IntType = LyaType("int",
                  unary_ops={'+', '-'},
                  binary_ops={'+', '-', '*', '/', '%'},
                  rel_ops={'==', '!=', '>', '>=', '<', '<='},
                  unary_opcodes={},
                  binary_opcodes={},
                  rel_opcodes={}
                  )

BoolType = LyaType("bool",
                   unary_ops={'!'},
                   binary_ops={},
                   rel_ops={'==', '!='},
                   unary_opcodes={},
                   binary_opcodes={},
                   rel_opcodes={}
                   )

CharType = LyaType("char",
                   unary_ops={},
                   binary_ops={},
                   rel_ops={'==', '!=', '>', '>=', '<', '<='},
                   unary_opcodes={},
                   binary_opcodes={},
                   rel_opcodes={}
                   )

StringType = LyaType("chars",
                     unary_ops={},
                     binary_ops={'+'},
                     rel_ops={'==', '!='},
                     unary_opcodes={},
                     binary_opcodes={},
                     rel_opcodes={}
                     )

VoidType = LyaType("void",
                   unary_ops={},
                   binary_ops={},
                   rel_ops={},
                   unary_opcodes={},
                   binary_opcodes={},
                   rel_opcodes={}
                   )

ArrayType = LyaType("array",
                    unary_ops={},
                    binary_ops={},
                    rel_ops={},
                    unary_opcodes={},
                    binary_opcodes={},
                    rel_opcodes={}
                    )


RefType = LyaType("ref",
                  unary_ops={"->"},
                  binary_ops={},
                  rel_ops={"==", "!="},
                  unary_opcodes={"->": "ldr"},
                  binary_opcodes={},
                  rel_opcodes={"==": "equ", "!=": "neq"}
                  )
