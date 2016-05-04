# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lya_ast.py
# AST for the Lya scripting language.
#
# ------------------------------------------------------------


class ASTNode(object):
    """
    Base class example for the AST nodes.  Each node is expected to
    define the _fields attribute which lists the names of stored
    attributes.   The __init__() method below takes positional
    arguments and assigns them to the appropriate fields.  Any
    additional arguments specified as keywords are also assigned.
    """

    _fields = []

    def __init__(self, *args, **kwargs):
        assert len(args) == len(self._fields)

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Assign additional keyword arguments if supplied
        for name, value in kwargs.items():
            setattr(self, name, value)


class Program(ASTNode):
    _fields = ['stmts']


class Statement(ASTNode):
    pass


class DeclarationStatement(Statement):
    _fields = ['dcls']


class SynonymStatement(Statement):
    _fields = ['syns']


class NewModeStatement(Statement):
    _fields = ['new_modes']


class ProcedureStatement(Statement):
    _fields = ['label', 'definition']


class ActionStatement(Statement):
    _fields = ['label', 'action']


class Declaration(ASTNode):
    _fields = ['ids', 'mode', 'init']


class SynonymDefinition(ASTNode):
    _fields = ['ids', 'mode', 'expr']


class ModeDefinition(ASTNode):
    _fields = ['ids', 'mode']


class Mode(ASTNode):
    _fields = ['type']


class DiscreteMode(Mode):
    _fields = ['name']


class DiscreteRangeMode(ASTNode):
    _fields = ['var', 'lit_range']


class LiteralRange(ASTNode):
    _fields = ['lbound', 'ubound']


class ReferenceMode(Mode):
    _fields = ['mode']


class CompositeMode(Mode):
    _fields = ['mode']


class StringMode(CompositeMode):
    _fields = ['strlen']


class StringLength(ASTNode):
    _fields = ['len']


class ArrayMode(CompositeMode):
    _fields = ['idxs', 'mode']


class IndexMode(ASTNode):
    _fields = ['mode']


class ElementMode(ASTNode):
    _fields = ['mode']





class Assignment(ASTNode):
    _fields = ['lvalue', 'op', 'rvalue']
