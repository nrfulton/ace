import clq
import clq.backends.opencl as ocl

OpenCL = ocl.Backend()

@clq.fn
def plus(a, b):
    return a + b
plus_ii = plus.compile(OpenCL, ocl.int, ocl.int)
print plus_ii.program_item.code

@clq.fn
def plus3(a,b,c,plus):
    return plus(a,plus(a,b))
plus3_iii = plus3.compile(OpenCL,ocl.int,ocl.int,ocl.int,plus_ii.cl_type)
program_items = plus3_iii.program_items
for program_item in program_items:
    print program_item.code


