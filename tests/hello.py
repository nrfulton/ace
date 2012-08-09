import clq
import clq.backends.opencl as ocl

OpenCL = ocl.Backend()

@clq.fn
def plus(a, b):
    return a + b

@clq.fn
def plus3(a,b,c,plus):
    return plus(a,plus(a,b))

plus3_iii = plus3.compile(OpenCL,ocl.int,ocl.int,ocl.int,plus.cl_type)

for program_item in plus3_iii.program_items:
    print program_item.code 
    



