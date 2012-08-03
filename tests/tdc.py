import clq
import clq.backends.opencl as ocl
import clq.extensions.language_types as lang
import sys
import os

os.environ['ACE_OCL_INCLUDES'] = ';'.join(sys.path) 

OpenCL = ocl.Backend()

OpenCL.include("<stdio.h>")

@clq.fn
def plus(a, b):
    x = 1
    if -a == 1:
        x = 3
        return a
    else:
        return b
    while a == 1:
        return a
    

plus_ii = plus.compile(OpenCL, ocl.int, 
                               ocl.int)

@clq.fn
def plus2(a,b,c,plus):
    return plus(a,plus(b,c))

plus2_iii = plus2.compile(OpenCL,ocl.int,ocl.int,ocl.int,plus_ii.cl_type)

for p in plus2_iii.program_items:
    print p.code

