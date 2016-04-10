#------------------------------------------------------------------------------
# lyaparser: parser.py
#
# Parser class: Parser and AST builder for the Lya language
#
#------------------------------------------------------------------------------
import re

from .ply import yacc

from . import lya_ast
from .lyalexer import LyaLexer
from .plyparser import PLYParser, Coord, ParseError


class LyaParser(PLYParser):
    def __init__(
            self,
            lex_optimize=True,
            lextab='pylyaparser.lextab',
            yacc_optimize=True,
            yacctab='pylyaparser.yacctab',
            yacc_debug=False,
            taboutputdir=''):
        """ Create a new LyaParser.

            Some arguments for controlling the debug/optimization
            level of the parser are provided. The defaults are
            tuned for release/performance mode.
            The simple rules for using them are:
            *) When tweaking CParser/CLexer, set these to False
            *) When releasing a stable parser, set to True

            lex_optimize:
                Set to False when you're modifying the lexer.
                Otherwise, changes in the lexer won't be used, if
                some lextab.py file exists.
                When releasing with a stable lexer, set to True
                to save the re-generation of the lexer table on
                each run.

            lextab:
                Points to the lex table that's used for optimized
                mode. Only if you're modifying the lexer and want
                some tests to avoid re-generating the table, make
                this point to a local lex table file (that's been
                earlier generated with lex_optimize=True)

            yacc_optimize:
                Set to False when you're modifying the parser.
                Otherwise, changes in the parser won't be used, if
                some parsetab.py file exists.
                When releasing with a stable parser, set to True
                to save the re-generation of the parser table on
                each run.

            yacctab:
                Points to the yacc table that's used for optimized
                mode. Only if you're modifying the parser, make
                this point to a local yacc table file

            yacc_debug:
                Generate a parser.out file that explains how yacc
                built the parsing table from the grammar.

            taboutputdir:
                Set this parameter to control the location of generated
                lextab and yacctab files.
        """
        self.lyalex = LyaLexer(
            error_func=self._lex_error_func,
            on_lbrace_func=self._lex_on_lbrace_func,
            on_rbrace_func=self._lex_on_rbrace_func,
            type_lookup_func=self._lex_type_lookup_func)

        self.lyalex.build(
            optimize=lex_optimize,
            lextab=lextab,
            outputdir=taboutputdir)
        self.tokens = self.lyalex.tokens

        rules_with_opt = [
            'abstract_declarator',
            'assignment_expression',
            'declaration_list',
            'declaration_specifiers',
            'designation',
            'expression',
            'identifier_list',
            'init_declarator_list',
            'initializer_list',
            'parameter_type_list',
            'specifier_qualifier_list',
            'block_item_list',
            'type_qualifier_list',
            'struct_declarator_list'
        ]

        for rule in rules_with_opt:
            self._create_opt_rule(rule)

        self.lyaparser = yacc.yacc(
            module=self,
            start='translation_unit_or_empty',
            debug=yacc_debug,
            optimize=yacc_optimize,
            tabmodule=yacctab,
            outputdir=taboutputdir)

        # Stack of scopes for keeping track of symbols. _scope_stack[-1] is
        # the current (topmost) scope. Each scope is a dictionary that
        # specifies whether a name is a type. If _scope_stack[n][name] is
        # True, 'name' is currently a type in the scope. If it's False,
        # 'name' is used in the scope but not as a type (for instance, if we
        # saw: int name;
        # If 'name' is not a key in _scope_stack[n] then 'name' was not defined
        # in this scope at all.
        self._scope_stack = [dict()]

        # Keeps track of the last token given to yacc (the lookahead token)
        self._last_yielded_token = None

    def parse(self, text, filename='', debuglevel=0):
        """ Parses C code and returns an AST.

            text:
                A string containing the C source code

            filename:
                Name of the file being parsed (for meaningful
                error messages)

            debuglevel:
                Debug level to yacc
        """
        self.lyalex.filename = filename
        self.lyalex.reset_lineno()
        self._scope_stack = [dict()]
        self._last_yielded_token = None
        return self.lyaparser.parse(
                input=text,
                lexer=self.lyalex,
                debug=debuglevel)

    ######################--   PRIVATE   --######################

    def _push_scope(self):
        self._scope_stack.append(dict())

    def _pop_scope(self):
        assert len(self._scope_stack) > 1
        self._scope_stack.pop()

    def _add_identifier(self, name, coord):
        """ Add a new object, function, or enum member name (ie an ID) to the
            current scope
        """
        if self._scope_stack[-1].get(name, False):
            self._parse_error(
                "Non-typedef %r previously declared as typedef "
                "in this scope" % name, coord)
        self._scope_stack[-1][name] = False

    def _is_type_in_scope(self, name):
        """ Is *name* a typedef-name in the current scope?
        """
        for scope in reversed(self._scope_stack):
            # If name is an identifier in this scope it shadows typedefs in
            # higher scopes.
            in_scope = scope.get(name)
            if in_scope is not None: return in_scope
        return False

    def _lex_error_func(self, msg, line, column):
        self._parse_error(msg, self._coord(line, column))

    def _lex_on_lbrace_func(self):
        self._push_scope()

    def _lex_on_rbrace_func(self):
        self._pop_scope()

    def _lex_type_lookup_func(self, name):
        """ Looks up types that were previously defined with
            typedef.
            Passed to the lexer for recognizing identifiers that
            are types.
        """
        is_type = self._is_type_in_scope(name)
        return is_type

    def _get_yacc_lookahead_token(self):
        """ We need access to yacc's lookahead token in certain cases.
            This is the last token yacc requested from the lexer, so we
            ask the lexer.
        """
        return self.lyalex.last_token


    ##
    ## Precedence and associativity of operators
    ##
    precedence = (
        ('left', 'LOR'),
        ('left', 'LAND'),
        ('left', 'OR'),
        ('left', 'XOR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD')
    )

    ##
    ## Grammar productions
    ## Implementation of the BNF defined in K&R2 A.13
    ##

    # In function definitions, the declarator can be followed by
    # a declaration list, for old "K&R style" function definitios.
    #
    def p_function_definition_1(self, p):
        """ function_definition : declarator declaration_list_opt compound_statement
        """
        # no declaration specifiers - 'int' becomes the default type
        spec = dict(
            qual=[],
            storage=[],
            type=[lya_ast.IdentifierType(['int'],
                                       coord=self._coord(p.lineno(1)))],
            function=[])

        p[0] = self._build_function_definition(
            spec=spec,
            decl=p[1],
            param_decls=p[2],
            body=p[3])

    def p_function_definition_2(self, p):
        """ function_definition : declaration_specifiers declarator declaration_list_opt compound_statement
        """
        spec = p[1]

        p[0] = self._build_function_definition(
            spec=spec,
            decl=p[2],
            param_decls=p[3],
            body=p[4])

    def p_statement(self, p):
        """ statement   : labeled_statement
                        | expression_statement
                        | compound_statement
                        | selection_statement
                        | iteration_statement
                        | jump_statement
                        | pppragma_directive
        """
        p[0] = p[1]

    # In C, declarations can come several in a line:
    #   int x, *px, romulo = 5;
    #
    # However, for the AST, we will split them to separate Decl
    # nodes.
    #
    # This rule splits its declarations and always returns a list
    # of Decl nodes, even if it's one element long.
    #
    def p_decl_body(self, p):
        """ decl_body : declaration_specifiers init_declarator_list_opt
        """
        spec = p[1]

        # p[2] (init_declarator_list_opt) is either a list or None
        #
        if p[2] is None:
            # By the standard, you must have at least one declarator unless
            # declaring a structure tag, a union tag, or the members of an
            # enumeration.
            #
            ty = spec['type']
            s_u_or_e = (lya_ast.Struct, lya_ast.Union, lya_ast.Enum)
            if len(ty) == 1 and isinstance(ty[0], s_u_or_e):
                decls = [lya_ast.Decl(
                    name=None,
                    quals=spec['qual'],
                    storage=spec['storage'],
                    funcspec=spec['function'],
                    type=ty[0],
                    init=None,
                    bitsize=None,
                    coord=ty[0].coord)]

            # However, this case can also occur on redeclared identifiers in
            # an inner scope.  The trouble is that the redeclared type's name
            # gets grouped into declaration_specifiers; _build_declarations
            # compensates for this.
            #
            else:
                decls = self._build_declarations(
                    spec=spec,
                    decls=[dict(decl=None, init=None)],
                    typedef_namespace=True)

        else:
            decls = self._build_declarations(
                spec=spec,
                decls=p[2],
                typedef_namespace=True)

        p[0] = decls

    # The declaration has been split to a decl_body sub-rule and
    # SEMI, because having them in a single rule created a problem
    # for defining typedefs.
    #
    # If a typedef line was directly followed by a line using the
    # type defined with the typedef, the type would not be
    # recognized. This is because to reduce the declaration rule,
    # the parser's lookahead asked for the token after SEMI, which
    # was the type from the next line, and the lexer had no chance
    # to see the updated type symbol table.
    #
    # Splitting solves this problem, because after seeing SEMI,
    # the parser reduces decl_body, which actually adds the new
    # type into the table to be seen by the lexer before the next
    # line is reached.
    def p_declaration(self, p):
        """ declaration : decl_body SEMI
        """
        p[0] = p[1]

    # Since each declaration is a list of declarations, this
    # rule will combine all the declarations and return a single
    # list
    #
    def p_declaration_list(self, p):
        """ declaration_list    : declaration
                                | declaration_list declaration
        """
        p[0] = p[1] if len(p) == 2 else p[1] + p[2]

    def p_declaration_specifiers_1(self, p):
        """ declaration_specifiers  : type_qualifier declaration_specifiers_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'qual')

    def p_declaration_specifiers_2(self, p):
        """ declaration_specifiers  : type_specifier declaration_specifiers_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'type')

    def p_declaration_specifiers_3(self, p):
        """ declaration_specifiers  : storage_class_specifier declaration_specifiers_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'storage')

    def p_declaration_specifiers_4(self, p):
        """ declaration_specifiers  : function_specifier declaration_specifiers_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'function')

    def p_storage_class_specifier(self, p):
        """ storage_class_specifier : AUTO
                                    | REGISTER
                                    | STATIC
                                    | EXTERN
                                    | TYPEDEF
        """
        p[0] = p[1]

    def p_function_specifier(self, p):
        """ function_specifier  : INLINE
        """
        p[0] = p[1]

    def p_type_specifier_1(self, p):
        """ type_specifier  : VOID
                            | _BOOL
                            | CHAR
                            | SHORT
                            | INT
                            | LONG
                            | FLOAT
                            | DOUBLE
                            | _COMPLEX
                            | SIGNED
                            | UNSIGNED
        """
        p[0] = lya_ast.IdentifierType([p[1]], coord=self._coord(p.lineno(1)))

    def p_type_specifier_2(self, p):
        """ type_specifier  : typedef_name
                            | enum_specifier
                            | struct_or_union_specifier
        """
        p[0] = p[1]

    def p_type_qualifier(self, p):
        """ type_qualifier  : CONST
                            | RESTRICT
                            | VOLATILE
        """
        p[0] = p[1]

    def p_init_declarator_list_1(self, p):
        """ init_declarator_list    : init_declarator
                                    | init_declarator_list COMMA init_declarator
        """
        p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

    # If the code is declaring a variable that was declared a typedef in an
    # outer scope, yacc will think the name is part of declaration_specifiers,
    # not init_declarator, and will then get confused by EQUALS.  Pass None
    # up in place of declarator, and handle this at a higher level.
    #
    def p_init_declarator_list_2(self, p):
        """ init_declarator_list    : EQUALS initializer
        """
        p[0] = [dict(decl=None, init=p[2])]

    # Similarly, if the code contains duplicate typedefs of, for example,
    # array types, the array portion will appear as an abstract declarator.
    #
    def p_init_declarator_list_3(self, p):
        """ init_declarator_list    : abstract_declarator
        """
        p[0] = [dict(decl=p[1], init=None)]

    # Returns a {decl=<declarator> : init=<initializer>} dictionary
    # If there's no initializer, uses None
    #
    def p_init_declarator(self, p):
        """ init_declarator : declarator
                            | declarator EQUALS initializer
        """
        p[0] = dict(decl=p[1], init=(p[3] if len(p) > 2 else None))

    def p_specifier_qualifier_list_1(self, p):
        """ specifier_qualifier_list    : type_qualifier specifier_qualifier_list_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'qual')

    def p_specifier_qualifier_list_2(self, p):
        """ specifier_qualifier_list    : type_specifier specifier_qualifier_list_opt
        """
        p[0] = self._add_declaration_specifier(p[2], p[1], 'type')

    # TYPEID is allowed here (and in other struct/enum related tag names), because
    # struct/enum tags reside in their own namespace and can be named the same as types
    #
    def p_struct_or_union_specifier_1(self, p):
        """ struct_or_union_specifier   : struct_or_union ID
                                        | struct_or_union TYPEID
        """
        klass = self._select_struct_union_class(p[1])
        p[0] = klass(
            name=p[2],
            decls=None,
            coord=self._coord(p.lineno(2)))

    def p_struct_or_union_specifier_2(self, p):
        """ struct_or_union_specifier : struct_or_union brace_open struct_declaration_list brace_close
        """
        klass = self._select_struct_union_class(p[1])
        p[0] = klass(
            name=None,
            decls=p[3],
            coord=self._coord(p.lineno(2)))

    def p_struct_or_union_specifier_3(self, p):
        """ struct_or_union_specifier   : struct_or_union ID brace_open struct_declaration_list brace_close
                                        | struct_or_union TYPEID brace_open struct_declaration_list brace_close
        """
        klass = self._select_struct_union_class(p[1])
        p[0] = klass(
            name=p[2],
            decls=p[4],
            coord=self._coord(p.lineno(2)))

    def p_struct_or_union(self, p):
        """ struct_or_union : STRUCT
                            | UNION
        """
        p[0] = p[1]

    # Combine all declarations into a single list
    #
    def p_struct_declaration_list(self, p):
        """ struct_declaration_list     : struct_declaration
                                        | struct_declaration_list struct_declaration
        """
        if len(p) == 2:
            p[0] = p[1] or []
        else:
            p[0] = p[1] + (p[2] or [])

    def p_struct_declaration_1(self, p):
        """ struct_declaration : specifier_qualifier_list struct_declarator_list_opt SEMI
        """
        spec = p[1]
        assert 'typedef' not in spec['storage']

        if p[2] is not None:
            decls = self._build_declarations(
                spec=spec,
                decls=p[2])

        elif len(spec['type']) == 1:
            # Anonymous struct/union, gcc extension, C1x feature.
            # Although the standard only allows structs/unions here, I see no
            # reason to disallow other types since some compilers have typedefs
            # here, and pylyaparser isn't about rejecting all invalid code.
            #
            node = spec['type'][0]
            if isinstance(node, lya_ast.Node):
                decl_type = node
            else:
                decl_type = lya_ast.IdentifierType(node)

            decls = self._build_declarations(
                spec=spec,
                decls=[dict(decl=decl_type)])

        else:
            # Structure/union members can have the same names as typedefs.
            # The trouble is that the member's name gets grouped into
            # specifier_qualifier_list; _build_declarations compensates.
            #
            decls = self._build_declarations(
                spec=spec,
                decls=[dict(decl=None, init=None)])

        p[0] = decls

    def p_struct_declaration_2(self, p):
        """ struct_declaration : specifier_qualifier_list abstract_declarator SEMI
        """
        # "Abstract declarator?!", you ask?  Structure members can have the
        # same names as typedefs.  The trouble is that the member's name gets
        # grouped into specifier_qualifier_list, leaving any remainder to
        # appear as an abstract declarator, as in:
        #   typedef int Foo;
        #   struct { Foo Foo[3]; };
        #
        p[0] = self._build_declarations(
                spec=p[1],
                decls=[dict(decl=p[2], init=None)])

    def p_struct_declaration_3(self, p):
        """ struct_declaration : SEMI
        """
        p[0] = None

    def p_struct_declarator_list(self, p):
        """ struct_declarator_list  : struct_declarator
                                    | struct_declarator_list COMMA struct_declarator
        """
        p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

    # struct_declarator passes up a dict with the keys: decl (for
    # the underlying declarator) and bitsize (for the bitsize)
    #
    def p_struct_declarator_1(self, p):
        """ struct_declarator : declarator
        """
        p[0] = {'decl': p[1], 'bitsize': None}

    def p_struct_declarator_2(self, p):
        """ struct_declarator   : declarator COLON constant_expression
                                | COLON constant_expression
        """
        if len(p) > 3:
            p[0] = {'decl': p[1], 'bitsize': p[3]}
        else:
            p[0] = {'decl': lya_ast.TypeDecl(None, None, None), 'bitsize': p[2]}

    def p_enum_specifier_1(self, p):
        """ enum_specifier  : ENUM ID
                            | ENUM TYPEID
        """
        p[0] = lya_ast.Enum(p[2], None, self._coord(p.lineno(1)))

    def p_enum_specifier_2(self, p):
        """ enum_specifier  : ENUM brace_open enumerator_list brace_close
        """
        p[0] = lya_ast.Enum(None, p[3], self._coord(p.lineno(1)))

    def p_enum_specifier_3(self, p):
        """ enum_specifier  : ENUM ID brace_open enumerator_list brace_close
                            | ENUM TYPEID brace_open enumerator_list brace_close
        """
        p[0] = lya_ast.Enum(p[2], p[4], self._coord(p.lineno(1)))

    def p_enumerator_list(self, p):
        """ enumerator_list : enumerator
                            | enumerator_list COMMA
                            | enumerator_list COMMA enumerator
        """
        if len(p) == 2:
            p[0] = lya_ast.EnumeratorList([p[1]], p[1].coord)
        elif len(p) == 3:
            p[0] = p[1]
        else:
            p[1].enumerators.append(p[3])
            p[0] = p[1]

    def p_enumerator(self, p):
        """ enumerator  : ID
                        | ID EQUALS constant_expression
        """
        if len(p) == 2:
            enumerator = lya_ast.Enumerator(
                        p[1], None,
                        self._coord(p.lineno(1)))
        else:
            enumerator = lya_ast.Enumerator(
                        p[1], p[3],
                        self._coord(p.lineno(1)))
        self._add_identifier(enumerator.name, enumerator.coord)

        p[0] = enumerator

    def p_declarator_1(self, p):
        """ declarator  : direct_declarator
        """
        p[0] = p[1]

    def p_declarator_2(self, p):
        """ declarator  : pointer direct_declarator
        """
        p[0] = self._type_modify_decl(p[2], p[1])

    # Since it's impossible for a type to be specified after a pointer, assume
    # it's intended to be the name for this declaration.  _add_identifier will
    # raise an error if this TYPEID can't be redeclared.
    #
    def p_declarator_3(self, p):
        """ declarator  : pointer TYPEID
        """
        decl = lya_ast.TypeDecl(
            declname=p[2],
            type=None,
            quals=None,
            coord=self._coord(p.lineno(2)))

        p[0] = self._type_modify_decl(decl, p[1])

    def p_direct_declarator_1(self, p):
        """ direct_declarator   : ID
        """
        p[0] = lya_ast.TypeDecl(
            declname=p[1],
            type=None,
            quals=None,
            coord=self._coord(p.lineno(1)))

    def p_direct_declarator_2(self, p):
        """ direct_declarator   : LPAREN declarator RPAREN
        """
        p[0] = p[2]

    def p_direct_declarator_3(self, p):
        """ direct_declarator   : direct_declarator LBRACKET type_qualifier_list_opt assignment_expression_opt RBRACKET
        """
        quals = (p[3] if len(p) > 5 else []) or []
        # Accept dimension qualifiers
        # Per C99 6.7.5.3 p7
        arr = lya_ast.ArrayDecl(
            type=None,
            dim=p[4] if len(p) > 5 else p[3],
            dim_quals=quals,
            coord=p[1].coord)

        p[0] = self._type_modify_decl(decl=p[1], modifier=arr)

    def p_direct_declarator_4(self, p):
        """ direct_declarator   : direct_declarator LBRACKET STATIC type_qualifier_list_opt assignment_expression RBRACKET
                                | direct_declarator LBRACKET type_qualifier_list STATIC assignment_expression RBRACKET
        """
        # Using slice notation for PLY objects doesn't work in Python 3 for the
        # version of PLY embedded with pylyaparser; see PLY Google Code issue 30.
        # Work around that here by listing the two elements separately.
        listed_quals = [item if isinstance(item, list) else [item]
            for item in [p[3],p[4]]]
        dim_quals = [qual for sublist in listed_quals for qual in sublist
            if qual is not None]
        arr = lya_ast.ArrayDecl(
            type=None,
            dim=p[5],
            dim_quals=dim_quals,
            coord=p[1].coord)

        p[0] = self._type_modify_decl(decl=p[1], modifier=arr)

    # Special for VLAs
    #
    def p_direct_declarator_5(self, p):
        """ direct_declarator   : direct_declarator LBRACKET type_qualifier_list_opt TIMES RBRACKET
        """
        arr = lya_ast.ArrayDecl(
            type=None,
            dim=lya_ast.ID(p[4], self._coord(p.lineno(4))),
            dim_quals=p[3] if p[3] != None else [],
            coord=p[1].coord)

        p[0] = self._type_modify_decl(decl=p[1], modifier=arr)

    def p_direct_declarator_6(self, p):
        """ direct_declarator   : direct_declarator LPAREN parameter_type_list RPAREN
                                | direct_declarator LPAREN identifier_list_opt RPAREN
        """
        func = lya_ast.FuncDecl(
            args=p[3],
            type=None,
            coord=p[1].coord)

        # To see why _get_yacc_lookahead_token is needed, consider:
        #   typedef char TT;
        #   void foo(int TT) { TT = 10; }
        # Outside the function, TT is a typedef, but inside (starting and
        # ending with the braces) it's a parameter.  The trouble begins with
        # yacc's lookahead token.  We don't know if we're declaring or
        # defining a function until we see LBRACE, but if we wait for yacc to
        # trigger a rule on that token, then TT will have already been read
        # and incorrectly interpreted as TYPEID.  We need to add the
        # parameters to the scope the moment the lexer sees LBRACE.
        #
        if self._get_yacc_lookahead_token().type == "LBRACE":
            if func.args is not None:
                for param in func.args.params:
                    if isinstance(param, lya_ast.EllipsisParam): break
                    self._add_identifier(param.name, param.coord)

        p[0] = self._type_modify_decl(decl=p[1], modifier=func)

    def p_pointer(self, p):
        """ pointer : TIMES type_qualifier_list_opt
                    | TIMES type_qualifier_list_opt pointer
        """
        coord = self._coord(p.lineno(1))
        # Pointer decls nest from inside out. This is important when different
        # levels have different qualifiers. For example:
        #
        #  char * const * p;
        #
        # Means "pointer to const pointer to char"
        #
        # While:
        #
        #  char ** const p;
        #
        # Means "const pointer to pointer to char"
        #
        # So when we construct PtrDecl nestings, the leftmost pointer goes in
        # as the most nested type.
        nested_type = lya_ast.PtrDecl(quals=p[2] or [], type=None, coord=coord)
        if len(p) > 3:
            tail_type = p[3]
            while tail_type.type is not None:
                tail_type = tail_type.type
            tail_type.type = nested_type
            p[0] = p[3]
        else:
            p[0] = nested_type

    def p_type_qualifier_list(self, p):
        """ type_qualifier_list : type_qualifier
                                | type_qualifier_list type_qualifier
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_parameter_type_list(self, p):
        """ parameter_type_list : parameter_list
                                | parameter_list COMMA ELLIPSIS
        """
        if len(p) > 2:
            p[1].params.append(lya_ast.EllipsisParam(self._coord(p.lineno(3))))

        p[0] = p[1]

    def p_parameter_list(self, p):
        """ parameter_list  : parameter_declaration
                            | parameter_list COMMA parameter_declaration
        """
        if len(p) == 2: # single parameter
            p[0] = lya_ast.ParamList([p[1]], p[1].coord)
        else:
            p[1].params.append(p[3])
            p[0] = p[1]

    def p_parameter_declaration_1(self, p):
        """ parameter_declaration   : declaration_specifiers declarator
        """
        spec = p[1]
        if not spec['type']:
            spec['type'] = [lya_ast.IdentifierType(['int'],
                coord=self._coord(p.lineno(1)))]
        p[0] = self._build_declarations(
            spec=spec,
            decls=[dict(decl=p[2])])[0]

    def p_parameter_declaration_2(self, p):
        """ parameter_declaration   : declaration_specifiers abstract_declarator_opt
        """
        spec = p[1]
        if not spec['type']:
            spec['type'] = [lya_ast.IdentifierType(['int'],
                coord=self._coord(p.lineno(1)))]

        # Parameters can have the same names as typedefs.  The trouble is that
        # the parameter's name gets grouped into declaration_specifiers, making
        # it look like an old-style declaration; compensate.
        #
        if len(spec['type']) > 1 and len(spec['type'][-1].names) == 1 and \
                self._is_type_in_scope(spec['type'][-1].names[0]):
            decl = self._build_declarations(
                    spec=spec,
                    decls=[dict(decl=p[2], init=None)])[0]

        # This truly is an old-style parameter declaration
        #
        else:
            decl = lya_ast.Typename(
                name='',
                quals=spec['qual'],
                type=p[2] or lya_ast.TypeDecl(None, None, None),
                coord=self._coord(p.lineno(2)))
            typename = spec['type']
            decl = self._fix_decl_name_type(decl, typename)

        p[0] = decl

    def p_identifier_list(self, p):
        """ identifier_list : identifier
                            | identifier_list COMMA identifier
        """
        if len(p) == 2: # single parameter
            p[0] = lya_ast.ParamList([p[1]], p[1].coord)
        else:
            p[1].params.append(p[3])
            p[0] = p[1]

    def p_initializer_1(self, p):
        """ initializer : assignment_expression
        """
        p[0] = p[1]

    def p_initializer_2(self, p):
        """ initializer : brace_open initializer_list_opt brace_close
                        | brace_open initializer_list COMMA brace_close
        """
        if p[2] is None:
            p[0] = lya_ast.InitList([], self._coord(p.lineno(1)))
        else:
            p[0] = p[2]

    def p_initializer_list(self, p):
        """ initializer_list    : designation_opt initializer
                                | initializer_list COMMA designation_opt initializer
        """
        if len(p) == 3: # single initializer
            init = p[2] if p[1] is None else lya_ast.NamedInitializer(p[1], p[2])
            p[0] = lya_ast.InitList([init], p[2].coord)
        else:
            init = p[4] if p[3] is None else lya_ast.NamedInitializer(p[3], p[4])
            p[1].exprs.append(init)
            p[0] = p[1]

    def p_designation(self, p):
        """ designation : designator_list EQUALS
        """
        p[0] = p[1]

    # Designators are represented as a list of nodes, in the order in which
    # they're written in the code.
    #
    def p_designator_list(self, p):
        """ designator_list : designator
                            | designator_list designator
        """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_designator(self, p):
        """ designator  : LBRACKET constant_expression RBRACKET
                        | PERIOD identifier
        """
        p[0] = p[2]

    def p_type_name(self, p):
        """ type_name   : specifier_qualifier_list abstract_declarator_opt
        """
        #~ print '=========='
        #~ print p[1]
        #~ print p[2]
        #~ print p[2].children()
        #~ print '=========='

        typename = lya_ast.Typename(
            name='',
            quals=p[1]['qual'],
            type=p[2] or lya_ast.TypeDecl(None, None, None),
            coord=self._coord(p.lineno(2)))

        p[0] = self._fix_decl_name_type(typename, p[1]['type'])

    def p_abstract_declarator_1(self, p):
        """ abstract_declarator     : pointer
        """
        dummytype = lya_ast.TypeDecl(None, None, None)
        p[0] = self._type_modify_decl(
            decl=dummytype,
            modifier=p[1])

    def p_abstract_declarator_2(self, p):
        """ abstract_declarator     : pointer direct_abstract_declarator
        """
        p[0] = self._type_modify_decl(p[2], p[1])

    def p_abstract_declarator_3(self, p):
        """ abstract_declarator     : direct_abstract_declarator
        """
        p[0] = p[1]

    # Creating and using direct_abstract_declarator_opt here
    # instead of listing both direct_abstract_declarator and the
    # lack of it in the beginning of _1 and _2 caused two
    # shift/reduce errors.
    #
    def p_direct_abstract_declarator_1(self, p):
        """ direct_abstract_declarator  : LPAREN abstract_declarator RPAREN """
        p[0] = p[2]

    def p_direct_abstract_declarator_2(self, p):
        """ direct_abstract_declarator  : direct_abstract_declarator LBRACKET assignment_expression_opt RBRACKET
        """
        arr = lya_ast.ArrayDecl(
            type=None,
            dim=p[3],
            dim_quals=[],
            coord=p[1].coord)

        p[0] = self._type_modify_decl(decl=p[1], modifier=arr)

    def p_direct_abstract_declarator_3(self, p):
        """ direct_abstract_declarator  : LBRACKET assignment_expression_opt RBRACKET
        """
        p[0] = lya_ast.ArrayDecl(
            type=lya_ast.TypeDecl(None, None, None),
            dim=p[2],
            dim_quals=[],
            coord=self._coord(p.lineno(1)))

    def p_direct_abstract_declarator_4(self, p):
        """ direct_abstract_declarator  : direct_abstract_declarator LBRACKET TIMES RBRACKET
        """
        arr = lya_ast.ArrayDecl(
            type=None,
            dim=lya_ast.ID(p[3], self._coord(p.lineno(3))),
            dim_quals=[],
            coord=p[1].coord)

        p[0] = self._type_modify_decl(decl=p[1], modifier=arr)

    def p_direct_abstract_declarator_5(self, p):
        """ direct_abstract_declarator  : LBRACKET TIMES RBRACKET
        """
        p[0] = lya_ast.ArrayDecl(
            type=lya_ast.TypeDecl(None, None, None),
            dim=lya_ast.ID(p[3], self._coord(p.lineno(3))),
            dim_quals=[],
            coord=self._coord(p.lineno(1)))

    def p_direct_abstract_declarator_6(self, p):
        """ direct_abstract_declarator  : direct_abstract_declarator LPAREN parameter_type_list_opt RPAREN
        """
        func = lya_ast.FuncDecl(
            args=p[3],
            type=None,
            coord=p[1].coord)

        p[0] = self._type_modify_decl(decl=p[1], modifier=func)

    def p_direct_abstract_declarator_7(self, p):
        """ direct_abstract_declarator  : LPAREN parameter_type_list_opt RPAREN
        """
        p[0] = lya_ast.FuncDecl(
            args=p[2],
            type=lya_ast.TypeDecl(None, None, None),
            coord=self._coord(p.lineno(1)))

    # declaration is a list, statement isn't. To make it consistent, block_item
    # will always be a list
    #
    def p_block_item(self, p):
        """ block_item  : declaration
                        | statement
        """
        p[0] = p[1] if isinstance(p[1], list) else [p[1]]

    # Since we made block_item a list, this just combines lists
    #
    def p_block_item_list(self, p):
        """ block_item_list : block_item
                            | block_item_list block_item
        """
        # Empty block items (plain ';') produce [None], so ignore them
        p[0] = p[1] if (len(p) == 2 or p[2] == [None]) else p[1] + p[2]

    def p_compound_statement_1(self, p):
        """ compound_statement : brace_open block_item_list_opt brace_close """
        p[0] = lya_ast.Compound(
            block_items=p[2],
            coord=self._coord(p.lineno(1)))

    def p_labeled_statement_1(self, p):
        """ labeled_statement : ID COLON statement """
        p[0] = lya_ast.Label(p[1], p[3], self._coord(p.lineno(1)))

    def p_labeled_statement_2(self, p):
        """ labeled_statement : CASE constant_expression COLON statement """
        p[0] = lya_ast.Case(p[2], [p[4]], self._coord(p.lineno(1)))

    def p_labeled_statement_3(self, p):
        """ labeled_statement : DEFAULT COLON statement """
        p[0] = lya_ast.Default([p[3]], self._coord(p.lineno(1)))

    def p_selection_statement_1(self, p):
        """ selection_statement : IF LPAREN expression RPAREN statement """
        p[0] = lya_ast.If(p[3], p[5], None, self._coord(p.lineno(1)))

    def p_selection_statement_2(self, p):
        """ selection_statement : IF LPAREN expression RPAREN statement ELSE statement """
        p[0] = lya_ast.If(p[3], p[5], p[7], self._coord(p.lineno(1)))

    def p_selection_statement_3(self, p):
        """ selection_statement : SWITCH LPAREN expression RPAREN statement """
        p[0] = fix_switch_cases(
                lya_ast.Switch(p[3], p[5], self._coord(p.lineno(1))))

    def p_iteration_statement_1(self, p):
        """ iteration_statement : WHILE LPAREN expression RPAREN statement """
        p[0] = lya_ast.While(p[3], p[5], self._coord(p.lineno(1)))

    def p_iteration_statement_2(self, p):
        """ iteration_statement : DO statement WHILE LPAREN expression RPAREN SEMI """
        p[0] = lya_ast.DoWhile(p[5], p[2], self._coord(p.lineno(1)))

    def p_iteration_statement_3(self, p):
        """ iteration_statement : FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement """
        p[0] = lya_ast.For(p[3], p[5], p[7], p[9], self._coord(p.lineno(1)))

    def p_iteration_statement_4(self, p):
        """ iteration_statement : FOR LPAREN declaration expression_opt SEMI expression_opt RPAREN statement """
        p[0] = lya_ast.For(lya_ast.DeclList(p[3], self._coord(p.lineno(1))),
                         p[4], p[6], p[8], self._coord(p.lineno(1)))

    def p_jump_statement_1(self, p):
        """ jump_statement  : GOTO ID SEMI """
        p[0] = lya_ast.Goto(p[2], self._coord(p.lineno(1)))

    def p_jump_statement_2(self, p):
        """ jump_statement  : BREAK SEMI """
        p[0] = lya_ast.Break(self._coord(p.lineno(1)))

    def p_jump_statement_3(self, p):
        """ jump_statement  : CONTINUE SEMI """
        p[0] = lya_ast.Continue(self._coord(p.lineno(1)))

    def p_jump_statement_4(self, p):
        """ jump_statement  : RETURN expression SEMI
                            | RETURN SEMI
        """
        p[0] = lya_ast.Return(p[2] if len(p) == 4 else None, self._coord(p.lineno(1)))

    def p_expression_statement(self, p):
        """ expression_statement : expression_opt SEMI """
        if p[1] is None:
            p[0] = lya_ast.EmptyStatement(self._coord(p.lineno(1)))
        else:
            p[0] = p[1]

    def p_expression(self, p):
        """ expression  : assignment_expression
                        | expression COMMA assignment_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            if not isinstance(p[1], lya_ast.ExprList):
                p[1] = lya_ast.ExprList([p[1]], p[1].coord)

            p[1].exprs.append(p[3])
            p[0] = p[1]

    def p_typedef_name(self, p):
        """ typedef_name : TYPEID """
        p[0] = lya_ast.IdentifierType([p[1]], coord=self._coord(p.lineno(1)))

    def p_assignment_expression(self, p):
        """ assignment_expression   : conditional_expression
                                    | unary_expression assignment_operator assignment_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = lya_ast.Assignment(p[2], p[1], p[3], p[1].coord)

    # K&R2 defines these as many separate rules, to encode
    # precedence and associativity. Why work hard ? I'll just use
    # the built in precedence/associativity specification feature
    # of PLY. (see precedence declaration above)
    #
    def p_assignment_operator(self, p):
        """ assignment_operator : EQUALS
                                | XOREQUAL
                                | TIMESEQUAL
                                | DIVEQUAL
                                | MODEQUAL
                                | PLUSEQUAL
                                | MINUSEQUAL
                                | LSHIFTEQUAL
                                | RSHIFTEQUAL
                                | ANDEQUAL
                                | OREQUAL
        """
        p[0] = p[1]

    def p_constant_expression(self, p):
        """ constant_expression : conditional_expression """
        p[0] = p[1]

    def p_conditional_expression(self, p):
        """ conditional_expression  : binary_expression
                                    | binary_expression CONDOP expression COLON conditional_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = lya_ast.TernaryOp(p[1], p[3], p[5], p[1].coord)

    def p_binary_expression(self, p):
        """ binary_expression   : cast_expression
                                | binary_expression TIMES binary_expression
                                | binary_expression DIVIDE binary_expression
                                | binary_expression MOD binary_expression
                                | binary_expression PLUS binary_expression
                                | binary_expression MINUS binary_expression
                                | binary_expression RSHIFT binary_expression
                                | binary_expression LSHIFT binary_expression
                                | binary_expression LT binary_expression
                                | binary_expression LE binary_expression
                                | binary_expression GE binary_expression
                                | binary_expression GT binary_expression
                                | binary_expression EQ binary_expression
                                | binary_expression NE binary_expression
                                | binary_expression AND binary_expression
                                | binary_expression OR binary_expression
                                | binary_expression XOR binary_expression
                                | binary_expression LAND binary_expression
                                | binary_expression LOR binary_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = lya_ast.BinaryOp(p[2], p[1], p[3], p[1].coord)

    def p_cast_expression_1(self, p):
        """ cast_expression : unary_expression """
        p[0] = p[1]

    def p_cast_expression_2(self, p):
        """ cast_expression : LPAREN type_name RPAREN cast_expression """
        p[0] = lya_ast.Cast(p[2], p[4], self._coord(p.lineno(1)))

    def p_unary_expression_1(self, p):
        """ unary_expression    : postfix_expression """
        p[0] = p[1]

    def p_unary_expression_2(self, p):
        """ unary_expression    : PLUSPLUS unary_expression
                                | MINUSMINUS unary_expression
                                | unary_operator cast_expression
        """
        p[0] = lya_ast.UnaryOp(p[1], p[2], p[2].coord)

    def p_unary_expression_3(self, p):
        """ unary_expression    : SIZEOF unary_expression
                                | SIZEOF LPAREN type_name RPAREN
        """
        p[0] = lya_ast.UnaryOp(
            p[1],
            p[2] if len(p) == 3 else p[3],
            self._coord(p.lineno(1)))

    def p_unary_operator(self, p):
        """ unary_operator  : AND
                            | TIMES
                            | PLUS
                            | MINUS
                            | NOT
                            | LNOT
        """
        p[0] = p[1]

    def p_postfix_expression_1(self, p):
        """ postfix_expression  : primary_expression """
        p[0] = p[1]

    def p_postfix_expression_2(self, p):
        """ postfix_expression  : postfix_expression LBRACKET expression RBRACKET """
        p[0] = lya_ast.ArrayRef(p[1], p[3], p[1].coord)

    def p_postfix_expression_3(self, p):
        """ postfix_expression  : postfix_expression LPAREN argument_expression_list RPAREN
                                | postfix_expression LPAREN RPAREN
        """
        p[0] = lya_ast.FuncCall(p[1], p[3] if len(p) == 5 else None, p[1].coord)

    def p_postfix_expression_4(self, p):
        """ postfix_expression  : postfix_expression PERIOD ID
                                | postfix_expression PERIOD TYPEID
                                | postfix_expression ARROW ID
                                | postfix_expression ARROW TYPEID
        """
        field = lya_ast.ID(p[3], self._coord(p.lineno(3)))
        p[0] = lya_ast.StructRef(p[1], p[2], field, p[1].coord)

    def p_postfix_expression_5(self, p):
        """ postfix_expression  : postfix_expression PLUSPLUS
                                | postfix_expression MINUSMINUS
        """
        p[0] = lya_ast.UnaryOp('p' + p[2], p[1], p[1].coord)

    def p_postfix_expression_6(self, p):
        """ postfix_expression  : LPAREN type_name RPAREN brace_open initializer_list brace_close
                                | LPAREN type_name RPAREN brace_open initializer_list COMMA brace_close
        """
        p[0] = lya_ast.CompoundLiteral(p[2], p[5])

    def p_primary_expression_1(self, p):
        """ primary_expression  : identifier """
        p[0] = p[1]

    def p_primary_expression_2(self, p):
        """ primary_expression  : constant """
        p[0] = p[1]

    def p_primary_expression_3(self, p):
        """ primary_expression  : unified_string_literal
                                | unified_wstring_literal
        """
        p[0] = p[1]

    def p_primary_expression_4(self, p):
        """ primary_expression  : LPAREN expression RPAREN """
        p[0] = p[2]

    def p_primary_expression_5(self, p):
        """ primary_expression  : OFFSETOF LPAREN type_name COMMA identifier RPAREN
        """
        coord = self._coord(p.lineno(1))
        p[0] = lya_ast.FuncCall(lya_ast.ID(p[1], coord),
                              lya_ast.ExprList([p[3], p[5]], coord),
                              coord)

    def p_argument_expression_list(self, p):
        """ argument_expression_list    : assignment_expression
                                        | argument_expression_list COMMA assignment_expression
        """
        if len(p) == 2: # single expr
            p[0] = lya_ast.ExprList([p[1]], p[1].coord)
        else:
            p[1].exprs.append(p[3])
            p[0] = p[1]

    def p_identifier(self, p):
        """ identifier  : ID """
        p[0] = lya_ast.ID(p[1], self._coord(p.lineno(1)))

    def p_constant_1(self, p):
        """ constant    : INT_CONST_DEC
                        | INT_CONST_OCT
                        | INT_CONST_HEX
                        | INT_CONST_BIN
        """
        p[0] = lya_ast.Constant(
            'int', p[1], self._coord(p.lineno(1)))

    def p_constant_2(self, p):
        """ constant    : FLOAT_CONST
                        | HEX_FLOAT_CONST
        """
        p[0] = lya_ast.Constant(
            'float', p[1], self._coord(p.lineno(1)))

    def p_constant_3(self, p):
        """ constant    : CHAR_CONST
                        | WCHAR_CONST
        """
        p[0] = lya_ast.Constant(
            'char', p[1], self._coord(p.lineno(1)))

    # The "unified" string and wstring literal rules are for supporting
    # concatenation of adjacent string literals.
    # I.e. "hello " "world" is seen by the C compiler as a single string literal
    # with the value "hello world"
    #
    def p_unified_string_literal(self, p):
        """ unified_string_literal  : STRING_LITERAL
                                    | unified_string_literal STRING_LITERAL
        """
        if len(p) == 2: # single literal
            p[0] = lya_ast.Constant(
                'string', p[1], self._coord(p.lineno(1)))
        else:
            p[1].value = p[1].value[:-1] + p[2][1:]
            p[0] = p[1]

    def p_unified_wstring_literal(self, p):
        """ unified_wstring_literal : WSTRING_LITERAL
                                    | unified_wstring_literal WSTRING_LITERAL
        """
        if len(p) == 2: # single literal
            p[0] = lya_ast.Constant(
                'string', p[1], self._coord(p.lineno(1)))
        else:
            p[1].value = p[1].value.rstrip()[:-1] + p[2][2:]
            p[0] = p[1]

    def p_brace_open(self, p):
        """ brace_open  :   LBRACE
        """
        p[0] = p[1]

    def p_brace_close(self, p):
        """ brace_close :   RBRACE
        """
        p[0] = p[1]

    def p_empty(self, p):
        'empty : '
        p[0] = None

    def p_error(self, p):
        # If error recovery is added here in the future, make sure
        # _get_yacc_lookahead_token still works!
        #
        if p:
            self._parse_error(
                'before: %s' % p.value,
                self._coord(lineno=p.lineno,
                            column=self.lyalex.find_tok_column(p)))
        else:
            self._parse_error('At end of input', '')


#------------------------------------------------------------------------------
if __name__ == "__main__":
    import pprint
    import time, sys

    #t1 = time.time()
    #parser = CParser(lex_optimize=True, yacc_debug=True, yacc_optimize=False)
    #sys.write(time.time() - t1)

    #buf = '''
        #int (*k)(int);
    #'''

    ## set debuglevel to 2 for debugging
    #t = parser.parse(buf, 'x.c', debuglevel=0)
    #t.show(showcoord=True)

