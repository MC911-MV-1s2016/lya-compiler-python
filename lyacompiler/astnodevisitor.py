#!/usr/bin/env python3
# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# astnodevisistor.py
# AST Generic Node Visitor
#
# ------------------------------------------------------------

from .lya_ast import ASTNode


class ASTNodeVisitor(object):
    """
    Class for visiting nodes of the parse tree.  This is modeled after
    a similar class in the standard library ast.NodeVisitor.  For each
    node, the visit(node) method calls a method visit_NodeName(node)
    which should be implemented in subclasses.  The generic_visit() method
    is called for all nodes where there is no matching visit_NodeName()
    method.
    Here is a example of a visitor that examines binary operators:
    class VisitOps(NodeVisitor):
        visit_Binop(self,node):
            print("Binary operator", node.op)
            self.visit(node.left)
            self.visit(node.right)
        visit_Unaryop(self,node):
            print("Unary operator", node.op)
            self.visit(node.expr)
    tree = parse(txt)
    VisitOps().visit(tree)
    """
    def __init__(self):
        self._debug_format_cache = dict()

    # Private

    def _generic_visit(self, node):
        """
        Method executed if no applicable visit_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        """
        for field in getattr(node, "_fields"):
            value = getattr(node, field, None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        self.visit(item)
            elif isinstance(value, ASTNode):
                self.visit(value)

    def _format_node_debug(self, node, depth=0, indent=2):
        indent_str = self._debug_format_cache.get(depth)
        if indent_str is None:
            indent_str = ""
            for d in range(depth):
                indent_str += ((" " * indent) + "|")
            indent_str += "- "
            self._debug_format_cache[depth] = indent_str
        return "{0}{1}".format(indent_str, str(node))

    # Public

    def visit(self, node):
        """
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        """
        if node:
            # Visiting node.
            visit_method = 'visit_' + node.class_name
            visitor = getattr(self, visit_method, self._generic_visit)
            return visitor(node)
        else:
            return None

    def show(self, node, depth=-1, indent=2):
        depth += 1
        self.debug_node(node, depth, indent)

        for field in getattr(node, "_fields"):
            value = getattr(node, field, None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        self.show(item, depth, indent)
            elif isinstance(value, ASTNode):
                self.show(value, depth, indent)

    def debug_node(self, node, depth, indent=2):
        if (indent is None) or (node is None):
            return
        print(self._format_node_debug(node, depth, indent))
