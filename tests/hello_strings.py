import clq
import clq.backends.opencl as ocl
import clq.extensions.language_types as lang
import sys
import os

os.environ['ACE_OCL_INCLUDES'] = ';'.join(sys.path) 

OpenCL = ocl.Backend()

OpenCL.include("<stdio.h>")
##TODO includes.
#@clq.fn
#def strcat(a,b):
#    return a
#strcat = strcat.compile(OpenCL, ocl.string, ocl.string)
#print strcat.program_item.code

@clq.fn
def plus(a, b):
    return a + b

plus_ii = plus.compile(OpenCL, lang.ConstrainedString(OpenCL, ".+"), 
                               lang.ConstrainedString(OpenCL, "."))

print plus_ii.program_item.code
