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

from . import LyaColor
from .lya_builtins import LyaType

@unique
class QualifierType(Enum):
    none = 0
    location = 1
    ref_location = 2


class ASTNode(object):
    """
    Base class example for the AST nodes.  Each node is expected to
    define the _fields attribute which lists the names of stored
    attributes.   The __init__() method below takes positional
    arguments and assigns them to the appropriate fields.  Any
    additional arguments specified as keywords are also assigned.
    """

    _fields = []
    _debug_fields = ['raw_type',        # LyaType: created or inherited
                     'name',            # Node name
                     'operation',       # Un/Binary Expression Operation
                     'value',           # Value, usually on constant nodes
                     'exp_value',       # When possible, expressions pre-computations
                     'synonym_value',   # Identifier synonym value
                     'label',           # Label value
                     'start_label',     # Procedure start label
                     'end_label',       # Procedure end label
                     'next_label',      # IfThenElse next label (If -> Then -> Else)
                     'exit_label',      # IfThenElse exit label
                     'heap_position',   # String constant position on string heap
                     'scope_level',     # Node's scope depth.
                     'offset',          # Memory 'slots' from scope base register
                     'displacement']    # Displacement form base register

    def __init__(self, *args, **kwargs):
        assert len(args) == len(self._fields)

        self.raw_type = None    # type: LyaType
        self.exp_value = None

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Assign additional keyword arguments if supplied
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __str__(self):
        debug_data = self.debug_data()

        s = "{0}{1}{2}".format(LyaColor.OKGREEN,
                               self.class_name,
                               LyaColor.ENDC)

        if debug_data is not None:
            s = "{0}: {1}".format(s, debug_data)

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

    def copy_type(self, node):
        pass


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
    :type identifier: Identifier
    :type definition: ProcedureDefinition
    :type start_label: int
    :type end_label: int
    """
    _fields = ['identifier', 'definition']

    def __init__(self, label, definition, **kwargs):
        super().__init__(label, definition, **kwargs)
        self.identifier = label
        self.definition = definition
        self.start_label = None
        self.end_label = None


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
    """
    :type identifiers: list[Identifier]
    :type mode: Mode
    :type initialization: Expression
    """

    _fields = ['identifiers', 'mode', 'expression']

    def __init__(self, identifiers, mode, expression, **kwargs):
        super().__init__(identifiers, mode, expression, **kwargs)
        self.identifiers = identifiers
        self.mode = mode
        self.expression = expression

# Visitar Expression.

# Assign to define or type -> ilegal operation.

class ModeDefinition(ASTNode):
    _fields = ['ids', 'mode']


class Mode(ASTNode):
    _fields = ['base_mode']

    def __init__(self, base_mode, **kwargs):
        super().__init__(base_mode, **kwargs)
        self.base_mode = base_mode
        self.memory_size = 1


class DiscreteMode(Mode):
    """
    :type name: str
    """
    _fields = ['name']

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.name = name


class DiscreteRangeMode(Mode):
    _fields = ['name', 'literal_range']


class LiteralRange(ASTNode):
    """
    :type lower_bound: Expression
    :type upper_bound: Expression
    """
    _fields = ['lower_bound', 'upper_bound']

    def __init__(self, lower_bound: 'Expression', upper_bound: 'Expression', **kwargs):
        super().__init__(lower_bound, upper_bound, **kwargs)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound


class ReferenceMode(Mode):
    """
    :type mode: Mode
    """

    _fields = ['mode']

    def __init__(self, mode, **kwargs):
        super().__init__(mode, **kwargs)
        self.mode = mode


class CompositeMode(Mode):
    pass


class StringMode(CompositeMode):
    """
    :type length: IntegerConstant
    """

    _fields = ['length']

    def __init__(self, length: 'IntegerConstant', **kwargs):
        super().__init__(length, **kwargs)
        self.length = length


class ArrayMode(CompositeMode):
    """
    :type index_modes: [LiteralRange]
    :type element_mode: Mode
    """

    _fields = ['index_modes']

    def __init__(self, index_modes, element_mode: Mode, **kwargs):
        self.lineno = None
        super().__init__(index_modes, **kwargs)
        self.index_modes = index_modes
        self.element_mode = element_mode


# class IndexMode(ASTNode):
#     _fields = ['literal_range']
#
#     def __init__(self, literal_range):


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
    :type qualifier: QualifierType
    :type synonym_value: int, str, bool
    :type label_value: int
    """

    _fields = ['name']

    def __init__(self, name, **kwargs):
        self.lineno = None
        super().__init__(name, **kwargs)
        self.name = name
        self.scope_level = None
        self.displacement = None
        self.start = None #range
        self.stop = None
        self.qualifier = QualifierType.none
        self.synonym_value = None
        self.label_value = None


