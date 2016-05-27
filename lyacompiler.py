#!/usr/bin/env python3
# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lyacompiler.py
#
# ------------------------------------------------------------


class LyaCompiler(object):

    modes = {
        "-d": "_debug",
        "-i": "_interactive",
        "-f": "_file",
        "-l": "_lya",
        "-e": "_examples",
        "-t": "_test",
        "-h": "_help"
    }

    help = {
        "-d": """Debug mode.Runs lya_debug_source code.\n\t\tUsage:   $ python3 lyacompiler.py -d""",
        "-i": """Interactive mode. Not implemented.""",
        "-f": """Source file mode. Loads lya source from file.\n\t\tUsage:   $ python3 lyacompiler.py -f <lya_source.lya>""",
        "-l": """Lya raw source mode. Not implemented.""",
        "-e": """Examples mode. Lists all available lya source files.\n\t\tUsage:   $ python3 lyacompiler.py -e""",
        "-t": """Test mode. Not implemented.""",
        "-h": """Help mode. Lists all available modes.\n\t\tUsage:   $ python3 lyacompiler.py -h"""
    }

    def __init__(self):
        pass

    def compile(self, args):

        if len(args) == 0:
            m = '-h'
        else:
            m = args[0]

        mode_method_name = "{0}_mode".format(self.modes.get(m, "_invalid"))
        mode_method = getattr(self.modes, mode_method_name, self._invalid_mode)
        mode_method(args)

    # Private

    def _compile(self, source_code: str):
        from lyacompiler.lyaparser import LyaParser
        from lyacompiler.lyavisitor import Visitor

        # Generating AST
        parser = LyaParser()
        ast = parser.parse(source_code)

        # Semantic Analysis
        semantic_visitor = Visitor()
        semantic_visitor.visit(ast)
        semantic_visitor.show(ast)

        # TODO: Code Generation Visitor

    def _debug_mode(self, args):
        pass

    def _interactive_mode(self, args):
        # TODO: Loop reading from input
        print("Interactive mode not implemented.")

    def _source_file_mode(self, args):
        pass

    def _lya_source_mode(self, args):
        pass

    def _examples_mode(self, args):
        # TODO: List all files in lyacompiler/lyaexamples
        pass

    def _run_tests_mode(self, args):
        print("Test mode not implemented.")
        pass

    def _help_mode(self):
        print("Available modes:")
        for key, value in self.modes.items():
            print("\t{0}: {1}".format(key, value))

    def _invalid_mode(self):
        print("Invalid mode")
        self._help_mode()

if __name__ == '__main__':

    import sys

    compiler = LyaCompiler()
    compiler.compile(sys.argv[1:])
