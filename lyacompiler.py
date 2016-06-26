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
            args.append('-h')

        m = args[0]

        mode_method_name = "{0}_mode".format(self.modes.get(m, "_invalid"))
        mode_method = getattr(self, mode_method_name, self._invalid_mode)
        mode_method(args[1:])

    # Private

    @staticmethod
    def _compile(source_code: str):

        from lyacompiler.lya_parser import LyaParser
        from lyacompiler.lya_visitor import Visitor
        from lyacompiler.lya_codegen import CodeGenerator
        from  lyacompiler.lya_virtualmachine import LyaVirtualMachine

        print("\n--- Lya Source Code ---\n")
        i = 1
        for line in source_code.split("\n"):
            print("{0}:\t{1}".format(i, line))
            i += 1

        print("\n--- Lya Source Code EOF ---\n")

        # Generating AST
        print("Parsing source code...\n")
        parser = LyaParser()
        ast = parser.parse(source_code)

        # Semantic Analysis
        print("\nAnalysing semantics...")
        semantic_visitor = Visitor()
        semantic_visitor.visit(ast)
        print("\n--- Decorated AST ---\n")
        semantic_visitor.show(ast)
        print("\n--- Decorated AST END ---\n")

        # Code Generation
        print("Generating code...")
        code_generator = CodeGenerator()
        code_generator.environment = ast.environment
        code_generator.visit(ast)
        print("\n--- Generated Code ---\n")
        for i in range(len(code_generator.instructions)):
            instruction = code_generator.instructions[i]
            print("{0}:\t{1}".format(i, str(instruction)))
        print("\n--- Generated Code END ---\n")

        # Program Execution
        print("--- Executing Code ---\n")
        lvm = LyaVirtualMachine()
        lvm.execute(code_generator.instructions,
                    code_generator.labels_map,
                    semantic_visitor.environment.string_constant_heap)
        print("\n--- Code executed ---")

    def _debug_mode(self, args):
        from lyacompiler.lya_debug_source import lya_debug_source
        self._compile(lya_debug_source)

    def _interactive_mode(self, args):
        # TODO: Loop reading from input
        print("Interactive mode not implemented.")

    def _file_mode(self, args):

        if len(args) < 1:
            self._invalid_mode(args)
            return

        file_name = args[0]

        print("Source file mode:")

        file = open(file_name)
        lya_source = file.read()

        self._compile(lya_source)

    def _lya_mode(self, args):
        print("Lya source mode not implemented.")

    def _examples_mode(self, args):
        from glob import glob
        print("Lya Examples:")
        for file_path in glob("./lyacompiler/lyaexamples/*.lya"):
            print("\t'{0}'".format(file_path))

    def _run_tests_mode(self, args):
        print("Test mode not implemented.")
        pass

    def _help_mode(self, args):
        print("Available modes:")
        for key, value in self.help.items():
            print("\t{0}: {1}".format(key, value))

    def _invalid_mode(self, args):
        print("Invalid mode.")
        self._help_mode(args)

if __name__ == '__main__':

    import sys

    compiler = LyaCompiler()
    compiler.compile(sys.argv[1:])