class Location(ASTNode):
    _fields = ['type']

    def __init__(self, type, **kwargs):
        super().__init__(type, **kwargs)
        self.type = type


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

    def __int__(self, value, **kwargs):
        super().__init__(value, **kwargs)
        self.value = value


class IntegerConstant(Constant):
    pass


class BooleanConstant(Constant):
    pass


class CharacterConstant(Constant):
    pass


class EmptyConstant(Constant):
    pass


class StringConstant(Constant):
    """
    :type value: str
    :type length: int
    :type heap_position: int
    """

    def __init__(self, value: str, **kwargs):
        super().__init__(value, **kwargs)
        self.length = len(value)
        self.heap_position = None


class ValueArrayElement(ASTNode):
    _fields = ['value', 'expr']


class ValueArraySlice(ASTNode):
    _fields = ['value', 'l_bound', 'u_bound']

class Expression(ASTNode):
    _fields = ['sub_expression']

    # ConditionalExpression
    # Constant
    # ValueArrayElement
    # ValueArraySlice
    # Expression

    # def __init__(self, sub_expression, **kwargs):
    #     super().__init__(sub_expression, **kwargs)
    #     self.sub_expression = sub_expression


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


class RelationalExpression(Expression):
    _fields = ['l_value', 'op', 'r_value']


class MembershipExpression(Expression):
    _fields = ['l_value', 'op', 'r_value']


class BinaryExpression(Expression):
    """
    """
    _fields = ['left', 'operation', 'right']

    def __init__(self, left, operation, right, **kwargs):
        self.lineno = None
        super().__init__(left, operation, right, **kwargs)
        self.left = left
        self.operation = operation
        self.right = right

    # def debug_data(self):
    #     return self.operation


class UnaryExpression(Expression):
    """

    """
    _fields = ['op', 'value']


class ReferencedLocation(ASTNode):
    _fields = ['loc']


class LabeledAction(Statement):
    """
    :type name: str
    :type action: Action
    :type label: int
    """
    _fields = ['name', 'action']

    def __init__(self, name: str, action: 'Action', **kwargs):
        self.lineno = None
        super().__init__(name, action, **kwargs)
        self.name = name
        self.action = action
        self.label = None


class Action(ASTNode):
    _fields = ['type']


class BracketedAction(Action):
    pass


class AssignmentAction(Action):
    """
    :type location: Location
    :type expression: expression
    """
    _fields = ['location', 'expression']

    def __init__(self, location: 'Location', expression: 'Expression', **kwargs):
        self.lineno = None
        super().__init__(location, expression, **kwargs)
        self.location = location
        self.expression = expression


class IfAction(Action):
    """
    :type boolean_expression: BooleanExpression
    :type then_clause: ThenClause
    :type else_clause:
    :type exit_label: int
    :type next_label: int       @nullable
    """
    _fields = ['boolean_expression', 'then_clause', 'else_clause']

    def __init__(self, boolean_expression: 'BooleanExpression', then_clause: 'ThenClause', else_clause, **kwargs):
        super().__init__(boolean_expression, then_clause, else_clause, **kwargs)
        self.boolean_expression = boolean_expression
        self.then_clause = then_clause
        self.else_clause = else_clause
        self.exit_label = None
        self.next_label = None


class ThenClause(ASTNode):
    """
    :type actions: List[Action]
    """
    _fields = ['actions']

    def __init__(self, actions: List['Action'], **kwargs):
        super().__init__(actions, **kwargs)
        self.actions = actions


class ElseClause(ASTNode):
    """
    :type actions: List[Action]
    :type label: int
    """
    _fields = ['actions']

    def __init__(self, actions: List['Action'], **kwargs):
        super().__init__(actions, **kwargs)
        self.actions = actions
        self.label = None


class ElsIfClause(ASTNode):
    """
    :type boolean_expression: BooleanExpression
    :type then_clause: ThenClause
    :type else_clause:
    :type label: int
    :type exit_label: int
    :type next_label: int       @nullable
    """
    _fields = ['boolean_expression', 'then_clause', 'else_clause']

    def __init__(self, boolean_expression: BooleanExpression, then_clause: ThenClause, else_clause, **kwargs):
        super().__init__(boolean_expression, then_clause, else_clause, **kwargs)
        self.boolean_expression = boolean_expression
        self.then_clause = then_clause
        self.else_clause = else_clause
        self.label = None
        self.exit_label = None
        self.next_label = None


