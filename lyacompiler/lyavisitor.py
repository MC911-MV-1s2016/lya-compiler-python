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

# from lyacompiler.astnodevisitor import ASTNodeVisitor
# from lyacompiler.lyaenvironment import Environment
# from lyacompiler.lya_ast import *

from astnodevisitor import ASTNodeVisitor
from lyaenvironment import Environment
from lya_ast import *


class Visitor(ASTNodeVisitor):
    """
    Program Visitor class. This class uses the visitor pattern as
    described in lya_ast.py.   It’s define methods of the form
    visit_NodeName() for each kind of AST node that we want to process.
    Note: You will need to adjust the names of the AST nodes if you
    picked different names.
    """
    def __init__(self):
        super().__init__()
        self.environment = Environment()

    # Private

    # TODO: RawType Mode
    # TODO: TypeChecker Class
    def _raw_type_id(self, id):
        name = "int"
        t = self.environment.raw_type(name)
        if t is None:
            # TODO: Define and raise Undefined/Unrecognized Type Exception (name)
            # TODO: Error function
            raise TypeError
        return t

    def _declare_type(self, name, type):
        pass

    # def error(self, a, b):
    #     pass
    #
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



    # def visit_Program(self, node, depth):
    #     self.environment.push(node)
    #     node.environment = self.environment
    #     node.symtab = self.environment.peek()
    #     # Visit all of the statements
    #     for statement in node.statements:
    #         self.visit(statement, depth)

    def visit_Program(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        for stmts in node.statements:
            self.visit(stmts)

    def visit_Declaration(self, node):
        for id in node.ids:
            # TODO: Check init type == mode.raw_type
            id.scope = self.environment.scope_level()
            id.declaration = node
            id.displacement = len(self.environment.peek())
            self.environment.add_local(id.name, id)

    def visit_SynonymStatement(self, node):
        for syn in node.synonyms:
            self.visit(syn)

    # def visit_SynonymStatement(self, node, level):
    #     # Visit all of the synonyms
        # for syn in node.syns:
        #     self.visit(syn)

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
# def decorate_DeclarationStatement(self, node):
    #     node.environment.add_local(node.i)
    #     pass

    # def decorate_Identifier(self, node):
    #     node.displacement = 1
