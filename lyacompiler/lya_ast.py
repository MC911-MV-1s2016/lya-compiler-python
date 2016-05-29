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


from typing import List

from enum import Enum, unique
from .lya_builtins import VoidType


@unique
class IDQualType(Enum):
    none = 0
    loc = 1
    ref = 2


class ASTNode(object):
    """
    Base class example for the AST nodes.  Each node is expected to
    define the _fields attribute which lists the names of stored
    attributes.   The __init__() method below takes positional
    arguments and assigns them to the appropriate fields.  Any
    additional arguments specified as keywords are also assigned.
    """

    _fields = []
    _raw_type_field = None
    _debug_fields = ['name', 'value', 'scope_level', 'offset', 'displacement']

    def __init__(self, *args, **kwargs):
        assert len(args) == len(self._fields)

        self.raw_type = VoidType

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Assign additional keyword arguments if supplied
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __str__(self):
        debug_data = self.debug_data()

        s = self.class_name

        if debug_data is not None:
            s = "{0}: {1}".format(self.class_name, debug_data)

        lineno = getattr(self, "lineno", None)

        if lineno is not None:
            s += " (at line :{0})".format(lineno)

        return s

    @property
    def class_name(self):
        return self.__class__.__name__

    def debug_data(self):
        d = None

        for field in self._debug_fields:
            value = getattr(self, field, None)
            if value is not None:
                if d is None:
                    d = "{0}={1}".format(field, value)
                else:
                    d = "{0}, {1}={2}".format(d, field, value)

        if d == '':
            d = None

        return d


class Program(ASTNode):
    """
    :type statements: list[Statement]
    """
    _fields = ['statements']

    def __init__(self, statements, **kwargs):
        super().__init__(statements, **kwargs)
        self.statements = statements


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
    """
    :type label: Identifier
    :type definition: ProcedureDefinition
    """
    _fields = ['label', 'definition']

    def __init__(self, label, definition, **kwargs):
        super().__init__(label, definition, **kwargs)
        self.label = label
        self.definition = definition


class Declaration(ASTNode):
    """
    :type ids: list[Identifier]
    :type mode: Mode
    :type init: Expression
    """

    _fields = ['ids', 'mode', 'init']

    def __init__(self, ids, mode, init, **kwargs):
        super().__init__(ids, mode, init, **kwargs)
        self.ids = ids
        self.mode = mode
        self.init = init

class SynonymDefinition(ASTNode):
    _fields = ['ids', 'mode', 'expr']


class ModeDefinition(ASTNode):
    _fields = ['ids', 'mode']


class Mode(ASTNode):

    _fields = ['type']

    def __init__(self, type, *args, **kwargs):
        super().__init__(type, *args, **kwargs)
        self.type = type
        self.memory_size = 1


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
    _fields = ['ids', 'mode']


class IndexMode(ASTNode):
    _fields = ['mode']


class ElementMode(ASTNode):
    _fields = ['mode']


class Identifier(ASTNode):
    """
    :type lineno: int
    :type name: str
    :type memory_size: int
    :type scope: int
    :type displacement: int
    :type start: int
    :type stop: int
    :type qual_type: IDQualType
    """

    _fields = ['name']

    def __init__(self, name, **kwargs):
        self.lineno = None
        super().__init__(name, **kwargs)
        self.name = name
        self.memory_size = 1
        self.scope_level = None
        self.displacement = None
        self.start = None
        self.stop = None
        self.qual_type = IDQualType.none


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

    def debug_data(self):
        return self.op


class Expression(ASTNode):
    _fields = ['sub_expression']


class ConditionalExpression(Expression):
    _fields = ['bool_expr', 'then_expr', 'elsif_expr', 'else_expr']


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


class BinOp(ASTNode):
    _fields = ['l_value', 'op', 'r_value']

    def debug_data(self):
        return self.op


class UnOp(ASTNode):
    _fields = ['op', 'value']


class ReferencedLocation(ASTNode):
    _fields = ['loc']


class LabeledAction(Statement):
    _fields = ['label', 'action']


class Action(ASTNode):
    _fields = ['type']


class BracketedAction(Action):
    pass


class AssignmentAction(Action):
    _fields = ['loc', 'op', 'expr']


class IfAction(Action):
    _fields = ['bool_expr', 'then_clause', 'else_clause']


class ThenClause(ASTNode):
    _fields = ['stmt']


class ElseClause(ASTNode):
    _fields = ['stmt']


class ElsifClause(ASTNode):
    _fields = ['bool_expr', 'then_clause', 'else_clause']


class DoAction(Action):
    _fields = ['ctrl', 'stmt']


class DoControl(ASTNode):
    _fields = ['for_ctrl', 'while_ctrl']


class ForControl(ASTNode):
    _fields = ['enum']


class StepEnumeration(ASTNode):
    _fields = ['counter', 'start_val', 'step_val', 'down', 'end_val']


class RangeEnumeration(ASTNode):
    _fields = ['counter', 'down', 'mode']


class WhileControl(ASTNode):
    _fields = ['expr']


class CallAction(Action):
    pass


class ProcCall(CallAction):
    _fields = ['name', 'params']


# class Parameter(ASTNode):
#     _fields = ['value']


class ExitAction(Action):
    _fields = ['label']


class ReturnAction(Action):
    _fields = ['result']


class ResultAction(Action):
    _fields = ['result']


class BuiltinCall(CallAction):
    _fields = ['name', 'param']


class ProcedureDefinition(ASTNode):
    """
    :type parameters: list[FormalParameter]
    :type result: ResultSpec
    :type statements: list[Statement]
    """

    _fields = ['parameters', 'result', 'statements']

    def __init__(self, parameters, result, statements, **kwargs):
        super().__init__(parameters, result, statements, **kwargs)
        self.parameters = parameters
        self.result = result
        self.statements = statements

    def validate_arguments(self, arguments: List[Expression]):
        pass


class FormalParameter(ASTNode):
    """
    :type ids: list[Identifier]
    :type spec: ParameterSpec
    """

    _fields = ['ids', 'spec']

    def __init__(self, ids, spec, **kwargs):
        super().__init__(ids, spec, **kwargs)
        self.ids = ids
        self.spec = spec


class ParameterSpec(ASTNode):
    """
    :type mode: Mode
    :type loc: IDQualType
    """

    _fields = ['mode', 'loc']

    def __init__(self, mode, loc, **kwargs):
        super().__init__(mode, loc, **kwargs)
        self.mode = mode
        self.loc = loc


class ResultSpec(ASTNode):
    """
    :type mode: Mode
    :type loc: IDQualType
    """

    _fields = ['mode', 'loc']

    def __init__(self, mode, loc, **kwargs):
        super().__init__(mode, loc, **kwargs)
        self.mode = mode
        self.loc = loc