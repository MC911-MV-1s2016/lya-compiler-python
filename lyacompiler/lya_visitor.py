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
        identifier.memory_size = entry_identifier.memory_size
        identifier.scope_level = entry_identifier.scope_level
        identifier.displacement = entry_identifier.displacement
        identifier.start = entry_identifier.start
        identifier.stop = entry_identifier.stop
        identifier.qual_type = entry_identifier.qual_type
        return entry_identifier

    def _lookup_procedure(self, proc_call: ProcCall):
        entry_procedure = self.current_scope.procedure_lookup(proc_call.name, proc_call.lineno)
        if entry_procedure is None:
            raise LyaNameError(proc_call.lineno, proc_call.name)
        return entry_procedure

    # def raw_type_unary(self, node, op, val):
    #     if hasattr(val, "check_type"):
    #         if op not in val.check_type.unary_ops:
    #             self.error(node.lineno,
    #                   "Unary operator {} not supported".format(op))
    #         return val.check_type
    #
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

    def visit_Program(self, program: Program):
        self.environment.start_new_scope(program)
        for statement in program.statements:
            self.visit(statement)
        self.environment.end_current_scope()

    # Statement -------------------------------------------------

    def visit_Declaration(self, declaration: Declaration):
        self.visit(declaration.mode)
        self.visit(declaration.init)
        if declaration.init is not None:
            if declaration.mode.raw_type != declaration.init.raw_type:
                raise LyaAssignmentError(declaration.ids[0].lineno,
                                         declaration.init.raw_type,
                                         declaration.mode.raw_type)
        # TODO: Check if string init fits.
        for identifier in declaration.ids:
            identifier.raw_type = declaration.mode.raw_type
            # TODO: Calculate string/array size.
            # Can init array/string? Check mem size.
            identifier.memory_size = declaration.mode.memory_size
            self.current_scope.add_declaration(identifier, declaration)

    def visit_SynonymStatement(self, node):
        # TODO: Visit/decorate SynonymDef
        for syn in node.synonyms:
            self.visit(syn)

    def visit_NewModeStatement(self, node):
        for new_mode in node.new_modes:
            self.visit(new_mode)

    # Procedure ------------------------------------------

    def visit_ProcedureStatement(self, procedure: ProcedureStatement):
        self.current_scope.add_procedure(procedure.label, procedure)
        self.environment.start_new_scope(procedure)

        definition = procedure.definition
        parameters = definition.parameters
        result = definition.result
        statements = definition.statements

        ret = Identifier("_ret")
        ret.raw_type = VoidType
        ret.qual_type = IDQualType.none

        if result is not None:
            self.visit(result)
            ret.raw_type = result.raw_type
            ret.qual_type = result.qual_type

        self.current_scope.add_return(ret)

        procedure.label.raw_type = ret.raw_type

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
            identifier.qual_type = parameter.spec.loc
            self.current_scope.add_parameter(identifier, parameter)

    def visit_ProcCall(self, call: ProcCall):
        for p in call.params:
            self.visit(p)

        proc_node = self._lookup_procedure(call)

        if len(call.params) != len(proc_node.definition.parameters):
            raise LyaProcedureCallError(call.lineno, call.name, None, len(call.params), len(proc_node.definition.parameters))

        for i in range(len(call.params)):
            a = call.params[i]
            p = proc_node.definition.parameters[i]

            if p.raw_type != a.raw_type:
                raise LyaArgumentTypeError(call.lineno, call.name, i, a.raw_type, p.raw_type)


    # Mode

    def visit_Mode(self, mode: Mode):
        self.visit(mode.base_mode)
        # TODO: If base_mode is Identifier (mode_name), check if defined as type
        mode.raw_type = mode.base_mode.raw_type

    def visit_DiscreteMode(self, discrete_mode: DiscreteMode):
        discrete_mode.raw_type = LyaType.from_string(discrete_mode.name)

    def visit_ReferenceMode(self, reference_mode: ReferenceMode):
        self.visit(reference_mode.mode)
        # TODO: Improve Reference Mode management (Ref RawType + Mode RaType)

    def visit_CompositeMode(self, composite_mode: CompositeMode):
        self.visit(composite_mode.mode)
        # TODO: Improve Array/String Type (size and raw type)
        if isinstance(composite_mode.mode, StringMode):
            composite_mode.raw_type = StringType
        elif isinstance(composite_mode.mode, ArrayMode):
            composite_mode.raw_type = ArrayType

    # Location

    def visit_Location(self, location: Location):
        self.visit(location.type)
        if isinstance(location.type, Identifier):
            ident = self._lookup_identifier(location.type)
        location.raw_type = location.type.raw_type

    # Expression

    def visit_Expression(self, expression: Expression):
        self.visit(expression.sub_expression)
        expression.raw_type = expression.sub_expression.raw_type

    # Constans / Literals

    def visit_IntegerConstant(self, iconst: IntegerConstant):
        iconst.raw_type = IntType

    def visit_BooleanConstant(self, bconst: BooleanConstant):
        bconst.raw_type = BoolType

    def visit_CharacterConstant(self, cconst: CharacterConstant):
        cconst.raw_type = CharType

    def visit_EmptyConstant(self, econst: EmptyConstant):
        econst.raw_type = VoidType

    def visit_StringConstant(self, sconst: StringConstant):
        sconst.raw_type = StringType

    # def visit_UnaryExpr(self, node):
    #     self.visit(node.expr)
    #     # Make sure that the operation is supported by the type
    #     raw_type = self.raw_type_unary(node, node.op, node.expr)
    #     # Set the result type to the same as the operand
    #     node.raw_type = raw_type

    # def visit_BinaryExpr(self,node):
    #     # Make sure left and right operands have the same type
    #     # Make sure the operation is supported
    #     self.visit(node.left)
    #     self.visit(node.right)
    #     raw_type = self.raw_type_binary(node, node.op, node.left, node.right)
    #     # Assign the result type
    #     node.raw_type = raw_type
