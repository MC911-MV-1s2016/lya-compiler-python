# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lya_errors.py
# Lya Errors
#
# ------------------------------------------------------------


from .lya_builtins import *
from .lya_ast import ASTNode

__all__ = [
    'LyaError',
    'LyaNameError',
    'LyaTypeError',
    'LyaOperationError',
    'LyaUnknownError'
]

# Index Out Of Range
# FuncCall (Wrong Params)
#

class LyaError(Exception):
    """Base class for exceptions in the Lya compiler."""
    pass


class LyaNameError(LyaError):
    """Exception raised for undefined names.

    Attributes:
        lineno -- The line number where the exception was raised.
        name -- The name that raised the exception.
        previous_def -- The line where name was previously defined.
            Defaults to None if name wasn't defined.
    """

    def __init__(self, lineno: int, name: str, previous_def: int = None):
        self.lineno = lineno
        self.name = name
        self.previous_def = previous_def

    def __str__(self):
        if self.previous_def is None:
            return "LyaNameError ({0}): name '{1}' not defined.".format(self.lineno, self.name)
        else:
            return "LyaNameError ({0}): name '{1}' redefinition. " \
                   "Previous definition at line {2}.".format(self.lineno, self.name, self.previous_def)


class LyaTypeError(LyaError):
    """Raised when an operation or function is applied to an object of inappropriate type.

    Attributes:
        lineno -- The line number where the exception was raised.
        current_type -- The actual LyaType that raised the error.
        expected_type -- The expected LyaType
    """

    def __init__(self, lineno: int, current_type: LyaType, expected_type: LyaType = None):
        self.lineno = lineno
        self.current_type = current_type
        self.expected_type = expected_type

    def __str__(self):
        if self.expected_type is None:
            return "LyaTypeError ({0}): Undefined type '{1}'.".format(self.lineno, self.current_type)
        else:
            return "LyaTypeError ({0}): '{1}' received. " \
                   "Expected '{2}'.".format(self.lineno, self.current_type, self.expected_type)


class LyaOperationError(LyaError):
    """Raised when an unsupported LyaType operation is performed.

    Attributes:
        lineno -- The line number where the exception was raised.
        left_type -- The type associated with the left operand.
        op -- The operation.
        right_type -- The operation associated with the right operand.

    Both left_type and right_type can be exclusively None (XOR).
    """

    def __init__(self, lineno: int, op, left_type=None, right_type=None):
        self.lineno = lineno
        self.left_type = left_type
        self.op = op
        self.right_type = right_type

    def __str__(self):
        if self.op is None:
            return "Malformed LyaOperationError: missing op."
        if self.left_type is not None and self.right_type is not None:
            return "LyaOperationError ({0}): Unsupported operation '{1}' between " \
                   "'{2}' and '{3}'.".format(self.lineno, self.op, self.left_type, self.right_type)
        if self.right_type is not None:
            return "LyaOperationError ({0}): Unsupported left operation '{1}' " \
                   "on '{2}'.".format(self.lineno, self.op, self.right_type)
        if self.left_type is not None:
            return "LyaOperationError ({0}): Unsupported right operation '{1}'" \
                   " on '{2}'.".format(self.lineno, self.op, self.left_type)
        return "Malformed LyaOperationError: missing left and right types."


class LyaUnknownError(LyaError):
    """Raised when an unknown exception was caught while visiting an ASTNode.

    Attributes:
        lineno -- The line number where the exception was raised.
        node - The ASTNode whose visitor raised an unhandled exception.
    """

    def __init__(self, lineno: int, node: ASTNode):
        self.lineno = lineno
        self.node = node

    def __str__(self):
        return "LyaUnknownError ({0}): Node {1}.".format(self.lineno, self.node.class_name)
