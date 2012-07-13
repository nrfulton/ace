import pycparser
import pycparserext.typechecker.type_checker as checker
from pycparserext.ext_c_parser import OpenCLCParser
from pycparserext.ext_c_generator import OpenCLCGenerator
import traceback

OCL_PARSER = OpenCLCParser() #The constructor does some heavy lifting.
def check(code, expect_success=True, show_trace=False, show_ast=False):
    """The template for all tests in this file."""
    ast = OCL_PARSER.parse(code)
    tc = checker.OpenCLTypeChecker(checker.Context())
    try:
        tc.visit(ast)
        assert expect_success #false positives
    except checker.TargetTypeCheckException as e:
        if not expect_success:
            assert True 
        else:
            if show_ast: ast.show()
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
#check(stuff)


################################################################################
#Compound Statements
################################################################################

#TODO visit_Compound needs to manage scope, but that causes issues ATM for some reason.


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
int main(int x) {
    stuff x;
    return main(s);
}
""",False) #wrong param

#Multiple functions
check("""
int main(int x) { return x; }
int other() { int x; int y; return main(y); }
""")

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
