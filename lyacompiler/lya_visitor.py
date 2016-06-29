# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lya_visitor.py
# Lya AST Nodes Visitor
#
# ------------------------------------------------------------

from .astnodevisitor import ASTNodeVisitor
from .lya_environment import Environment
from .lya_ast import *
from .lya_errors import *
from .lya_builtins import *


class Visitor(ASTNodeVisitor):
    """
    Program Visitor class. This class uses the visitor pattern as
    described in astnodevisitor.py.   It’s define methods of the form
    visit_NodeName() for each kind of AST node that we want to process.
    Note: You will need to adjust the names of the AST nodes if you
    picked different names.
    """
    def __init__(self):
        super().__init__()
        self.environment = Environment()
        self.errors = []
        self.label_count = 1

    def visit(self, node):
        # TODO: Can try to bypass error to continue compilation.
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

    @property
    def current_scope(self):
        return self.environment.current_scope

    def _lookup_identifier(self, identifier):
        entry_identifier = self.current_scope.identifier_lookup(identifier.name)
        if entry_identifier is None:
            raise LyaNameError(identifier.lineno, identifier.name)
        identifier.raw_type = entry_identifier.raw_type
        identifier.scope_level = entry_identifier.scope_level
        identifier.displacement = entry_identifier.displacement
        identifier.start = entry_identifier.start
        identifier.stop = entry_identifier.stop
        identifier.qualifier = entry_identifier.qualifier
        identifier.synonym_value = entry_identifier.synonym_value
        return entry_identifier

    def _lookup_type(self, identifier: Identifier):
        raw_type = self.current_scope.type_lookup(identifier.name, identifier.lineno)
        if raw_type is None:
            raise LyaNameError(identifier.lineno, identifier.name)
        return raw_type

    def _lookup_procedure(self, proc_call: ProcedureCall):
        entry_procedure = self.current_scope.procedure_lookup(proc_call.identifier.name, proc_call.lineno)
        if entry_procedure is None:
            raise LyaNameError(proc_call.lineno, proc_call.identifier.name)
        return entry_procedure

    # def raw_type_unary(self, node, op, val):
    #     if hasattr(val, "check_type"):
    #         if op not in val.check_type.unary_ops:
    #             self.error(node.lineno,
    #                   "Unary operator {} not supported".format(op))
    #         return val.check_type

    def _get_binary_integer_side_value(self, side):
        if isinstance(side, IntegerConstant):
            return side.value
        if isinstance(side, Location):
            if isinstance(side.type, Identifier):
                return side.type.synonym_value
        return None

    def _get_binary_boolean_side_value(self, side):
        if isinstance(side, BooleanConstant):
            return side.value
        if isinstance(side, Location):
            if isinstance(side.type, Identifier):
                return side.type.synonym_value
        return None

    def _evaluate_binary_expression(self, operation, left, right):
        """If possible, computes the binary expression.
        Assumes semantic analysis was made
        :param operation:
        :param left:
        :param right:
        :return:
        """
        raw_type = left.raw_type
        exp_value = None

        if isinstance(raw_type, LyaIntType):
            left_val = self._get_binary_integer_side_value(left)
            right_val = self._get_binary_integer_side_value(right)
            if left_val is not None and right_val is not None:
                exp_value = eval("{0}{1}{2}".format(left_val, operation, right_val))

        # TODO: Ref binary op.

        return raw_type, exp_value


    def _evaluate_relational_expression(self, operation, left, right):
        """If possible, computes the relational expression.
        Assumes semantic analysis was made
        :param operation:
        :param left:
        :param right:
        :return:
        """
        raw_type = left.raw_type
        exp_value = None

        if isinstance(raw_type, LyaBoolType):
            left_val = self._get_binary_boolean_side_value(left)
            right_val = self._get_binary_boolean_side_value(right)
            if left_val is not None and right_val is not None:
                exp_value = eval("{0}{1}{2}".format(left_val, operation, right_val))

        # TODO: Ref binary op.

        return raw_type, exp_value

    # def raw_type_binary(self, node, op, left, right):
    #     if hasattr(left, "check_type") and hasattr(right, "check_type"):
    #         if left.check_type != right.check_type:
    #             self.error(node.lineno,
    #             "Binary operator {} does not have matching types".format(op))
    #             return left.check_type
    #         errside = None
    #         if op not in left.check_type.binary_ops:
    #             errside = "LHS"
    #         if op not in right.check_type.binary_ops:
    #             errside = "RHS"
    #         if errside is not None:
    #             self.error(node.lineno,
    #                   "Binary operator {} not supported on {} of expression".format(op, errside))
    #     return left.check_type

    # Program ----------------------------------------------------------------------------------------------------------

    def visit_Program(self, program: Program):
        self.environment.start_new_scope(program)
        for statement in program.statements:
            self.visit(statement)
        self.environment.end_current_scope()

    # Statement --------------------------------------------------------------------------------------------------------

    def visit_Declaration(self, declaration: Declaration):
        self.visit(declaration.mode)
        self.visit(declaration.init)
        if declaration.init is not None:
            if declaration.mode.raw_type != declaration.init.raw_type:
                raise LyaAssignmentError(declaration.ids[0].lineno,
                                         declaration.init.raw_type,
                                         declaration.mode.raw_type)
            if isinstance(declaration.mode.raw_type, LyaStringType):
                if declaration.mode.raw_type.memory_size < declaration.init.raw_type.memory_size:
                    raise LyaGenericError(declaration.ids[0].lineno,
                                          declaration,
                                          "Initializing chars[{0}] "
                                          "with string[{1}] {2}.".format(declaration.mode.raw_type.memory_size,
                                                                         declaration.init.raw_type.memory_size,
                                                                         declaration.init.exp_value))

            # TODO: Array Initialization?

        for identifier in declaration.ids:
            identifier.raw_type = declaration.mode.raw_type
            # identifier.memory_size = declaration.mode.memory_size
            self.current_scope.add_declaration(identifier, declaration)

    def visit_SynonymStatement(self, node):
        for syn in node.synonyms:
            self.visit(syn)

    def visit_SynonymDefinition(self, synonym: SynonymDefinition):
        self.visit(synonym.expression)

        if synonym.expression.exp_value is None:
            raise LyaGenericError(synonym.identifiers[0].lineno,
                                  synonym, "Unable to resolve synonym definition expression at compile time.")

        if synonym.mode is not None:
            self.visit(synonym.mode)
            if synonym.mode.raw_type != synonym.expression.raw_type:
                raise LyaAssignmentError(synonym.identifiers[0].lineno,
                                         synonym.expression.raw_type,
                                         synonym.mode.raw_type)

        synonym.raw_type = synonym.expression.raw_type

        for identifier in synonym.identifiers:
            identifier.raw_type = synonym.raw_type
            identifier.synonym_value = synonym.expression.exp_value
            self.current_scope.add_synonym(identifier, synonym)

    def visit_NewModeStatement(self, node):
        for new_mode in node.new_modes:
            self.visit(new_mode)

    # Procedure --------------------------------------------------------------------------------------------------------

    def visit_ProcedureStatement(self, procedure: ProcedureStatement):
        self.current_scope.add_procedure(procedure.identifier, procedure)
        self.environment.start_new_scope(procedure)

        procedure.start_label = self.environment.generate_label()
        procedure.end_label = self.environment.generate_label()

        definition = procedure.definition
        parameters = definition.parameters
        result = definition.result
        statements = definition.statements

        ret = Identifier("_ret")
        ret.raw_type = LTF.void_type()
        ret.qualifier = QualifierType.none

        if result is not None:
            self.visit(result)
            ret.raw_type = result.raw_type
            ret.qualifier = result.loc

        self.current_scope.add_return(ret)

        procedure.identifier.raw_type = ret.raw_type
        procedure.identifier.qualifier = ret.qualifier

        for p in parameters:
            self.visit(p)
        for s in statements:
            self.visit(s)

        ret.displacement = self.current_scope.parameters_displacement

        self.environment.end_current_scope()

    def visit_FormalParameter(self, parameter: FormalParameter):
        self.visit(parameter.spec)
        parameter.raw_type = parameter.spec.mode.raw_type
        for identifier in parameter.ids:
            identifier.raw_type = parameter.spec.mode.raw_type
            # TODO: Calculate memory size for string/arrays
            identifier.memory_size = parameter.spec.mode.memory_size
            identifier.qualifier = parameter.spec.loc
            self.current_scope.add_parameter(identifier, parameter)

    def visit_ProcedureCall(self, call: ProcedureCall):
        for parameter in call.expressions:
            self.visit(parameter)

        procedure = self._lookup_procedure(call)
        procedure_definition = procedure.definition
        call.raw_type = procedure.identifier.raw_type
        call.scope_level = procedure.scope.level
        call.start_label = procedure.start_label
        # TODO: E loc?

        procedure_parameters_ids = []
        for p in procedure_definition.parameters:
            procedure_parameters_ids += p.ids

        n_procedure_parameters = len(procedure_parameters_ids)
        n_call_parameters = len(call.expressions)

        if n_procedure_parameters != n_call_parameters:
            raise LyaProcedureCallError(call.lineno, call.identifier.name, None,
                                        n_call_parameters, n_procedure_parameters)

        for i in range(n_call_parameters):
            expression = call.expressions[i]
            parameter_id = procedure_parameters_ids[i]

            if parameter_id.raw_type != expression.raw_type:
                raise LyaArgumentTypeError(call.lineno, call.identifier.name, i,
                                           expression.raw_type, parameter_id.raw_type)

            if parameter_id.qualifier is QualifierType.location:
                if not isinstance(expression, Location):
                    #TODO raise error about not passing a variable as parameter
                    pass

                expression.sub_expression.type.qualifier = QualifierType.ref_location


    def visit_ResultSpec(self, spec: ResultSpec):
        self.visit(spec.mode)
        spec.raw_type = spec.mode.raw_type

    def visit_ReturnAction(self, return_action: ReturnAction):
        if return_action.expression is not None and self.current_scope.ret.raw_type != LTF.void_type():
            # TODO: Returning on void function
            pass
        self.visit(return_action.expression)
        self.current_scope.add_result(return_action.lineno, return_action.expression)
        return_action.displacement = self.current_scope.parameters_displacement

    def visit_ResultAction(self, result: ResultAction):
        if self.current_scope.ret.raw_type == LTF.void_type():
            raise LyaGenericError(result.lineno, result, "Error setting a result on void return function.")

        self.visit(result.expression)

        if isinstance(result.expression.sub_expression, Location):
            result.expression.sub_expression.type.qualifier = self.current_scope.ret.qualifier

        self.current_scope.add_result(result.expression, result.lineno)
        result.displacement = self.current_scope.parameters_displacement

    def visit_BuiltinCall(self, builtin_call: BuiltinCall):
        n = len(builtin_call.expressions)
        if n != 1 and builtin_call.name != 'print':
            raise LyaProcedureCallError(builtin_call.lineno, builtin_call.name, None, n, 1)

        for exp in builtin_call.expressions:
            self.visit(exp)

        name = builtin_call.name
        expression = builtin_call.expressions[0]

        if name == 'print':
            if not isinstance(expression.raw_type, LyaArrayType) \
                    and not isinstance(expression.raw_type, LyaStringType) \
                    and not expression.raw_type.memory_size == 1:
                raise LyaGenericError(builtin_call.lineno, BuiltinCall,
                                      "Unsupported read() builtin call.")
            builtin_call.raw_type = LTF.void_type()

        if name == 'read':
            if not isinstance(expression.raw_type, LyaStringType) \
                    and not expression.raw_type.memory_size == 1:
                raise LyaGenericError(builtin_call.lineno, BuiltinCall,
                                      "Unsupported read() builtin call.")
            builtin_call.raw_type = LTF.void_type()

        if name == 'lower' or name == 'upper':
            builtin_call.raw_type = LTF.int_type()
            # TODO: Only accept array?
            if not isinstance(expression.raw_type, LyaArrayType):
                raise LyaArgumentTypeError(builtin_call.lineno, name, 0,
                                           expression.raw_type, 'array')

        if name == 'length':
            builtin_call.raw_type = LTF.int_type()
            if not isinstance(expression.raw_type, LyaArrayType) or not isinstance(expression.raw_type, LyaStringType):
                raise LyaGenericError(builtin_call.lineno, builtin_call,
                                      "Method length() only applies to 'chars' and 'array'. "
                                      "Received '{}'".format(expression.raw_type))
        else:
            # TODO SUCC, PRED, NUM??
            pass

    # Mode -------------------------------------------------------------------------------------------------------------

    def visit_ModeDefinition(self, mode_definition: ModeDefinition):
        self.visit(mode_definition.mode)
        mode_definition.raw_type = mode_definition.mode.raw_type

        for identifier in mode_definition.identifiers:
            identifier.raw_type = mode_definition.raw_type
            self.current_scope.add_new_type(identifier, mode_definition)

    def visit_Mode(self, mode: Mode):
        self.visit(mode.base_mode)
        if isinstance(mode.base_mode, Identifier):
            mode.raw_type = self._lookup_type(mode.base_mode)
        else:
            mode.raw_type = mode.base_mode.raw_type

    def visit_DiscreteMode(self, discrete_mode: DiscreteMode):
        discrete_mode.raw_type = LTF.base_type_from_string(discrete_mode.name)

    # TODO: Visit discrete range mode

    def visit_ReferenceMode(self, reference_mode: ReferenceMode):
        self.visit(reference_mode.mode)

        if reference_mode.mode.raw_type is LyaRefType:
            raise LyaGenericError(reference_mode.lineno, reference_mode, "Unsupported multiple indirection.")
        reference_mode.raw_type = LTF.ref_type(reference_mode.mode.raw_type)
        # TODO: Improve Reference Mode management (Ref RawType + Mode RawType)
        # and comparisons between types

    def visit_StringMode(self, string_mode: StringMode):
        string_mode.raw_type = LTF.string_type(string_mode.length.value)

    def visit_ArrayMode(self, array_mode: ArrayMode):
        array_ranges = []
        self.visit(array_mode.element_mode)

        for index_mode in array_mode.index_modes:
            # array[10]
            self.visit(index_mode)
            if isinstance(index_mode, IntegerConstant):
                if index_mode <= 0:
                    raise LyaGenericError(array_mode.lineno,
                                          array_mode,
                                          "Invalid array mode. "
                                          "Array size must be greater than zero.")
                array_ranges.append((0, index_mode.value - 1))
            elif isinstance(index_mode, LiteralRange):
                if index_mode.lower_bound.exp_value is None:
                    raise LyaGenericError(array_mode.lineno,
                                          array_mode,
                                          "Invalid array mode. "
                                          "Could not infer range lower bound integer value at compilation time.")
                if index_mode.lower_bound.raw_type != LTF.int_type():
                    raise LyaGenericError(array_mode.lineno,
                                          array_mode,
                                          "Invalid array mode. Invalid range lower bound type. "
                                          "Received '{0}'. Expected '{1}'.".format(index_mode.lower_bound.raw_type,
                                                                                   LTF.int_type()))
                lb = index_mode.lower_bound.exp_value

                if index_mode.upper_bound.exp_value is None:
                    raise LyaGenericError(array_mode.lineno,
                                          array_mode,
                                          "Invalid array mode. "
                                          "Could not infer range upper bound integer value at compilation time.")
                if index_mode.upper_bound.raw_type != LTF.int_type():
                    raise LyaGenericError(array_mode.lineno,
                                          array_mode,
                                          "Invalid array mode. Invalid range upper bound type. "
                                          "Received '{0}'. Expected '{1}'.".format(index_mode.lower_bound.raw_type,
                                                                                   LTF.int_type()))
                ub = index_mode.upper_bound.exp_value

                # TODO: Validate lb and ub. (Size > 0. lb can be bigger than ub??)

                array_ranges.append((lb, ub))
            else:
                raise LyaGenericError(array_mode.lineno,
                                      array_mode,
                                      "Invalid array index_mode {0}.".format(array_mode.index_modes));

        array_mode.raw_type = LTF.array_type(array_mode.element_mode.raw_type, array_ranges)

    # Location ---------------------------------------------------------------------------------------------------------

    def visit_Location(self, location: Location):
        self.visit(location.type)
        if isinstance(location.type, Identifier):
            self._lookup_identifier(location.type)
            # identifier = self._lookup_identifier(location.type)
        location.raw_type = location.type.raw_type

    def visit_DereferencedReference(self, dereferenced_reference: DereferencedReference):
        self.visit(dereferenced_reference.loc)

        if not isinstance(dereferenced_reference.loc.raw_type, LyaRefType):
            raise LyaTypeError(dereferenced_reference.lineno, dereferenced_reference.loc.raw_type,
                               LyaRefType._name)

        dereferenced_reference.raw_type = dereferenced_reference.loc.raw_type.referenced_type

    def visit_ReferencedLocation(self, referenced_location: ReferencedLocation):
        self.visit(referenced_location.loc)
        referenced_location.raw_type = LTF.ref_type(referenced_location.loc.raw_type)

    def visit_Element(self, element: Element):
        # TODO: More levels?
        self.visit(element.location)
        element.raw_type = element.location.raw_type
        for expression in element.expressions:
            self.visit(expression)
            if expression.raw_type != LTF.int_type():
                raise LyaTypeError(element.lineno, expression.raw_type, LTF.int_type())

        if isinstance(element.location, Identifier):
            self._lookup_identifier(element.location)
        else:
            self.visit(element.location)

        depth = len(element.expressions)

        if isinstance(element.location.raw_type, LyaStringType):
            # StringElement only reduced from identifier (not loc)
            # TODO: Check-n-raise
            if depth != 1:
                # StringElement doesn't suport multiple indexes.
                raise LyaGenericError(element.lineno, element, "StringElement doesn't support multiple indexes.")
            element.raw_type = LyaStringType(1)
        elif isinstance(element.location.raw_type, LyaArrayType):
            raw_type = element.location.raw_type.get_referenced_type(depth)
            if raw_type is None:
                raise LyaGenericError(element.lineno, element, "Array '{0}' out of range index "
                                                               "depth ({1}) access.".format(element.location.raw_type,
                                                                                            depth))
            element.raw_type = raw_type
        else:
            raise LyaGenericError(element.lineno, element, "Unsupported element location "
                                                           "type '{0}'.".format(element.location.raw_type))


    # Expression -------------------------------------------------------------------------------------------------------

    def visit_Expression(self, expression: Expression):
        self.visit(expression.sub_expression)
        expression.raw_type = expression.sub_expression.raw_type
        if isinstance(expression.sub_expression, Constant):
            expression.exp_value = expression.sub_expression.value
        if isinstance(expression.sub_expression, Expression):
            expression.exp_value = expression.sub_expression.exp_value
        if isinstance(expression.sub_expression, Location):
            if isinstance(expression.sub_expression.type, Identifier):
                expression.exp_value = expression.sub_expression.type.synonym_value

    def visit_BooleanExpression(self, boolean_expression: BooleanExpression):
        self.visit(boolean_expression.sub_expression)
        if boolean_expression.sub_expression.raw_type != LTF.bool_type():
            # TODO: BooleanExpression lineno?
            pass
            # raise LyaTypeError(-1, boolean_expression.sub_expression.raw_type, LTF.bool_type())

    def visit_BinaryExpression(self, binary_expression: BinaryExpression):
        self.visit(binary_expression.left)
        self.visit(binary_expression.right)

        op = binary_expression.operation
        left = binary_expression.left
        right = binary_expression.right

        if left.raw_type != right.raw_type:
            raise LyaOperationError(binary_expression.lineno, op, left.raw_type, right.raw_type)

        if op not in left.raw_type.binary_ops:
            raise LyaOperationError(binary_expression.lineno, op, left_type=left.raw_type)

        if op not in right.raw_type.binary_ops:
            raise LyaOperationError(binary_expression.lineno, op, right_type=right.raw_type)

        raw_type, exp_value = self._evaluate_binary_expression(op, left, right)
        binary_expression.raw_type = raw_type
        binary_expression.exp_value = exp_value

    def visit_RelationalExpression(self, relational_expression: RelationalExpression):
        self.visit(relational_expression.l_value)
        self.visit(relational_expression.r_value)

        op = relational_expression.op
        left = relational_expression.l_value
        right = relational_expression.r_value

        if left.raw_type != right.raw_type:
            raise LyaOperationError(relational_expression.lineno, op, left.raw_type, right.raw_type)

        if op not in left.raw_type.relational_ops:
            raise LyaOperationError(relational_expression.lineno, op, left_type=left.raw_type)

        if op not in right.raw_type.relational_ops:
            raise LyaOperationError(relational_expression.lineno, op, right_type=right.raw_type)

        raw_type, exp_value = self._evaluate_relational_expression(op, left, right)
        relational_expression.raw_type = LTF.bool_type()
        relational_expression.exp_value = exp_value

    def visit_UnaryExpression(self, unary_expression):
        value = unary_expression.value
        op = unary_expression.op

        self.visit(value)

        # Make sure that the operation is supported by the type
        if op not in value.raw_type.unary_ops:
            raise LyaOperationError(unary_expression.lineno, op, left_type=value.raw_type)

        # raw_type = self.raw_type_unary(unary_expression, unary_expression.op, unary_expression.expr)
        # Set the result type to the same as the operand
        unary_expression.raw_type = value.raw_type

    # Action -----------------------------------------------------------------------------------------------------------

    def visit_LabeledAction(self, labeled_action: LabeledAction):
        labeled_action.label = self.environment.add_label(labeled_action.name)
        self.visit(labeled_action.action)

    # def visit_Action(self, action: Action):

    # def visit_BracketedAction(self, bracketed_action: BracketedAction):

    def visit_AssignmentAction(self, assignment: AssignmentAction):
        self.visit(assignment.location)

        if isinstance(assignment.location.type, ProcedureCall):
            procedure_call = assignment.location.type
            procedure_statement = self._lookup_procedure(procedure_call)

            if procedure_statement.definition.result.loc != QualifierType.ref_location:
                raise LyaGenericError(assignment.lineno, assignment,
                                      "Atributing result to non-LOC function call.")

        self.visit(assignment.expression)

        # TODO: Array (array <- array?), ArrayElement, Slices, Strings... other locs

        if assignment.location.raw_type != assignment.expression.raw_type:
            raise LyaTypeError(assignment.lineno, assignment.expression.raw_type, assignment.location.raw_type)

        # TODO: Checar se cabe no location (mem_size)
        # TODO: Checar ranges respeitados? FAz sentido?

    # IfAction ---------------------------------------------------------------------------------------------------------

    def visit_IfAction(self, if_action: IfAction):
        self.visit(if_action.boolean_expression)
        if_action.next_label = self.environment.generate_label()
        self.visit(if_action.then_clause)
        if if_action.else_clause is not None:
            if_action.exit_label = self.environment.generate_label()
            if isinstance(if_action.else_clause, ElsIfClause):
                if_action.else_clause.exit_label = if_action.exit_label
            if_action.else_clause.label = if_action.next_label
            self.visit(if_action.else_clause)

    def visit_ElsIfClause(self, else_if_clause: ElsIfClause):
        self.visit(else_if_clause.boolean_expression)
        self.visit(else_if_clause.then_clause)
        if else_if_clause.else_clause is not None:
            else_if_clause.next_label = self.environment.generate_label()
            if isinstance(else_if_clause.else_clause, ElsIfClause):
                else_if_clause.else_clause.exit_label = else_if_clause.exit_label
            else_if_clause.else_clause.label = else_if_clause.next_label
            self.visit(else_if_clause.else_clause)

    # Do_Action --------------------------------------------------------------------------------------------------------

    def visit_DoAction(self, do_action: DoAction):
        do_action.start_label = self.environment.generate_label()
        self.visit(do_action.control)
        if do_action.control.while_control is not None:
            do_action.end_label = self.environment.generate_label()
        for action in do_action.actions:
            self.visit(action)

    # def visit_ForControl(self, for_control: ForControl):
    #     self.visit(for_control.iteration)

    def visit_StepEnumeration(self, step: StepEnumeration):
        self._lookup_identifier(step.identifier)

        if step.identifier.raw_type != LTF.int_type():
            raise LyaTypeError(step.lineno, step.identifier.raw_type, LTF.int_type())

        self.visit(step.start_expression)
        if step.start_expression.raw_type != LTF.int_type():
            raise LyaTypeError(step.lineno, step.start_expression.raw_type, LTF.int_type())

        if step.step_expression is not None:
            self.visit(step.step_expression)
            if step.step_expression.sub_expression.raw_type != LTF.int_type():
                raise LyaTypeError(step.lineno, step.step_expression.sub_expression.raw_type, LTF.int_type())

        self.visit(step.end_expression)
        if step.end_expression.raw_type != LTF.int_type():
            raise LyaTypeError(step.lineno, step.end_expression.raw_type, LTF.int_type())

    def visit_RangeEnumeration(self, range_enum: RangeEnumeration):
        entry = self.current_scope.entry_lookup(range_enum.counter)

        if entry is None:
            raise LyaNameError(range_enum.lineno, range_enum.counter)

        self.visit(range_enum.mode)

    def visit_WhileControl(self, while_control: WhileControl):
        self.visit(while_control.boolean_expression)
        if while_control.boolean_expression.sub_expression.raw_type != LTF.bool_type():
            raise LyaTypeError(while_control.lineno,
                               while_control.boolean_expression.sub_expression.raw_type,
                               LTF.bool_type())

    # Exit Action

    def visit_ExitAction(self, exit_action: ExitAction):
        # TODO: Check if can exit to label?
        label = self.environment.lookup_label(exit_action.name)
        if label is None:
            raise LyaNameError(exit_action.lineno, label.name)
        exit_action.exit_label = label

    # Constants / Literals

    def visit_IntegerConstant(self, iconst: IntegerConstant):
        iconst.raw_type = LTF.int_type()

    def visit_BooleanConstant(self, bconst: BooleanConstant):
        bconst.raw_type = LTF.bool_type()

    def visit_CharacterConstant(self, cconst: CharacterConstant):
        cconst.raw_type = LTF.char_type()

    def visit_EmptyConstant(self, econst: EmptyConstant):
        econst.raw_type = LTF.void_type()

    def visit_StringConstant(self, sconst: StringConstant):
        sconst.heap_position = self.environment.store_string_constant(sconst.value)
        sconst.raw_type = LTF.string_type(sconst.length)