# TODO: Marcar o que é nullable nos nós

class DoAction(Action):
    """
    :type control: DoControl
    :type actions: List[Action]
    :type start_label: int
    :type end_label: int    @nullable
    """
    _fields = ['control', 'actions']

    def __init__(self, control: 'DoControl', actions: List['Action'], **kwargs):
        super().__init__(control, actions, **kwargs)
        self.control = control
        self.actions = actions
        self.start_label = None
        self.end_label = None


class DoControl(ASTNode):
    """
    :type for_control: ForControl
    :type while_control: WhileControl
    """
    _fields = ["for_control", "while_control"]

    def __init__(self, for_control: 'ForControl', while_control: 'WhileControl', **kwargs):
        super().__init__(for_control, while_control, **kwargs)
        self.for_control = for_control
        self.while_control = while_control


class ForControl(ASTNode):
    """
    :type iteration:  Iteration
    """
    _fields = ['iteration']

    def __init__(self, iteration: 'Iteration', **kwargs):
        super().__init__(iteration, **kwargs)
        self.iteration = iteration


class Iteration(ASTNode):
    pass


class StepEnumeration(Iteration):
    """
    :type identifier: Identifier
    :type start_expression: IntegerExpression
    :type step_expression: IntegerExpression @nullable
    :type down: bool
    :type end_expression: IntegerExpression
    """
    _fields = ['identifier', 'start_expression', 'step_expression', 'down', 'end_expression']

    def __init__(self, identifier: 'Identifier',
                 start_expression: 'IntegerExpression',
                 step_expression: 'IntegerExpression',
                 down: bool,
                 end_expression: 'IntegerExpression',
                 **kwargs):
        self.lineno = None
        super().__init__(identifier, start_expression, step_expression, down, end_expression, **kwargs)
        # TODO: start and end integer_exp -> discrete_exp
        self.identifier = identifier
        self.start_expression = start_expression
        self.step_expression = step_expression
        self.down = down
        self.end_expression = end_expression


class RangeEnumeration(Iteration):
    _fields = ['counter', 'down', 'mode']


class WhileControl(ASTNode):
    """
    :type boolean_expression: BooleanExpression
    """
    _fields = ['boolean_expression']

    def __init__(self, boolean_expression: 'BooleanExpression', **kwargs):
        self.lineno = None
        super().__init__(boolean_expression, **kwargs)
        self.boolean_expression = boolean_expression


class CallAction(Action):
    pass


class ProcedureCall(CallAction):
    """
    :type identifier: Identifier
    :type expressions: list[Expression]
    :type start_label: int
    """
    _fields = ['identifier', 'expressions']

    def __init__(self, identifier, expressions, **kwargs):
        self.lineno = None
        super().__init__(identifier, expressions, **kwargs)
        self.identifier = identifier
        self.expressions = expressions
        self.start_label = None


class ExitAction(Action):
    """
    :type name: str
    :type exit_label: int
    """
    _fields = ['name']

    def __init__(self, name: str, **kwargs):
        self.lineno = None
        super().__init__(name, **kwargs)
        self.name = name
        self.exit_label = None


class ReturnAction(Action):
    """
    :type result: Expression
    :type displacement: int
    """
    _fields = ['expression']

    def __init__(self, expression, **kwargs):
        self.lineno = None
        super().__init__(expression, **kwargs)
        self.expression = expression
        self.displacement = None


class ResultAction(Action):
    """
    :type result: Expression
    :type displacement: int     @nullable
    """
    _fields = ['expression']

    def __init__(self, expression, **kwargs):
        self.lineno = None
        super().__init__(expression, **kwargs)
        self.expression = expression
        self.displacement = None


class BuiltinCall(CallAction):
    """
    :type name: str
    :type expressions: List[Expression]
    """
    _fields = ['name', 'expressions']

    def __init__(self, name: str, expressions: List['Expression'], **kwargs):
        self.lineno = None
        super().__init__(name, expressions, **kwargs)
        self.name = name
        self.expressions = expressions


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
    :type loc: QualifierType
    """

    _fields = ['mode', 'loc']

    def __init__(self, mode, loc, **kwargs):
        super().__init__(mode, loc, **kwargs)
        self.mode = mode
        self.loc = loc


class ResultSpec(ASTNode):
    """
    :type mode: Mode
    :type loc: QualifierType
    """

    _fields = ['mode', 'loc']

    def __init__(self, mode, loc, **kwargs):
        super().__init__(mode, loc, **kwargs)
        self.mode = mode
        self.loc = loc
