import pycparser
import pycparserext.typechecker.type_checker as checker
from pycparserext.typechecker.type_checker import Context
from pycparserext.ext_c_parser import OpenCLCParser
from pycparserext.ext_c_generator import OpenCLCGenerator
import traceback
import cypy

OCL_PARSER = OpenCLCParser() #For speed, we only initialize once.
def check(code, expect_success=True, show_trace=False, show_ast=False):
    """The template for all tests in this file."""
    ast = OCL_PARSER.parse(code)        
    if show_ast: ast.show()
    g = Context()
    tc = checker.OpenCLTypeChecker(g) #create checker w/ new ctx
    try:
        tc.visit(ast)
        assert expect_success #false positives
    except checker.TargetTypeCheckException as e:
        if not expect_success:
            assert True 
        else:
            if show_trace: traceback.print_exc()
            print "ERROR: %s" % e.message
            assert False #false negatives   

################################################################################
#Code Snippets
################################################################################
#These are useful code snippets that are used in many tests.

#When many built-in types are acceptable, this is almost never acceptable.
stuff = """
typedef struct { 
    int a; 
} stuff;
"""
check(stuff)

################################################################################
#Function Definition and Application
################################################################################

check("""
__kernel int main() {
    return 0;
}
""")

check("""
int main() {
    return main();
}
""")

check("""
int main() {
}
""")
check(stuff + """
int main(int x) {
    stuff x;
    return x;
}
""",False) #wrong return

#Param lists
check("""
int main(int x) {
    return main(x);
}
""")
check(stuff + """
int fun(int x) {
    stuff x;
    return fun(s);
}
""",False) #wrong param

#Multiple functions
check("""
int fun(int x) { return x; }
int other() { int x; int y; return fun(y); }
""")

check("""
int fun(int x) { return x; }
int other() { int x; int y; return fun(y,y); }
""",False) #too many args passed to fun.

check("""
int main() {
    int main;
    main();
}
""",False)#redeclaring main as a non-function.

#Ellisis
check("""
int func(int x, char y, ...) { return func(1,'c',2,3,4); }
""")

check("""
int func(int x, char y, ...) { return func(1,'c'); }
""")

check("""
int func(int x, char y, ...) { return func(1); }
""",False)


#Fwd Decls
check(stuff + """
int function(int);

int function(int x) {
    return x+1;
}
""")

check(stuff + """
int function(int);

int function(int);

int function(int x) {
    return x+1;
}
""") #appropriate redecl of fwd decls

check(stuff + """
stuff function(int);

int function(int x) {
    return x+1;
}
""", False) #inappropriate redecl of fwd decls


################################################################################
#Conditionals (if, switch, ternary)
################################################################################

#If
check("""
void main() {
    int x;
    int y;
    if(x == y) {
        x = y;
    }
}""")
check("""
void main() {
    int x;
    int y;
    if(x == y) {
        int z;
    }
    z = 1;
}""",False) #scope
check(stuff + """
int main() {
    stuff s;
    int y;
    if(s) {
        x = y;
    }
}""", False) #s is not boolean.

#Ternary
check("""
int main() {
    int x;
    int y;
    return x == y ? x : y;
}""")
check(stuff+"""
int main() {
    int x;
    stuff y;
    return 1==1 ? x : y ;
}""",False) #left type != right type


################################################################################
#Loops (for,while)
################################################################################

#For
check("""
void main() {
    
    for(int i = 0 ; i == 100 ; i++) {
        i;
    }
}
""")

check("""
void main() {
    for(int i = 0 ; i == 100 ; i++) {
        i;
    }
    i;
}
""",False) #scope

check("""
void main() {
    for(int i = 0 ; i; i++) {
        i;
    }
}
""",False) #condition must be bool


#while
check("""
void main() {
    while(1==1) { int x; }
}""")

check("""
void main() {
    while(1==1) { int x; } x = 1;
}""", False) #scope

check(stuff + """
void main() {
    stuff s;
    while(s) { int x; }
}""",False) #not a boolean.


################################################################################
#Expression Lists
################################################################################

check("""
int main() {
    int x;
    int a[4] = {x,1,2,3};
    return 0;
}
""")

check(stuff + """
int main() {
    stuff s;
    stuff a[4] = {s,1,2,3};
    return 0;
}
""", False) #expression list types don't match.


################################################################################
#Array Declaration
################################################################################
check("""
int main() {
    int x[2];
    return 0;
}
""")

#Dimension
check(stuff + """
int main() {
    stuff s;
    int x[s];
    return 0;
}
""",False)

#value
check("""
int main() {
    int x[2] = {1,2};
}
""")

