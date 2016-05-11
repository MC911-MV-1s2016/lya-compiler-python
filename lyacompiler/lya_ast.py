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
    _indent = 2

    def __init__(self, *args, **kwargs):
        assert len(args) == len(self._fields)

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Assign additional keyword arguments if supplied
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __str__(self):
        debug_data = self.debug_data()
        s = self.name

        if debug_data is not None:
            s = "{0}: {1}".format(self.name, debug_data)

        lineno = getattr(self, "lineno", None)

        if lineno is not None:
            s += " (at line {0})".format(lineno)

        return s

    @property
    def name(self):
        return self.__class__.__name__

    def debug_data(self):
        return None


class Program(ASTNode):
    _fields = ['statements']

    def debug_data(self):
        return "Debug data test"

# Statement


class Statement(ASTNode):
    pass


class DeclarationStatement(Statement):
    _fields = ['declarations']


class SynonymStatement(Statement):
    _fields = ['synonyms']


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
    _fields = ['type']

    def debug_data(self):
        return "Type {0}".format(self.type)


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
    _fields = ['ids', 'mode']


class IndexMode(ASTNode):
    _fields = ['mode']


class ElementMode(ASTNode):
    _fields = ['mode']


class Identifier(ASTNode):
    _fields = ['ids']


class Location(ASTNode):
    _fields = ['type']


class DereferencedReference(ASTNode):
    _fields = ['loc']


class StringElement(ASTNode):
    _fields = ['ids', 'st_element']


class StartElement(ASTNode):
    _fields = ['expr']


class StringSlice(ASTNode):
    _fields = ['ids', 'l_elem', 'r_elem']


class ArrayElement(ASTNode):
    _fields = ['loc', 'expr']


class ArraySlice(ASTNode):
    _fields = ['loc', 'l_bound', 'u_bound']


class Constant(ASTNode):
    _fields = ['value']


class IntegerConstant(Constant):
    pass


class BooleanConstant(Constant):
    pass


class CharacterConstant(Constant):
    pass


class EmptyConstant(Constant):
    pass


class StringConstant(Constant):
    pass


class ValueArrayElement(ASTNode):
    _fields = ['value', 'expr']


class ValueArraySlice(ASTNode):
    _fields = ['value', 'l_bound', 'u_bound']



class Assignment(ASTNode):
    _fields = ['l_value', 'op', 'r_value']


class Expression(ASTNode):
    _fields = ['value']


class IntegerExpression(Expression):
    pass


class BooleanExpression(Expression):
    pass


class ThenExpression(Expression):
    pass


class ElseExpression(Expression):
    pass


class ElsifExpression(Expression):
    _fields = ['elsif_expr', 'bool_expr', 'then_expr']



class ConditionalExpression(ASTNode):
    _fields = ['bool_expr', 'then_expr', 'elsif_expr', 'else_expr']