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

    def _lookup_procedure(self, proc_call: ProcedureCall):
        entry_procedure = self.current_scope.procedure_lookup(proc_call.identifier.name, proc_call.lineno)
        if entry_procedure is None:
            raise LyaNameError(proc_call.lineno, proc_call.identifier.name)
        return entry_procedure
    # ----

    def visit_Program(self, program: Program):
        self.current_scope = program.scope
        self._add_instruction(STP())
        self._add_instruction(ALC(program.offset))

        for stmts in program.statements:
            self.visit(stmts)

        self._add_instruction(DLC(program.offset))
        self._add_instruction(END())

    # Statement -------------------------------------------------

    def visit_Declaration(self, declaration: Declaration):
        if declaration.init is not None:
            # TODO: Load string constant
            for identifier in declaration.ids:
                if declaration.init.exp_value is not None:
                    self._add_instruction(LDC(declaration.init.exp_value))
                else:
                    self.visit(declaration.init)
                self._add_instruction(STV(self.current_scope.level, identifier.displacement))

    # Procedure ------------------------------------------

    def visit_ProcedureStatement(self, procedure: ProcedureStatement):
        self.current_scope = procedure.scope
        self._add_instruction(JMP(procedure.end_label))
        self._add_instruction(LBL(procedure.start_label))
        self._add_instruction(ENF(self.current_scope.level))
        self._add_instruction(ALC(procedure.offset))

        self.visit(procedure.definition)
        #TODO

        # calculating the number of parameters received
        n_params = 0
        for p in procedure.definition.parameters:
            n_params += len(p.ids)

        self._add_instruction(DLC(procedure.offset))

        if procedure.identifier.raw_type is not LyaVoidType:
            self._add_instruction(RET(self.current_scope.level, n_params))
        self._add_instruction(LBL(procedure.end_label))
        self.current_scope = self.current_scope.parent

    def visit_ProcedureCall(self, call: ProcedureCall):
        procedure = self._lookup_procedure(call)
        ret = procedure.scope.ret
        if ret is not None:
            self._add_instruction(ALC(ret.raw_type.memory_size))

        for expression in reversed(call.expressions):
            exp = expression.sub_expression
            if isinstance(exp, Expression):
                if exp.exp_value:
                    # TODO: Otimização - carregar str cte
                    self._add_instruction(LDC(exp.exp_value))
                    pass
            else:
                self.visit(expression)
            # exp = expression.sub_expression
            # if isinstance(exp, Location):
            #     if isinstance(exp.type, Identifier):
            #         self._add_instruction(LDV(exp.type.scope_level, exp.type.displacement))
            # elif isinstance(exp, Expression):
            #     if exp.exp_value:
            #         # TODO: Otimização - carregar str cte
            #         self._add_instruction(LDC(exp.exp_value))
            #         pass
            # else:
            #     self.visit(exp)

        self._add_instruction(CFU(call.scope_level))

    # def visit_ResultSpec(self, spec: ResultSpec):
    #     self.visit(spec.mode)
    #     spec.raw_type = spec.mode.raw_type

    def visit_ReturnAction(self, return_action: ReturnAction):
        enclosure = self.current_scope.enclosure
        end_label = enclosure.end_label

        if self.current_scope.ret.raw_type == LTF.void_type():
            # TODO: Returning on void function
            pass

        if return_action.expression is not None:
            self.visit(return_action.expression)
            self._add_instruction(STV(self.current_scope.level, return_action.displacement))

        self._add_instruction(JMP(end_label))
    #
    def visit_ResultAction(self, result: ResultAction):
        self.visit(result.expression)
        self._add_instruction(STV(self.current_scope.level, result.displacement))

        # if self.current_scope.ret.raw_type == LTF.void_type():
        #     # TODO: Error setting result on void return function.
        #     pass
        # self.visit(result.expression)
        # self.current_scope.add_result(result.expression, result.lineno)
        # result.displacement = self.current_scope.parameters_displacement

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
    # Location

    def visit_Location(self, location: Location):
            if isinstance(location.type, Identifier):
                self._add_instruction(LDV(location.type.scope_level, location.type.displacement))
            else:
                self.visit(location.type)


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
    def visit_BinaryExpression(self, binary_expression: BinaryExpression):
        # Make sure left and right operands have the same type
        # Make sure the operation is supported

        left = binary_expression.left
        right = binary_expression.right
        op = binary_expression.operation

        if isinstance(left, Location):
            if isinstance(left.type, Identifier):
                self._add_instruction(LDV(left.type.scope_level, left.type.displacement))
        elif isinstance(left, Expression):
            if left.exp_value:
                # TODO: Otimização - carregar str cte
                self._add_instruction(LDC(left.exp_value))
                pass
        else:
            self.visit(left)

        if isinstance(right, Location):
            if isinstance(right.type, Identifier):
                self._add_instruction(LDV(right.type.scope_level, right.type.displacement))
        elif isinstance(left, Expression):
            if right.exp_value:
                # TODO: Otimização - carregar cte
                self._add_instruction(LDC(right.exp_value))
                pass
        else:
            self.visit(right)

        self._add_instruction(left.raw_type.get_binary_instruction(op))

    def visit_RelationalExpression(self, relational_expression: RelationalExpression):
        # Make sure left and right operands have the same type
        # Make sure the operation is supported

        left = relational_expression.l_value
        right = relational_expression.r_value
        op = relational_expression.op

        if isinstance(left, Location):
            if isinstance(left.type, Identifier):
                self._add_instruction(LDV(left.type.scope_level, left.type.displacement))
        elif isinstance(left, Expression):
            if left.exp_value:
                # TODO: Otimização - carregar str cte
                self._add_instruction(LDC(left.exp_value))
                pass
        else:
            self.visit(left)

        if isinstance(right, Location):
            if isinstance(right.type, Identifier):
                self._add_instruction(LDV(right.type.scope_level, right.type.displacement))
        elif isinstance(left, Expression):
            if right.exp_value:
                # TODO: Otimização - carregar cte
                self._add_instruction(LDC(right.exp_value))
                pass
        else:
            self.visit(right)

        self._add_instruction(left.raw_type.get_relational_instruction(op))


    def visit_UnaryExpression(self, unary_expression: UnaryExpression):
        value = unary_expression.value
        op = unary_expression.op

        if isinstance(value, Location):
            if isinstance(value.type, Identifier):
                self._add_instruction(LDV(value.type.scope_level, value.type.displacement))
        elif isinstance(value, Expression):
            if value.exp_value:
                # TODO: Otimização - carregar str cte
                self._add_instruction(LDC(value.exp_value))
                pass
        else:
            self.visit(value)

        self._add_instruction(value.raw_type.get_unary_instruction(op))

    # Action -----------------------------------------------------------------------------------------------------------

    # def visit_Action(self, action: Action):

    # def visit_BracketedAction(self, bracketed_action: BracketedAction):

    def visit_AssignmentAction(self, assignment: AssignmentAction):
        self.visit(assignment.expression)
        if isinstance(assignment.location.type, Identifier):
            self._add_instruction(STV(assignment.location.type.scope_level, assignment.location.type.displacement))

    # IfAction ---------------------------------------------------------------------------------------------------------

    # TODO: CodeGen If compare
    # TODO: CodeGen If labels
    # TODO: CodeGen BinaryExp all ops
    # TODO: CodeGen result
    # TODO: CodeGen Builtin read
    # TODO: CodeGen Builtin print


    def visit_IfAction(self, if_action: IfAction):
        # IfAction
        self.visit(if_action.boolean_expression)
        self._add_instruction(JOF(if_action.next_label))

        # ThenClause
        self.visit(if_action.then_clause)
        self._add_instruction(JMP(if_action.exit_label))

        # ElseClause
        if if_action.else_clause is not None:
            self._add_instruction(LBL(if_action.next_label))
            self.visit(if_action.else_clause)

        self._add_instruction(LBL(if_action.exit_label))

    def visit_ElsIfClause(self, else_if_clause: ElsIfClause):
        # If
        self.visit(else_if_clause.boolean_expression)
        self._add_instruction(JOF(else_if_clause.next_label))

        # Then
        self.visit(else_if_clause.then_clause)
        self._add_instruction(JMP(else_if_clause.exit_label))

        # Else
        if else_if_clause.else_clause is not None:
            self._add_instruction(LBL(else_if_clause.next_label))
            self.visit(else_if_clause.else_clause)
