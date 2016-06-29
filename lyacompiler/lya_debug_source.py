lya_source_dcl = """
    dcl dcl1 int;
    dcl dcl2, dcl3, dcl4, dcl5 char;
    dcl dcl6, dcl7 int, dcl8 bool;
    dcl dcl9 int = 5;
    dcl dcl10, dcl11 int = 6;
    dcl dcl12 int, dcl13, dcl14 int = 10;
    dcl dcl15 int (2:5);
    dcl dcl16 char (0:10);
    dcl dcl17 bool(10:11);
    dcl dcl18 dcl17 (1:2);
    dcl dcl19 int (0:1) (1:2);
    """

lya_source_syn = """
    syn syn1 = 1;
    syn syn2, syn3, syn4 = 3;
    syn syn5 int = 2;
    syn syn6, syn7 int = 3;
    syn syn8 = 10, syn9 = 12;
    syn syn10, syn11 int = 13, syn12 = 20;
    """

lya_source_type = """
    type type1 = int;
    type type2 = char;
    type type3 = bool;
    type type4 = type3;
    type type7, type8 = int;
    type type9, type10, type11 = char;
    type type12 = bool, type13 = type9;
    type type14 = int, type15, type16 = char, type17, type18, type19 = char;
    type type20 = ref int;
    type type21 = ref ref type20;
    type type22 = chars[20];
    type type23 = array [int] char;
    type type24 = array[1:2] bool;
    type type25 = array[int, bool, char, mode1(1:4), int(3:5), 1:5] bool;
    """

lya_source_composite_mode = """
    dcl cms1 chars [10];
    dcl cma1 array [int] bool;
    dcl cma2 array [bool, int] char;
    """

lya_source_procedure1 = """
    power: proc (n int, r int) returns (int);
        dcl c int;
        type t = bool;
    end;
    """

lya_source_procedure2 = """
    power: proc (n int, r int) returns (int);
    end;
    """

lya_source_procedure3 = """
    power: proc (n int, r int);
        dcl c int;
        type t = bool;
    end;
    """

lya_source_procedure4 = """
    power: proc () returns (int);
        dcl c int;
        type t = bool;
    end;
    """

lya_source_procedure5 = """
    power: proc (n int, r int);
    end;
    """

lya_source_procedure6 = """
    power: proc () returns (int);
    end;
    """

lya_source_procedure7 = """
    power: proc ();
        dcl c int;
    end;
    """

lya_source_procedure8 = """
    power: proc ();
    end;
    """

lya_source_procedure9 = """
    power: proc (n int loc, r, z int) returns (int loc);
        dcl c, d int = 1;
        type t = bool;
    end;
    """

lya_source_if1 = """
    label: if 1+2 then
        exit label1;
    else
        exit label2;
    fi;
    """

lya_source_if2 = """
    if 1+2 then
        exit label1;
        exit label2;
    fi;
    """

lya_source_if3 = """
    if 1+2 then
    else
        exit label2;
        exit label3;
    fi;
    """

lya_source_if4 = """
    if 1+2 then
    else
    fi;
    """

lya_source_if5 = """
    if 1+2 then
        exit label1;
    elsif 1+2 then
        exit label2;
        exit label22;
    else
        exit lable3;
    fi;
    """

lya_source_if6 = """
    if 1+2 then
        exit label1;
    elsif 1+2 then
        exit label2;
        exit label22;
    fi;
    """

lya_source_if7 = """
    if 1+2 then
        if 1+3 then
            exit label1;
        fi;
    elsif 1+2 then
        exit label2;
        if 2+5 then
        else
            exit label22;
        fi;
    else
        if 2+5 then
            exit a1;
        elsif 1+2 then
            exit label22;
        fi;
    fi;
    """

lya_source_action1 = """
    label1: ac1 = 10 + 10;
    ac2 += 2;
    ac3 -= 10;
    ac4 *= 55;
    ac5 /= 1;
    ac5 %= 20;
    ac6 &= 2;
    """

lya_source_expression = """
    dcl var1 int=3+5-7*7/9%3;
    dcl var2 int = 2 in 3;
    dcl var3 bool = 5 && 3 || 1 == 2 & 2;
    dcl var4 bool = if 2 then 3 else 5 fi;
    dcl var2 int = var1 + 3;
    """

