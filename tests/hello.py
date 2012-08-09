import clq
import clq.backends.opencl as ocl

OpenCL = ocl.Backend()
OpenCL.correspondence_check = False

@clq.fn
def plus(a, b):
    return a + b

#plus_ii = plus.compile(OpenCL, ocl.int, ocl.int)
#print plus_ii.program_item.code

@clq.fn
def plus3(a,b,c,plus_fn):
    return plus_fn(a,plus_fn(a,b))

plus3_iii = plus3.compile(OpenCL,ocl.int,ocl.int,ocl.int,plus.cl_type)

for program_item in plus3_iii.program_items:
    print program_item.code 
    



