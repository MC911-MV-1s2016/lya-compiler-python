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


class ASTNode(object):
    """
    Base class example for the AST nodes.  Each node is expected to
    define the _fields attribute which lists the names of stored
    attributes.   The __init__() method below takes positional
    arguments and assigns them to the appropriate fields.  Any
    additional arguments specified as keywords are also assigned.
    """

    _fields = []
    _indent = 2

    def __init__(self, *args, **kwargs):
        assert len(args) == len(self._fields)

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Assign additional keyword arguments if supplied
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __str__(self):
        debug_data = self.debug_data()
        if debug_data is None:
            return self.name
        return "{0}: {1}".format(self.name, debug_data)

    @property
    def name(self):
        return self.__class__.__name__

    def debug_data(self):
        return None


class Program(ASTNode):
    _fields = ['statements']

    def debug_data(self):
        return "Debug data test"

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
    _fields = ['label', 'definition']


class ActionStatement(Statement):
    _fields = ['label', 'action']


# Declaration


class Declaration(ASTNode):
    _fields = ['ids', 'mode', 'init']


# class Initialization(ASTNode):
#     _fields = ['expression']


class Assignment(ASTNode):
    _fields = ['l_value', 'op', 'r_value']
