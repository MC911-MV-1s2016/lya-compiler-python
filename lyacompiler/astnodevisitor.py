# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# nodevisistor.py
# AST Generic Node Visitor
#
# ------------------------------------------------------------

from lya_ast import ASTNode
# from lyacompiler.lya_ast import ASTNode


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
    def __init__(self, indent=None):
        self._debug_indent = indent
        self._debug_format_cache = dict()

    # Private

    def _generic_visit(self, node, depth=0):
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
                        self.visit(item, depth)
            elif isinstance(value, ASTNode):
                self.visit(value, depth)

    def _format_node_debug(self, node, depth=0):
        indent = self._debug_format_cache.get(depth)
        if indent is None:
            indent = ""
            for d in range(depth):
                indent += ((" " * self._debug_indent) + "|")
            indent += "- "
            self._debug_format_cache[depth] = indent
        return "{0}{1}".format(indent, str(node))

    # Public

    def visit(self, node, depth=-1):
        """
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        """
        if node:
            depth += 1
            self.debug_node(node, depth)
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self._generic_visit)
            return visitor(node, depth)
        else:
            return None

    def debug_node(self, node, depth):
        if self._debug_indent is None:
            return
        print(self._format_node_debug(node, depth))
