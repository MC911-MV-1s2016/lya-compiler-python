# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# symboltable.py
# Symbol Table.
#
# ------------------------------------------------------------


class SymbolTable(dict):
    """
    Class representing a symbol table. It should
    provide functionality for adding and looking
    up nodes associated with identifiers.
    """
    def __init__(self, enclosure=None):
        super().__init__()
        self.enclosure = enclosure

    def add(self, name, value):
        self[name] = value

    def lookup(self, name):
        return self.get(name, None)

    def return_type(self):
        if self.enclosure:
            return self.enclosure.mode
        return None
