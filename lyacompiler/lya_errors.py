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

from . import LyaColor
from .lya_builtins import *
from .lya_ast import ASTNode
# from .lya_scope import SymbolEntry

__all__ = [
    'LyaError',
    'LyaNameError',
    'LyaTypeError',
    'LyaAssignmentError',
    'LyaOperationError',
    'LyaUnknownError'
]

# Index Out Of Range
# FuncCall (Wrong Params)
#


class LyaError(Exception):
    """Base class for exceptions in the Lya compiler."""

    def __init__(self, lineno: int):
        self.lineno = lineno

    def __str__(self):
        err_msg = "{0}{1} (line: {2}){3}".format(LyaColor.WARNING,
                                                 self.class_name,
                                                 self.lineno,
                                                 LyaColor.ENDC)
        message = self.message()
        if message is not None:
            err_msg = "{0}: {1}".format(err_msg, message)
        return err_msg

    @property
    def class_name(self):
        return self.__class__.__name__

    def message(self):
        return None

# fun call err args, wrong number, wrong types


class LyaNameError(LyaError):
    """Exception raised for undefined names.

    Attributes:
        lineno -- The line number where the exception was raised.
        name -- The name that raised the exception.
        previous_def -- The SymbolTable entry with the previous declaration.
            Defaults to None if name wasn't defined.
    """

    def __init__(self, lineno: int, name: str, previous_def=None):
        super().__init__(lineno)
        self.name = name
        self.previous_def = previous_def

    def message(self):
        if self.previous_def is None:
            return "Name '{0}' not defined.".format(self.name)
        else:
            return "Name '{0}' redefinition. Previously defined as " \
                   "'{1}' at line {2}.".format(self.name,
                                             self.previous_def.raw_type,
                                             self.previous_def.lineno)


class LyaTypeError(LyaError):
    """Raised when an operation or function is applied to an object of inappropriate type.

    Attributes:
        lineno -- The line number where the exception was raised.
        current_type -- The actual LyaType that raised the error.
        expected_type -- The expected LyaType
    """

    def __init__(self, lineno: int, current_type: LyaType, expected_type: LyaType = None):
        super().__init__(lineno)
        self.current_type = current_type
        self.expected_type = expected_type

    def message(self):
        if self.expected_type is None:
            return "Undefined type '{0}'.".format(self.current_type)
        else:
            return "Type '{0}' received. Expected '{1}'.".format(self.current_type,
                                                                 self.expected_type)


class LyaAssignmentError(LyaTypeError):
    """Raised when trying to assign to location with incompatible type.

    Attributes:
        lineno -- The line number where the exception was raised.
        current_type -- The actual LyaType that raised the error.
        expected_type -- The expected LyaType
    """

    def __init__(self, lineno: int, current_type: LyaType, expected_type: LyaType):
        super().__init__(lineno, current_type, expected_type)

    def message(self):
        return "Assigning '{0}' to '{1}'.".format(self.current_type,
                                                  self.expected_type)


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

    def message(self):
        if self.op is None:
            return "Malformed LyaOperationError: missing op."
        if self.left_type is not None and self.right_type is not None:
            return "Unsupported operation '{0}' between " \
                   "'{1}' and '{2}'.".format(self.op,
                                             self.left_type, self.right_type)
        if self.right_type is not None:
            return "Unsupported left operation '{0}' " \
                   "on '{1}'.".format(self.op, self.right_type)
        if self.left_type is not None:
            return "Unsupported right operation '{0}'" \
                   " on '{1}'.".format(self.op, self.left_type)
        return "Malformed LyaOperationError: missing left and right types."


class LyaUnknownError(LyaError):
    """Raised when an unknown exception was caught while visiting an ASTNode.

    Attributes:
        lineno -- The line number where the exception was raised.
        node - The ASTNode whose visitor raised an unhandled exception.
    """

    def __init__(self, lineno: int, node: ASTNode):
        super().__init__(lineno)
        self.node = node

    def message(self):
        return "Node {1}.".format(self.node.class_name)
