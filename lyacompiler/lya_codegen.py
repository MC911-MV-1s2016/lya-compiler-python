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
        self.instructions_index = 0
        self.labels_map = {}
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
        instruction.index = self.instructions_index
        self.instructions.append(instruction)
        if isinstance(instruction, LBL):
            self.labels_map[instruction.i] = instruction.index
        self.instructions_index += 1

    def _lookup_procedure(self, proc_call: ProcedureCall):
        entry_procedure = self.current_scope.procedure_lookup(proc_call.identifier.name, proc_call.lineno)
        if entry_procedure is None:
            raise LyaNameError(proc_call.lineno, proc_call.identifier.name)
        return entry_procedure

    # Code Generation ----

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

        if procedure.offset != 0:
            self._add_instruction(ALC(procedure.offset))

        self.visit(procedure.definition)

        if procedure.offset != 0:
            self._add_instruction(DLC(procedure.offset))

        if procedure.identifier.raw_type is not LyaVoidType:
            # Calculating the number of parameters received
            mem_size = 0
            n_params = 0
            for p in procedure.definition.parameters:
                for i in p.ids:
                    mem_size += i.raw_type.memory_size
            self._add_instruction(RET(self.current_scope.level, mem_size))

        self._add_instruction(LBL(procedure.end_label))
        self.current_scope = self.current_scope.parent

    def visit_ProcedureCall(self, call: ProcedureCall):
        procedure = self._lookup_procedure(call)
        ret = procedure.scope.ret
        if ret is not None and ret.raw_type.memory_size > 0:
            self._add_instruction(ALC(ret.raw_type.memory_size))

        for expression in reversed(call.expressions):
            exp = expression.sub_expression
            if isinstance(exp, Expression):
                if exp.exp_value:
                    # TODO: Carregar str cte
                    self._add_instruction(LDC(exp.exp_value))
                    pass
            else:
                self.visit(expression)

        self._add_instruction(CFU(call.start_label))

        # if procedure.definition.result.loc is QualifierType.ref_location:
        #     self._add_instruction(GRC())

    def visit_ReturnAction(self, return_action: ReturnAction):
        procedure = self.current_scope.enclosure    # type: ProcedureStatement
        end_label = procedure.end_label

        if return_action.expression is not None:
            self.visit(return_action.expression)
            self._add_instruction(STV(self.current_scope.level, return_action.displacement))
        self._add_instruction(JMP(end_label))

    def visit_ResultAction(self, result: ResultAction):
        result.expression.sub_expression.qualifier = QualifierType.location
        self.visit(result.expression)

        self._add_instruction(STV(self.current_scope.level, result.displacement))

    def visit_BuiltinCall(self, builtin_call: BuiltinCall):

        name = builtin_call.name

        if name == 'print':
            print_arg_list = builtin_call.expressions  # type: Expression

            for print_arg in print_arg_list:
                self.visit(print_arg)
                if isinstance(print_arg.raw_type, LyaStringType):
                    self._add_instruction(PRS())
                elif isinstance(print_arg.sub_expression, StringConstant):
                    self._add_instruction(PRC(print_arg.sub_expression.heap_position))
                elif isinstance(print_arg.sub_expression, LyaArrayType):
                    # TODO: Improve array printing
                    self._add_instruction(PRT(print_arg.sub_expression.length))
                else:
                    self._add_instruction(PRV())

        # if name == 'print':
        #     print_arg = builtin_call.expressions[0]     # type: Expression
        #
        #     self.visit(print_arg)
        #     if isinstance(print_arg.raw_type, LyaStringType):
        #         self._add_instruction(PRS())
        #     elif isinstance(print_arg.sub_expression, StringConstant):
        #         self._add_instruction(PRC(print_arg.sub_expression.heap_position))
        #     elif isinstance(print_arg.sub_expression, LyaArrayType):
        #         # TODO: Improove array printing
        #         self._add_instruction(PRT(print_arg.sub_expression.length))
        #     else:
        #         self._add_instruction(PRV())

        if name == 'read':
            read_arg = builtin_call.expressions[0]      # type: Expression
            location = read_arg.sub_expression          # type: Location
            identifier = location.type                  # type: Identifier
            if isinstance(read_arg.raw_type, LyaStringType):
                self._add_instruction(RDS())
                self._add_instruction(STS(read_arg.raw_type.length))
            else:
                self._add_instruction(RDV())
                self._add_instruction(STV(identifier.scope_level, identifier.displacement))

        if name == 'lower':
            read_arg = builtin_call.expressions[0]      # type: Expression
            location = read_arg.sub_expression          # type: Location
            raw_type = location.raw_type                # type: LyaArrayType
            self._add_instruction(LDC(raw_type.index_range[0]))

        if name == 'upper':
            read_arg = builtin_call.expressions[0]      # type: Expression
            location = read_arg.sub_expression          # type: Location
            raw_type = location.raw_type                # type: LyaArrayType
            self._add_instruction(LDC(raw_type.index_range[1]))

        if name == 'length':
            read_arg = builtin_call.expressions[0]      # type: Expression
            location = read_arg.sub_expression          # type: Location
            raw_type = location.raw_type
            self._add_instruction(LDC(raw_type.length))


    # Location

    def visit_Location(self, location: Location):
            if isinstance(location.type, Identifier):
                # TODO: Other location types
                if location.type.qualifier is QualifierType.location:
                    self._add_instruction(LRV(location.type.scope_level, location.type.displacement))
                elif location.type.qualifier is QualifierType.ref_location:
                    self._add_instruction(LDR(location.type.scope_level, location.type.displacement))
                else:
                    self._add_instruction(LDV(location.type.scope_level, location.type.displacement))
            else:
                self.visit(location.type)

    def visit_DereferencedReference(self, dereferenced_reference: DereferencedReference):
        if isinstance(dereferenced_reference.loc.type, Identifier):
            self._add_instruction(LRV(dereferenced_reference.loc.type.scope_level, dereferenced_reference.loc.type.displacement))
        else:
            self.visit(dereferenced_reference.loc.type)

    def visit_ReferencedLocation(self, referenced_location: ReferencedLocation):
        if isinstance(referenced_location.loc.type, Identifier):
            self._add_instruction(LDR(referenced_location.loc.type.scope_level, referenced_location.loc.type.displacement))
        else:
            self.visit(referenced_location.loc.type)
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

    # Constants / Literals ----------------------------------

    def visit_IntegerConstant(self, iconst: IntegerConstant):
        self._add_instruction(LDC(iconst.value))

    def visit_BooleanConstant(self, bconst: BooleanConstant):
        self._add_instruction(LDC(bconst.value))

    def visit_CharacterConstant(self, cconst: CharacterConstant):
        cconst.raw_type = LTF.char_type()

    # def visit_EmptyConstant(self, econst: EmptyConstant):
    #     econst.raw_type = LTF.void_type()

    # def visit_StringConstant(self, sconst: StringConstant):
    #     sconst.heap_position = self.environment.store_string_constant(sconst.value)
    #     sconst.raw_type = LTF.string_type(sconst.length)

    def visit_BinaryExpression(self, binary_expression: BinaryExpression):

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

        # TODO: Refatorar RelationalExpression

        left = relational_expression.l_value
        right = relational_expression.r_value
        op = relational_expression.op

        if isinstance(left, Location):
            if isinstance(left.type, Identifier):
                self._add_instruction(LDV(left.type.scope_level, left.type.displacement))
        elif isinstance(left, Expression):
            if left.exp_value:
                # TODO: Carregar str cte
                self._add_instruction(LDC(left.exp_value))
                pass
        else:
            self.visit(left)

        if isinstance(right, Location):
            if isinstance(right.type, Identifier):
                self._add_instruction(LDV(right.type.scope_level, right.type.displacement))
        elif isinstance(left, Expression):
            if right.exp_value:
                # TODO: Carregar cte
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
                # TODO: Carregar str cte
                self._add_instruction(LDC(value.exp_value))
                pass
        else:
            self.visit(value)

        self._add_instruction(value.raw_type.get_unary_instruction(op))

    # Action -----------------------------------------------------------------------------------------------------------

    def visit_LabeledAction(self, labeled_action: LabeledAction):
        self.visit(labeled_action.action)
        self._add_instruction(LBL(labeled_action.label))

    # def visit_Action(self, action: Action):

    # def visit_BracketedAction(self, bracketed_action: BracketedAction):

    def visit_AssignmentAction(self, assignment: AssignmentAction):
        if isinstance(assignment.location.type, ProcedureCall):
            self.visit(assignment.location.type)

        self.visit(assignment.expression)
        # Assignment Location
        if isinstance(assignment.location.type, Identifier):
            if assignment.location.type.qualifier == QualifierType.location:
                self._add_instruction(SRV(assignment.location.type.scope_level, assignment.location.type.displacement))
            else:
                self._add_instruction(STV(assignment.location.type.scope_level, assignment.location.type.displacement))
        elif isinstance(assignment.location.type, Element):
            # TODO: Função para acessar elemento e e colocar instruction no assign
            pass

        # Assignment Expression
        if hasattr(assignment.expression, 'sub_expression'):
            if isinstance(assignment.expression.sub_expression, Location):
                if isinstance(assignment.expression.sub_expression.type, ProcedureCall):
                    procedure_call = assignment.expression.sub_expression.type
                    procedure_statement = self._lookup_procedure(procedure_call)

                    if procedure_statement.definition.result.loc == QualifierType.ref_location:
                        self._add_instruction(GRC())
                if isinstance(assignment.expression.sub_expression.type, Element):
                    # TODO: Resolver elemento e colocar instrução para grc
                    pass

        if isinstance(assignment.location.type, ProcedureCall):
            # TODO: Não tem que checar se o call tem retorno antes de fazer isso?
            self._add_instruction(SMV(assignment.location.type.raw_type.memory_size))

    # IfAction ---------------------------------------------------------------------------------------------------------

    def visit_IfAction(self, if_action: IfAction):
        # IfAction
        self.visit(if_action.boolean_expression)
        self._add_instruction(JOF(if_action.next_label))

        # ThenClause
        self.visit(if_action.then_clause)

        # ElseClause
        if if_action.else_clause is not None:
            self._add_instruction(JMP(if_action.exit_label))
            self._add_instruction(LBL(if_action.next_label))
            self.visit(if_action.else_clause)
            self._add_instruction(LBL(if_action.exit_label))
        else:
            self._add_instruction(LBL(if_action.next_label))

        # if if_action.exit_label is not None:
        #     self._add_instruction(LBL(if_action.exit_label))

    def visit_ElsIfClause(self, else_if_clause: ElsIfClause):
        # If
        self.visit(else_if_clause.boolean_expression)
        self._add_instruction(JOF(else_if_clause.next_label))

        # Then
        self.visit(else_if_clause.then_clause)

        # Else
        if else_if_clause.else_clause is not None:
            self._add_instruction(JMP(else_if_clause.exit_label))
            self._add_instruction(LBL(else_if_clause.next_label))
            self.visit(else_if_clause.else_clause)
        else:
            self._add_instruction(LBL(else_if_clause.next_label))

    # DoAction ---------------------------------------------------------------------------------------------------------

    def visit_DoAction(self, do_action: DoAction):

        # For setup.
        if do_action.control.for_control is not None:
            iteration = do_action.control.for_control.iteration
            if isinstance(iteration, StepEnumeration):
                self.visit(iteration.start_expression)
                self._add_instruction(STV(iteration.identifier.scope_level,
                                          iteration.identifier.displacement))
            else:
                # TODO: RangeEnumeration
                pass

        self._add_instruction(LBL(do_action.start_label))

        # While Control. Stopping condition.
        if do_action.control.while_control is not None:
            self.visit(do_action.control.while_control.boolean_expression)
            self._add_instruction(JOF(do_action.end_label))

        for action in do_action.actions:
            self.visit(action)

        # For Control. Stopping condition.
        if do_action.control.for_control is not None:
            iteration = do_action.control.for_control.iteration
            if isinstance(iteration, StepEnumeration):

                # Push i (control identifier)
                self._add_instruction(LDV(iteration.identifier.scope_level,
                                          iteration.identifier.displacement))

                if iteration.step_expression is not None:
                    # Push step value.
                    self.visit(iteration.step_expression)
                else:
                    # Push 1.
                    self._add_instruction(LDC(1))

                if iteration.down:
                    # i - step
                    self._add_instruction(SUB())
                else:
                    # i + step
                    self._add_instruction(ADD())
                # Storing updated i.
                self._add_instruction(STV(iteration.identifier.scope_level,
                                          iteration.identifier.displacement))
                # Pushing i back to memory.
                self._add_instruction(LDV(iteration.identifier.scope_level,
                                          iteration.identifier.displacement))
                # Push end value.
                self.visit(iteration.end_expression)
                # Checking if stopping condition reached.
                if iteration.down:
                    # i < end
                    self._add_instruction(LES())
                else:
                    # i > end
                    self._add_instruction(GRT())
                # If not stopping condition, go to next iteration.
                self._add_instruction(JOF(do_action.start_label))
            else:
                # TODO: RangeEnumeration
                pass

        # Next iteration.
        if do_action.control.while_control is not None \
                and do_action.control.for_control is None:
            self._add_instruction(JMP(do_action.start_label))

        if do_action.end_label is not None:
            self._add_instruction(LBL(do_action.end_label))

    # Exit Action

    def visit_ExitAction(self, exit_action: ExitAction):
        self._add_instruction(JMP(exit_action.exit_label))