#incorrectly typed value
check(stuff + """
int main() {
    stuff s;
    int x[2] = {1,s};
}
""", False)


################################################################################
#Array Reference
################################################################################

check("""
int main() {
    int x[2] = {1,2};
    return x[0];
}""")

check("""
int main() {
    int y;
    return y[0];
}""",False) #y isn't an array

check(stuff + """
int main() {
    stuff s;
    int x[2] = {1,2};
    return x[s];
}""",False) #s isn't an index type.


################################################################################
#Empty Statement
################################################################################

check("""int main() {int x; ; return 0; }""")


################################################################################
#Enum
################################################################################

check("""
int main() {
    enum {zero,one,two,four=4};
}
int zero;
""")

check("""
int main() {
    enum seq {zero,one,two,four=4};
    seq = zero;
    seq = four;
}
""")

check("""
int main() {
    enum seq {zero,one,two,four=4};
    int zero;
}
""", False) #redeclaration of zero.

check("""
int main() {
    enum seq {zero,one,two,four=4};
    int seq;
}
""", False) #redeclaration of seq.

check("""
int main() {
    enum seq {zero,one,two,four=4};
    int seq;
}
""", False) #keyword for variable name. 

#check("""
#int main() {
#    enum seq {zero,one,two,four=4};
#    zero = one;
#}
#""", False) #lvalue TODO-fail 


################################################################################
#Typedef
################################################################################

check("""
int main() {
    typedef int XXX;
    XXX a;
}
""")


################################################################################
#Pointers
################################################################################

check("""
int main() {
    int* x;
}
""")

#check("""
#typedef struct { int x; } S;
#int main() {
#    S *s, t;
#    s->x = 1;
#    t.x = 1;
#}
#""") # TODO bug in the parser?


################################################################################
#Struct
################################################################################

check(stuff + """
int main() {
    int x,y,z;
    x = y = z;
}
""")

check(stuff + """
int main() {
    int x,y,z;
    stuff s;
    y = s;
}
""",False)


################################################################################
#Struct
################################################################################

check("""
int main() {
    typedef struct {
        int x;
        char y;
    } XXX;
    XXX a;
    a.x = 1;
    a.y = 'c';
}
""")

check("""
int main() {
    typedef struct {
        int x;
        char y;
    } XXX;
    XXX a;
    a.x = 1;
    a.y = 'c';
}
XXX x;
""",False) #XXX typedef is out of scope at last line.

check("""
int main() {
    typedef struct {
        int x;
        char y;
    } XXX;
    XXX a;
    XXX b;
    a.x = b;
}
""",False) #assignment

check("""
int main() {
    typedef struct {
        int x;
        char y;
    } XXX;
    XXX* a;
    a.x;
}
""",False) #ptrs, no ptrs.

check("""
int main() {
    typedef struct {
        int x;
        char y;
    } XXX;
    XXX a;
    a->x;
}
""",False) #ptrs, no ptrs.

################################################################################
#Union Types
################################################################################

check("""
int main() {
    union U {
        int x;
        char y;
    };
    union U x;
    x.x;
}
""")

check("""
int main() {
    union u {
        int x;
        char y;
    } udata;
    udata.x;
    udata.y;
}
""")

check("""
int main() {
    union u {
        int x;
        char y;
    } udata;
    udata.z;
}
""",False) #z isn't a member.


################################################################################
#Compound Literal
################################################################################

check("""
typedef struct { int x; int y; } XXX;
int main() {
    XXX x = {1,2};
    return x.x;
}
""")

check("""
typedef struct { int x; int y; } XXX;
int main() {
    XXX x = {1};
    return x.x;
}
""")

check("""
typedef struct { int x; int y; } XXX;
int main() {
    XXX x = {1,2,3};
    return x.x;
}
""",False)#too many initializer args

check(stuff + """
typedef struct { int x; int y; } XXX;
int main() {
    stuff s;
    XXX x = {1,s};
    return x.x;
}
""",False)#wrong initializer type

################################################################################
#Named Initializers
################################################################################

check("""
int main() {
    union u {
        int x;
        char y;
    } udata = {'c'};
    udata.x;
}
""") 


################################################################################
#Misc. C/OCL stuff
################################################################################

check("""
inline void func() {
    int x = 0;
}
""")

check("""
int func() {
    return abs(-1);
}
""")


#built-in functions
check("""
int func() {
    short x;
    short y = tanh(x);
}
""")

check("""
int func() {
    char x;
    char y;
    short z;
    z = upsample(x,y);
}
""")

################################################################################
#Funtion specifiers
################################################################################

check("""
__kernel int func() {
    return 1;
}
""")