lya_source_action2 = """
    exit label1;
    result 1 + 2;
    return;
    return 2 + 1;
    """

lya_source_call1 = """
    function();
    function(1);
    function(1, 2);
    function(1+2, 2);
    function(1,2,3/2);
    """

lya_source_call2 = """
    num(1);
    pred();
    succ(1,2);
    upper(1/2);
    lower(2/3);
    length();
    read(100);
    print(var2+2);
    """

lya_source_do1 = """
    dcl var int = 3;
    do od;
    do var = 2; od;
    do while 1; od;
    do while 3; var = 32; od;
    """

lya_source_do2 = """
    do for counter in int; od;
    do for counter in bool; var3 = 12; od;
    do for counter down in char; od;
    do for counter in int while 3; var = 32; od;
    do for counter = 3 to 8; od;
    do for counter = 3 down to 8; od;
    do for counter = 3 by 5 to 8; od;
    do for counter = 3 by 5 down to 8; od;
    """

lya_source_do3 = """
    dcl var int = 3;
    do od;
    do var = 2; od;
    do while var; od;
    do while 3; var = 32; od;
    """

test2_source = """dcl m int = 2, n int = 3;
p: proc (x int);
  dcl s int;
  s = m * x;
  print(s);
end;
p(n);"""

test3_source = """dcl m int = 2, n int = 3;
p: proc (x, y int, b bool) returns (int);
    dcl s int = x;
    if b then
        s += y;
        result s;
    else
        result y;
    fi;
end;

dcl b bool;
read (b);
print (p(m, n, b));"""

test4_source = """dcl i int, b bool = true;
x:
  do while b;
        read (i);
        if i <= 0 then
            exit x;
        fi;
        print (i*i);
  od;
print (0);"""

test5_source = """dcl i, soma int;
soma = 0;
do for i=1 to 10;
    soma += i;
od;
print (soma);
"""

test6_source = """dcl i int;
dcl soma int = 0, b bool = true;

do for i=1 to 10 while b;
    soma += i;
    if soma > 100 then
        b = false;
    fi;
od;
print (soma);"""

test7_source = """dcl i,j int, r ref int;

p: proc(x int, y ref int) returns (int);
  dcl b bool;
  read(b);
  if b then
     y = -> i;
     result y->;
  else
     y = r;
     result r->;
  fi;
end;

read(i);
r = -> i;
print(p(i,->j));"""

test8_source = """dcl i int, j,k int = 2;

p: proc(x int, y int loc) returns (int loc);
    dcl z int = y;
    y = x;
    result k;
    print(z); /* print 2 */
end;

i = p(3,j);
print(i);
print(j);  /* print 2,3 */"""

test9_source = """dcl a array[3:10] int;
dcl i,j int;

read(j);
a[3]=2*j;
do
  for i = 4 to 10;
    a[i] = 5+i;
od;
print(a[j]);"""


syn_test_source = """syn sy1 = 20;
syn sy6 = sy1;
syn sy2 char = 'c';
syn sy3 bool = true;
syn sy4 int = 1 + sy1;"""


dcl_op_source = """dcl var1 int=3+5-7*7/9%3; dcl var2 int = 2 in 3;"""
dcl_op_source2 = """dcl var2, varx char;\ndcl var3, var4 int = 10;\ndcl var5 = 10 + 5 * (10 - 20);"""

test_rel_exp_source = """dcl m bool = false, n bool = false;
p: proc (x bool);
  dcl s bool;
  s = m >= x;
end;
p(n);"""

test_unary_op_source = """dcl m int = 2, n int = 3;
p: proc (x int);
  dcl s bool;
  s = !true;
end;
p(n);"""

test_elsif_source = """dcl m int = 2, n int = 3, y, s int, b bool = true;
    if b then
        s += y;
    elsif b then
        s = y;
    else
        s = 3;
    fi;

print (s);"""

testret_source = """dcl m int = 2, n int = 3;
p: proc (x, y int, b bool) returns (int);
    dcl s int = x;
    if b then
        s += y;
        return s;
    else
        result y;
    fi;
end;

dcl b bool = true;
read (b);
print (p(m, n, b));"""


# The only variable exported from this module.
__all__ = ['lya_debug_source']

lya_debug_source = test7_source
#lya_debug_source = lya_source_do3
