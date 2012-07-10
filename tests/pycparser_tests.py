import pycparser
from pycparserext.ext_c_parser import OpenCLCParser
from pycparserext.ext_c_generator import OpenCLCGenerator


p = OpenCLCParser()
ast = p.parse("__kernel int plus(int a, int b) {return (a + b);}")

print ast.show()

print OpenCLCGenerator().visit(ast)