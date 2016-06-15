# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lya_codegen.py
# Lya Decorated AST Code Generator
#
# ------------------------------------------------------------

from .astnodevisitor import ASTNodeVisitor
from .lya_ast import *
from .lya_errors import *
from .lya_builtins import *
from .lya_lvminstruction import *
from .lya_scope import LyaScope

class CodeGenerator(ASTNodeVisitor):
    """
    """
    def __init__(self):
        super().__init__()
        self.environment = None
        self.current_scope = None   # type: LyaScope
        self.instructions = []
        self.errors = []
        self.labels_map = {}

    def _add_label(self, name):
        self.labels_map[name] = len(self.labels_map) + 1

    def _lookup_label(self, name):
        return self.labels_map.get(name, None)

    def visit(self, node):
        try:
            super().visit(node)
        except LyaError as err:
            print(LyaColor.WARNING + str(err) + LyaColor.ENDC)
            self.errors.append(err)
            exit()
        else:
            # Called if no errors raised.
            pass
        finally:
            # Called always.
            pass

    def _add_instruction(self, instruction: LyaInstruction):
        self.instructions.append(instruction)

    # ----


    def visit_Program(self, program: Program):
        self.current_scope = program.scope
        self._add_instruction(STP())
        self._add_instruction(ALC(self.current_scope.level, ))


        # for statement in program.statements:
        #     self.visit(statement)
        # self.environment.end_current_scope()

    # # Statement -------------------------------------------------
    #
    def visit_Declaration(self, declaration: Declaration):

        if declaration.init is not None:
            if declaration.init.exp_value is None:
                self.visit(declaration.init)

            self._add_instruction(LDC(declaration.init.exp_value))

            for identifier in declaration.ids:
                self._add_instruction(STV(self.current_scope.level, identifier.displacement))
    #
    # def visit_SynonymStatement(self, node):
    #     # TODO: Visit/decorate SynonymDef
    #     for syn in node.synonyms:
    #         self.visit(syn)
    #
    # def visit_NewModeStatement(self, node):
    #     for new_mode in node.new_modes:
    #         self.visit(new_mode)
    #
    # # Procedure ------------------------------------------
    #
    def visit_ProcedureStatement(self, procedure: ProcedureStatement):
        self.current_scope = procedure.scope
        self._add_label(procedure.label.name)

        self.visit(procedure.definition)

        #TODO

        self.current_scope = self.current_scope.parent
    #
    # def visit_FormalParameter(self, parameter: FormalParameter):
    #     self.visit(parameter.spec)
    #     parameter.raw_type = parameter.spec.mode.raw_type
    #     for identifier in parameter.ids:
    #         identifier.raw_type = parameter.spec.mode.raw_type
    #         # TODO: Calculate memory size for string/arrays
    #         identifier.memory_size = parameter.spec.mode.memory_size
    #         identifier.qualifier = parameter.spec.loc
    #         self.current_scope.add_parameter(identifier, parameter)
    #
    # def visit_ProcedureCall(self, call: ProcedureCall):
    #
    #     for parameter in call.expressions:
    #         self.visit(parameter)
    #
    #     procedure_definition = self._lookup_procedure(call).definition
    #
    #     n_procedure_parameters = len(procedure_definition.parameters)
    #     n_call_parameters = len(call.expressions)
    #
    #     if n_procedure_parameters != n_call_parameters:
    #         raise LyaProcedureCallError(call.lineno, call.identifier.name, None, n_call_parameters, n_procedure_parameters)
    #
    #     for i in range(n_call_parameters):
    #         expression = call.expressions[i]
    #         parameter = procedure_definition.parameters[i]
    #
    #         if parameter.raw_type != expression.raw_type:
    #             raise LyaArgumentTypeError(call.lineno, call.identifier.name, i, expression.raw_type, parameter.raw_type)
    #
    # def visit_ResultSpec(self, spec: ResultSpec):
    #     self.visit(spec.mode)
    #
    #     spec.raw_type = spec.mode.raw_type
    #
    # def visit_ReturnAction(self, ret: ReturnAction):
    #     self.visit(ret.result)
    #
    #     self.current_scope.add_result(ret)
    #
    #
    # def visit_ResultAction(self, ret: ResultAction):
    #     self.visit(ret.result)
    #
    #     self.current_scope.add_result(ret)
    #
    # # Mode
    #
    # def visit_Mode(self, mode: Mode):
    #     self.visit(mode.base_mode)
    #     # TODO: If base_mode is Identifier (mode_name), check if defined as type
    #     mode.raw_type = mode.base_mode.raw_type
    #
    # def visit_DiscreteMode(self, discrete_mode: DiscreteMode):
    #     discrete_mode.raw_type = LTF.base_type_from_string(discrete_mode.name)
    #
    # # TODO: Visit discrete range mode
    #
    # def visit_ReferenceMode(self, reference_mode: ReferenceMode):
    #     self.visit(reference_mode.mode)
    #     # TODO: Improve Reference Mode management (Ref RawType + Mode RaType)
    #
    # def visit_StringMode(self, string_mode: StringMode):
    #     string_mode.raw_type = LTF.string_type(string_mode.length.value)
    #
    # def visit_ArrayMode(self, array_mode: ArrayMode):
    #     array_ranges = []
    #     self.visit(array_mode.element_mode)
    #
    #     for index_mode in array_mode.index_modes:
    #         # array[10]
    #         self.visit(index_mode)
    #         if isinstance(index_mode, IntegerConstant):
    #             if index_mode <= 0:
    #                 raise LyaGenericError(array_mode.lineno,
    #                                       array_mode,
    #                                       "Invalid array mode. "
    #                                       "Array size must be greater than zero.")
    #             array_ranges.append((0, index_mode.value - 1))
    #         elif isinstance(index_mode, LiteralRange):
    #             if index_mode.lower_bound.exp_value is None:
    #                 raise LyaGenericError(array_mode.lineno,
    #                                       array_mode,
    #                                       "Invalid array mode. "
    #                                       "Could not infer range lower bound integer value at compilation time.")
    #             if index_mode.lower_bound.raw_type != LTF.int_type():
    #                 raise LyaGenericError(array_mode.lineno,
    #                                       array_mode,
    #                                       "Invalid array mode. Invalid range lower bound type. "
    #                                       "Received '{0}'. Expected '{1}'.".format(index_mode.lower_bound.raw_type,
    #                                                                                LTF.int_type()))
    #             lb = index_mode.lower_bound.exp_value
    #
    #             if index_mode.upper_bound.exp_value is None:
    #                 raise LyaGenericError(array_mode.lineno,
    #                                       array_mode,
    #                                       "Invalid array mode. "
    #                                       "Could not infer range upper bound integer value at compilation time.")
    #             if index_mode.upper_bound.raw_type != LTF.int_type():
    #                 raise LyaGenericError(array_mode.lineno,
    #                                       array_mode,
    #                                       "Invalid array mode. Invalid range upper bound type. "
    #                                       "Received '{0}'. Expected '{1}'.".format(index_mode.lower_bound.raw_type,
    #                                                                                LTF.int_type()))
    #             ub = index_mode.upper_bound.exp_value
    #
    #             # TODO: Validate lb and ub. (Size > 0. lb can be bigger than ub??)
    #
    #             array_ranges.append((lb, ub))
    #         else:
    #             raise LyaGenericError(array_mode.lineno,
    #                                   array_mode,
    #                                   "Invalid array index_mode {0}.".format(array_mode.index_modes));
    #
    #     array_mode.raw_type = LTF.array_type(array_mode.element_mode.raw_type, array_ranges)
    #
    # # Location
    #
    # def visit_Location(self, location: Location):
    #     self.visit(location.type)
    #     if isinstance(location.type, Identifier):
    #         identifier = self._lookup_identifier(location.type)
    #
    #     location.raw_type = location.type.raw_type
    #
    # # Expression
    #
    # def visit_Expression(self, expression: Expression):
    #     self.visit(expression.sub_expression)
    #     expression.raw_type = expression.sub_expression.raw_type
    #     if isinstance(expression.sub_expression, Constant):
    #         expression.exp_value = expression.sub_expression.value
    #
    # # Do_Action
    #
    # def visit_StepEnumeration(self, step: StepEnumeration):
    #     entry = self.current_scope.entry_lookup(step.counter)
    #
    #     if entry is None:
    #         raise LyaNameError(step.lineno, step.counter)
    #
    #     self.visit(step.start_val)
    #     self.visit(step.step_val)
    #     self.visit(step.end_val)
    #
    #     if step.start_val.raw_type != LTF.int_type():
    #         raise LyaTypeError(step.lineno, step.start_val.raw_type, LTF.int_type())
    #
    #     if step.step_val.sub_expression.raw_type != LTF.int_type():
    #         raise LyaTypeError(step.lineno, step.step_val.sub_expression.raw_type, LTF.int_type())
    #
    #     if step.end_val.raw_type != LTF.int_type():
    #         raise LyaTypeError(step.lineno, step.end_val.raw_type, LTF.int_type())
    #
    # def visit_RangeEnumeration(self, range_enum: RangeEnumeration):
    #     entry = self.current_scope.entry_lookup(range_enum.counter)
    #
    #     if entry is None:
    #         raise LyaNameError(range_enum.lineno, range_enum.counter)
    #
    #     self.visit(range_enum.mode)
    #
    # def visit_WhileControl(self, ctrl: WhileControl):
    #     self.visit(ctrl.expr)
    #
    #     if ctrl.expr.sub_expression.raw_type != LTF.bool_type():
    #         raise LyaTypeError(ctrl.lineno, ctrl.expr.sub_expression.raw_type, LTF.bool_type())
    #
    # # Constants / Literals
    #
    # def visit_IntegerConstant(self, iconst: IntegerConstant):
    #     iconst.raw_type = LTF.int_type()
    #
    # def visit_BooleanConstant(self, bconst: BooleanConstant):
    #     bconst.raw_type = LTF.bool_type()
    #
    # def visit_CharacterConstant(self, cconst: CharacterConstant):
    #     cconst.raw_type = LTF.char_type()
    #
    # def visit_EmptyConstant(self, econst: EmptyConstant):
    #     econst.raw_type = LTF.void_type()
    #
    # def visit_StringConstant(self, sconst: StringConstant):
    #     sconst.heap_position = self.environment.store_string_constant(sconst.value)
    #     sconst.raw_type = LTF.string_type(sconst.length)
    #
    # # def visit_UnaryExpr(self, node):
    # #     self.visit(node.expr)
    # #     # Make sure that the operation is supported by the type
    # #     raw_type = self.raw_type_unary(node, node.op, node.expr)
    # #     # Set the result type to the same as the operand
    # #     node.raw_type = raw_type
    #
    # # def visit_BinaryExpr(self,node):
    # #     # Make sure left and right operands have the same type
    # #     # Make sure the operation is supported
    # #     self.visit(node.left)
    # #     self.visit(node.right)
    # #     raw_type = self.raw_type_binary(node, node.op, node.left, node.right)
    # #     # Assign the result type
    # #     node.raw_type = raw_type
