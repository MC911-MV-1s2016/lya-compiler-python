#!/usr/bin/env python3
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

# from enum import Enum, unique
# from lyacompiler.lyabuiltins import *

from enum import Enum, unique
from .lyabuiltins import VoidType


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
    _debug_fields = ['name', 'scope', 'offset', 'displacement']

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
    """-novo escopo
    """
    _fields = ['statements']

    def debug_data(self):
        return "testing debug data string"

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
    """-adicionar o label no escopo
    -criar um novo escopo
    -visitar def->result (p/ saber o tipo de retorno)
    -visitar a definition
    -percorrer def->stmts p/ checar se os tipos do return coincidem com
    o tipo de return da funcao
    -remover o escopo
    """
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
    _fields = ['ids', 'mode']


class IndexMode(ASTNode):
    _fields = ['mode']


class ElementMode(ASTNode):
    _fields = ['mode']


class Identifier(ASTNode):
    _fields = ['name']


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

    def debug_data(self):
        return self.value


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
    _fields = ['value']


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
    """ -visitar a lista de parametros e stmts (ok)
    """
    _fields = ['params', 'result', 'stmts']


class FormalParameter(ASTNode):
    """-visitar o spec (ok)
    -visitar os ids (ok) e adiciona-los no escopo (add formalparam) (ok)
    -associar a cada id o seu tipo
    """
    _fields = ['ids', 'spec']


class ParameterSpec(ASTNode):
    _fields = ['mode', 'loc']


class ResultSpec(ASTNode):
    _fields = ['mode', 'loc']