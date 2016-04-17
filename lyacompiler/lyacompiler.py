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

def compile(source_code):

    import pprint

    from lyaparser import LyaParser

    print("Generating AST")
    parser = LyaParser()
    AST = parser.parse(source_code)
    pprint.pprint(AST, indent=2)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("""
        Invalid cmd...
        Usage:   $ python3 lyacompiler.py <lya_source.lya>
        Example: $ python3 lyacompiler.py ./lyaexamples/armstrong_number.lya
        """)
        exit()

    file_name = sys.argv[1]

    file = open(file_name)
    lya_source = file.read()

    print("Lya Source")
    print(lya_source)

    compile(lya_source)

