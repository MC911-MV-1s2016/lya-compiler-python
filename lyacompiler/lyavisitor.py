# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lyavisitor.py
# Lya AST Nodes Visitor
#
# ------------------------------------------------------------

from .astnodevisitor import ASTNodeVisitor
from .lyaenvironment import Environment
from .lya_ast import *
from .lya_errors import *
from .lya_builtins import *


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
            print(bcolors.WARNING + str(err) + bcolors.ENDC)
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
        program.offset = self.current_scope.locals_displacement
        self.environment.end_current_scope()

    def visit_Declaration(self, declaration: Declaration):
        self.visit(declaration.mode)
        self.visit(declaration.init)
        # TODO: Check if init expression matches mode.
        # Check type
        # Can init array/string? Check mem size.
        for identifier in declaration.ids:
            identifier.raw_type = declaration.mode.raw_type
            # TODO: Calculate string/array size.
            identifier.memory_size = declaration.mode.memory_size
            self.current_scope.add_declaration(identifier, declaration)

    def visit_SynonymStatement(self, node):
        for syn in node.synonyms:
            self.visit(syn)

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

        for identifier in parameter.ids:
            identifier.raw_type = parameter.spec.mode.raw_type
            # TODO: Calculate memory size for string/arrays
            identifier.memory_size = parameter.spec.mode.memory_size
            identifier.qual_type = parameter.spec.loc
            self.current_scope.add_parameter(identifier, parameter)

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
