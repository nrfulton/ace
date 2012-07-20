import pycparser
from pycparserext.ext_c_parser import OpenCLCParser
from pycparserext.ext_c_generator import OpenCLCGenerator
import types
#import cypy

################################################################################
#C99 defintion
################################################################################

def c99fn(name,args=list(),return_type="void"):
    """Gets a FunctionType for a c99 built-in function"""
    #Create types out of argument names.
    arg_types = list()
    for arg in args:
        if arg.endswith("*"):
            arg.pop()
            t = Type(arg)
            t.is_ptr = True
            arg_types.append(t)
        else:
            arg_types.append(Type(arg))
    
    #Create type out of return type name
    return_type_t = None
    if return_type.endswith("*"):
        return_type.pop()
        return_type_t = Type(return_type)
        return_type_t.is_ptr = True
    else:
        return_type_t = Type(return_type)
        
    return FunctionType(name, arg_types, return_type_t)

c99_binops = ("+","-")
c99_conditional_ops = ("==","!=","<","<=",">",">=")
c99_unary_ops = ("-","!")

c99_op_pairs = {
    ('uchar', 'uchar'): 'uint',
    ('uchar', 'char'): 'uint',
    ('uchar', 'ushort'): 'uint',
    ('uchar', 'short'): 'uint',
    ('uchar', 'uint'): 'uint',
    ('uchar', 'int'): 'uint',
    ('uchar', 'ulong'): 'uint',
    ('uchar', 'long'): 'ulong',
    ('uchar', 'half'): 'float',
    ('uchar', 'float'): 'float',
    ('uchar', 'double'): 'double',
    ('uchar', 'uintptr_t'): 'uintptr_t',
    ('uchar', 'intptr_t'): 'uintptr_t',
    ('uchar', 'size_t'): 'size_t',
    ('uchar', 'ptrdiff_t'): 'size_t',
    
    ('char', 'uchar'): 'uint',
    ('char', 'char'): 'int',
    ('char', 'ushort'): 'uint',
    ('char', 'short'): 'int',
    ('char', 'uint'): 'uint',
    ('char', 'int'): 'int',
    ('char', 'ulong'): 'ulong',
    ('char', 'long'): 'long',
    ('char', 'half'): 'float',
    ('char', 'float'): 'float',
    ('char', 'double'): 'double',
    ('char', 'uintptr_t'): 'uintptr_t',
    ('char', 'intptr_t'): 'intptr_t',
    ('char', 'size_t'): 'size_t',
    ('char', 'ptrdiff_t'): 'ptrdiff_t',
    
    ('ushort', 'uchar'): 'uint',
    ('ushort', 'char'): 'uint',
    ('ushort', 'ushort'): 'uint',
    ('ushort', 'short'): 'uint',
    ('ushort', 'uint'): 'uint',
    ('ushort', 'int'): 'uint',
    ('ushort', 'ulong'): 'uint',
    ('ushort', 'long'): 'ulong',
    ('ushort', 'half'): 'float',
    ('ushort', 'float'): 'float',
    ('ushort', 'double'): 'double',
    ('ushort', 'uintptr_t'): 'uintptr_t',
    ('ushort', 'intptr_t'): 'uintptr_t',
    ('ushort', 'size_t'): 'size_t',
    ('ushort', 'ptrdiff_t'): 'size_t',
    
    ('short', 'uchar'): 'uint',
    ('short', 'char'): 'int',
    ('short', 'ushort'): 'uint',
    ('short', 'short'): 'int',
    ('short', 'uint'): 'uint',
    ('short', 'int'): 'int',
    ('short', 'ulong'): 'ulong',
    ('short', 'long'): 'long',
    ('short', 'half'): 'float',
    ('short', 'float'): 'float',
    ('short', 'double'): 'double',
    ('short', 'uintptr_t'): 'uintptr_t',
    ('short', 'intptr_t'): 'intptr_t',
    ('short', 'size_t'): 'size_t',
    ('short', 'ptrdiff_t'): 'ptrdiff_t',
    
    ('uint', 'uchar'): 'uint',
    ('uint', 'char'): 'uint',
    ('uint', 'ushort'): 'uint',
    ('uint', 'short'): 'uint',
    ('uint', 'uint'): 'uint',
    ('uint', 'int'): 'uint',
    ('uint', 'ulong'): 'ulong',
    ('uint', 'long'): 'ulong',
    ('uint', 'half'): 'float',
    ('uint', 'float'): 'float',
    ('uint', 'double'): 'double',
    ('uint', 'uintptr_t'): 'uintptr_t',
    ('uint', 'intptr_t'): 'uintptr_t',
    ('uint', 'size_t'): 'size_t',
    ('uint', 'ptrdiff_t'): 'size_t',
    
    ('int', 'uchar'): 'uint',
    ('int', 'char'): 'int',
    ('int', 'ushort'): 'uint',
    ('int', 'short'): 'int',
    ('int', 'uint'): 'uint',
    ('int', 'int'): 'int',
    ('int', 'ulong'): 'ulong',
    ('int', 'long'): 'long',
    ('int', 'half'): 'float',
    ('int', 'float'): 'float',
    ('int', 'double'): 'double',
    ('int', 'uintptr_t'): 'uintptr_t',
    ('int', 'intptr_t'): 'intptr_t',
    ('int', 'size_t'): 'size_t',
    ('int', 'ptrdiff_t'): 'ptrdiff_t',
    
    ('ulong', 'uchar'): 'ulong',
    ('ulong', 'char'): 'ulong',
    ('ulong', 'ushort'): 'ulong',
    ('ulong', 'short'): 'ulong',
    ('ulong', 'uint'): 'ulong',
    ('ulong', 'int'): 'ulong',
    ('ulong', 'ulong'): 'ulong',
    ('ulong', 'long'): 'ulong',
    ('ulong', 'half'): None,
    ('ulong', 'float'): 'float',
    ('ulong', 'double'): 'double',
    ('ulong', 'uintptr_t'): 'ulong',
    ('ulong', 'intptr_t'): 'ulong',
    ('ulong', 'size_t'): 'ulong',
    ('ulong', 'ptrdiff_t'): 'ulong',
    
    ('long', 'uchar'): 'ulong',
    ('long', 'char'): 'long',
    ('long', 'ushort'): 'ulong',
    ('long', 'short'): 'long',
    ('long', 'uint'): 'ulong',
    ('long', 'int'): 'long',
    ('long', 'ulong'): 'ulong',
    ('long', 'long'): 'long',
    ('long', 'half'): None,
    ('long', 'float'): 'float',
    ('long', 'double'): 'double',
    ('long', 'uintptr_t'): 'ulong',
    ('long', 'intptr_t'): 'long',
    ('long', 'size_t'): 'ulong',
    ('long', 'ptrdiff_t'): 'long',
    
    ('half', 'uchar'): 'float',
    ('half', 'char'): 'float',
    ('half', 'ushort'): 'float',
    ('half', 'short'): 'float',
    ('half', 'uint'): 'float',
    ('half', 'int'): 'float',
    ('half', 'ulong'): None,
    ('half', 'long'): None,
    ('half', 'half'): 'float',
    ('half', 'float'): 'float',
    ('half', 'double'): 'double',
    ('half', 'uintptr_t'): None,
    ('half', 'intptr_t'): None,
    ('half', 'size_t'): None,
    ('half', 'ptrdiff_t'): None,
    
    ('float', 'uchar'): 'float',
    ('float', 'char'): 'float',
    ('float', 'ushort'): 'float',
    ('float', 'short'): 'float',
    ('float', 'uint'): 'float',
    ('float', 'int'): 'float',
    ('float', 'ulong'): 'float',
    ('float', 'long'): 'float',
    ('float', 'half'): 'float',
    ('float', 'float'): 'float',
    ('float', 'double'): 'double',
    ('float', 'uintptr_t'): 'float',
    ('float', 'intptr_t'): 'float',
    ('float', 'size_t'): 'float',
    ('float', 'ptrdiff_t'): 'float',
        
    ('double', 'uchar'): 'double',
    ('double', 'char'): 'double',
    ('double', 'ushort'): 'double',
    ('double', 'short'): 'double',
    ('double', 'uint'): 'double',
    ('double', 'int'): 'double',
    ('double', 'ulong'): 'double',
    ('double', 'long'): 'double',
    ('double', 'half'): 'double',
    ('double', 'float'): 'double',
    ('double', 'double'): 'double',
    ('double', 'uintptr_t'): 'double',
    ('double', 'intptr_t'): 'double',
    ('double', 'size_t'): 'double',
    ('double', 'ptrdiff_t'): 'double',
    
    ('uintptr_t', 'uchar'): 'uintptr_t',
    ('uintptr_t', 'char'): 'uintptr_t',
    ('uintptr_t', 'ushort'): 'uintptr_t',
    ('uintptr_t', 'short'): 'uintptr_t',
    ('uintptr_t', 'uint'): 'uintptr_t',
    ('uintptr_t', 'int'): 'uintptr_t',
    ('uintptr_t', 'ulong'): 'ulong',
    ('uintptr_t', 'long'): 'ulong',
    ('uintptr_t', 'half'): None,
    ('uintptr_t', 'float'): 'float',
    ('uintptr_t', 'double'): 'double',
    ('uintptr_t', 'uintptr_t'): 'uintptr_t',
    ('uintptr_t', 'intptr_t'): 'uintptr_t',
    ('uintptr_t', 'size_t'): 'uintptr_t',   
    ('uintptr_t', 'ptrdiff_t'): 'uintptr_t',
    
    ('intptr_t', 'uchar'): 'uintptr_t',
    ('intptr_t', 'char'): 'intptr_t',
    ('intptr_t', 'ushort'): 'uintptr_t',
    ('intptr_t', 'short'): 'intptr_t',
    ('intptr_t', 'uint'): 'uintptr_t',
    ('intptr_t', 'int'): 'intptr_t',
    ('intptr_t', 'ulong'): 'ulong',
    ('intptr_t', 'long'): 'long',
    ('intptr_t', 'half'): None,
    ('intptr_t', 'float'): 'float',
    ('intptr_t', 'double'): 'double',
    ('intptr_t', 'uintptr_t'): 'uintptr_t',
    ('intptr_t', 'intptr_t'): 'intptr_t',
    ('intptr_t', 'size_t'): 'uintptr_t',
    ('intptr_t', 'ptrdiff_t'): 'intptr_t',
    
    ('size_t', 'uchar'): 'size_t',
    ('size_t', 'char'): 'size_t',
    ('size_t', 'ushort'): 'size_t',
    ('size_t', 'short'): 'size_t',
    ('size_t', 'uint'): 'size_t',
    ('size_t', 'int'): 'size_t',
    ('size_t', 'ulong'): 'ulong',
    ('size_t', 'long'): 'ulong',
    ('size_t', 'half'): None,
    ('size_t', 'float'): 'float',
    ('size_t', 'double'): 'double',
    ('size_t', 'uintptr_t'): 'uintptr_t',
    ('size_t', 'intptr_t'): 'uintptr_t',
    ('size_t', 'size_t'): 'size_t',   
    ('size_t', 'ptrdiff_t'): 'size_t',
    
    ('ptrdiff_t', 'uchar'): 'size_t',
    ('ptrdiff_t', 'char'): 'ptrdiff_t',
    ('ptrdiff_t', 'ushort'): 'size_t',
    ('ptrdiff_t', 'short'): 'ptrdiff_t',
    ('ptrdiff_t', 'uint'): 'size_t',
    ('ptrdiff_t', 'int'): 'ptrdiff_t',
    ('ptrdiff_t', 'ulong'): 'ulong',
    ('ptrdiff_t', 'long'): 'long',
    ('ptrdiff_t', 'half'): None,
    ('ptrdiff_t', 'float'): 'float',
    ('ptrdiff_t', 'double'): 'double',
    ('ptrdiff_t', 'uintptr_t'): 'uintptr_t',
    ('ptrdiff_t', 'intptr_t'): 'intptr_t',
    ('ptrdiff_t', 'size_t'): 'size_t',   
    ('ptrdiff_t', 'ptrdiff_t'): 'ptrdiff_t',
}

#Vector types
c99_scalar_types = ("uchar", "char",
         "ushort", "short",
         "uint", "int",
         "ulong", "long",
         "uintptr_t", "intptr_t",
         "size_t", "ptrdiff_t",
         "half", "float", "double",
         "void", "bool") 

vector_type_sizes = (2, 3, 4, 8, 16)

c99_vector_types = list()
for t in c99_scalar_types:
    for s in vector_type_sizes: c99_vector_types.append("%s%s"%(t,s))

#left can be substituted for right.
c99_substitutions = (
                     #char
                     ('char', 'uchar'),
                     ('char', 'int'),
                     #uchar
                     ('uchar', 'char'),
                     
                     #int
                     ('int', 'uint'),
                     ('int', 'size_t'),
                     ('int', 'long'),
                     #uint
                     ('uint','int'),
                     
                     #long
                     ('long', 'ulong'),
                     ('long', 'int'),
                     #ulong
                     ('ulong','long'),
                     
                     #size_t
                     ('size_t', 'int'),
                    )
def transitive_sub_r(given,expected,intermediate,tested):
    """Use trensitive_sub
    
    intermediate = the current left hand size.
    
    tested = a list of values that have already been attempted, and is used for
    cycle avoidance.
    """
    if given == None or intermediate == None: return False
    if intermediate == None: intermediate = given
    tested.append(intermediate)
    for s in c99_substitutions:
        if s[0] == intermediate:
            if s[1] == expected: return True
            if not s[1] in tested:
                if transitive_sub_r(given,expected,s[1],tested):
                    return True
    return False

def transitive_sub(given,expected):
    """Determines if there's a path from given to expected in c99_substitutions.
    """
    return transitive_sub_r(given, expected, expected, list())

################################################################################
#            ACE/OCL/Typechecker Correspodence                                   #
################################################################################
class Correspondence(object):
    @classmethod
    def tc_to_ace(cls, tc_t):
        """Converts Typechecker type to Ace type."""
        pass #TODO
    
    @classmethod
    def ace_to_tc(cls, ace_t):
        """Converts Ace type ot Typechecker type"""
        pass #TODO
        
    @classmethod
    def tc_to_ocl(cls, tc_t):
        """Converts Typechecker type to OCL type"""
        return str(tc_t)

################################################################################
#                      TYPING CHECKING RULES                                   #
################################################################################
class TypeDefinitions(object):
    """ This class contains a definition of C99.
    
    We build up types and then call `exists` just before introducing
    a variable in to the context in order to ensure that the variable's type is
    valid C99.
    """ 
    def __init__(self, context):       
        """Populates the object with data from the c99 specification."""
        #The context
        self._g = context
        
        #built-in OpenCL Integer
        #TODO this was generated based on the OpenCL spec, but there's a lot of
        #unnecessary reptition -- each function needs only one defintion 
        #(in terms of ints.)
        ### Begin generated code ###
        self.functions = dict()
        # Global Built-in Functions [6.11.1]self.functions["get_work_dim"] = c99fn("get_work_dim", (,), "uint")
        self.functions["get_global_size"] = c99fn("get_global_size", ("uint",), "size_t")
        self.functions["get_global_id"] = c99fn("get_global_id", ("uint",), "size_t")
        self.functions["get_local_size"] = c99fn("get_local_size", ("uint",), "size_t")
        self.functions["get_local_id"] = c99fn("get_local_id", ("uint",), "size_t")
        self.functions["get_num_groups"] = c99fn("get_num_groups", ("uint",), "size_t")
        self.functions["get_group_id"] = c99fn("get_group_id", ("uint",), "size_t")
        self.functions["get_global_offset"] = c99fn("get_global_offset", ("uint",), "size_t")
        # Integer Built-in Functions [6.11.2]self.functions["acos"] = c99fn("acos", ("char",), "char")
        self.functions["acos"] = c99fn("acos", ("char2",), "char2")
        self.functions["acos"] = c99fn("acos", ("char4",), "char4")
        self.functions["acos"] = c99fn("acos", ("char8",), "char8")
        self.functions["acos"] = c99fn("acos", ("char16",), "char16")
        self.functions["acos"] = c99fn("acos", ("uchar",), "uchar")
        self.functions["acos"] = c99fn("acos", ("uchar2",), "uchar2")
        self.functions["acos"] = c99fn("acos", ("uchar4",), "uchar4")
        self.functions["acos"] = c99fn("acos", ("uchar8",), "uchar8")
        self.functions["acos"] = c99fn("acos", ("uchar16",), "uchar16")
        self.functions["acos"] = c99fn("acos", ("short",), "short")
        self.functions["acos"] = c99fn("acos", ("short2",), "short2")
        self.functions["acos"] = c99fn("acos", ("short4",), "short4")
        self.functions["acos"] = c99fn("acos", ("short8",), "short8")
        self.functions["acos"] = c99fn("acos", ("short16",), "short16")
        self.functions["acos"] = c99fn("acos", ("ushort",), "ushort")
        self.functions["acos"] = c99fn("acos", ("ushort2",), "ushort2")
        self.functions["acos"] = c99fn("acos", ("ushort4",), "ushort4")
        self.functions["acos"] = c99fn("acos", ("ushort8",), "ushort8")
        self.functions["acos"] = c99fn("acos", ("ushort16",), "ushort16")
        self.functions["acos"] = c99fn("acos", ("int",), "int")
        self.functions["acos"] = c99fn("acos", ("int2",), "int2")
        self.functions["acos"] = c99fn("acos", ("int4",), "int4")
        self.functions["acos"] = c99fn("acos", ("int8",), "int8")
        self.functions["acos"] = c99fn("acos", ("int16",), "int16")
        self.functions["acos"] = c99fn("acos", ("uint",), "uint")
        self.functions["acos"] = c99fn("acos", ("uint2",), "uint2")
        self.functions["acos"] = c99fn("acos", ("uint4",), "uint4")
        self.functions["acos"] = c99fn("acos", ("uint8",), "uint8")
        self.functions["acos"] = c99fn("acos", ("uint16",), "uint16")
        self.functions["acos"] = c99fn("acos", ("long",), "long")
        self.functions["acos"] = c99fn("acos", ("long2",), "long2")
        self.functions["acos"] = c99fn("acos", ("long4",), "long4")
        self.functions["acos"] = c99fn("acos", ("long8",), "long8")
        self.functions["acos"] = c99fn("acos", ("long16",), "long16")
        self.functions["acos"] = c99fn("acos", ("ulong",), "ulong")
        self.functions["acos"] = c99fn("acos", ("ulong2",), "ulong2")
        self.functions["acos"] = c99fn("acos", ("ulong4",), "ulong4")
        self.functions["acos"] = c99fn("acos", ("ulong8",), "ulong8")
        self.functions["acos"] = c99fn("acos", ("ulong16",), "ulong16")
        self.functions["acosh"] = c99fn("acosh", ("char",), "char")
        self.functions["acosh"] = c99fn("acosh", ("char2",), "char2")
        self.functions["acosh"] = c99fn("acosh", ("char4",), "char4")
        self.functions["acosh"] = c99fn("acosh", ("char8",), "char8")
        self.functions["acosh"] = c99fn("acosh", ("char16",), "char16")
        self.functions["acosh"] = c99fn("acosh", ("uchar",), "uchar")
        self.functions["acosh"] = c99fn("acosh", ("uchar2",), "uchar2")
        self.functions["acosh"] = c99fn("acosh", ("uchar4",), "uchar4")
        self.functions["acosh"] = c99fn("acosh", ("uchar8",), "uchar8")
        self.functions["acosh"] = c99fn("acosh", ("uchar16",), "uchar16")
        self.functions["acosh"] = c99fn("acosh", ("short",), "short")
        self.functions["acosh"] = c99fn("acosh", ("short2",), "short2")
        self.functions["acosh"] = c99fn("acosh", ("short4",), "short4")
        self.functions["acosh"] = c99fn("acosh", ("short8",), "short8")
        self.functions["acosh"] = c99fn("acosh", ("short16",), "short16")
        self.functions["acosh"] = c99fn("acosh", ("ushort",), "ushort")
        self.functions["acosh"] = c99fn("acosh", ("ushort2",), "ushort2")
        self.functions["acosh"] = c99fn("acosh", ("ushort4",), "ushort4")
        self.functions["acosh"] = c99fn("acosh", ("ushort8",), "ushort8")
        self.functions["acosh"] = c99fn("acosh", ("ushort16",), "ushort16")
        self.functions["acosh"] = c99fn("acosh", ("int",), "int")
        self.functions["acosh"] = c99fn("acosh", ("int2",), "int2")
        self.functions["acosh"] = c99fn("acosh", ("int4",), "int4")
        self.functions["acosh"] = c99fn("acosh", ("int8",), "int8")
        self.functions["acosh"] = c99fn("acosh", ("int16",), "int16")
        self.functions["acosh"] = c99fn("acosh", ("uint",), "uint")
        self.functions["acosh"] = c99fn("acosh", ("uint2",), "uint2")
        self.functions["acosh"] = c99fn("acosh", ("uint4",), "uint4")
        self.functions["acosh"] = c99fn("acosh", ("uint8",), "uint8")
        self.functions["acosh"] = c99fn("acosh", ("uint16",), "uint16")
        self.functions["acosh"] = c99fn("acosh", ("long",), "long")
        self.functions["acosh"] = c99fn("acosh", ("long2",), "long2")
        self.functions["acosh"] = c99fn("acosh", ("long4",), "long4")
        self.functions["acosh"] = c99fn("acosh", ("long8",), "long8")
        self.functions["acosh"] = c99fn("acosh", ("long16",), "long16")
        self.functions["acosh"] = c99fn("acosh", ("ulong",), "ulong")
        self.functions["acosh"] = c99fn("acosh", ("ulong2",), "ulong2")
        self.functions["acosh"] = c99fn("acosh", ("ulong4",), "ulong4")
        self.functions["acosh"] = c99fn("acosh", ("ulong8",), "ulong8")
        self.functions["acosh"] = c99fn("acosh", ("ulong16",), "ulong16")
        self.functions["acospi"] = c99fn("acospi", ("char",), "char")
        self.functions["acospi"] = c99fn("acospi", ("char2",), "char2")
        self.functions["acospi"] = c99fn("acospi", ("char4",), "char4")
        self.functions["acospi"] = c99fn("acospi", ("char8",), "char8")
        self.functions["acospi"] = c99fn("acospi", ("char16",), "char16")
        self.functions["acospi"] = c99fn("acospi", ("uchar",), "uchar")
        self.functions["acospi"] = c99fn("acospi", ("uchar2",), "uchar2")
        self.functions["acospi"] = c99fn("acospi", ("uchar4",), "uchar4")
        self.functions["acospi"] = c99fn("acospi", ("uchar8",), "uchar8")
        self.functions["acospi"] = c99fn("acospi", ("uchar16",), "uchar16")
        self.functions["acospi"] = c99fn("acospi", ("short",), "short")
        self.functions["acospi"] = c99fn("acospi", ("short2",), "short2")
        self.functions["acospi"] = c99fn("acospi", ("short4",), "short4")
        self.functions["acospi"] = c99fn("acospi", ("short8",), "short8")
        self.functions["acospi"] = c99fn("acospi", ("short16",), "short16")
        self.functions["acospi"] = c99fn("acospi", ("ushort",), "ushort")
        self.functions["acospi"] = c99fn("acospi", ("ushort2",), "ushort2")
        self.functions["acospi"] = c99fn("acospi", ("ushort4",), "ushort4")
        self.functions["acospi"] = c99fn("acospi", ("ushort8",), "ushort8")
        self.functions["acospi"] = c99fn("acospi", ("ushort16",), "ushort16")
        self.functions["acospi"] = c99fn("acospi", ("int",), "int")
        self.functions["acospi"] = c99fn("acospi", ("int2",), "int2")
        self.functions["acospi"] = c99fn("acospi", ("int4",), "int4")
        self.functions["acospi"] = c99fn("acospi", ("int8",), "int8")
        self.functions["acospi"] = c99fn("acospi", ("int16",), "int16")
        self.functions["acospi"] = c99fn("acospi", ("uint",), "uint")
        self.functions["acospi"] = c99fn("acospi", ("uint2",), "uint2")
        self.functions["acospi"] = c99fn("acospi", ("uint4",), "uint4")
        self.functions["acospi"] = c99fn("acospi", ("uint8",), "uint8")
        self.functions["acospi"] = c99fn("acospi", ("uint16",), "uint16")
        self.functions["acospi"] = c99fn("acospi", ("long",), "long")
        self.functions["acospi"] = c99fn("acospi", ("long2",), "long2")
        self.functions["acospi"] = c99fn("acospi", ("long4",), "long4")
        self.functions["acospi"] = c99fn("acospi", ("long8",), "long8")
        self.functions["acospi"] = c99fn("acospi", ("long16",), "long16")
        self.functions["acospi"] = c99fn("acospi", ("ulong",), "ulong")
        self.functions["acospi"] = c99fn("acospi", ("ulong2",), "ulong2")
        self.functions["acospi"] = c99fn("acospi", ("ulong4",), "ulong4")
        self.functions["acospi"] = c99fn("acospi", ("ulong8",), "ulong8")
        self.functions["acospi"] = c99fn("acospi", ("ulong16",), "ulong16")
        self.functions["atan"] = c99fn("atan", ("char",), "char")
        self.functions["atan"] = c99fn("atan", ("char2",), "char2")
        self.functions["atan"] = c99fn("atan", ("char4",), "char4")
        self.functions["atan"] = c99fn("atan", ("char8",), "char8")
        self.functions["atan"] = c99fn("atan", ("char16",), "char16")
        self.functions["atan"] = c99fn("atan", ("uchar",), "uchar")
        self.functions["atan"] = c99fn("atan", ("uchar2",), "uchar2")
        self.functions["atan"] = c99fn("atan", ("uchar4",), "uchar4")
        self.functions["atan"] = c99fn("atan", ("uchar8",), "uchar8")
        self.functions["atan"] = c99fn("atan", ("uchar16",), "uchar16")
        self.functions["atan"] = c99fn("atan", ("short",), "short")
        self.functions["atan"] = c99fn("atan", ("short2",), "short2")
        self.functions["atan"] = c99fn("atan", ("short4",), "short4")
        self.functions["atan"] = c99fn("atan", ("short8",), "short8")
        self.functions["atan"] = c99fn("atan", ("short16",), "short16")
        self.functions["atan"] = c99fn("atan", ("ushort",), "ushort")
        self.functions["atan"] = c99fn("atan", ("ushort2",), "ushort2")
        self.functions["atan"] = c99fn("atan", ("ushort4",), "ushort4")
        self.functions["atan"] = c99fn("atan", ("ushort8",), "ushort8")
        self.functions["atan"] = c99fn("atan", ("ushort16",), "ushort16")
        self.functions["atan"] = c99fn("atan", ("int",), "int")
        self.functions["atan"] = c99fn("atan", ("int2",), "int2")
        self.functions["atan"] = c99fn("atan", ("int4",), "int4")
        self.functions["atan"] = c99fn("atan", ("int8",), "int8")
        self.functions["atan"] = c99fn("atan", ("int16",), "int16")
        self.functions["atan"] = c99fn("atan", ("uint",), "uint")
        self.functions["atan"] = c99fn("atan", ("uint2",), "uint2")
        self.functions["atan"] = c99fn("atan", ("uint4",), "uint4")
        self.functions["atan"] = c99fn("atan", ("uint8",), "uint8")
        self.functions["atan"] = c99fn("atan", ("uint16",), "uint16")
        self.functions["atan"] = c99fn("atan", ("long",), "long")
        self.functions["atan"] = c99fn("atan", ("long2",), "long2")
        self.functions["atan"] = c99fn("atan", ("long4",), "long4")
        self.functions["atan"] = c99fn("atan", ("long8",), "long8")
        self.functions["atan"] = c99fn("atan", ("long16",), "long16")
        self.functions["atan"] = c99fn("atan", ("ulong",), "ulong")
        self.functions["atan"] = c99fn("atan", ("ulong2",), "ulong2")
        self.functions["atan"] = c99fn("atan", ("ulong4",), "ulong4")
        self.functions["atan"] = c99fn("atan", ("ulong8",), "ulong8")
        self.functions["atan"] = c99fn("atan", ("ulong16",), "ulong16")
        self.functions["atan2"] = c99fn("atan2", ("char","char",), "char")
        self.functions["atan2"] = c99fn("atan2", ("char2","char2",), "char2")
        self.functions["atan2"] = c99fn("atan2", ("char4","char4",), "char4")
        self.functions["atan2"] = c99fn("atan2", ("char8","char8",), "char8")
        self.functions["atan2"] = c99fn("atan2", ("char16","char16",), "char16")
        self.functions["atan2"] = c99fn("atan2", ("uchar","uchar",), "uchar")
        self.functions["atan2"] = c99fn("atan2", ("uchar2","uchar2",), "uchar2")
        self.functions["atan2"] = c99fn("atan2", ("uchar4","uchar4",), "uchar4")
        self.functions["atan2"] = c99fn("atan2", ("uchar8","uchar8",), "uchar8")
        self.functions["atan2"] = c99fn("atan2", ("uchar16","uchar16",), "uchar16")
        self.functions["atan2"] = c99fn("atan2", ("short","short",), "short")
        self.functions["atan2"] = c99fn("atan2", ("short2","short2",), "short2")
        self.functions["atan2"] = c99fn("atan2", ("short4","short4",), "short4")
        self.functions["atan2"] = c99fn("atan2", ("short8","short8",), "short8")
        self.functions["atan2"] = c99fn("atan2", ("short16","short16",), "short16")
        self.functions["atan2"] = c99fn("atan2", ("ushort","ushort",), "ushort")
        self.functions["atan2"] = c99fn("atan2", ("ushort2","ushort2",), "ushort2")
        self.functions["atan2"] = c99fn("atan2", ("ushort4","ushort4",), "ushort4")
        self.functions["atan2"] = c99fn("atan2", ("ushort8","ushort8",), "ushort8")
        self.functions["atan2"] = c99fn("atan2", ("ushort16","ushort16",), "ushort16")
        self.functions["atan2"] = c99fn("atan2", ("int","int",), "int")
        self.functions["atan2"] = c99fn("atan2", ("int2","int2",), "int2")
        self.functions["atan2"] = c99fn("atan2", ("int4","int4",), "int4")
        self.functions["atan2"] = c99fn("atan2", ("int8","int8",), "int8")
        self.functions["atan2"] = c99fn("atan2", ("int16","int16",), "int16")
        self.functions["atan2"] = c99fn("atan2", ("uint","uint",), "uint")
        self.functions["atan2"] = c99fn("atan2", ("uint2","uint2",), "uint2")
        self.functions["atan2"] = c99fn("atan2", ("uint4","uint4",), "uint4")
        self.functions["atan2"] = c99fn("atan2", ("uint8","uint8",), "uint8")
        self.functions["atan2"] = c99fn("atan2", ("uint16","uint16",), "uint16")
        self.functions["atan2"] = c99fn("atan2", ("long","long",), "long")
        self.functions["atan2"] = c99fn("atan2", ("long2","long2",), "long2")
        self.functions["atan2"] = c99fn("atan2", ("long4","long4",), "long4")
        self.functions["atan2"] = c99fn("atan2", ("long8","long8",), "long8")
        self.functions["atan2"] = c99fn("atan2", ("long16","long16",), "long16")
        self.functions["atan2"] = c99fn("atan2", ("ulong","ulong",), "ulong")
        self.functions["atan2"] = c99fn("atan2", ("ulong2","ulong2",), "ulong2")
        self.functions["atan2"] = c99fn("atan2", ("ulong4","ulong4",), "ulong4")
        self.functions["atan2"] = c99fn("atan2", ("ulong8","ulong8",), "ulong8")
        self.functions["atan2"] = c99fn("atan2", ("ulong16","ulong16",), "ulong16")
        self.functions["atanh"] = c99fn("atanh", ("char",), "char")
        self.functions["atanh"] = c99fn("atanh", ("char2",), "char2")
        self.functions["atanh"] = c99fn("atanh", ("char4",), "char4")
        self.functions["atanh"] = c99fn("atanh", ("char8",), "char8")
        self.functions["atanh"] = c99fn("atanh", ("char16",), "char16")
        self.functions["atanh"] = c99fn("atanh", ("uchar",), "uchar")
        self.functions["atanh"] = c99fn("atanh", ("uchar2",), "uchar2")
        self.functions["atanh"] = c99fn("atanh", ("uchar4",), "uchar4")
        self.functions["atanh"] = c99fn("atanh", ("uchar8",), "uchar8")
        self.functions["atanh"] = c99fn("atanh", ("uchar16",), "uchar16")
        self.functions["atanh"] = c99fn("atanh", ("short",), "short")
        self.functions["atanh"] = c99fn("atanh", ("short2",), "short2")
        self.functions["atanh"] = c99fn("atanh", ("short4",), "short4")
        self.functions["atanh"] = c99fn("atanh", ("short8",), "short8")
        self.functions["atanh"] = c99fn("atanh", ("short16",), "short16")
        self.functions["atanh"] = c99fn("atanh", ("ushort",), "ushort")
        self.functions["atanh"] = c99fn("atanh", ("ushort2",), "ushort2")
        self.functions["atanh"] = c99fn("atanh", ("ushort4",), "ushort4")
        self.functions["atanh"] = c99fn("atanh", ("ushort8",), "ushort8")
        self.functions["atanh"] = c99fn("atanh", ("ushort16",), "ushort16")
        self.functions["atanh"] = c99fn("atanh", ("int",), "int")
        self.functions["atanh"] = c99fn("atanh", ("int2",), "int2")
        self.functions["atanh"] = c99fn("atanh", ("int4",), "int4")
        self.functions["atanh"] = c99fn("atanh", ("int8",), "int8")
        self.functions["atanh"] = c99fn("atanh", ("int16",), "int16")
        self.functions["atanh"] = c99fn("atanh", ("uint",), "uint")
        self.functions["atanh"] = c99fn("atanh", ("uint2",), "uint2")
        self.functions["atanh"] = c99fn("atanh", ("uint4",), "uint4")
        self.functions["atanh"] = c99fn("atanh", ("uint8",), "uint8")
        self.functions["atanh"] = c99fn("atanh", ("uint16",), "uint16")
        self.functions["atanh"] = c99fn("atanh", ("long",), "long")
        self.functions["atanh"] = c99fn("atanh", ("long2",), "long2")
        self.functions["atanh"] = c99fn("atanh", ("long4",), "long4")
        self.functions["atanh"] = c99fn("atanh", ("long8",), "long8")
        self.functions["atanh"] = c99fn("atanh", ("long16",), "long16")
        self.functions["atanh"] = c99fn("atanh", ("ulong",), "ulong")
        self.functions["atanh"] = c99fn("atanh", ("ulong2",), "ulong2")
        self.functions["atanh"] = c99fn("atanh", ("ulong4",), "ulong4")
        self.functions["atanh"] = c99fn("atanh", ("ulong8",), "ulong8")
        self.functions["atanh"] = c99fn("atanh", ("ulong16",), "ulong16")
        self.functions["atanpi"] = c99fn("atanpi", ("char",), "char")
        self.functions["atanpi"] = c99fn("atanpi", ("char2",), "char2")
        self.functions["atanpi"] = c99fn("atanpi", ("char4",), "char4")
        self.functions["atanpi"] = c99fn("atanpi", ("char8",), "char8")
        self.functions["atanpi"] = c99fn("atanpi", ("char16",), "char16")
        self.functions["atanpi"] = c99fn("atanpi", ("uchar",), "uchar")
        self.functions["atanpi"] = c99fn("atanpi", ("uchar2",), "uchar2")
        self.functions["atanpi"] = c99fn("atanpi", ("uchar4",), "uchar4")
        self.functions["atanpi"] = c99fn("atanpi", ("uchar8",), "uchar8")
        self.functions["atanpi"] = c99fn("atanpi", ("uchar16",), "uchar16")
        self.functions["atanpi"] = c99fn("atanpi", ("short",), "short")
        self.functions["atanpi"] = c99fn("atanpi", ("short2",), "short2")
        self.functions["atanpi"] = c99fn("atanpi", ("short4",), "short4")
        self.functions["atanpi"] = c99fn("atanpi", ("short8",), "short8")
        self.functions["atanpi"] = c99fn("atanpi", ("short16",), "short16")
        self.functions["atanpi"] = c99fn("atanpi", ("ushort",), "ushort")
        self.functions["atanpi"] = c99fn("atanpi", ("ushort2",), "ushort2")
        self.functions["atanpi"] = c99fn("atanpi", ("ushort4",), "ushort4")
        self.functions["atanpi"] = c99fn("atanpi", ("ushort8",), "ushort8")
        self.functions["atanpi"] = c99fn("atanpi", ("ushort16",), "ushort16")
        self.functions["atanpi"] = c99fn("atanpi", ("int",), "int")
        self.functions["atanpi"] = c99fn("atanpi", ("int2",), "int2")
        self.functions["atanpi"] = c99fn("atanpi", ("int4",), "int4")
        self.functions["atanpi"] = c99fn("atanpi", ("int8",), "int8")
        self.functions["atanpi"] = c99fn("atanpi", ("int16",), "int16")
        self.functions["atanpi"] = c99fn("atanpi", ("uint",), "uint")
        self.functions["atanpi"] = c99fn("atanpi", ("uint2",), "uint2")
        self.functions["atanpi"] = c99fn("atanpi", ("uint4",), "uint4")
        self.functions["atanpi"] = c99fn("atanpi", ("uint8",), "uint8")
        self.functions["atanpi"] = c99fn("atanpi", ("uint16",), "uint16")
        self.functions["atanpi"] = c99fn("atanpi", ("long",), "long")
        self.functions["atanpi"] = c99fn("atanpi", ("long2",), "long2")
        self.functions["atanpi"] = c99fn("atanpi", ("long4",), "long4")
        self.functions["atanpi"] = c99fn("atanpi", ("long8",), "long8")
        self.functions["atanpi"] = c99fn("atanpi", ("long16",), "long16")
        self.functions["atanpi"] = c99fn("atanpi", ("ulong",), "ulong")
        self.functions["atanpi"] = c99fn("atanpi", ("ulong2",), "ulong2")
        self.functions["atanpi"] = c99fn("atanpi", ("ulong4",), "ulong4")
        self.functions["atanpi"] = c99fn("atanpi", ("ulong8",), "ulong8")
        self.functions["atanpi"] = c99fn("atanpi", ("ulong16",), "ulong16")
        self.functions["atan2pi"] = c99fn("atan2pi", ("char","char",), "char")
        self.functions["atan2pi"] = c99fn("atan2pi", ("char2","char2",), "char2")
        self.functions["atan2pi"] = c99fn("atan2pi", ("char4","char4",), "char4")
        self.functions["atan2pi"] = c99fn("atan2pi", ("char8","char8",), "char8")
        self.functions["atan2pi"] = c99fn("atan2pi", ("char16","char16",), "char16")
        self.functions["atan2pi"] = c99fn("atan2pi", ("uchar","uchar",), "uchar")
        self.functions["atan2pi"] = c99fn("atan2pi", ("uchar2","uchar2",), "uchar2")
        self.functions["atan2pi"] = c99fn("atan2pi", ("uchar4","uchar4",), "uchar4")
        self.functions["atan2pi"] = c99fn("atan2pi", ("uchar8","uchar8",), "uchar8")
        self.functions["atan2pi"] = c99fn("atan2pi", ("uchar16","uchar16",), "uchar16")
        self.functions["atan2pi"] = c99fn("atan2pi", ("short","short",), "short")
        self.functions["atan2pi"] = c99fn("atan2pi", ("short2","short2",), "short2")
        self.functions["atan2pi"] = c99fn("atan2pi", ("short4","short4",), "short4")
        self.functions["atan2pi"] = c99fn("atan2pi", ("short8","short8",), "short8")
        self.functions["atan2pi"] = c99fn("atan2pi", ("short16","short16",), "short16")
        self.functions["atan2pi"] = c99fn("atan2pi", ("ushort","ushort",), "ushort")
        self.functions["atan2pi"] = c99fn("atan2pi", ("ushort2","ushort2",), "ushort2")
        self.functions["atan2pi"] = c99fn("atan2pi", ("ushort4","ushort4",), "ushort4")
        self.functions["atan2pi"] = c99fn("atan2pi", ("ushort8","ushort8",), "ushort8")
        self.functions["atan2pi"] = c99fn("atan2pi", ("ushort16","ushort16",), "ushort16")
        self.functions["atan2pi"] = c99fn("atan2pi", ("int","int",), "int")
        self.functions["atan2pi"] = c99fn("atan2pi", ("int2","int2",), "int2")
        self.functions["atan2pi"] = c99fn("atan2pi", ("int4","int4",), "int4")
        self.functions["atan2pi"] = c99fn("atan2pi", ("int8","int8",), "int8")
        self.functions["atan2pi"] = c99fn("atan2pi", ("int16","int16",), "int16")
        self.functions["atan2pi"] = c99fn("atan2pi", ("uint","uint",), "uint")
        self.functions["atan2pi"] = c99fn("atan2pi", ("uint2","uint2",), "uint2")
        self.functions["atan2pi"] = c99fn("atan2pi", ("uint4","uint4",), "uint4")
        self.functions["atan2pi"] = c99fn("atan2pi", ("uint8","uint8",), "uint8")
        self.functions["atan2pi"] = c99fn("atan2pi", ("uint16","uint16",), "uint16")
        self.functions["atan2pi"] = c99fn("atan2pi", ("long","long",), "long")
        self.functions["atan2pi"] = c99fn("atan2pi", ("long2","long2",), "long2")
        self.functions["atan2pi"] = c99fn("atan2pi", ("long4","long4",), "long4")
        self.functions["atan2pi"] = c99fn("atan2pi", ("long8","long8",), "long8")
        self.functions["atan2pi"] = c99fn("atan2pi", ("long16","long16",), "long16")
        self.functions["atan2pi"] = c99fn("atan2pi", ("ulong","ulong",), "ulong")
        self.functions["atan2pi"] = c99fn("atan2pi", ("ulong2","ulong2",), "ulong2")
        self.functions["atan2pi"] = c99fn("atan2pi", ("ulong4","ulong4",), "ulong4")
        self.functions["atan2pi"] = c99fn("atan2pi", ("ulong8","ulong8",), "ulong8")
        self.functions["atan2pi"] = c99fn("atan2pi", ("ulong16","ulong16",), "ulong16")
        self.functions["cbry"] = c99fn("cbry", ("char",), "char")
        self.functions["cbry"] = c99fn("cbry", ("char2",), "char2")
        self.functions["cbry"] = c99fn("cbry", ("char4",), "char4")
        self.functions["cbry"] = c99fn("cbry", ("char8",), "char8")
        self.functions["cbry"] = c99fn("cbry", ("char16",), "char16")
        self.functions["cbry"] = c99fn("cbry", ("uchar",), "uchar")
        self.functions["cbry"] = c99fn("cbry", ("uchar2",), "uchar2")
        self.functions["cbry"] = c99fn("cbry", ("uchar4",), "uchar4")
        self.functions["cbry"] = c99fn("cbry", ("uchar8",), "uchar8")
        self.functions["cbry"] = c99fn("cbry", ("uchar16",), "uchar16")
        self.functions["cbry"] = c99fn("cbry", ("short",), "short")
        self.functions["cbry"] = c99fn("cbry", ("short2",), "short2")
        self.functions["cbry"] = c99fn("cbry", ("short4",), "short4")
        self.functions["cbry"] = c99fn("cbry", ("short8",), "short8")
        self.functions["cbry"] = c99fn("cbry", ("short16",), "short16")
        self.functions["cbry"] = c99fn("cbry", ("ushort",), "ushort")
        self.functions["cbry"] = c99fn("cbry", ("ushort2",), "ushort2")
        self.functions["cbry"] = c99fn("cbry", ("ushort4",), "ushort4")
        self.functions["cbry"] = c99fn("cbry", ("ushort8",), "ushort8")
        self.functions["cbry"] = c99fn("cbry", ("ushort16",), "ushort16")
        self.functions["cbry"] = c99fn("cbry", ("int",), "int")
        self.functions["cbry"] = c99fn("cbry", ("int2",), "int2")
        self.functions["cbry"] = c99fn("cbry", ("int4",), "int4")
        self.functions["cbry"] = c99fn("cbry", ("int8",), "int8")
        self.functions["cbry"] = c99fn("cbry", ("int16",), "int16")
        self.functions["cbry"] = c99fn("cbry", ("uint",), "uint")
        self.functions["cbry"] = c99fn("cbry", ("uint2",), "uint2")
        self.functions["cbry"] = c99fn("cbry", ("uint4",), "uint4")
        self.functions["cbry"] = c99fn("cbry", ("uint8",), "uint8")
        self.functions["cbry"] = c99fn("cbry", ("uint16",), "uint16")
        self.functions["cbry"] = c99fn("cbry", ("long",), "long")
        self.functions["cbry"] = c99fn("cbry", ("long2",), "long2")
        self.functions["cbry"] = c99fn("cbry", ("long4",), "long4")
        self.functions["cbry"] = c99fn("cbry", ("long8",), "long8")
        self.functions["cbry"] = c99fn("cbry", ("long16",), "long16")
        self.functions["cbry"] = c99fn("cbry", ("ulong",), "ulong")
        self.functions["cbry"] = c99fn("cbry", ("ulong2",), "ulong2")
        self.functions["cbry"] = c99fn("cbry", ("ulong4",), "ulong4")
        self.functions["cbry"] = c99fn("cbry", ("ulong8",), "ulong8")
        self.functions["cbry"] = c99fn("cbry", ("ulong16",), "ulong16")
        self.functions["ceil"] = c99fn("ceil", ("char",), "char")
        self.functions["ceil"] = c99fn("ceil", ("char2",), "char2")
        self.functions["ceil"] = c99fn("ceil", ("char4",), "char4")
        self.functions["ceil"] = c99fn("ceil", ("char8",), "char8")
        self.functions["ceil"] = c99fn("ceil", ("char16",), "char16")
        self.functions["ceil"] = c99fn("ceil", ("uchar",), "uchar")
        self.functions["ceil"] = c99fn("ceil", ("uchar2",), "uchar2")
        self.functions["ceil"] = c99fn("ceil", ("uchar4",), "uchar4")
        self.functions["ceil"] = c99fn("ceil", ("uchar8",), "uchar8")
        self.functions["ceil"] = c99fn("ceil", ("uchar16",), "uchar16")
        self.functions["ceil"] = c99fn("ceil", ("short",), "short")
        self.functions["ceil"] = c99fn("ceil", ("short2",), "short2")
        self.functions["ceil"] = c99fn("ceil", ("short4",), "short4")
        self.functions["ceil"] = c99fn("ceil", ("short8",), "short8")
        self.functions["ceil"] = c99fn("ceil", ("short16",), "short16")
        self.functions["ceil"] = c99fn("ceil", ("ushort",), "ushort")
        self.functions["ceil"] = c99fn("ceil", ("ushort2",), "ushort2")
        self.functions["ceil"] = c99fn("ceil", ("ushort4",), "ushort4")
        self.functions["ceil"] = c99fn("ceil", ("ushort8",), "ushort8")
        self.functions["ceil"] = c99fn("ceil", ("ushort16",), "ushort16")
        self.functions["ceil"] = c99fn("ceil", ("int",), "int")
        self.functions["ceil"] = c99fn("ceil", ("int2",), "int2")
        self.functions["ceil"] = c99fn("ceil", ("int4",), "int4")
        self.functions["ceil"] = c99fn("ceil", ("int8",), "int8")
        self.functions["ceil"] = c99fn("ceil", ("int16",), "int16")
        self.functions["ceil"] = c99fn("ceil", ("uint",), "uint")
        self.functions["ceil"] = c99fn("ceil", ("uint2",), "uint2")
        self.functions["ceil"] = c99fn("ceil", ("uint4",), "uint4")
        self.functions["ceil"] = c99fn("ceil", ("uint8",), "uint8")
        self.functions["ceil"] = c99fn("ceil", ("uint16",), "uint16")
        self.functions["ceil"] = c99fn("ceil", ("long",), "long")
        self.functions["ceil"] = c99fn("ceil", ("long2",), "long2")
        self.functions["ceil"] = c99fn("ceil", ("long4",), "long4")
        self.functions["ceil"] = c99fn("ceil", ("long8",), "long8")
        self.functions["ceil"] = c99fn("ceil", ("long16",), "long16")
        self.functions["ceil"] = c99fn("ceil", ("ulong",), "ulong")
        self.functions["ceil"] = c99fn("ceil", ("ulong2",), "ulong2")
        self.functions["ceil"] = c99fn("ceil", ("ulong4",), "ulong4")
        self.functions["ceil"] = c99fn("ceil", ("ulong8",), "ulong8")
        self.functions["ceil"] = c99fn("ceil", ("ulong16",), "ulong16")
        self.functions["copysign"] = c99fn("copysign", ("char","char",), "char")
        self.functions["copysign"] = c99fn("copysign", ("char2","char2",), "char2")
        self.functions["copysign"] = c99fn("copysign", ("char4","char4",), "char4")
        self.functions["copysign"] = c99fn("copysign", ("char8","char8",), "char8")
        self.functions["copysign"] = c99fn("copysign", ("char16","char16",), "char16")
        self.functions["copysign"] = c99fn("copysign", ("uchar","uchar",), "uchar")
        self.functions["copysign"] = c99fn("copysign", ("uchar2","uchar2",), "uchar2")
        self.functions["copysign"] = c99fn("copysign", ("uchar4","uchar4",), "uchar4")
        self.functions["copysign"] = c99fn("copysign", ("uchar8","uchar8",), "uchar8")
        self.functions["copysign"] = c99fn("copysign", ("uchar16","uchar16",), "uchar16")
        self.functions["copysign"] = c99fn("copysign", ("short","short",), "short")
        self.functions["copysign"] = c99fn("copysign", ("short2","short2",), "short2")
        self.functions["copysign"] = c99fn("copysign", ("short4","short4",), "short4")
        self.functions["copysign"] = c99fn("copysign", ("short8","short8",), "short8")
        self.functions["copysign"] = c99fn("copysign", ("short16","short16",), "short16")
        self.functions["copysign"] = c99fn("copysign", ("ushort","ushort",), "ushort")
        self.functions["copysign"] = c99fn("copysign", ("ushort2","ushort2",), "ushort2")
        self.functions["copysign"] = c99fn("copysign", ("ushort4","ushort4",), "ushort4")
        self.functions["copysign"] = c99fn("copysign", ("ushort8","ushort8",), "ushort8")
        self.functions["copysign"] = c99fn("copysign", ("ushort16","ushort16",), "ushort16")
        self.functions["copysign"] = c99fn("copysign", ("int","int",), "int")
        self.functions["copysign"] = c99fn("copysign", ("int2","int2",), "int2")
        self.functions["copysign"] = c99fn("copysign", ("int4","int4",), "int4")
        self.functions["copysign"] = c99fn("copysign", ("int8","int8",), "int8")
        self.functions["copysign"] = c99fn("copysign", ("int16","int16",), "int16")
        self.functions["copysign"] = c99fn("copysign", ("uint","uint",), "uint")
        self.functions["copysign"] = c99fn("copysign", ("uint2","uint2",), "uint2")
        self.functions["copysign"] = c99fn("copysign", ("uint4","uint4",), "uint4")
        self.functions["copysign"] = c99fn("copysign", ("uint8","uint8",), "uint8")
        self.functions["copysign"] = c99fn("copysign", ("uint16","uint16",), "uint16")
        self.functions["copysign"] = c99fn("copysign", ("long","long",), "long")
        self.functions["copysign"] = c99fn("copysign", ("long2","long2",), "long2")
        self.functions["copysign"] = c99fn("copysign", ("long4","long4",), "long4")
        self.functions["copysign"] = c99fn("copysign", ("long8","long8",), "long8")
        self.functions["copysign"] = c99fn("copysign", ("long16","long16",), "long16")
        self.functions["copysign"] = c99fn("copysign", ("ulong","ulong",), "ulong")
        self.functions["copysign"] = c99fn("copysign", ("ulong2","ulong2",), "ulong2")
        self.functions["copysign"] = c99fn("copysign", ("ulong4","ulong4",), "ulong4")
        self.functions["copysign"] = c99fn("copysign", ("ulong8","ulong8",), "ulong8")
        self.functions["copysign"] = c99fn("copysign", ("ulong16","ulong16",), "ulong16")
        self.functions["cos"] = c99fn("cos", ("char",), "char")
        self.functions["cos"] = c99fn("cos", ("char2",), "char2")
        self.functions["cos"] = c99fn("cos", ("char4",), "char4")
        self.functions["cos"] = c99fn("cos", ("char8",), "char8")
        self.functions["cos"] = c99fn("cos", ("char16",), "char16")
        self.functions["cos"] = c99fn("cos", ("uchar",), "uchar")
        self.functions["cos"] = c99fn("cos", ("uchar2",), "uchar2")
        self.functions["cos"] = c99fn("cos", ("uchar4",), "uchar4")
        self.functions["cos"] = c99fn("cos", ("uchar8",), "uchar8")
        self.functions["cos"] = c99fn("cos", ("uchar16",), "uchar16")
        self.functions["cos"] = c99fn("cos", ("short",), "short")
        self.functions["cos"] = c99fn("cos", ("short2",), "short2")
        self.functions["cos"] = c99fn("cos", ("short4",), "short4")
        self.functions["cos"] = c99fn("cos", ("short8",), "short8")
        self.functions["cos"] = c99fn("cos", ("short16",), "short16")
        self.functions["cos"] = c99fn("cos", ("ushort",), "ushort")
        self.functions["cos"] = c99fn("cos", ("ushort2",), "ushort2")
        self.functions["cos"] = c99fn("cos", ("ushort4",), "ushort4")
        self.functions["cos"] = c99fn("cos", ("ushort8",), "ushort8")
        self.functions["cos"] = c99fn("cos", ("ushort16",), "ushort16")
        self.functions["cos"] = c99fn("cos", ("int",), "int")
        self.functions["cos"] = c99fn("cos", ("int2",), "int2")
        self.functions["cos"] = c99fn("cos", ("int4",), "int4")
        self.functions["cos"] = c99fn("cos", ("int8",), "int8")
        self.functions["cos"] = c99fn("cos", ("int16",), "int16")
        self.functions["cos"] = c99fn("cos", ("uint",), "uint")
        self.functions["cos"] = c99fn("cos", ("uint2",), "uint2")
        self.functions["cos"] = c99fn("cos", ("uint4",), "uint4")
        self.functions["cos"] = c99fn("cos", ("uint8",), "uint8")
        self.functions["cos"] = c99fn("cos", ("uint16",), "uint16")
        self.functions["cos"] = c99fn("cos", ("long",), "long")
        self.functions["cos"] = c99fn("cos", ("long2",), "long2")
        self.functions["cos"] = c99fn("cos", ("long4",), "long4")
        self.functions["cos"] = c99fn("cos", ("long8",), "long8")
        self.functions["cos"] = c99fn("cos", ("long16",), "long16")
        self.functions["cos"] = c99fn("cos", ("ulong",), "ulong")
        self.functions["cos"] = c99fn("cos", ("ulong2",), "ulong2")
        self.functions["cos"] = c99fn("cos", ("ulong4",), "ulong4")
        self.functions["cos"] = c99fn("cos", ("ulong8",), "ulong8")
        self.functions["cos"] = c99fn("cos", ("ulong16",), "ulong16")
        self.functions["cosh"] = c99fn("cosh", ("char",), "char")
        self.functions["cosh"] = c99fn("cosh", ("char2",), "char2")
        self.functions["cosh"] = c99fn("cosh", ("char4",), "char4")
        self.functions["cosh"] = c99fn("cosh", ("char8",), "char8")
        self.functions["cosh"] = c99fn("cosh", ("char16",), "char16")
        self.functions["cosh"] = c99fn("cosh", ("uchar",), "uchar")
        self.functions["cosh"] = c99fn("cosh", ("uchar2",), "uchar2")
        self.functions["cosh"] = c99fn("cosh", ("uchar4",), "uchar4")
        self.functions["cosh"] = c99fn("cosh", ("uchar8",), "uchar8")
        self.functions["cosh"] = c99fn("cosh", ("uchar16",), "uchar16")
        self.functions["cosh"] = c99fn("cosh", ("short",), "short")
        self.functions["cosh"] = c99fn("cosh", ("short2",), "short2")
        self.functions["cosh"] = c99fn("cosh", ("short4",), "short4")
        self.functions["cosh"] = c99fn("cosh", ("short8",), "short8")
        self.functions["cosh"] = c99fn("cosh", ("short16",), "short16")
        self.functions["cosh"] = c99fn("cosh", ("ushort",), "ushort")
        self.functions["cosh"] = c99fn("cosh", ("ushort2",), "ushort2")
        self.functions["cosh"] = c99fn("cosh", ("ushort4",), "ushort4")
        self.functions["cosh"] = c99fn("cosh", ("ushort8",), "ushort8")
        self.functions["cosh"] = c99fn("cosh", ("ushort16",), "ushort16")
        self.functions["cosh"] = c99fn("cosh", ("int",), "int")
        self.functions["cosh"] = c99fn("cosh", ("int2",), "int2")
        self.functions["cosh"] = c99fn("cosh", ("int4",), "int4")
        self.functions["cosh"] = c99fn("cosh", ("int8",), "int8")
        self.functions["cosh"] = c99fn("cosh", ("int16",), "int16")
        self.functions["cosh"] = c99fn("cosh", ("uint",), "uint")
        self.functions["cosh"] = c99fn("cosh", ("uint2",), "uint2")
        self.functions["cosh"] = c99fn("cosh", ("uint4",), "uint4")
        self.functions["cosh"] = c99fn("cosh", ("uint8",), "uint8")
        self.functions["cosh"] = c99fn("cosh", ("uint16",), "uint16")
        self.functions["cosh"] = c99fn("cosh", ("long",), "long")
        self.functions["cosh"] = c99fn("cosh", ("long2",), "long2")
        self.functions["cosh"] = c99fn("cosh", ("long4",), "long4")
        self.functions["cosh"] = c99fn("cosh", ("long8",), "long8")
        self.functions["cosh"] = c99fn("cosh", ("long16",), "long16")
        self.functions["cosh"] = c99fn("cosh", ("ulong",), "ulong")
        self.functions["cosh"] = c99fn("cosh", ("ulong2",), "ulong2")
        self.functions["cosh"] = c99fn("cosh", ("ulong4",), "ulong4")
        self.functions["cosh"] = c99fn("cosh", ("ulong8",), "ulong8")
        self.functions["cosh"] = c99fn("cosh", ("ulong16",), "ulong16")
        self.functions["cospi"] = c99fn("cospi", ("char",), "char")
        self.functions["cospi"] = c99fn("cospi", ("char2",), "char2")
        self.functions["cospi"] = c99fn("cospi", ("char4",), "char4")
        self.functions["cospi"] = c99fn("cospi", ("char8",), "char8")
        self.functions["cospi"] = c99fn("cospi", ("char16",), "char16")
        self.functions["cospi"] = c99fn("cospi", ("uchar",), "uchar")
        self.functions["cospi"] = c99fn("cospi", ("uchar2",), "uchar2")
        self.functions["cospi"] = c99fn("cospi", ("uchar4",), "uchar4")
        self.functions["cospi"] = c99fn("cospi", ("uchar8",), "uchar8")
        self.functions["cospi"] = c99fn("cospi", ("uchar16",), "uchar16")
        self.functions["cospi"] = c99fn("cospi", ("short",), "short")
        self.functions["cospi"] = c99fn("cospi", ("short2",), "short2")
        self.functions["cospi"] = c99fn("cospi", ("short4",), "short4")
        self.functions["cospi"] = c99fn("cospi", ("short8",), "short8")
        self.functions["cospi"] = c99fn("cospi", ("short16",), "short16")
        self.functions["cospi"] = c99fn("cospi", ("ushort",), "ushort")
        self.functions["cospi"] = c99fn("cospi", ("ushort2",), "ushort2")
        self.functions["cospi"] = c99fn("cospi", ("ushort4",), "ushort4")
        self.functions["cospi"] = c99fn("cospi", ("ushort8",), "ushort8")
        self.functions["cospi"] = c99fn("cospi", ("ushort16",), "ushort16")
        self.functions["cospi"] = c99fn("cospi", ("int",), "int")
        self.functions["cospi"] = c99fn("cospi", ("int2",), "int2")
        self.functions["cospi"] = c99fn("cospi", ("int4",), "int4")
        self.functions["cospi"] = c99fn("cospi", ("int8",), "int8")
        self.functions["cospi"] = c99fn("cospi", ("int16",), "int16")
        self.functions["cospi"] = c99fn("cospi", ("uint",), "uint")
        self.functions["cospi"] = c99fn("cospi", ("uint2",), "uint2")
        self.functions["cospi"] = c99fn("cospi", ("uint4",), "uint4")
        self.functions["cospi"] = c99fn("cospi", ("uint8",), "uint8")
        self.functions["cospi"] = c99fn("cospi", ("uint16",), "uint16")
        self.functions["cospi"] = c99fn("cospi", ("long",), "long")
        self.functions["cospi"] = c99fn("cospi", ("long2",), "long2")
        self.functions["cospi"] = c99fn("cospi", ("long4",), "long4")
        self.functions["cospi"] = c99fn("cospi", ("long8",), "long8")
        self.functions["cospi"] = c99fn("cospi", ("long16",), "long16")
        self.functions["cospi"] = c99fn("cospi", ("ulong",), "ulong")
        self.functions["cospi"] = c99fn("cospi", ("ulong2",), "ulong2")
        self.functions["cospi"] = c99fn("cospi", ("ulong4",), "ulong4")
        self.functions["cospi"] = c99fn("cospi", ("ulong8",), "ulong8")
        self.functions["cospi"] = c99fn("cospi", ("ulong16",), "ulong16")
        self.functions["erfc"] = c99fn("erfc", ("char",), "char")
        self.functions["erfc"] = c99fn("erfc", ("char2",), "char2")
        self.functions["erfc"] = c99fn("erfc", ("char4",), "char4")
        self.functions["erfc"] = c99fn("erfc", ("char8",), "char8")
        self.functions["erfc"] = c99fn("erfc", ("char16",), "char16")
        self.functions["erfc"] = c99fn("erfc", ("uchar",), "uchar")
        self.functions["erfc"] = c99fn("erfc", ("uchar2",), "uchar2")
        self.functions["erfc"] = c99fn("erfc", ("uchar4",), "uchar4")
        self.functions["erfc"] = c99fn("erfc", ("uchar8",), "uchar8")
        self.functions["erfc"] = c99fn("erfc", ("uchar16",), "uchar16")
        self.functions["erfc"] = c99fn("erfc", ("short",), "short")
        self.functions["erfc"] = c99fn("erfc", ("short2",), "short2")
        self.functions["erfc"] = c99fn("erfc", ("short4",), "short4")
        self.functions["erfc"] = c99fn("erfc", ("short8",), "short8")
        self.functions["erfc"] = c99fn("erfc", ("short16",), "short16")
        self.functions["erfc"] = c99fn("erfc", ("ushort",), "ushort")
        self.functions["erfc"] = c99fn("erfc", ("ushort2",), "ushort2")
        self.functions["erfc"] = c99fn("erfc", ("ushort4",), "ushort4")
        self.functions["erfc"] = c99fn("erfc", ("ushort8",), "ushort8")
        self.functions["erfc"] = c99fn("erfc", ("ushort16",), "ushort16")
        self.functions["erfc"] = c99fn("erfc", ("int",), "int")
        self.functions["erfc"] = c99fn("erfc", ("int2",), "int2")
        self.functions["erfc"] = c99fn("erfc", ("int4",), "int4")
        self.functions["erfc"] = c99fn("erfc", ("int8",), "int8")
        self.functions["erfc"] = c99fn("erfc", ("int16",), "int16")
        self.functions["erfc"] = c99fn("erfc", ("uint",), "uint")
        self.functions["erfc"] = c99fn("erfc", ("uint2",), "uint2")
        self.functions["erfc"] = c99fn("erfc", ("uint4",), "uint4")
        self.functions["erfc"] = c99fn("erfc", ("uint8",), "uint8")
        self.functions["erfc"] = c99fn("erfc", ("uint16",), "uint16")
        self.functions["erfc"] = c99fn("erfc", ("long",), "long")
        self.functions["erfc"] = c99fn("erfc", ("long2",), "long2")
        self.functions["erfc"] = c99fn("erfc", ("long4",), "long4")
        self.functions["erfc"] = c99fn("erfc", ("long8",), "long8")
        self.functions["erfc"] = c99fn("erfc", ("long16",), "long16")
        self.functions["erfc"] = c99fn("erfc", ("ulong",), "ulong")
        self.functions["erfc"] = c99fn("erfc", ("ulong2",), "ulong2")
        self.functions["erfc"] = c99fn("erfc", ("ulong4",), "ulong4")
        self.functions["erfc"] = c99fn("erfc", ("ulong8",), "ulong8")
        self.functions["erfc"] = c99fn("erfc", ("ulong16",), "ulong16")
        self.functions["erf"] = c99fn("erf", ("char",), "char")
        self.functions["erf"] = c99fn("erf", ("char2",), "char2")
        self.functions["erf"] = c99fn("erf", ("char4",), "char4")
        self.functions["erf"] = c99fn("erf", ("char8",), "char8")
        self.functions["erf"] = c99fn("erf", ("char16",), "char16")
        self.functions["erf"] = c99fn("erf", ("uchar",), "uchar")
        self.functions["erf"] = c99fn("erf", ("uchar2",), "uchar2")
        self.functions["erf"] = c99fn("erf", ("uchar4",), "uchar4")
        self.functions["erf"] = c99fn("erf", ("uchar8",), "uchar8")
        self.functions["erf"] = c99fn("erf", ("uchar16",), "uchar16")
        self.functions["erf"] = c99fn("erf", ("short",), "short")
        self.functions["erf"] = c99fn("erf", ("short2",), "short2")
        self.functions["erf"] = c99fn("erf", ("short4",), "short4")
        self.functions["erf"] = c99fn("erf", ("short8",), "short8")
        self.functions["erf"] = c99fn("erf", ("short16",), "short16")
        self.functions["erf"] = c99fn("erf", ("ushort",), "ushort")
        self.functions["erf"] = c99fn("erf", ("ushort2",), "ushort2")
        self.functions["erf"] = c99fn("erf", ("ushort4",), "ushort4")
        self.functions["erf"] = c99fn("erf", ("ushort8",), "ushort8")
        self.functions["erf"] = c99fn("erf", ("ushort16",), "ushort16")
        self.functions["erf"] = c99fn("erf", ("int",), "int")
        self.functions["erf"] = c99fn("erf", ("int2",), "int2")
        self.functions["erf"] = c99fn("erf", ("int4",), "int4")
        self.functions["erf"] = c99fn("erf", ("int8",), "int8")
        self.functions["erf"] = c99fn("erf", ("int16",), "int16")
        self.functions["erf"] = c99fn("erf", ("uint",), "uint")
        self.functions["erf"] = c99fn("erf", ("uint2",), "uint2")
        self.functions["erf"] = c99fn("erf", ("uint4",), "uint4")
        self.functions["erf"] = c99fn("erf", ("uint8",), "uint8")
        self.functions["erf"] = c99fn("erf", ("uint16",), "uint16")
        self.functions["erf"] = c99fn("erf", ("long",), "long")
        self.functions["erf"] = c99fn("erf", ("long2",), "long2")
        self.functions["erf"] = c99fn("erf", ("long4",), "long4")
        self.functions["erf"] = c99fn("erf", ("long8",), "long8")
        self.functions["erf"] = c99fn("erf", ("long16",), "long16")
        self.functions["erf"] = c99fn("erf", ("ulong",), "ulong")
        self.functions["erf"] = c99fn("erf", ("ulong2",), "ulong2")
        self.functions["erf"] = c99fn("erf", ("ulong4",), "ulong4")
        self.functions["erf"] = c99fn("erf", ("ulong8",), "ulong8")
        self.functions["erf"] = c99fn("erf", ("ulong16",), "ulong16")
        self.functions["exp"] = c99fn("exp", ("char",), "char")
        self.functions["exp"] = c99fn("exp", ("char2",), "char2")
        self.functions["exp"] = c99fn("exp", ("char4",), "char4")
        self.functions["exp"] = c99fn("exp", ("char8",), "char8")
        self.functions["exp"] = c99fn("exp", ("char16",), "char16")
        self.functions["exp"] = c99fn("exp", ("uchar",), "uchar")
        self.functions["exp"] = c99fn("exp", ("uchar2",), "uchar2")
        self.functions["exp"] = c99fn("exp", ("uchar4",), "uchar4")
        self.functions["exp"] = c99fn("exp", ("uchar8",), "uchar8")
        self.functions["exp"] = c99fn("exp", ("uchar16",), "uchar16")
        self.functions["exp"] = c99fn("exp", ("short",), "short")
        self.functions["exp"] = c99fn("exp", ("short2",), "short2")
        self.functions["exp"] = c99fn("exp", ("short4",), "short4")
        self.functions["exp"] = c99fn("exp", ("short8",), "short8")
        self.functions["exp"] = c99fn("exp", ("short16",), "short16")
        self.functions["exp"] = c99fn("exp", ("ushort",), "ushort")
        self.functions["exp"] = c99fn("exp", ("ushort2",), "ushort2")
        self.functions["exp"] = c99fn("exp", ("ushort4",), "ushort4")
        self.functions["exp"] = c99fn("exp", ("ushort8",), "ushort8")
        self.functions["exp"] = c99fn("exp", ("ushort16",), "ushort16")
        self.functions["exp"] = c99fn("exp", ("int",), "int")
        self.functions["exp"] = c99fn("exp", ("int2",), "int2")
        self.functions["exp"] = c99fn("exp", ("int4",), "int4")
        self.functions["exp"] = c99fn("exp", ("int8",), "int8")
        self.functions["exp"] = c99fn("exp", ("int16",), "int16")
        self.functions["exp"] = c99fn("exp", ("uint",), "uint")
        self.functions["exp"] = c99fn("exp", ("uint2",), "uint2")
        self.functions["exp"] = c99fn("exp", ("uint4",), "uint4")
        self.functions["exp"] = c99fn("exp", ("uint8",), "uint8")
        self.functions["exp"] = c99fn("exp", ("uint16",), "uint16")
        self.functions["exp"] = c99fn("exp", ("long",), "long")
        self.functions["exp"] = c99fn("exp", ("long2",), "long2")
        self.functions["exp"] = c99fn("exp", ("long4",), "long4")
        self.functions["exp"] = c99fn("exp", ("long8",), "long8")
        self.functions["exp"] = c99fn("exp", ("long16",), "long16")
        self.functions["exp"] = c99fn("exp", ("ulong",), "ulong")
        self.functions["exp"] = c99fn("exp", ("ulong2",), "ulong2")
        self.functions["exp"] = c99fn("exp", ("ulong4",), "ulong4")
        self.functions["exp"] = c99fn("exp", ("ulong8",), "ulong8")
        self.functions["exp"] = c99fn("exp", ("ulong16",), "ulong16")
        self.functions["exp2"] = c99fn("exp2", ("char","char",), "char")
        self.functions["exp2"] = c99fn("exp2", ("char2","char2",), "char2")
        self.functions["exp2"] = c99fn("exp2", ("char4","char4",), "char4")
        self.functions["exp2"] = c99fn("exp2", ("char8","char8",), "char8")
        self.functions["exp2"] = c99fn("exp2", ("char16","char16",), "char16")
        self.functions["exp2"] = c99fn("exp2", ("uchar","uchar",), "uchar")
        self.functions["exp2"] = c99fn("exp2", ("uchar2","uchar2",), "uchar2")
        self.functions["exp2"] = c99fn("exp2", ("uchar4","uchar4",), "uchar4")
        self.functions["exp2"] = c99fn("exp2", ("uchar8","uchar8",), "uchar8")
        self.functions["exp2"] = c99fn("exp2", ("uchar16","uchar16",), "uchar16")
        self.functions["exp2"] = c99fn("exp2", ("short","short",), "short")
        self.functions["exp2"] = c99fn("exp2", ("short2","short2",), "short2")
        self.functions["exp2"] = c99fn("exp2", ("short4","short4",), "short4")
        self.functions["exp2"] = c99fn("exp2", ("short8","short8",), "short8")
        self.functions["exp2"] = c99fn("exp2", ("short16","short16",), "short16")
        self.functions["exp2"] = c99fn("exp2", ("ushort","ushort",), "ushort")
        self.functions["exp2"] = c99fn("exp2", ("ushort2","ushort2",), "ushort2")
        self.functions["exp2"] = c99fn("exp2", ("ushort4","ushort4",), "ushort4")
        self.functions["exp2"] = c99fn("exp2", ("ushort8","ushort8",), "ushort8")
        self.functions["exp2"] = c99fn("exp2", ("ushort16","ushort16",), "ushort16")
        self.functions["exp2"] = c99fn("exp2", ("int","int",), "int")
        self.functions["exp2"] = c99fn("exp2", ("int2","int2",), "int2")
        self.functions["exp2"] = c99fn("exp2", ("int4","int4",), "int4")
        self.functions["exp2"] = c99fn("exp2", ("int8","int8",), "int8")
        self.functions["exp2"] = c99fn("exp2", ("int16","int16",), "int16")
        self.functions["exp2"] = c99fn("exp2", ("uint","uint",), "uint")
        self.functions["exp2"] = c99fn("exp2", ("uint2","uint2",), "uint2")
        self.functions["exp2"] = c99fn("exp2", ("uint4","uint4",), "uint4")
        self.functions["exp2"] = c99fn("exp2", ("uint8","uint8",), "uint8")
        self.functions["exp2"] = c99fn("exp2", ("uint16","uint16",), "uint16")
        self.functions["exp2"] = c99fn("exp2", ("long","long",), "long")
        self.functions["exp2"] = c99fn("exp2", ("long2","long2",), "long2")
        self.functions["exp2"] = c99fn("exp2", ("long4","long4",), "long4")
        self.functions["exp2"] = c99fn("exp2", ("long8","long8",), "long8")
        self.functions["exp2"] = c99fn("exp2", ("long16","long16",), "long16")
        self.functions["exp2"] = c99fn("exp2", ("ulong","ulong",), "ulong")
        self.functions["exp2"] = c99fn("exp2", ("ulong2","ulong2",), "ulong2")
        self.functions["exp2"] = c99fn("exp2", ("ulong4","ulong4",), "ulong4")
        self.functions["exp2"] = c99fn("exp2", ("ulong8","ulong8",), "ulong8")
        self.functions["exp2"] = c99fn("exp2", ("ulong16","ulong16",), "ulong16")
        self.functions["exp10"] = c99fn("exp10", ("char",), "char")
        self.functions["exp10"] = c99fn("exp10", ("char2",), "char2")
        self.functions["exp10"] = c99fn("exp10", ("char4",), "char4")
        self.functions["exp10"] = c99fn("exp10", ("char8",), "char8")
        self.functions["exp10"] = c99fn("exp10", ("char16",), "char16")
        self.functions["exp10"] = c99fn("exp10", ("uchar",), "uchar")
        self.functions["exp10"] = c99fn("exp10", ("uchar2",), "uchar2")
        self.functions["exp10"] = c99fn("exp10", ("uchar4",), "uchar4")
        self.functions["exp10"] = c99fn("exp10", ("uchar8",), "uchar8")
        self.functions["exp10"] = c99fn("exp10", ("uchar16",), "uchar16")
        self.functions["exp10"] = c99fn("exp10", ("short",), "short")
        self.functions["exp10"] = c99fn("exp10", ("short2",), "short2")
        self.functions["exp10"] = c99fn("exp10", ("short4",), "short4")
        self.functions["exp10"] = c99fn("exp10", ("short8",), "short8")
        self.functions["exp10"] = c99fn("exp10", ("short16",), "short16")
        self.functions["exp10"] = c99fn("exp10", ("ushort",), "ushort")
        self.functions["exp10"] = c99fn("exp10", ("ushort2",), "ushort2")
        self.functions["exp10"] = c99fn("exp10", ("ushort4",), "ushort4")
        self.functions["exp10"] = c99fn("exp10", ("ushort8",), "ushort8")
        self.functions["exp10"] = c99fn("exp10", ("ushort16",), "ushort16")
        self.functions["exp10"] = c99fn("exp10", ("int",), "int")
        self.functions["exp10"] = c99fn("exp10", ("int2",), "int2")
        self.functions["exp10"] = c99fn("exp10", ("int4",), "int4")
        self.functions["exp10"] = c99fn("exp10", ("int8",), "int8")
        self.functions["exp10"] = c99fn("exp10", ("int16",), "int16")
        self.functions["exp10"] = c99fn("exp10", ("uint",), "uint")
        self.functions["exp10"] = c99fn("exp10", ("uint2",), "uint2")
        self.functions["exp10"] = c99fn("exp10", ("uint4",), "uint4")
        self.functions["exp10"] = c99fn("exp10", ("uint8",), "uint8")
        self.functions["exp10"] = c99fn("exp10", ("uint16",), "uint16")
        self.functions["exp10"] = c99fn("exp10", ("long",), "long")
        self.functions["exp10"] = c99fn("exp10", ("long2",), "long2")
        self.functions["exp10"] = c99fn("exp10", ("long4",), "long4")
        self.functions["exp10"] = c99fn("exp10", ("long8",), "long8")
        self.functions["exp10"] = c99fn("exp10", ("long16",), "long16")
        self.functions["exp10"] = c99fn("exp10", ("ulong",), "ulong")
        self.functions["exp10"] = c99fn("exp10", ("ulong2",), "ulong2")
        self.functions["exp10"] = c99fn("exp10", ("ulong4",), "ulong4")
        self.functions["exp10"] = c99fn("exp10", ("ulong8",), "ulong8")
        self.functions["exp10"] = c99fn("exp10", ("ulong16",), "ulong16")
        self.functions["expm1"] = c99fn("expm1", ("char",), "char")
        self.functions["expm1"] = c99fn("expm1", ("char2",), "char2")
        self.functions["expm1"] = c99fn("expm1", ("char4",), "char4")
        self.functions["expm1"] = c99fn("expm1", ("char8",), "char8")
        self.functions["expm1"] = c99fn("expm1", ("char16",), "char16")
        self.functions["expm1"] = c99fn("expm1", ("uchar",), "uchar")
        self.functions["expm1"] = c99fn("expm1", ("uchar2",), "uchar2")
        self.functions["expm1"] = c99fn("expm1", ("uchar4",), "uchar4")
        self.functions["expm1"] = c99fn("expm1", ("uchar8",), "uchar8")
        self.functions["expm1"] = c99fn("expm1", ("uchar16",), "uchar16")
        self.functions["expm1"] = c99fn("expm1", ("short",), "short")
        self.functions["expm1"] = c99fn("expm1", ("short2",), "short2")
        self.functions["expm1"] = c99fn("expm1", ("short4",), "short4")
        self.functions["expm1"] = c99fn("expm1", ("short8",), "short8")
        self.functions["expm1"] = c99fn("expm1", ("short16",), "short16")
        self.functions["expm1"] = c99fn("expm1", ("ushort",), "ushort")
        self.functions["expm1"] = c99fn("expm1", ("ushort2",), "ushort2")
        self.functions["expm1"] = c99fn("expm1", ("ushort4",), "ushort4")
        self.functions["expm1"] = c99fn("expm1", ("ushort8",), "ushort8")
        self.functions["expm1"] = c99fn("expm1", ("ushort16",), "ushort16")
        self.functions["expm1"] = c99fn("expm1", ("int",), "int")
        self.functions["expm1"] = c99fn("expm1", ("int2",), "int2")
        self.functions["expm1"] = c99fn("expm1", ("int4",), "int4")
        self.functions["expm1"] = c99fn("expm1", ("int8",), "int8")
        self.functions["expm1"] = c99fn("expm1", ("int16",), "int16")
        self.functions["expm1"] = c99fn("expm1", ("uint",), "uint")
        self.functions["expm1"] = c99fn("expm1", ("uint2",), "uint2")
        self.functions["expm1"] = c99fn("expm1", ("uint4",), "uint4")
        self.functions["expm1"] = c99fn("expm1", ("uint8",), "uint8")
        self.functions["expm1"] = c99fn("expm1", ("uint16",), "uint16")
        self.functions["expm1"] = c99fn("expm1", ("long",), "long")
        self.functions["expm1"] = c99fn("expm1", ("long2",), "long2")
        self.functions["expm1"] = c99fn("expm1", ("long4",), "long4")
        self.functions["expm1"] = c99fn("expm1", ("long8",), "long8")
        self.functions["expm1"] = c99fn("expm1", ("long16",), "long16")
        self.functions["expm1"] = c99fn("expm1", ("ulong",), "ulong")
        self.functions["expm1"] = c99fn("expm1", ("ulong2",), "ulong2")
        self.functions["expm1"] = c99fn("expm1", ("ulong4",), "ulong4")
        self.functions["expm1"] = c99fn("expm1", ("ulong8",), "ulong8")
        self.functions["expm1"] = c99fn("expm1", ("ulong16",), "ulong16")
        self.functions["fabs"] = c99fn("fabs", ("char",), "char")
        self.functions["fabs"] = c99fn("fabs", ("char2",), "char2")
        self.functions["fabs"] = c99fn("fabs", ("char4",), "char4")
        self.functions["fabs"] = c99fn("fabs", ("char8",), "char8")
        self.functions["fabs"] = c99fn("fabs", ("char16",), "char16")
        self.functions["fabs"] = c99fn("fabs", ("uchar",), "uchar")
        self.functions["fabs"] = c99fn("fabs", ("uchar2",), "uchar2")
        self.functions["fabs"] = c99fn("fabs", ("uchar4",), "uchar4")
        self.functions["fabs"] = c99fn("fabs", ("uchar8",), "uchar8")
        self.functions["fabs"] = c99fn("fabs", ("uchar16",), "uchar16")
        self.functions["fabs"] = c99fn("fabs", ("short",), "short")
        self.functions["fabs"] = c99fn("fabs", ("short2",), "short2")
        self.functions["fabs"] = c99fn("fabs", ("short4",), "short4")
        self.functions["fabs"] = c99fn("fabs", ("short8",), "short8")
        self.functions["fabs"] = c99fn("fabs", ("short16",), "short16")
        self.functions["fabs"] = c99fn("fabs", ("ushort",), "ushort")
        self.functions["fabs"] = c99fn("fabs", ("ushort2",), "ushort2")
        self.functions["fabs"] = c99fn("fabs", ("ushort4",), "ushort4")
        self.functions["fabs"] = c99fn("fabs", ("ushort8",), "ushort8")
        self.functions["fabs"] = c99fn("fabs", ("ushort16",), "ushort16")
        self.functions["fabs"] = c99fn("fabs", ("int",), "int")
        self.functions["fabs"] = c99fn("fabs", ("int2",), "int2")
        self.functions["fabs"] = c99fn("fabs", ("int4",), "int4")
        self.functions["fabs"] = c99fn("fabs", ("int8",), "int8")
        self.functions["fabs"] = c99fn("fabs", ("int16",), "int16")
        self.functions["fabs"] = c99fn("fabs", ("uint",), "uint")
        self.functions["fabs"] = c99fn("fabs", ("uint2",), "uint2")
        self.functions["fabs"] = c99fn("fabs", ("uint4",), "uint4")
        self.functions["fabs"] = c99fn("fabs", ("uint8",), "uint8")
        self.functions["fabs"] = c99fn("fabs", ("uint16",), "uint16")
        self.functions["fabs"] = c99fn("fabs", ("long",), "long")
        self.functions["fabs"] = c99fn("fabs", ("long2",), "long2")
        self.functions["fabs"] = c99fn("fabs", ("long4",), "long4")
        self.functions["fabs"] = c99fn("fabs", ("long8",), "long8")
        self.functions["fabs"] = c99fn("fabs", ("long16",), "long16")
        self.functions["fabs"] = c99fn("fabs", ("ulong",), "ulong")
        self.functions["fabs"] = c99fn("fabs", ("ulong2",), "ulong2")
        self.functions["fabs"] = c99fn("fabs", ("ulong4",), "ulong4")
        self.functions["fabs"] = c99fn("fabs", ("ulong8",), "ulong8")
        self.functions["fabs"] = c99fn("fabs", ("ulong16",), "ulong16")
        self.functions["fdim"] = c99fn("fdim", ("char","char",), "char")
        self.functions["fdim"] = c99fn("fdim", ("char2","char2",), "char2")
        self.functions["fdim"] = c99fn("fdim", ("char4","char4",), "char4")
        self.functions["fdim"] = c99fn("fdim", ("char8","char8",), "char8")
        self.functions["fdim"] = c99fn("fdim", ("char16","char16",), "char16")
        self.functions["fdim"] = c99fn("fdim", ("uchar","uchar",), "uchar")
        self.functions["fdim"] = c99fn("fdim", ("uchar2","uchar2",), "uchar2")
        self.functions["fdim"] = c99fn("fdim", ("uchar4","uchar4",), "uchar4")
        self.functions["fdim"] = c99fn("fdim", ("uchar8","uchar8",), "uchar8")
        self.functions["fdim"] = c99fn("fdim", ("uchar16","uchar16",), "uchar16")
        self.functions["fdim"] = c99fn("fdim", ("short","short",), "short")
        self.functions["fdim"] = c99fn("fdim", ("short2","short2",), "short2")
        self.functions["fdim"] = c99fn("fdim", ("short4","short4",), "short4")
        self.functions["fdim"] = c99fn("fdim", ("short8","short8",), "short8")
        self.functions["fdim"] = c99fn("fdim", ("short16","short16",), "short16")
        self.functions["fdim"] = c99fn("fdim", ("ushort","ushort",), "ushort")
        self.functions["fdim"] = c99fn("fdim", ("ushort2","ushort2",), "ushort2")
        self.functions["fdim"] = c99fn("fdim", ("ushort4","ushort4",), "ushort4")
        self.functions["fdim"] = c99fn("fdim", ("ushort8","ushort8",), "ushort8")
        self.functions["fdim"] = c99fn("fdim", ("ushort16","ushort16",), "ushort16")
        self.functions["fdim"] = c99fn("fdim", ("int","int",), "int")
        self.functions["fdim"] = c99fn("fdim", ("int2","int2",), "int2")
        self.functions["fdim"] = c99fn("fdim", ("int4","int4",), "int4")
        self.functions["fdim"] = c99fn("fdim", ("int8","int8",), "int8")
        self.functions["fdim"] = c99fn("fdim", ("int16","int16",), "int16")
        self.functions["fdim"] = c99fn("fdim", ("uint","uint",), "uint")
        self.functions["fdim"] = c99fn("fdim", ("uint2","uint2",), "uint2")
        self.functions["fdim"] = c99fn("fdim", ("uint4","uint4",), "uint4")
        self.functions["fdim"] = c99fn("fdim", ("uint8","uint8",), "uint8")
        self.functions["fdim"] = c99fn("fdim", ("uint16","uint16",), "uint16")
        self.functions["fdim"] = c99fn("fdim", ("long","long",), "long")
        self.functions["fdim"] = c99fn("fdim", ("long2","long2",), "long2")
        self.functions["fdim"] = c99fn("fdim", ("long4","long4",), "long4")
        self.functions["fdim"] = c99fn("fdim", ("long8","long8",), "long8")
        self.functions["fdim"] = c99fn("fdim", ("long16","long16",), "long16")
        self.functions["fdim"] = c99fn("fdim", ("ulong","ulong",), "ulong")
        self.functions["fdim"] = c99fn("fdim", ("ulong2","ulong2",), "ulong2")
        self.functions["fdim"] = c99fn("fdim", ("ulong4","ulong4",), "ulong4")
        self.functions["fdim"] = c99fn("fdim", ("ulong8","ulong8",), "ulong8")
        self.functions["fdim"] = c99fn("fdim", ("ulong16","ulong16",), "ulong16")
        self.functions["floor"] = c99fn("floor", ("char",), "char")
        self.functions["floor"] = c99fn("floor", ("char2",), "char2")
        self.functions["floor"] = c99fn("floor", ("char4",), "char4")
        self.functions["floor"] = c99fn("floor", ("char8",), "char8")
        self.functions["floor"] = c99fn("floor", ("char16",), "char16")
        self.functions["floor"] = c99fn("floor", ("uchar",), "uchar")
        self.functions["floor"] = c99fn("floor", ("uchar2",), "uchar2")
        self.functions["floor"] = c99fn("floor", ("uchar4",), "uchar4")
        self.functions["floor"] = c99fn("floor", ("uchar8",), "uchar8")
        self.functions["floor"] = c99fn("floor", ("uchar16",), "uchar16")
        self.functions["floor"] = c99fn("floor", ("short",), "short")
        self.functions["floor"] = c99fn("floor", ("short2",), "short2")
        self.functions["floor"] = c99fn("floor", ("short4",), "short4")
        self.functions["floor"] = c99fn("floor", ("short8",), "short8")
        self.functions["floor"] = c99fn("floor", ("short16",), "short16")
        self.functions["floor"] = c99fn("floor", ("ushort",), "ushort")
        self.functions["floor"] = c99fn("floor", ("ushort2",), "ushort2")
        self.functions["floor"] = c99fn("floor", ("ushort4",), "ushort4")
        self.functions["floor"] = c99fn("floor", ("ushort8",), "ushort8")
        self.functions["floor"] = c99fn("floor", ("ushort16",), "ushort16")
        self.functions["floor"] = c99fn("floor", ("int",), "int")
        self.functions["floor"] = c99fn("floor", ("int2",), "int2")
        self.functions["floor"] = c99fn("floor", ("int4",), "int4")
        self.functions["floor"] = c99fn("floor", ("int8",), "int8")
        self.functions["floor"] = c99fn("floor", ("int16",), "int16")
        self.functions["floor"] = c99fn("floor", ("uint",), "uint")
        self.functions["floor"] = c99fn("floor", ("uint2",), "uint2")
        self.functions["floor"] = c99fn("floor", ("uint4",), "uint4")
        self.functions["floor"] = c99fn("floor", ("uint8",), "uint8")
        self.functions["floor"] = c99fn("floor", ("uint16",), "uint16")
        self.functions["floor"] = c99fn("floor", ("long",), "long")
        self.functions["floor"] = c99fn("floor", ("long2",), "long2")
        self.functions["floor"] = c99fn("floor", ("long4",), "long4")
        self.functions["floor"] = c99fn("floor", ("long8",), "long8")
        self.functions["floor"] = c99fn("floor", ("long16",), "long16")
        self.functions["floor"] = c99fn("floor", ("ulong",), "ulong")
        self.functions["floor"] = c99fn("floor", ("ulong2",), "ulong2")
        self.functions["floor"] = c99fn("floor", ("ulong4",), "ulong4")
        self.functions["floor"] = c99fn("floor", ("ulong8",), "ulong8")
        self.functions["floor"] = c99fn("floor", ("ulong16",), "ulong16")
        self.functions["fma"] = c99fn("fma", ("char","char","char",), "char")
        self.functions["fma"] = c99fn("fma", ("char2","char2","char2",), "char2")
        self.functions["fma"] = c99fn("fma", ("char4","char4","char4",), "char4")
        self.functions["fma"] = c99fn("fma", ("char8","char8","char8",), "char8")
        self.functions["fma"] = c99fn("fma", ("char16","char16","char16",), "char16")
        self.functions["fma"] = c99fn("fma", ("uchar","uchar","uchar",), "uchar")
        self.functions["fma"] = c99fn("fma", ("uchar2","uchar2","uchar2",), "uchar2")
        self.functions["fma"] = c99fn("fma", ("uchar4","uchar4","uchar4",), "uchar4")
        self.functions["fma"] = c99fn("fma", ("uchar8","uchar8","uchar8",), "uchar8")
        self.functions["fma"] = c99fn("fma", ("uchar16","uchar16","uchar16",), "uchar16")
        self.functions["fma"] = c99fn("fma", ("short","short","short",), "short")
        self.functions["fma"] = c99fn("fma", ("short2","short2","short2",), "short2")
        self.functions["fma"] = c99fn("fma", ("short4","short4","short4",), "short4")
        self.functions["fma"] = c99fn("fma", ("short8","short8","short8",), "short8")
        self.functions["fma"] = c99fn("fma", ("short16","short16","short16",), "short16")
        self.functions["fma"] = c99fn("fma", ("ushort","ushort","ushort",), "ushort")
        self.functions["fma"] = c99fn("fma", ("ushort2","ushort2","ushort2",), "ushort2")
        self.functions["fma"] = c99fn("fma", ("ushort4","ushort4","ushort4",), "ushort4")
        self.functions["fma"] = c99fn("fma", ("ushort8","ushort8","ushort8",), "ushort8")
        self.functions["fma"] = c99fn("fma", ("ushort16","ushort16","ushort16",), "ushort16")
        self.functions["fma"] = c99fn("fma", ("int","int","int",), "int")
        self.functions["fma"] = c99fn("fma", ("int2","int2","int2",), "int2")
        self.functions["fma"] = c99fn("fma", ("int4","int4","int4",), "int4")
        self.functions["fma"] = c99fn("fma", ("int8","int8","int8",), "int8")
        self.functions["fma"] = c99fn("fma", ("int16","int16","int16",), "int16")
        self.functions["fma"] = c99fn("fma", ("uint","uint","uint",), "uint")
        self.functions["fma"] = c99fn("fma", ("uint2","uint2","uint2",), "uint2")
        self.functions["fma"] = c99fn("fma", ("uint4","uint4","uint4",), "uint4")
        self.functions["fma"] = c99fn("fma", ("uint8","uint8","uint8",), "uint8")
        self.functions["fma"] = c99fn("fma", ("uint16","uint16","uint16",), "uint16")
        self.functions["fma"] = c99fn("fma", ("long","long","long",), "long")
        self.functions["fma"] = c99fn("fma", ("long2","long2","long2",), "long2")
        self.functions["fma"] = c99fn("fma", ("long4","long4","long4",), "long4")
        self.functions["fma"] = c99fn("fma", ("long8","long8","long8",), "long8")
        self.functions["fma"] = c99fn("fma", ("long16","long16","long16",), "long16")
        self.functions["fma"] = c99fn("fma", ("ulong","ulong","ulong",), "ulong")
        self.functions["fma"] = c99fn("fma", ("ulong2","ulong2","ulong2",), "ulong2")
        self.functions["fma"] = c99fn("fma", ("ulong4","ulong4","ulong4",), "ulong4")
        self.functions["fma"] = c99fn("fma", ("ulong8","ulong8","ulong8",), "ulong8")
        self.functions["fma"] = c99fn("fma", ("ulong16","ulong16","ulong16",), "ulong16")
        self.functions["fmax"] = c99fn("fmax", ("char","char",), "char")
        self.functions["fmax"] = c99fn("fmax", ("char2","char2",), "char2")
        self.functions["fmax"] = c99fn("fmax", ("char4","char4",), "char4")
        self.functions["fmax"] = c99fn("fmax", ("char8","char8",), "char8")
        self.functions["fmax"] = c99fn("fmax", ("char16","char16",), "char16")
        self.functions["fmax"] = c99fn("fmax", ("uchar","uchar",), "uchar")
        self.functions["fmax"] = c99fn("fmax", ("uchar2","uchar2",), "uchar2")
        self.functions["fmax"] = c99fn("fmax", ("uchar4","uchar4",), "uchar4")
        self.functions["fmax"] = c99fn("fmax", ("uchar8","uchar8",), "uchar8")
        self.functions["fmax"] = c99fn("fmax", ("uchar16","uchar16",), "uchar16")
        self.functions["fmax"] = c99fn("fmax", ("short","short",), "short")
        self.functions["fmax"] = c99fn("fmax", ("short2","short2",), "short2")
        self.functions["fmax"] = c99fn("fmax", ("short4","short4",), "short4")
        self.functions["fmax"] = c99fn("fmax", ("short8","short8",), "short8")
        self.functions["fmax"] = c99fn("fmax", ("short16","short16",), "short16")
        self.functions["fmax"] = c99fn("fmax", ("ushort","ushort",), "ushort")
        self.functions["fmax"] = c99fn("fmax", ("ushort2","ushort2",), "ushort2")
        self.functions["fmax"] = c99fn("fmax", ("ushort4","ushort4",), "ushort4")
        self.functions["fmax"] = c99fn("fmax", ("ushort8","ushort8",), "ushort8")
        self.functions["fmax"] = c99fn("fmax", ("ushort16","ushort16",), "ushort16")
        self.functions["fmax"] = c99fn("fmax", ("int","int",), "int")
        self.functions["fmax"] = c99fn("fmax", ("int2","int2",), "int2")
        self.functions["fmax"] = c99fn("fmax", ("int4","int4",), "int4")
        self.functions["fmax"] = c99fn("fmax", ("int8","int8",), "int8")
        self.functions["fmax"] = c99fn("fmax", ("int16","int16",), "int16")
        self.functions["fmax"] = c99fn("fmax", ("uint","uint",), "uint")
        self.functions["fmax"] = c99fn("fmax", ("uint2","uint2",), "uint2")
        self.functions["fmax"] = c99fn("fmax", ("uint4","uint4",), "uint4")
        self.functions["fmax"] = c99fn("fmax", ("uint8","uint8",), "uint8")
        self.functions["fmax"] = c99fn("fmax", ("uint16","uint16",), "uint16")
        self.functions["fmax"] = c99fn("fmax", ("long","long",), "long")
        self.functions["fmax"] = c99fn("fmax", ("long2","long2",), "long2")
        self.functions["fmax"] = c99fn("fmax", ("long4","long4",), "long4")
        self.functions["fmax"] = c99fn("fmax", ("long8","long8",), "long8")
        self.functions["fmax"] = c99fn("fmax", ("long16","long16",), "long16")
        self.functions["fmax"] = c99fn("fmax", ("ulong","ulong",), "ulong")
        self.functions["fmax"] = c99fn("fmax", ("ulong2","ulong2",), "ulong2")
        self.functions["fmax"] = c99fn("fmax", ("ulong4","ulong4",), "ulong4")
        self.functions["fmax"] = c99fn("fmax", ("ulong8","ulong8",), "ulong8")
        self.functions["fmax"] = c99fn("fmax", ("ulong16","ulong16",), "ulong16")
        self.functions["fmax"] = c99fn("fmax", ("char","float",), "char")
        self.functions["fmax"] = c99fn("fmax", ("char2","float",), "char2")
        self.functions["fmax"] = c99fn("fmax", ("char4","float",), "char4")
        self.functions["fmax"] = c99fn("fmax", ("char8","float",), "char8")
        self.functions["fmax"] = c99fn("fmax", ("char16","float",), "char16")
        self.functions["fmax"] = c99fn("fmax", ("uchar","float",), "uchar")
        self.functions["fmax"] = c99fn("fmax", ("uchar2","float",), "uchar2")
        self.functions["fmax"] = c99fn("fmax", ("uchar4","float",), "uchar4")
        self.functions["fmax"] = c99fn("fmax", ("uchar8","float",), "uchar8")
        self.functions["fmax"] = c99fn("fmax", ("uchar16","float",), "uchar16")
        self.functions["fmax"] = c99fn("fmax", ("short","float",), "short")
        self.functions["fmax"] = c99fn("fmax", ("short2","float",), "short2")
        self.functions["fmax"] = c99fn("fmax", ("short4","float",), "short4")
        self.functions["fmax"] = c99fn("fmax", ("short8","float",), "short8")
        self.functions["fmax"] = c99fn("fmax", ("short16","float",), "short16")
        self.functions["fmax"] = c99fn("fmax", ("ushort","float",), "ushort")
        self.functions["fmax"] = c99fn("fmax", ("ushort2","float",), "ushort2")
        self.functions["fmax"] = c99fn("fmax", ("ushort4","float",), "ushort4")
        self.functions["fmax"] = c99fn("fmax", ("ushort8","float",), "ushort8")
        self.functions["fmax"] = c99fn("fmax", ("ushort16","float",), "ushort16")
        self.functions["fmax"] = c99fn("fmax", ("int","float",), "int")
        self.functions["fmax"] = c99fn("fmax", ("int2","float",), "int2")
        self.functions["fmax"] = c99fn("fmax", ("int4","float",), "int4")
        self.functions["fmax"] = c99fn("fmax", ("int8","float",), "int8")
        self.functions["fmax"] = c99fn("fmax", ("int16","float",), "int16")
        self.functions["fmax"] = c99fn("fmax", ("uint","float",), "uint")
        self.functions["fmax"] = c99fn("fmax", ("uint2","float",), "uint2")
        self.functions["fmax"] = c99fn("fmax", ("uint4","float",), "uint4")
        self.functions["fmax"] = c99fn("fmax", ("uint8","float",), "uint8")
        self.functions["fmax"] = c99fn("fmax", ("uint16","float",), "uint16")
        self.functions["fmax"] = c99fn("fmax", ("long","float",), "long")
        self.functions["fmax"] = c99fn("fmax", ("long2","float",), "long2")
        self.functions["fmax"] = c99fn("fmax", ("long4","float",), "long4")
        self.functions["fmax"] = c99fn("fmax", ("long8","float",), "long8")
        self.functions["fmax"] = c99fn("fmax", ("long16","float",), "long16")
        self.functions["fmax"] = c99fn("fmax", ("ulong","float",), "ulong")
        self.functions["fmax"] = c99fn("fmax", ("ulong2","float",), "ulong2")
        self.functions["fmax"] = c99fn("fmax", ("ulong4","float",), "ulong4")
        self.functions["fmax"] = c99fn("fmax", ("ulong8","float",), "ulong8")
        self.functions["fmax"] = c99fn("fmax", ("ulong16","float",), "ulong16")
        self.functions["fmin"] = c99fn("fmin", ("char","char",), "char")
        self.functions["fmin"] = c99fn("fmin", ("char2","char2",), "char2")
        self.functions["fmin"] = c99fn("fmin", ("char4","char4",), "char4")
        self.functions["fmin"] = c99fn("fmin", ("char8","char8",), "char8")
        self.functions["fmin"] = c99fn("fmin", ("char16","char16",), "char16")
        self.functions["fmin"] = c99fn("fmin", ("uchar","uchar",), "uchar")
        self.functions["fmin"] = c99fn("fmin", ("uchar2","uchar2",), "uchar2")
        self.functions["fmin"] = c99fn("fmin", ("uchar4","uchar4",), "uchar4")
        self.functions["fmin"] = c99fn("fmin", ("uchar8","uchar8",), "uchar8")
        self.functions["fmin"] = c99fn("fmin", ("uchar16","uchar16",), "uchar16")
        self.functions["fmin"] = c99fn("fmin", ("short","short",), "short")
        self.functions["fmin"] = c99fn("fmin", ("short2","short2",), "short2")
        self.functions["fmin"] = c99fn("fmin", ("short4","short4",), "short4")
        self.functions["fmin"] = c99fn("fmin", ("short8","short8",), "short8")
        self.functions["fmin"] = c99fn("fmin", ("short16","short16",), "short16")
        self.functions["fmin"] = c99fn("fmin", ("ushort","ushort",), "ushort")
        self.functions["fmin"] = c99fn("fmin", ("ushort2","ushort2",), "ushort2")
        self.functions["fmin"] = c99fn("fmin", ("ushort4","ushort4",), "ushort4")
        self.functions["fmin"] = c99fn("fmin", ("ushort8","ushort8",), "ushort8")
        self.functions["fmin"] = c99fn("fmin", ("ushort16","ushort16",), "ushort16")
        self.functions["fmin"] = c99fn("fmin", ("int","int",), "int")
        self.functions["fmin"] = c99fn("fmin", ("int2","int2",), "int2")
        self.functions["fmin"] = c99fn("fmin", ("int4","int4",), "int4")
        self.functions["fmin"] = c99fn("fmin", ("int8","int8",), "int8")
        self.functions["fmin"] = c99fn("fmin", ("int16","int16",), "int16")
        self.functions["fmin"] = c99fn("fmin", ("uint","uint",), "uint")
        self.functions["fmin"] = c99fn("fmin", ("uint2","uint2",), "uint2")
        self.functions["fmin"] = c99fn("fmin", ("uint4","uint4",), "uint4")
        self.functions["fmin"] = c99fn("fmin", ("uint8","uint8",), "uint8")
        self.functions["fmin"] = c99fn("fmin", ("uint16","uint16",), "uint16")
        self.functions["fmin"] = c99fn("fmin", ("long","long",), "long")
        self.functions["fmin"] = c99fn("fmin", ("long2","long2",), "long2")
        self.functions["fmin"] = c99fn("fmin", ("long4","long4",), "long4")
        self.functions["fmin"] = c99fn("fmin", ("long8","long8",), "long8")
        self.functions["fmin"] = c99fn("fmin", ("long16","long16",), "long16")
        self.functions["fmin"] = c99fn("fmin", ("ulong","ulong",), "ulong")
        self.functions["fmin"] = c99fn("fmin", ("ulong2","ulong2",), "ulong2")
        self.functions["fmin"] = c99fn("fmin", ("ulong4","ulong4",), "ulong4")
        self.functions["fmin"] = c99fn("fmin", ("ulong8","ulong8",), "ulong8")
        self.functions["fmin"] = c99fn("fmin", ("ulong16","ulong16",), "ulong16")
        self.functions["fmin"] = c99fn("fmin", ("char","float",), "char")
        self.functions["fmin"] = c99fn("fmin", ("char2","float",), "char2")
        self.functions["fmin"] = c99fn("fmin", ("char4","float",), "char4")
        self.functions["fmin"] = c99fn("fmin", ("char8","float",), "char8")
        self.functions["fmin"] = c99fn("fmin", ("char16","float",), "char16")
        self.functions["fmin"] = c99fn("fmin", ("uchar","float",), "uchar")
        self.functions["fmin"] = c99fn("fmin", ("uchar2","float",), "uchar2")
        self.functions["fmin"] = c99fn("fmin", ("uchar4","float",), "uchar4")
        self.functions["fmin"] = c99fn("fmin", ("uchar8","float",), "uchar8")
        self.functions["fmin"] = c99fn("fmin", ("uchar16","float",), "uchar16")
        self.functions["fmin"] = c99fn("fmin", ("short","float",), "short")
        self.functions["fmin"] = c99fn("fmin", ("short2","float",), "short2")
        self.functions["fmin"] = c99fn("fmin", ("short4","float",), "short4")
        self.functions["fmin"] = c99fn("fmin", ("short8","float",), "short8")
        self.functions["fmin"] = c99fn("fmin", ("short16","float",), "short16")
        self.functions["fmin"] = c99fn("fmin", ("ushort","float",), "ushort")
        self.functions["fmin"] = c99fn("fmin", ("ushort2","float",), "ushort2")
        self.functions["fmin"] = c99fn("fmin", ("ushort4","float",), "ushort4")
        self.functions["fmin"] = c99fn("fmin", ("ushort8","float",), "ushort8")
        self.functions["fmin"] = c99fn("fmin", ("ushort16","float",), "ushort16")
        self.functions["fmin"] = c99fn("fmin", ("int","float",), "int")
        self.functions["fmin"] = c99fn("fmin", ("int2","float",), "int2")
        self.functions["fmin"] = c99fn("fmin", ("int4","float",), "int4")
        self.functions["fmin"] = c99fn("fmin", ("int8","float",), "int8")
        self.functions["fmin"] = c99fn("fmin", ("int16","float",), "int16")
        self.functions["fmin"] = c99fn("fmin", ("uint","float",), "uint")
        self.functions["fmin"] = c99fn("fmin", ("uint2","float",), "uint2")
        self.functions["fmin"] = c99fn("fmin", ("uint4","float",), "uint4")
        self.functions["fmin"] = c99fn("fmin", ("uint8","float",), "uint8")
        self.functions["fmin"] = c99fn("fmin", ("uint16","float",), "uint16")
        self.functions["fmin"] = c99fn("fmin", ("long","float",), "long")
        self.functions["fmin"] = c99fn("fmin", ("long2","float",), "long2")
        self.functions["fmin"] = c99fn("fmin", ("long4","float",), "long4")
        self.functions["fmin"] = c99fn("fmin", ("long8","float",), "long8")
        self.functions["fmin"] = c99fn("fmin", ("long16","float",), "long16")
        self.functions["fmin"] = c99fn("fmin", ("ulong","float",), "ulong")
        self.functions["fmin"] = c99fn("fmin", ("ulong2","float",), "ulong2")
        self.functions["fmin"] = c99fn("fmin", ("ulong4","float",), "ulong4")
        self.functions["fmin"] = c99fn("fmin", ("ulong8","float",), "ulong8")
        self.functions["fmin"] = c99fn("fmin", ("ulong16","float",), "ulong16")
        self.functions["fmod"] = c99fn("fmod", ("char","char",), "char")
        self.functions["fmod"] = c99fn("fmod", ("char2","char2",), "char2")
        self.functions["fmod"] = c99fn("fmod", ("char4","char4",), "char4")
        self.functions["fmod"] = c99fn("fmod", ("char8","char8",), "char8")
        self.functions["fmod"] = c99fn("fmod", ("char16","char16",), "char16")
        self.functions["fmod"] = c99fn("fmod", ("uchar","uchar",), "uchar")
        self.functions["fmod"] = c99fn("fmod", ("uchar2","uchar2",), "uchar2")
        self.functions["fmod"] = c99fn("fmod", ("uchar4","uchar4",), "uchar4")
        self.functions["fmod"] = c99fn("fmod", ("uchar8","uchar8",), "uchar8")
        self.functions["fmod"] = c99fn("fmod", ("uchar16","uchar16",), "uchar16")
        self.functions["fmod"] = c99fn("fmod", ("short","short",), "short")
        self.functions["fmod"] = c99fn("fmod", ("short2","short2",), "short2")
        self.functions["fmod"] = c99fn("fmod", ("short4","short4",), "short4")
        self.functions["fmod"] = c99fn("fmod", ("short8","short8",), "short8")
        self.functions["fmod"] = c99fn("fmod", ("short16","short16",), "short16")
        self.functions["fmod"] = c99fn("fmod", ("ushort","ushort",), "ushort")
        self.functions["fmod"] = c99fn("fmod", ("ushort2","ushort2",), "ushort2")
        self.functions["fmod"] = c99fn("fmod", ("ushort4","ushort4",), "ushort4")
        self.functions["fmod"] = c99fn("fmod", ("ushort8","ushort8",), "ushort8")
        self.functions["fmod"] = c99fn("fmod", ("ushort16","ushort16",), "ushort16")
        self.functions["fmod"] = c99fn("fmod", ("int","int",), "int")
        self.functions["fmod"] = c99fn("fmod", ("int2","int2",), "int2")
        self.functions["fmod"] = c99fn("fmod", ("int4","int4",), "int4")
        self.functions["fmod"] = c99fn("fmod", ("int8","int8",), "int8")
        self.functions["fmod"] = c99fn("fmod", ("int16","int16",), "int16")
        self.functions["fmod"] = c99fn("fmod", ("uint","uint",), "uint")
        self.functions["fmod"] = c99fn("fmod", ("uint2","uint2",), "uint2")
        self.functions["fmod"] = c99fn("fmod", ("uint4","uint4",), "uint4")
        self.functions["fmod"] = c99fn("fmod", ("uint8","uint8",), "uint8")
        self.functions["fmod"] = c99fn("fmod", ("uint16","uint16",), "uint16")
        self.functions["fmod"] = c99fn("fmod", ("long","long",), "long")
        self.functions["fmod"] = c99fn("fmod", ("long2","long2",), "long2")
        self.functions["fmod"] = c99fn("fmod", ("long4","long4",), "long4")
        self.functions["fmod"] = c99fn("fmod", ("long8","long8",), "long8")
        self.functions["fmod"] = c99fn("fmod", ("long16","long16",), "long16")
        self.functions["fmod"] = c99fn("fmod", ("ulong","ulong",), "ulong")
        self.functions["fmod"] = c99fn("fmod", ("ulong2","ulong2",), "ulong2")
        self.functions["fmod"] = c99fn("fmod", ("ulong4","ulong4",), "ulong4")
        self.functions["fmod"] = c99fn("fmod", ("ulong8","ulong8",), "ulong8")
        self.functions["fmod"] = c99fn("fmod", ("ulong16","ulong16",), "ulong16")
        #TODO: fract#TODO: frexpself.functions["hypo"] = c99fn("hypo", ("char","char",), "char")
        self.functions["hypo"] = c99fn("hypo", ("char2","char2",), "char2")
        self.functions["hypo"] = c99fn("hypo", ("char4","char4",), "char4")
        self.functions["hypo"] = c99fn("hypo", ("char8","char8",), "char8")
        self.functions["hypo"] = c99fn("hypo", ("char16","char16",), "char16")
        self.functions["hypo"] = c99fn("hypo", ("uchar","uchar",), "uchar")
        self.functions["hypo"] = c99fn("hypo", ("uchar2","uchar2",), "uchar2")
        self.functions["hypo"] = c99fn("hypo", ("uchar4","uchar4",), "uchar4")
        self.functions["hypo"] = c99fn("hypo", ("uchar8","uchar8",), "uchar8")
        self.functions["hypo"] = c99fn("hypo", ("uchar16","uchar16",), "uchar16")
        self.functions["hypo"] = c99fn("hypo", ("short","short",), "short")
        self.functions["hypo"] = c99fn("hypo", ("short2","short2",), "short2")
        self.functions["hypo"] = c99fn("hypo", ("short4","short4",), "short4")
        self.functions["hypo"] = c99fn("hypo", ("short8","short8",), "short8")
        self.functions["hypo"] = c99fn("hypo", ("short16","short16",), "short16")
        self.functions["hypo"] = c99fn("hypo", ("ushort","ushort",), "ushort")
        self.functions["hypo"] = c99fn("hypo", ("ushort2","ushort2",), "ushort2")
        self.functions["hypo"] = c99fn("hypo", ("ushort4","ushort4",), "ushort4")
        self.functions["hypo"] = c99fn("hypo", ("ushort8","ushort8",), "ushort8")
        self.functions["hypo"] = c99fn("hypo", ("ushort16","ushort16",), "ushort16")
        self.functions["hypo"] = c99fn("hypo", ("int","int",), "int")
        self.functions["hypo"] = c99fn("hypo", ("int2","int2",), "int2")
        self.functions["hypo"] = c99fn("hypo", ("int4","int4",), "int4")
        self.functions["hypo"] = c99fn("hypo", ("int8","int8",), "int8")
        self.functions["hypo"] = c99fn("hypo", ("int16","int16",), "int16")
        self.functions["hypo"] = c99fn("hypo", ("uint","uint",), "uint")
        self.functions["hypo"] = c99fn("hypo", ("uint2","uint2",), "uint2")
        self.functions["hypo"] = c99fn("hypo", ("uint4","uint4",), "uint4")
        self.functions["hypo"] = c99fn("hypo", ("uint8","uint8",), "uint8")
        self.functions["hypo"] = c99fn("hypo", ("uint16","uint16",), "uint16")
        self.functions["hypo"] = c99fn("hypo", ("long","long",), "long")
        self.functions["hypo"] = c99fn("hypo", ("long2","long2",), "long2")
        self.functions["hypo"] = c99fn("hypo", ("long4","long4",), "long4")
        self.functions["hypo"] = c99fn("hypo", ("long8","long8",), "long8")
        self.functions["hypo"] = c99fn("hypo", ("long16","long16",), "long16")
        self.functions["hypo"] = c99fn("hypo", ("ulong","ulong",), "ulong")
        self.functions["hypo"] = c99fn("hypo", ("ulong2","ulong2",), "ulong2")
        self.functions["hypo"] = c99fn("hypo", ("ulong4","ulong4",), "ulong4")
        self.functions["hypo"] = c99fn("hypo", ("ulong8","ulong8",), "ulong8")
        self.functions["hypo"] = c99fn("hypo", ("ulong16","ulong16",), "ulong16")
        self.functions["ilogb"] = c99fn("ilogb", ("int",), "float")
        self.functions["ilogb2"] = c99fn("ilogb2", ("int",), "float2")
        self.functions["ilogb4"] = c99fn("ilogb4", ("int",), "float4")
        self.functions["ilogb8"] = c99fn("ilogb8", ("int",), "float8")
        self.functions["ilogb16"] = c99fn("ilogb16", ("int",), "float16")
        self.functions["ldexp"] = c99fn("ldexp", ("float","int",), "float")
        self.functions["ldexp"] = c99fn("ldexp", ("float2","int2",), "float2")
        self.functions["ldexp"] = c99fn("ldexp", ("float4","int4",), "float4")
        self.functions["ldexp"] = c99fn("ldexp", ("float8","int8",), "float8")
        self.functions["ldexp"] = c99fn("ldexp", ("float16","int16",), "float16")
        self.functions["lgamma"] = c99fn("lgamma", ("char",), "char")
        self.functions["lgamma"] = c99fn("lgamma", ("char2",), "char2")
        self.functions["lgamma"] = c99fn("lgamma", ("char4",), "char4")
        self.functions["lgamma"] = c99fn("lgamma", ("char8",), "char8")
        self.functions["lgamma"] = c99fn("lgamma", ("char16",), "char16")
        self.functions["lgamma"] = c99fn("lgamma", ("uchar",), "uchar")
        self.functions["lgamma"] = c99fn("lgamma", ("uchar2",), "uchar2")
        self.functions["lgamma"] = c99fn("lgamma", ("uchar4",), "uchar4")
        self.functions["lgamma"] = c99fn("lgamma", ("uchar8",), "uchar8")
        self.functions["lgamma"] = c99fn("lgamma", ("uchar16",), "uchar16")
        self.functions["lgamma"] = c99fn("lgamma", ("short",), "short")
        self.functions["lgamma"] = c99fn("lgamma", ("short2",), "short2")
        self.functions["lgamma"] = c99fn("lgamma", ("short4",), "short4")
        self.functions["lgamma"] = c99fn("lgamma", ("short8",), "short8")
        self.functions["lgamma"] = c99fn("lgamma", ("short16",), "short16")
        self.functions["lgamma"] = c99fn("lgamma", ("ushort",), "ushort")
        self.functions["lgamma"] = c99fn("lgamma", ("ushort2",), "ushort2")
        self.functions["lgamma"] = c99fn("lgamma", ("ushort4",), "ushort4")
        self.functions["lgamma"] = c99fn("lgamma", ("ushort8",), "ushort8")
        self.functions["lgamma"] = c99fn("lgamma", ("ushort16",), "ushort16")
        self.functions["lgamma"] = c99fn("lgamma", ("int",), "int")
        self.functions["lgamma"] = c99fn("lgamma", ("int2",), "int2")
        self.functions["lgamma"] = c99fn("lgamma", ("int4",), "int4")
        self.functions["lgamma"] = c99fn("lgamma", ("int8",), "int8")
        self.functions["lgamma"] = c99fn("lgamma", ("int16",), "int16")
        self.functions["lgamma"] = c99fn("lgamma", ("uint",), "uint")
        self.functions["lgamma"] = c99fn("lgamma", ("uint2",), "uint2")
        self.functions["lgamma"] = c99fn("lgamma", ("uint4",), "uint4")
        self.functions["lgamma"] = c99fn("lgamma", ("uint8",), "uint8")
        self.functions["lgamma"] = c99fn("lgamma", ("uint16",), "uint16")
        self.functions["lgamma"] = c99fn("lgamma", ("long",), "long")
        self.functions["lgamma"] = c99fn("lgamma", ("long2",), "long2")
        self.functions["lgamma"] = c99fn("lgamma", ("long4",), "long4")
        self.functions["lgamma"] = c99fn("lgamma", ("long8",), "long8")
        self.functions["lgamma"] = c99fn("lgamma", ("long16",), "long16")
        self.functions["lgamma"] = c99fn("lgamma", ("ulong",), "ulong")
        self.functions["lgamma"] = c99fn("lgamma", ("ulong2",), "ulong2")
        self.functions["lgamma"] = c99fn("lgamma", ("ulong4",), "ulong4")
        self.functions["lgamma"] = c99fn("lgamma", ("ulong8",), "ulong8")
        self.functions["lgamma"] = c99fn("lgamma", ("ulong16",), "ulong16")
        #TODO: lgamma_rself.functions["log"] = c99fn("log", ("char",), "char")
        self.functions["log"] = c99fn("log", ("char2",), "char2")
        self.functions["log"] = c99fn("log", ("char4",), "char4")
        self.functions["log"] = c99fn("log", ("char8",), "char8")
        self.functions["log"] = c99fn("log", ("char16",), "char16")
        self.functions["log"] = c99fn("log", ("uchar",), "uchar")
        self.functions["log"] = c99fn("log", ("uchar2",), "uchar2")
        self.functions["log"] = c99fn("log", ("uchar4",), "uchar4")
        self.functions["log"] = c99fn("log", ("uchar8",), "uchar8")
        self.functions["log"] = c99fn("log", ("uchar16",), "uchar16")
        self.functions["log"] = c99fn("log", ("short",), "short")
        self.functions["log"] = c99fn("log", ("short2",), "short2")
        self.functions["log"] = c99fn("log", ("short4",), "short4")
        self.functions["log"] = c99fn("log", ("short8",), "short8")
        self.functions["log"] = c99fn("log", ("short16",), "short16")
        self.functions["log"] = c99fn("log", ("ushort",), "ushort")
        self.functions["log"] = c99fn("log", ("ushort2",), "ushort2")
        self.functions["log"] = c99fn("log", ("ushort4",), "ushort4")
        self.functions["log"] = c99fn("log", ("ushort8",), "ushort8")
        self.functions["log"] = c99fn("log", ("ushort16",), "ushort16")
        self.functions["log"] = c99fn("log", ("int",), "int")
        self.functions["log"] = c99fn("log", ("int2",), "int2")
        self.functions["log"] = c99fn("log", ("int4",), "int4")
        self.functions["log"] = c99fn("log", ("int8",), "int8")
        self.functions["log"] = c99fn("log", ("int16",), "int16")
        self.functions["log"] = c99fn("log", ("uint",), "uint")
        self.functions["log"] = c99fn("log", ("uint2",), "uint2")
        self.functions["log"] = c99fn("log", ("uint4",), "uint4")
        self.functions["log"] = c99fn("log", ("uint8",), "uint8")
        self.functions["log"] = c99fn("log", ("uint16",), "uint16")
        self.functions["log"] = c99fn("log", ("long",), "long")
        self.functions["log"] = c99fn("log", ("long2",), "long2")
        self.functions["log"] = c99fn("log", ("long4",), "long4")
        self.functions["log"] = c99fn("log", ("long8",), "long8")
        self.functions["log"] = c99fn("log", ("long16",), "long16")
        self.functions["log"] = c99fn("log", ("ulong",), "ulong")
        self.functions["log"] = c99fn("log", ("ulong2",), "ulong2")
        self.functions["log"] = c99fn("log", ("ulong4",), "ulong4")
        self.functions["log"] = c99fn("log", ("ulong8",), "ulong8")
        self.functions["log"] = c99fn("log", ("ulong16",), "ulong16")
        self.functions["log2"] = c99fn("log2", ("char",), "char")
        self.functions["log2"] = c99fn("log2", ("char2",), "char2")
        self.functions["log2"] = c99fn("log2", ("char4",), "char4")
        self.functions["log2"] = c99fn("log2", ("char8",), "char8")
        self.functions["log2"] = c99fn("log2", ("char16",), "char16")
        self.functions["log2"] = c99fn("log2", ("uchar",), "uchar")
        self.functions["log2"] = c99fn("log2", ("uchar2",), "uchar2")
        self.functions["log2"] = c99fn("log2", ("uchar4",), "uchar4")
        self.functions["log2"] = c99fn("log2", ("uchar8",), "uchar8")
        self.functions["log2"] = c99fn("log2", ("uchar16",), "uchar16")
        self.functions["log2"] = c99fn("log2", ("short",), "short")
        self.functions["log2"] = c99fn("log2", ("short2",), "short2")
        self.functions["log2"] = c99fn("log2", ("short4",), "short4")
        self.functions["log2"] = c99fn("log2", ("short8",), "short8")
        self.functions["log2"] = c99fn("log2", ("short16",), "short16")
        self.functions["log2"] = c99fn("log2", ("ushort",), "ushort")
        self.functions["log2"] = c99fn("log2", ("ushort2",), "ushort2")
        self.functions["log2"] = c99fn("log2", ("ushort4",), "ushort4")
        self.functions["log2"] = c99fn("log2", ("ushort8",), "ushort8")
        self.functions["log2"] = c99fn("log2", ("ushort16",), "ushort16")
        self.functions["log2"] = c99fn("log2", ("int",), "int")
        self.functions["log2"] = c99fn("log2", ("int2",), "int2")
        self.functions["log2"] = c99fn("log2", ("int4",), "int4")
        self.functions["log2"] = c99fn("log2", ("int8",), "int8")
        self.functions["log2"] = c99fn("log2", ("int16",), "int16")
        self.functions["log2"] = c99fn("log2", ("uint",), "uint")
        self.functions["log2"] = c99fn("log2", ("uint2",), "uint2")
        self.functions["log2"] = c99fn("log2", ("uint4",), "uint4")
        self.functions["log2"] = c99fn("log2", ("uint8",), "uint8")
        self.functions["log2"] = c99fn("log2", ("uint16",), "uint16")
        self.functions["log2"] = c99fn("log2", ("long",), "long")
        self.functions["log2"] = c99fn("log2", ("long2",), "long2")
        self.functions["log2"] = c99fn("log2", ("long4",), "long4")
        self.functions["log2"] = c99fn("log2", ("long8",), "long8")
        self.functions["log2"] = c99fn("log2", ("long16",), "long16")
        self.functions["log2"] = c99fn("log2", ("ulong",), "ulong")
        self.functions["log2"] = c99fn("log2", ("ulong2",), "ulong2")
        self.functions["log2"] = c99fn("log2", ("ulong4",), "ulong4")
        self.functions["log2"] = c99fn("log2", ("ulong8",), "ulong8")
        self.functions["log2"] = c99fn("log2", ("ulong16",), "ulong16")
        self.functions["log10"] = c99fn("log10", ("char",), "char")
        self.functions["log10"] = c99fn("log10", ("char2",), "char2")
        self.functions["log10"] = c99fn("log10", ("char4",), "char4")
        self.functions["log10"] = c99fn("log10", ("char8",), "char8")
        self.functions["log10"] = c99fn("log10", ("char16",), "char16")
        self.functions["log10"] = c99fn("log10", ("uchar",), "uchar")
        self.functions["log10"] = c99fn("log10", ("uchar2",), "uchar2")
        self.functions["log10"] = c99fn("log10", ("uchar4",), "uchar4")
        self.functions["log10"] = c99fn("log10", ("uchar8",), "uchar8")
        self.functions["log10"] = c99fn("log10", ("uchar16",), "uchar16")
        self.functions["log10"] = c99fn("log10", ("short",), "short")
        self.functions["log10"] = c99fn("log10", ("short2",), "short2")
        self.functions["log10"] = c99fn("log10", ("short4",), "short4")
        self.functions["log10"] = c99fn("log10", ("short8",), "short8")
        self.functions["log10"] = c99fn("log10", ("short16",), "short16")
        self.functions["log10"] = c99fn("log10", ("ushort",), "ushort")
        self.functions["log10"] = c99fn("log10", ("ushort2",), "ushort2")
        self.functions["log10"] = c99fn("log10", ("ushort4",), "ushort4")
        self.functions["log10"] = c99fn("log10", ("ushort8",), "ushort8")
        self.functions["log10"] = c99fn("log10", ("ushort16",), "ushort16")
        self.functions["log10"] = c99fn("log10", ("int",), "int")
        self.functions["log10"] = c99fn("log10", ("int2",), "int2")
        self.functions["log10"] = c99fn("log10", ("int4",), "int4")
        self.functions["log10"] = c99fn("log10", ("int8",), "int8")
        self.functions["log10"] = c99fn("log10", ("int16",), "int16")
        self.functions["log10"] = c99fn("log10", ("uint",), "uint")
        self.functions["log10"] = c99fn("log10", ("uint2",), "uint2")
        self.functions["log10"] = c99fn("log10", ("uint4",), "uint4")
        self.functions["log10"] = c99fn("log10", ("uint8",), "uint8")
        self.functions["log10"] = c99fn("log10", ("uint16",), "uint16")
        self.functions["log10"] = c99fn("log10", ("long",), "long")
        self.functions["log10"] = c99fn("log10", ("long2",), "long2")
        self.functions["log10"] = c99fn("log10", ("long4",), "long4")
        self.functions["log10"] = c99fn("log10", ("long8",), "long8")
        self.functions["log10"] = c99fn("log10", ("long16",), "long16")
        self.functions["log10"] = c99fn("log10", ("ulong",), "ulong")
        self.functions["log10"] = c99fn("log10", ("ulong2",), "ulong2")
        self.functions["log10"] = c99fn("log10", ("ulong4",), "ulong4")
        self.functions["log10"] = c99fn("log10", ("ulong8",), "ulong8")
        self.functions["log10"] = c99fn("log10", ("ulong16",), "ulong16")
        self.functions["log1p"] = c99fn("log1p", ("char",), "char")
        self.functions["log1p"] = c99fn("log1p", ("char2",), "char2")
        self.functions["log1p"] = c99fn("log1p", ("char4",), "char4")
        self.functions["log1p"] = c99fn("log1p", ("char8",), "char8")
        self.functions["log1p"] = c99fn("log1p", ("char16",), "char16")
        self.functions["log1p"] = c99fn("log1p", ("uchar",), "uchar")
        self.functions["log1p"] = c99fn("log1p", ("uchar2",), "uchar2")
        self.functions["log1p"] = c99fn("log1p", ("uchar4",), "uchar4")
        self.functions["log1p"] = c99fn("log1p", ("uchar8",), "uchar8")
        self.functions["log1p"] = c99fn("log1p", ("uchar16",), "uchar16")
        self.functions["log1p"] = c99fn("log1p", ("short",), "short")
        self.functions["log1p"] = c99fn("log1p", ("short2",), "short2")
        self.functions["log1p"] = c99fn("log1p", ("short4",), "short4")
        self.functions["log1p"] = c99fn("log1p", ("short8",), "short8")
        self.functions["log1p"] = c99fn("log1p", ("short16",), "short16")
        self.functions["log1p"] = c99fn("log1p", ("ushort",), "ushort")
        self.functions["log1p"] = c99fn("log1p", ("ushort2",), "ushort2")
        self.functions["log1p"] = c99fn("log1p", ("ushort4",), "ushort4")
        self.functions["log1p"] = c99fn("log1p", ("ushort8",), "ushort8")
        self.functions["log1p"] = c99fn("log1p", ("ushort16",), "ushort16")
        self.functions["log1p"] = c99fn("log1p", ("int",), "int")
        self.functions["log1p"] = c99fn("log1p", ("int2",), "int2")
        self.functions["log1p"] = c99fn("log1p", ("int4",), "int4")
        self.functions["log1p"] = c99fn("log1p", ("int8",), "int8")
        self.functions["log1p"] = c99fn("log1p", ("int16",), "int16")
        self.functions["log1p"] = c99fn("log1p", ("uint",), "uint")
        self.functions["log1p"] = c99fn("log1p", ("uint2",), "uint2")
        self.functions["log1p"] = c99fn("log1p", ("uint4",), "uint4")
        self.functions["log1p"] = c99fn("log1p", ("uint8",), "uint8")
        self.functions["log1p"] = c99fn("log1p", ("uint16",), "uint16")
        self.functions["log1p"] = c99fn("log1p", ("long",), "long")
        self.functions["log1p"] = c99fn("log1p", ("long2",), "long2")
        self.functions["log1p"] = c99fn("log1p", ("long4",), "long4")
        self.functions["log1p"] = c99fn("log1p", ("long8",), "long8")
        self.functions["log1p"] = c99fn("log1p", ("long16",), "long16")
        self.functions["log1p"] = c99fn("log1p", ("ulong",), "ulong")
        self.functions["log1p"] = c99fn("log1p", ("ulong2",), "ulong2")
        self.functions["log1p"] = c99fn("log1p", ("ulong4",), "ulong4")
        self.functions["log1p"] = c99fn("log1p", ("ulong8",), "ulong8")
        self.functions["log1p"] = c99fn("log1p", ("ulong16",), "ulong16")
        self.functions["logb"] = c99fn("logb", ("char",), "char")
        self.functions["logb"] = c99fn("logb", ("char2",), "char2")
        self.functions["logb"] = c99fn("logb", ("char4",), "char4")
        self.functions["logb"] = c99fn("logb", ("char8",), "char8")
        self.functions["logb"] = c99fn("logb", ("char16",), "char16")
        self.functions["logb"] = c99fn("logb", ("uchar",), "uchar")
        self.functions["logb"] = c99fn("logb", ("uchar2",), "uchar2")
        self.functions["logb"] = c99fn("logb", ("uchar4",), "uchar4")
        self.functions["logb"] = c99fn("logb", ("uchar8",), "uchar8")
        self.functions["logb"] = c99fn("logb", ("uchar16",), "uchar16")
        self.functions["logb"] = c99fn("logb", ("short",), "short")
        self.functions["logb"] = c99fn("logb", ("short2",), "short2")
        self.functions["logb"] = c99fn("logb", ("short4",), "short4")
        self.functions["logb"] = c99fn("logb", ("short8",), "short8")
        self.functions["logb"] = c99fn("logb", ("short16",), "short16")
        self.functions["logb"] = c99fn("logb", ("ushort",), "ushort")
        self.functions["logb"] = c99fn("logb", ("ushort2",), "ushort2")
        self.functions["logb"] = c99fn("logb", ("ushort4",), "ushort4")
        self.functions["logb"] = c99fn("logb", ("ushort8",), "ushort8")
        self.functions["logb"] = c99fn("logb", ("ushort16",), "ushort16")
        self.functions["logb"] = c99fn("logb", ("int",), "int")
        self.functions["logb"] = c99fn("logb", ("int2",), "int2")
        self.functions["logb"] = c99fn("logb", ("int4",), "int4")
        self.functions["logb"] = c99fn("logb", ("int8",), "int8")
        self.functions["logb"] = c99fn("logb", ("int16",), "int16")
        self.functions["logb"] = c99fn("logb", ("uint",), "uint")
        self.functions["logb"] = c99fn("logb", ("uint2",), "uint2")
        self.functions["logb"] = c99fn("logb", ("uint4",), "uint4")
        self.functions["logb"] = c99fn("logb", ("uint8",), "uint8")
        self.functions["logb"] = c99fn("logb", ("uint16",), "uint16")
        self.functions["logb"] = c99fn("logb", ("long",), "long")
        self.functions["logb"] = c99fn("logb", ("long2",), "long2")
        self.functions["logb"] = c99fn("logb", ("long4",), "long4")
        self.functions["logb"] = c99fn("logb", ("long8",), "long8")
        self.functions["logb"] = c99fn("logb", ("long16",), "long16")
        self.functions["logb"] = c99fn("logb", ("ulong",), "ulong")
        self.functions["logb"] = c99fn("logb", ("ulong2",), "ulong2")
        self.functions["logb"] = c99fn("logb", ("ulong4",), "ulong4")
        self.functions["logb"] = c99fn("logb", ("ulong8",), "ulong8")
        self.functions["logb"] = c99fn("logb", ("ulong16",), "ulong16")
        self.functions["mad"] = c99fn("mad", ("char",), "char")
        self.functions["mad"] = c99fn("mad", ("char2",), "char2")
        self.functions["mad"] = c99fn("mad", ("char4",), "char4")
        self.functions["mad"] = c99fn("mad", ("char8",), "char8")
        self.functions["mad"] = c99fn("mad", ("char16",), "char16")
        self.functions["mad"] = c99fn("mad", ("uchar",), "uchar")
        self.functions["mad"] = c99fn("mad", ("uchar2",), "uchar2")
        self.functions["mad"] = c99fn("mad", ("uchar4",), "uchar4")
        self.functions["mad"] = c99fn("mad", ("uchar8",), "uchar8")
        self.functions["mad"] = c99fn("mad", ("uchar16",), "uchar16")
        self.functions["mad"] = c99fn("mad", ("short",), "short")
        self.functions["mad"] = c99fn("mad", ("short2",), "short2")
        self.functions["mad"] = c99fn("mad", ("short4",), "short4")
        self.functions["mad"] = c99fn("mad", ("short8",), "short8")
        self.functions["mad"] = c99fn("mad", ("short16",), "short16")
        self.functions["mad"] = c99fn("mad", ("ushort",), "ushort")
        self.functions["mad"] = c99fn("mad", ("ushort2",), "ushort2")
        self.functions["mad"] = c99fn("mad", ("ushort4",), "ushort4")
        self.functions["mad"] = c99fn("mad", ("ushort8",), "ushort8")
        self.functions["mad"] = c99fn("mad", ("ushort16",), "ushort16")
        self.functions["mad"] = c99fn("mad", ("int",), "int")
        self.functions["mad"] = c99fn("mad", ("int2",), "int2")
        self.functions["mad"] = c99fn("mad", ("int4",), "int4")
        self.functions["mad"] = c99fn("mad", ("int8",), "int8")
        self.functions["mad"] = c99fn("mad", ("int16",), "int16")
        self.functions["mad"] = c99fn("mad", ("uint",), "uint")
        self.functions["mad"] = c99fn("mad", ("uint2",), "uint2")
        self.functions["mad"] = c99fn("mad", ("uint4",), "uint4")
        self.functions["mad"] = c99fn("mad", ("uint8",), "uint8")
        self.functions["mad"] = c99fn("mad", ("uint16",), "uint16")
        self.functions["mad"] = c99fn("mad", ("long",), "long")
        self.functions["mad"] = c99fn("mad", ("long2",), "long2")
        self.functions["mad"] = c99fn("mad", ("long4",), "long4")
        self.functions["mad"] = c99fn("mad", ("long8",), "long8")
        self.functions["mad"] = c99fn("mad", ("long16",), "long16")
        self.functions["mad"] = c99fn("mad", ("ulong",), "ulong")
        self.functions["mad"] = c99fn("mad", ("ulong2",), "ulong2")
        self.functions["mad"] = c99fn("mad", ("ulong4",), "ulong4")
        self.functions["mad"] = c99fn("mad", ("ulong8",), "ulong8")
        self.functions["mad"] = c99fn("mad", ("ulong16",), "ulong16")
        self.functions["maxmag"] = c99fn("maxmag", ("char","char",), "char")
        self.functions["maxmag"] = c99fn("maxmag", ("char2","char2",), "char2")
        self.functions["maxmag"] = c99fn("maxmag", ("char4","char4",), "char4")
        self.functions["maxmag"] = c99fn("maxmag", ("char8","char8",), "char8")
        self.functions["maxmag"] = c99fn("maxmag", ("char16","char16",), "char16")
        self.functions["maxmag"] = c99fn("maxmag", ("uchar","uchar",), "uchar")
        self.functions["maxmag"] = c99fn("maxmag", ("uchar2","uchar2",), "uchar2")
        self.functions["maxmag"] = c99fn("maxmag", ("uchar4","uchar4",), "uchar4")
        self.functions["maxmag"] = c99fn("maxmag", ("uchar8","uchar8",), "uchar8")
        self.functions["maxmag"] = c99fn("maxmag", ("uchar16","uchar16",), "uchar16")
        self.functions["maxmag"] = c99fn("maxmag", ("short","short",), "short")
        self.functions["maxmag"] = c99fn("maxmag", ("short2","short2",), "short2")
        self.functions["maxmag"] = c99fn("maxmag", ("short4","short4",), "short4")
        self.functions["maxmag"] = c99fn("maxmag", ("short8","short8",), "short8")
        self.functions["maxmag"] = c99fn("maxmag", ("short16","short16",), "short16")
        self.functions["maxmag"] = c99fn("maxmag", ("ushort","ushort",), "ushort")
        self.functions["maxmag"] = c99fn("maxmag", ("ushort2","ushort2",), "ushort2")
        self.functions["maxmag"] = c99fn("maxmag", ("ushort4","ushort4",), "ushort4")
        self.functions["maxmag"] = c99fn("maxmag", ("ushort8","ushort8",), "ushort8")
        self.functions["maxmag"] = c99fn("maxmag", ("ushort16","ushort16",), "ushort16")
        self.functions["maxmag"] = c99fn("maxmag", ("int","int",), "int")
        self.functions["maxmag"] = c99fn("maxmag", ("int2","int2",), "int2")
        self.functions["maxmag"] = c99fn("maxmag", ("int4","int4",), "int4")
        self.functions["maxmag"] = c99fn("maxmag", ("int8","int8",), "int8")
        self.functions["maxmag"] = c99fn("maxmag", ("int16","int16",), "int16")
        self.functions["maxmag"] = c99fn("maxmag", ("uint","uint",), "uint")
        self.functions["maxmag"] = c99fn("maxmag", ("uint2","uint2",), "uint2")
        self.functions["maxmag"] = c99fn("maxmag", ("uint4","uint4",), "uint4")
        self.functions["maxmag"] = c99fn("maxmag", ("uint8","uint8",), "uint8")
        self.functions["maxmag"] = c99fn("maxmag", ("uint16","uint16",), "uint16")
        self.functions["maxmag"] = c99fn("maxmag", ("long","long",), "long")
        self.functions["maxmag"] = c99fn("maxmag", ("long2","long2",), "long2")
        self.functions["maxmag"] = c99fn("maxmag", ("long4","long4",), "long4")
        self.functions["maxmag"] = c99fn("maxmag", ("long8","long8",), "long8")
        self.functions["maxmag"] = c99fn("maxmag", ("long16","long16",), "long16")
        self.functions["maxmag"] = c99fn("maxmag", ("ulong","ulong",), "ulong")
        self.functions["maxmag"] = c99fn("maxmag", ("ulong2","ulong2",), "ulong2")
        self.functions["maxmag"] = c99fn("maxmag", ("ulong4","ulong4",), "ulong4")
        self.functions["maxmag"] = c99fn("maxmag", ("ulong8","ulong8",), "ulong8")
        self.functions["maxmag"] = c99fn("maxmag", ("ulong16","ulong16",), "ulong16")
        self.functions["minmag"] = c99fn("minmag", ("char","char",), "char")
        self.functions["minmag"] = c99fn("minmag", ("char2","char2",), "char2")
        self.functions["minmag"] = c99fn("minmag", ("char4","char4",), "char4")
        self.functions["minmag"] = c99fn("minmag", ("char8","char8",), "char8")
        self.functions["minmag"] = c99fn("minmag", ("char16","char16",), "char16")
        self.functions["minmag"] = c99fn("minmag", ("uchar","uchar",), "uchar")
        self.functions["minmag"] = c99fn("minmag", ("uchar2","uchar2",), "uchar2")
        self.functions["minmag"] = c99fn("minmag", ("uchar4","uchar4",), "uchar4")
        self.functions["minmag"] = c99fn("minmag", ("uchar8","uchar8",), "uchar8")
        self.functions["minmag"] = c99fn("minmag", ("uchar16","uchar16",), "uchar16")
        self.functions["minmag"] = c99fn("minmag", ("short","short",), "short")
        self.functions["minmag"] = c99fn("minmag", ("short2","short2",), "short2")
        self.functions["minmag"] = c99fn("minmag", ("short4","short4",), "short4")
        self.functions["minmag"] = c99fn("minmag", ("short8","short8",), "short8")
        self.functions["minmag"] = c99fn("minmag", ("short16","short16",), "short16")
        self.functions["minmag"] = c99fn("minmag", ("ushort","ushort",), "ushort")
        self.functions["minmag"] = c99fn("minmag", ("ushort2","ushort2",), "ushort2")
        self.functions["minmag"] = c99fn("minmag", ("ushort4","ushort4",), "ushort4")
        self.functions["minmag"] = c99fn("minmag", ("ushort8","ushort8",), "ushort8")
        self.functions["minmag"] = c99fn("minmag", ("ushort16","ushort16",), "ushort16")
        self.functions["minmag"] = c99fn("minmag", ("int","int",), "int")
        self.functions["minmag"] = c99fn("minmag", ("int2","int2",), "int2")
        self.functions["minmag"] = c99fn("minmag", ("int4","int4",), "int4")
        self.functions["minmag"] = c99fn("minmag", ("int8","int8",), "int8")
        self.functions["minmag"] = c99fn("minmag", ("int16","int16",), "int16")
        self.functions["minmag"] = c99fn("minmag", ("uint","uint",), "uint")
        self.functions["minmag"] = c99fn("minmag", ("uint2","uint2",), "uint2")
        self.functions["minmag"] = c99fn("minmag", ("uint4","uint4",), "uint4")
        self.functions["minmag"] = c99fn("minmag", ("uint8","uint8",), "uint8")
        self.functions["minmag"] = c99fn("minmag", ("uint16","uint16",), "uint16")
        self.functions["minmag"] = c99fn("minmag", ("long","long",), "long")
        self.functions["minmag"] = c99fn("minmag", ("long2","long2",), "long2")
        self.functions["minmag"] = c99fn("minmag", ("long4","long4",), "long4")
        self.functions["minmag"] = c99fn("minmag", ("long8","long8",), "long8")
        self.functions["minmag"] = c99fn("minmag", ("long16","long16",), "long16")
        self.functions["minmag"] = c99fn("minmag", ("ulong","ulong",), "ulong")
        self.functions["minmag"] = c99fn("minmag", ("ulong2","ulong2",), "ulong2")
        self.functions["minmag"] = c99fn("minmag", ("ulong4","ulong4",), "ulong4")
        self.functions["minmag"] = c99fn("minmag", ("ulong8","ulong8",), "ulong8")
        self.functions["minmag"] = c99fn("minmag", ("ulong16","ulong16",), "ulong16")
        #TODO: modfself.functions["nan"] = c99fn("nan", ("unit",), "float")
        self.functions["nan"] = c99fn("nan", ("unit2",), "float2")
        self.functions["nan"] = c99fn("nan", ("unit4",), "float4")
        self.functions["nan"] = c99fn("nan", ("unit8",), "float8")
        self.functions["nan"] = c99fn("nan", ("unit16",), "float16")
        self.functions["nextafter"] = c99fn("nextafter", ("char","char",), "char")
        self.functions["nextafter"] = c99fn("nextafter", ("char2","char2",), "char2")
        self.functions["nextafter"] = c99fn("nextafter", ("char4","char4",), "char4")
        self.functions["nextafter"] = c99fn("nextafter", ("char8","char8",), "char8")
        self.functions["nextafter"] = c99fn("nextafter", ("char16","char16",), "char16")
        self.functions["nextafter"] = c99fn("nextafter", ("uchar","uchar",), "uchar")
        self.functions["nextafter"] = c99fn("nextafter", ("uchar2","uchar2",), "uchar2")
        self.functions["nextafter"] = c99fn("nextafter", ("uchar4","uchar4",), "uchar4")
        self.functions["nextafter"] = c99fn("nextafter", ("uchar8","uchar8",), "uchar8")
        self.functions["nextafter"] = c99fn("nextafter", ("uchar16","uchar16",), "uchar16")
        self.functions["nextafter"] = c99fn("nextafter", ("short","short",), "short")
        self.functions["nextafter"] = c99fn("nextafter", ("short2","short2",), "short2")
        self.functions["nextafter"] = c99fn("nextafter", ("short4","short4",), "short4")
        self.functions["nextafter"] = c99fn("nextafter", ("short8","short8",), "short8")
        self.functions["nextafter"] = c99fn("nextafter", ("short16","short16",), "short16")
        self.functions["nextafter"] = c99fn("nextafter", ("ushort","ushort",), "ushort")
        self.functions["nextafter"] = c99fn("nextafter", ("ushort2","ushort2",), "ushort2")
        self.functions["nextafter"] = c99fn("nextafter", ("ushort4","ushort4",), "ushort4")
        self.functions["nextafter"] = c99fn("nextafter", ("ushort8","ushort8",), "ushort8")
        self.functions["nextafter"] = c99fn("nextafter", ("ushort16","ushort16",), "ushort16")
        self.functions["nextafter"] = c99fn("nextafter", ("int","int",), "int")
        self.functions["nextafter"] = c99fn("nextafter", ("int2","int2",), "int2")
        self.functions["nextafter"] = c99fn("nextafter", ("int4","int4",), "int4")
        self.functions["nextafter"] = c99fn("nextafter", ("int8","int8",), "int8")
        self.functions["nextafter"] = c99fn("nextafter", ("int16","int16",), "int16")
        self.functions["nextafter"] = c99fn("nextafter", ("uint","uint",), "uint")
        self.functions["nextafter"] = c99fn("nextafter", ("uint2","uint2",), "uint2")
        self.functions["nextafter"] = c99fn("nextafter", ("uint4","uint4",), "uint4")
        self.functions["nextafter"] = c99fn("nextafter", ("uint8","uint8",), "uint8")
        self.functions["nextafter"] = c99fn("nextafter", ("uint16","uint16",), "uint16")
        self.functions["nextafter"] = c99fn("nextafter", ("long","long",), "long")
        self.functions["nextafter"] = c99fn("nextafter", ("long2","long2",), "long2")
        self.functions["nextafter"] = c99fn("nextafter", ("long4","long4",), "long4")
        self.functions["nextafter"] = c99fn("nextafter", ("long8","long8",), "long8")
        self.functions["nextafter"] = c99fn("nextafter", ("long16","long16",), "long16")
        self.functions["nextafter"] = c99fn("nextafter", ("ulong","ulong",), "ulong")
        self.functions["nextafter"] = c99fn("nextafter", ("ulong2","ulong2",), "ulong2")
        self.functions["nextafter"] = c99fn("nextafter", ("ulong4","ulong4",), "ulong4")
        self.functions["nextafter"] = c99fn("nextafter", ("ulong8","ulong8",), "ulong8")
        self.functions["nextafter"] = c99fn("nextafter", ("ulong16","ulong16",), "ulong16")
        self.functions["pow"] = c99fn("pow", ("char","char",), "char")
        self.functions["pow"] = c99fn("pow", ("char2","char2",), "char2")
        self.functions["pow"] = c99fn("pow", ("char4","char4",), "char4")
        self.functions["pow"] = c99fn("pow", ("char8","char8",), "char8")
        self.functions["pow"] = c99fn("pow", ("char16","char16",), "char16")
        self.functions["pow"] = c99fn("pow", ("uchar","uchar",), "uchar")
        self.functions["pow"] = c99fn("pow", ("uchar2","uchar2",), "uchar2")
        self.functions["pow"] = c99fn("pow", ("uchar4","uchar4",), "uchar4")
        self.functions["pow"] = c99fn("pow", ("uchar8","uchar8",), "uchar8")
        self.functions["pow"] = c99fn("pow", ("uchar16","uchar16",), "uchar16")
        self.functions["pow"] = c99fn("pow", ("short","short",), "short")
        self.functions["pow"] = c99fn("pow", ("short2","short2",), "short2")
        self.functions["pow"] = c99fn("pow", ("short4","short4",), "short4")
        self.functions["pow"] = c99fn("pow", ("short8","short8",), "short8")
        self.functions["pow"] = c99fn("pow", ("short16","short16",), "short16")
        self.functions["pow"] = c99fn("pow", ("ushort","ushort",), "ushort")
        self.functions["pow"] = c99fn("pow", ("ushort2","ushort2",), "ushort2")
        self.functions["pow"] = c99fn("pow", ("ushort4","ushort4",), "ushort4")
        self.functions["pow"] = c99fn("pow", ("ushort8","ushort8",), "ushort8")
        self.functions["pow"] = c99fn("pow", ("ushort16","ushort16",), "ushort16")
        self.functions["pow"] = c99fn("pow", ("int","int",), "int")
        self.functions["pow"] = c99fn("pow", ("int2","int2",), "int2")
        self.functions["pow"] = c99fn("pow", ("int4","int4",), "int4")
        self.functions["pow"] = c99fn("pow", ("int8","int8",), "int8")
        self.functions["pow"] = c99fn("pow", ("int16","int16",), "int16")
        self.functions["pow"] = c99fn("pow", ("uint","uint",), "uint")
        self.functions["pow"] = c99fn("pow", ("uint2","uint2",), "uint2")
        self.functions["pow"] = c99fn("pow", ("uint4","uint4",), "uint4")
        self.functions["pow"] = c99fn("pow", ("uint8","uint8",), "uint8")
        self.functions["pow"] = c99fn("pow", ("uint16","uint16",), "uint16")
        self.functions["pow"] = c99fn("pow", ("long","long",), "long")
        self.functions["pow"] = c99fn("pow", ("long2","long2",), "long2")
        self.functions["pow"] = c99fn("pow", ("long4","long4",), "long4")
        self.functions["pow"] = c99fn("pow", ("long8","long8",), "long8")
        self.functions["pow"] = c99fn("pow", ("long16","long16",), "long16")
        self.functions["pow"] = c99fn("pow", ("ulong","ulong",), "ulong")
        self.functions["pow"] = c99fn("pow", ("ulong2","ulong2",), "ulong2")
        self.functions["pow"] = c99fn("pow", ("ulong4","ulong4",), "ulong4")
        self.functions["pow"] = c99fn("pow", ("ulong8","ulong8",), "ulong8")
        self.functions["pow"] = c99fn("pow", ("ulong16","ulong16",), "ulong16")
        self.functions["pown"] = c99fn("pown", ("float","int",), "float")
        self.functions["pown"] = c99fn("pown", ("float2","int2",), "float2")
        self.functions["pown"] = c99fn("pown", ("float4","int4",), "float4")
        self.functions["pown"] = c99fn("pown", ("float8","int8",), "float8")
        self.functions["pown"] = c99fn("pown", ("float16","int16",), "float16")
        self.functions["powr"] = c99fn("powr", ("char","char",), "char")
        self.functions["powr"] = c99fn("powr", ("char2","char2",), "char2")
        self.functions["powr"] = c99fn("powr", ("char4","char4",), "char4")
        self.functions["powr"] = c99fn("powr", ("char8","char8",), "char8")
        self.functions["powr"] = c99fn("powr", ("char16","char16",), "char16")
        self.functions["powr"] = c99fn("powr", ("uchar","uchar",), "uchar")
        self.functions["powr"] = c99fn("powr", ("uchar2","uchar2",), "uchar2")
        self.functions["powr"] = c99fn("powr", ("uchar4","uchar4",), "uchar4")
        self.functions["powr"] = c99fn("powr", ("uchar8","uchar8",), "uchar8")
        self.functions["powr"] = c99fn("powr", ("uchar16","uchar16",), "uchar16")
        self.functions["powr"] = c99fn("powr", ("short","short",), "short")
        self.functions["powr"] = c99fn("powr", ("short2","short2",), "short2")
        self.functions["powr"] = c99fn("powr", ("short4","short4",), "short4")
        self.functions["powr"] = c99fn("powr", ("short8","short8",), "short8")
        self.functions["powr"] = c99fn("powr", ("short16","short16",), "short16")
        self.functions["powr"] = c99fn("powr", ("ushort","ushort",), "ushort")
        self.functions["powr"] = c99fn("powr", ("ushort2","ushort2",), "ushort2")
        self.functions["powr"] = c99fn("powr", ("ushort4","ushort4",), "ushort4")
        self.functions["powr"] = c99fn("powr", ("ushort8","ushort8",), "ushort8")
        self.functions["powr"] = c99fn("powr", ("ushort16","ushort16",), "ushort16")
        self.functions["powr"] = c99fn("powr", ("int","int",), "int")
        self.functions["powr"] = c99fn("powr", ("int2","int2",), "int2")
        self.functions["powr"] = c99fn("powr", ("int4","int4",), "int4")
        self.functions["powr"] = c99fn("powr", ("int8","int8",), "int8")
        self.functions["powr"] = c99fn("powr", ("int16","int16",), "int16")
        self.functions["powr"] = c99fn("powr", ("uint","uint",), "uint")
        self.functions["powr"] = c99fn("powr", ("uint2","uint2",), "uint2")
        self.functions["powr"] = c99fn("powr", ("uint4","uint4",), "uint4")
        self.functions["powr"] = c99fn("powr", ("uint8","uint8",), "uint8")
        self.functions["powr"] = c99fn("powr", ("uint16","uint16",), "uint16")
        self.functions["powr"] = c99fn("powr", ("long","long",), "long")
        self.functions["powr"] = c99fn("powr", ("long2","long2",), "long2")
        self.functions["powr"] = c99fn("powr", ("long4","long4",), "long4")
        self.functions["powr"] = c99fn("powr", ("long8","long8",), "long8")
        self.functions["powr"] = c99fn("powr", ("long16","long16",), "long16")
        self.functions["powr"] = c99fn("powr", ("ulong","ulong",), "ulong")
        self.functions["powr"] = c99fn("powr", ("ulong2","ulong2",), "ulong2")
        self.functions["powr"] = c99fn("powr", ("ulong4","ulong4",), "ulong4")
        self.functions["powr"] = c99fn("powr", ("ulong8","ulong8",), "ulong8")
        self.functions["powr"] = c99fn("powr", ("ulong16","ulong16",), "ulong16")
        #TODO: floatn,float,remquoself.functions["rint"] = c99fn("rint", ("char",), "char")
        self.functions["rint"] = c99fn("rint", ("char2",), "char2")
        self.functions["rint"] = c99fn("rint", ("char4",), "char4")
        self.functions["rint"] = c99fn("rint", ("char8",), "char8")
        self.functions["rint"] = c99fn("rint", ("char16",), "char16")
        self.functions["rint"] = c99fn("rint", ("uchar",), "uchar")
        self.functions["rint"] = c99fn("rint", ("uchar2",), "uchar2")
        self.functions["rint"] = c99fn("rint", ("uchar4",), "uchar4")
        self.functions["rint"] = c99fn("rint", ("uchar8",), "uchar8")
        self.functions["rint"] = c99fn("rint", ("uchar16",), "uchar16")
        self.functions["rint"] = c99fn("rint", ("short",), "short")
        self.functions["rint"] = c99fn("rint", ("short2",), "short2")
        self.functions["rint"] = c99fn("rint", ("short4",), "short4")
        self.functions["rint"] = c99fn("rint", ("short8",), "short8")
        self.functions["rint"] = c99fn("rint", ("short16",), "short16")
        self.functions["rint"] = c99fn("rint", ("ushort",), "ushort")
        self.functions["rint"] = c99fn("rint", ("ushort2",), "ushort2")
        self.functions["rint"] = c99fn("rint", ("ushort4",), "ushort4")
        self.functions["rint"] = c99fn("rint", ("ushort8",), "ushort8")
        self.functions["rint"] = c99fn("rint", ("ushort16",), "ushort16")
        self.functions["rint"] = c99fn("rint", ("int",), "int")
        self.functions["rint"] = c99fn("rint", ("int2",), "int2")
        self.functions["rint"] = c99fn("rint", ("int4",), "int4")
        self.functions["rint"] = c99fn("rint", ("int8",), "int8")
        self.functions["rint"] = c99fn("rint", ("int16",), "int16")
        self.functions["rint"] = c99fn("rint", ("uint",), "uint")
        self.functions["rint"] = c99fn("rint", ("uint2",), "uint2")
        self.functions["rint"] = c99fn("rint", ("uint4",), "uint4")
        self.functions["rint"] = c99fn("rint", ("uint8",), "uint8")
        self.functions["rint"] = c99fn("rint", ("uint16",), "uint16")
        self.functions["rint"] = c99fn("rint", ("long",), "long")
        self.functions["rint"] = c99fn("rint", ("long2",), "long2")
        self.functions["rint"] = c99fn("rint", ("long4",), "long4")
        self.functions["rint"] = c99fn("rint", ("long8",), "long8")
        self.functions["rint"] = c99fn("rint", ("long16",), "long16")
        self.functions["rint"] = c99fn("rint", ("ulong",), "ulong")
        self.functions["rint"] = c99fn("rint", ("ulong2",), "ulong2")
        self.functions["rint"] = c99fn("rint", ("ulong4",), "ulong4")
        self.functions["rint"] = c99fn("rint", ("ulong8",), "ulong8")
        self.functions["rint"] = c99fn("rint", ("ulong16",), "ulong16")
        self.functions["rootn"] = c99fn("rootn", ("float","int",), "float")
        self.functions["rootn"] = c99fn("rootn", ("float2","int2",), "float2")
        self.functions["rootn"] = c99fn("rootn", ("float4","int4",), "float4")
        self.functions["rootn"] = c99fn("rootn", ("float8","int8",), "float8")
        self.functions["rootn"] = c99fn("rootn", ("float16","int16",), "float16")
        self.functions["round"] = c99fn("round", ("char",), "char")
        self.functions["round"] = c99fn("round", ("char2",), "char2")
        self.functions["round"] = c99fn("round", ("char4",), "char4")
        self.functions["round"] = c99fn("round", ("char8",), "char8")
        self.functions["round"] = c99fn("round", ("char16",), "char16")
        self.functions["round"] = c99fn("round", ("uchar",), "uchar")
        self.functions["round"] = c99fn("round", ("uchar2",), "uchar2")
        self.functions["round"] = c99fn("round", ("uchar4",), "uchar4")
        self.functions["round"] = c99fn("round", ("uchar8",), "uchar8")
        self.functions["round"] = c99fn("round", ("uchar16",), "uchar16")
        self.functions["round"] = c99fn("round", ("short",), "short")
        self.functions["round"] = c99fn("round", ("short2",), "short2")
        self.functions["round"] = c99fn("round", ("short4",), "short4")
        self.functions["round"] = c99fn("round", ("short8",), "short8")
        self.functions["round"] = c99fn("round", ("short16",), "short16")
        self.functions["round"] = c99fn("round", ("ushort",), "ushort")
        self.functions["round"] = c99fn("round", ("ushort2",), "ushort2")
        self.functions["round"] = c99fn("round", ("ushort4",), "ushort4")
        self.functions["round"] = c99fn("round", ("ushort8",), "ushort8")
        self.functions["round"] = c99fn("round", ("ushort16",), "ushort16")
        self.functions["round"] = c99fn("round", ("int",), "int")
        self.functions["round"] = c99fn("round", ("int2",), "int2")
        self.functions["round"] = c99fn("round", ("int4",), "int4")
        self.functions["round"] = c99fn("round", ("int8",), "int8")
        self.functions["round"] = c99fn("round", ("int16",), "int16")
        self.functions["round"] = c99fn("round", ("uint",), "uint")
        self.functions["round"] = c99fn("round", ("uint2",), "uint2")
        self.functions["round"] = c99fn("round", ("uint4",), "uint4")
        self.functions["round"] = c99fn("round", ("uint8",), "uint8")
        self.functions["round"] = c99fn("round", ("uint16",), "uint16")
        self.functions["round"] = c99fn("round", ("long",), "long")
        self.functions["round"] = c99fn("round", ("long2",), "long2")
        self.functions["round"] = c99fn("round", ("long4",), "long4")
        self.functions["round"] = c99fn("round", ("long8",), "long8")
        self.functions["round"] = c99fn("round", ("long16",), "long16")
        self.functions["round"] = c99fn("round", ("ulong",), "ulong")
        self.functions["round"] = c99fn("round", ("ulong2",), "ulong2")
        self.functions["round"] = c99fn("round", ("ulong4",), "ulong4")
        self.functions["round"] = c99fn("round", ("ulong8",), "ulong8")
        self.functions["round"] = c99fn("round", ("ulong16",), "ulong16")
        self.functions["rsqrt"] = c99fn("rsqrt", ("char",), "char")
        self.functions["rsqrt"] = c99fn("rsqrt", ("char2",), "char2")
        self.functions["rsqrt"] = c99fn("rsqrt", ("char4",), "char4")
        self.functions["rsqrt"] = c99fn("rsqrt", ("char8",), "char8")
        self.functions["rsqrt"] = c99fn("rsqrt", ("char16",), "char16")
        self.functions["rsqrt"] = c99fn("rsqrt", ("uchar",), "uchar")
        self.functions["rsqrt"] = c99fn("rsqrt", ("uchar2",), "uchar2")
        self.functions["rsqrt"] = c99fn("rsqrt", ("uchar4",), "uchar4")
        self.functions["rsqrt"] = c99fn("rsqrt", ("uchar8",), "uchar8")
        self.functions["rsqrt"] = c99fn("rsqrt", ("uchar16",), "uchar16")
        self.functions["rsqrt"] = c99fn("rsqrt", ("short",), "short")
        self.functions["rsqrt"] = c99fn("rsqrt", ("short2",), "short2")
        self.functions["rsqrt"] = c99fn("rsqrt", ("short4",), "short4")
        self.functions["rsqrt"] = c99fn("rsqrt", ("short8",), "short8")
        self.functions["rsqrt"] = c99fn("rsqrt", ("short16",), "short16")
        self.functions["rsqrt"] = c99fn("rsqrt", ("ushort",), "ushort")
        self.functions["rsqrt"] = c99fn("rsqrt", ("ushort2",), "ushort2")
        self.functions["rsqrt"] = c99fn("rsqrt", ("ushort4",), "ushort4")
        self.functions["rsqrt"] = c99fn("rsqrt", ("ushort8",), "ushort8")
        self.functions["rsqrt"] = c99fn("rsqrt", ("ushort16",), "ushort16")
        self.functions["rsqrt"] = c99fn("rsqrt", ("int",), "int")
        self.functions["rsqrt"] = c99fn("rsqrt", ("int2",), "int2")
        self.functions["rsqrt"] = c99fn("rsqrt", ("int4",), "int4")
        self.functions["rsqrt"] = c99fn("rsqrt", ("int8",), "int8")
        self.functions["rsqrt"] = c99fn("rsqrt", ("int16",), "int16")
        self.functions["rsqrt"] = c99fn("rsqrt", ("uint",), "uint")
        self.functions["rsqrt"] = c99fn("rsqrt", ("uint2",), "uint2")
        self.functions["rsqrt"] = c99fn("rsqrt", ("uint4",), "uint4")
        self.functions["rsqrt"] = c99fn("rsqrt", ("uint8",), "uint8")
        self.functions["rsqrt"] = c99fn("rsqrt", ("uint16",), "uint16")
        self.functions["rsqrt"] = c99fn("rsqrt", ("long",), "long")
        self.functions["rsqrt"] = c99fn("rsqrt", ("long2",), "long2")
        self.functions["rsqrt"] = c99fn("rsqrt", ("long4",), "long4")
        self.functions["rsqrt"] = c99fn("rsqrt", ("long8",), "long8")
        self.functions["rsqrt"] = c99fn("rsqrt", ("long16",), "long16")
        self.functions["rsqrt"] = c99fn("rsqrt", ("ulong",), "ulong")
        self.functions["rsqrt"] = c99fn("rsqrt", ("ulong2",), "ulong2")
        self.functions["rsqrt"] = c99fn("rsqrt", ("ulong4",), "ulong4")
        self.functions["rsqrt"] = c99fn("rsqrt", ("ulong8",), "ulong8")
        self.functions["rsqrt"] = c99fn("rsqrt", ("ulong16",), "ulong16")
        self.functions["sin"] = c99fn("sin", ("char",), "char")
        self.functions["sin"] = c99fn("sin", ("char2",), "char2")
        self.functions["sin"] = c99fn("sin", ("char4",), "char4")
        self.functions["sin"] = c99fn("sin", ("char8",), "char8")
        self.functions["sin"] = c99fn("sin", ("char16",), "char16")
        self.functions["sin"] = c99fn("sin", ("uchar",), "uchar")
        self.functions["sin"] = c99fn("sin", ("uchar2",), "uchar2")
        self.functions["sin"] = c99fn("sin", ("uchar4",), "uchar4")
        self.functions["sin"] = c99fn("sin", ("uchar8",), "uchar8")
        self.functions["sin"] = c99fn("sin", ("uchar16",), "uchar16")
        self.functions["sin"] = c99fn("sin", ("short",), "short")
        self.functions["sin"] = c99fn("sin", ("short2",), "short2")
        self.functions["sin"] = c99fn("sin", ("short4",), "short4")
        self.functions["sin"] = c99fn("sin", ("short8",), "short8")
        self.functions["sin"] = c99fn("sin", ("short16",), "short16")
        self.functions["sin"] = c99fn("sin", ("ushort",), "ushort")
        self.functions["sin"] = c99fn("sin", ("ushort2",), "ushort2")
        self.functions["sin"] = c99fn("sin", ("ushort4",), "ushort4")
        self.functions["sin"] = c99fn("sin", ("ushort8",), "ushort8")
        self.functions["sin"] = c99fn("sin", ("ushort16",), "ushort16")
        self.functions["sin"] = c99fn("sin", ("int",), "int")
        self.functions["sin"] = c99fn("sin", ("int2",), "int2")
        self.functions["sin"] = c99fn("sin", ("int4",), "int4")
        self.functions["sin"] = c99fn("sin", ("int8",), "int8")
        self.functions["sin"] = c99fn("sin", ("int16",), "int16")
        self.functions["sin"] = c99fn("sin", ("uint",), "uint")
        self.functions["sin"] = c99fn("sin", ("uint2",), "uint2")
        self.functions["sin"] = c99fn("sin", ("uint4",), "uint4")
        self.functions["sin"] = c99fn("sin", ("uint8",), "uint8")
        self.functions["sin"] = c99fn("sin", ("uint16",), "uint16")
        self.functions["sin"] = c99fn("sin", ("long",), "long")
        self.functions["sin"] = c99fn("sin", ("long2",), "long2")
        self.functions["sin"] = c99fn("sin", ("long4",), "long4")
        self.functions["sin"] = c99fn("sin", ("long8",), "long8")
        self.functions["sin"] = c99fn("sin", ("long16",), "long16")
        self.functions["sin"] = c99fn("sin", ("ulong",), "ulong")
        self.functions["sin"] = c99fn("sin", ("ulong2",), "ulong2")
        self.functions["sin"] = c99fn("sin", ("ulong4",), "ulong4")
        self.functions["sin"] = c99fn("sin", ("ulong8",), "ulong8")
        self.functions["sin"] = c99fn("sin", ("ulong16",), "ulong16")
        #TODO: sincosself.functions["sinh"] = c99fn("sinh", ("char",), "char")
        self.functions["sinh"] = c99fn("sinh", ("char2",), "char2")
        self.functions["sinh"] = c99fn("sinh", ("char4",), "char4")
        self.functions["sinh"] = c99fn("sinh", ("char8",), "char8")
        self.functions["sinh"] = c99fn("sinh", ("char16",), "char16")
        self.functions["sinh"] = c99fn("sinh", ("uchar",), "uchar")
        self.functions["sinh"] = c99fn("sinh", ("uchar2",), "uchar2")
        self.functions["sinh"] = c99fn("sinh", ("uchar4",), "uchar4")
        self.functions["sinh"] = c99fn("sinh", ("uchar8",), "uchar8")
        self.functions["sinh"] = c99fn("sinh", ("uchar16",), "uchar16")
        self.functions["sinh"] = c99fn("sinh", ("short",), "short")
        self.functions["sinh"] = c99fn("sinh", ("short2",), "short2")
        self.functions["sinh"] = c99fn("sinh", ("short4",), "short4")
        self.functions["sinh"] = c99fn("sinh", ("short8",), "short8")
        self.functions["sinh"] = c99fn("sinh", ("short16",), "short16")
        self.functions["sinh"] = c99fn("sinh", ("ushort",), "ushort")
        self.functions["sinh"] = c99fn("sinh", ("ushort2",), "ushort2")
        self.functions["sinh"] = c99fn("sinh", ("ushort4",), "ushort4")
        self.functions["sinh"] = c99fn("sinh", ("ushort8",), "ushort8")
        self.functions["sinh"] = c99fn("sinh", ("ushort16",), "ushort16")
        self.functions["sinh"] = c99fn("sinh", ("int",), "int")
        self.functions["sinh"] = c99fn("sinh", ("int2",), "int2")
        self.functions["sinh"] = c99fn("sinh", ("int4",), "int4")
        self.functions["sinh"] = c99fn("sinh", ("int8",), "int8")
        self.functions["sinh"] = c99fn("sinh", ("int16",), "int16")
        self.functions["sinh"] = c99fn("sinh", ("uint",), "uint")
        self.functions["sinh"] = c99fn("sinh", ("uint2",), "uint2")
        self.functions["sinh"] = c99fn("sinh", ("uint4",), "uint4")
        self.functions["sinh"] = c99fn("sinh", ("uint8",), "uint8")
        self.functions["sinh"] = c99fn("sinh", ("uint16",), "uint16")
        self.functions["sinh"] = c99fn("sinh", ("long",), "long")
        self.functions["sinh"] = c99fn("sinh", ("long2",), "long2")
        self.functions["sinh"] = c99fn("sinh", ("long4",), "long4")
        self.functions["sinh"] = c99fn("sinh", ("long8",), "long8")
        self.functions["sinh"] = c99fn("sinh", ("long16",), "long16")
        self.functions["sinh"] = c99fn("sinh", ("ulong",), "ulong")
        self.functions["sinh"] = c99fn("sinh", ("ulong2",), "ulong2")
        self.functions["sinh"] = c99fn("sinh", ("ulong4",), "ulong4")
        self.functions["sinh"] = c99fn("sinh", ("ulong8",), "ulong8")
        self.functions["sinh"] = c99fn("sinh", ("ulong16",), "ulong16")
        self.functions["sinpi"] = c99fn("sinpi", ("char",), "char")
        self.functions["sinpi"] = c99fn("sinpi", ("char2",), "char2")
        self.functions["sinpi"] = c99fn("sinpi", ("char4",), "char4")
        self.functions["sinpi"] = c99fn("sinpi", ("char8",), "char8")
        self.functions["sinpi"] = c99fn("sinpi", ("char16",), "char16")
        self.functions["sinpi"] = c99fn("sinpi", ("uchar",), "uchar")
        self.functions["sinpi"] = c99fn("sinpi", ("uchar2",), "uchar2")
        self.functions["sinpi"] = c99fn("sinpi", ("uchar4",), "uchar4")
        self.functions["sinpi"] = c99fn("sinpi", ("uchar8",), "uchar8")
        self.functions["sinpi"] = c99fn("sinpi", ("uchar16",), "uchar16")
        self.functions["sinpi"] = c99fn("sinpi", ("short",), "short")
        self.functions["sinpi"] = c99fn("sinpi", ("short2",), "short2")
        self.functions["sinpi"] = c99fn("sinpi", ("short4",), "short4")
        self.functions["sinpi"] = c99fn("sinpi", ("short8",), "short8")
        self.functions["sinpi"] = c99fn("sinpi", ("short16",), "short16")
        self.functions["sinpi"] = c99fn("sinpi", ("ushort",), "ushort")
        self.functions["sinpi"] = c99fn("sinpi", ("ushort2",), "ushort2")
        self.functions["sinpi"] = c99fn("sinpi", ("ushort4",), "ushort4")
        self.functions["sinpi"] = c99fn("sinpi", ("ushort8",), "ushort8")
        self.functions["sinpi"] = c99fn("sinpi", ("ushort16",), "ushort16")
        self.functions["sinpi"] = c99fn("sinpi", ("int",), "int")
        self.functions["sinpi"] = c99fn("sinpi", ("int2",), "int2")
        self.functions["sinpi"] = c99fn("sinpi", ("int4",), "int4")
        self.functions["sinpi"] = c99fn("sinpi", ("int8",), "int8")
        self.functions["sinpi"] = c99fn("sinpi", ("int16",), "int16")
        self.functions["sinpi"] = c99fn("sinpi", ("uint",), "uint")
        self.functions["sinpi"] = c99fn("sinpi", ("uint2",), "uint2")
        self.functions["sinpi"] = c99fn("sinpi", ("uint4",), "uint4")
        self.functions["sinpi"] = c99fn("sinpi", ("uint8",), "uint8")
        self.functions["sinpi"] = c99fn("sinpi", ("uint16",), "uint16")
        self.functions["sinpi"] = c99fn("sinpi", ("long",), "long")
        self.functions["sinpi"] = c99fn("sinpi", ("long2",), "long2")
        self.functions["sinpi"] = c99fn("sinpi", ("long4",), "long4")
        self.functions["sinpi"] = c99fn("sinpi", ("long8",), "long8")
        self.functions["sinpi"] = c99fn("sinpi", ("long16",), "long16")
        self.functions["sinpi"] = c99fn("sinpi", ("ulong",), "ulong")
        self.functions["sinpi"] = c99fn("sinpi", ("ulong2",), "ulong2")
        self.functions["sinpi"] = c99fn("sinpi", ("ulong4",), "ulong4")
        self.functions["sinpi"] = c99fn("sinpi", ("ulong8",), "ulong8")
        self.functions["sinpi"] = c99fn("sinpi", ("ulong16",), "ulong16")
        self.functions["sqrt"] = c99fn("sqrt", ("char",), "char")
        self.functions["sqrt"] = c99fn("sqrt", ("char2",), "char2")
        self.functions["sqrt"] = c99fn("sqrt", ("char4",), "char4")
        self.functions["sqrt"] = c99fn("sqrt", ("char8",), "char8")
        self.functions["sqrt"] = c99fn("sqrt", ("char16",), "char16")
        self.functions["sqrt"] = c99fn("sqrt", ("uchar",), "uchar")
        self.functions["sqrt"] = c99fn("sqrt", ("uchar2",), "uchar2")
        self.functions["sqrt"] = c99fn("sqrt", ("uchar4",), "uchar4")
        self.functions["sqrt"] = c99fn("sqrt", ("uchar8",), "uchar8")
        self.functions["sqrt"] = c99fn("sqrt", ("uchar16",), "uchar16")
        self.functions["sqrt"] = c99fn("sqrt", ("short",), "short")
        self.functions["sqrt"] = c99fn("sqrt", ("short2",), "short2")
        self.functions["sqrt"] = c99fn("sqrt", ("short4",), "short4")
        self.functions["sqrt"] = c99fn("sqrt", ("short8",), "short8")
        self.functions["sqrt"] = c99fn("sqrt", ("short16",), "short16")
        self.functions["sqrt"] = c99fn("sqrt", ("ushort",), "ushort")
        self.functions["sqrt"] = c99fn("sqrt", ("ushort2",), "ushort2")
        self.functions["sqrt"] = c99fn("sqrt", ("ushort4",), "ushort4")
        self.functions["sqrt"] = c99fn("sqrt", ("ushort8",), "ushort8")
        self.functions["sqrt"] = c99fn("sqrt", ("ushort16",), "ushort16")
        self.functions["sqrt"] = c99fn("sqrt", ("int",), "int")
        self.functions["sqrt"] = c99fn("sqrt", ("int2",), "int2")
        self.functions["sqrt"] = c99fn("sqrt", ("int4",), "int4")
        self.functions["sqrt"] = c99fn("sqrt", ("int8",), "int8")
        self.functions["sqrt"] = c99fn("sqrt", ("int16",), "int16")
        self.functions["sqrt"] = c99fn("sqrt", ("uint",), "uint")
        self.functions["sqrt"] = c99fn("sqrt", ("uint2",), "uint2")
        self.functions["sqrt"] = c99fn("sqrt", ("uint4",), "uint4")
        self.functions["sqrt"] = c99fn("sqrt", ("uint8",), "uint8")
        self.functions["sqrt"] = c99fn("sqrt", ("uint16",), "uint16")
        self.functions["sqrt"] = c99fn("sqrt", ("long",), "long")
        self.functions["sqrt"] = c99fn("sqrt", ("long2",), "long2")
        self.functions["sqrt"] = c99fn("sqrt", ("long4",), "long4")
        self.functions["sqrt"] = c99fn("sqrt", ("long8",), "long8")
        self.functions["sqrt"] = c99fn("sqrt", ("long16",), "long16")
        self.functions["sqrt"] = c99fn("sqrt", ("ulong",), "ulong")
        self.functions["sqrt"] = c99fn("sqrt", ("ulong2",), "ulong2")
        self.functions["sqrt"] = c99fn("sqrt", ("ulong4",), "ulong4")
        self.functions["sqrt"] = c99fn("sqrt", ("ulong8",), "ulong8")
        self.functions["sqrt"] = c99fn("sqrt", ("ulong16",), "ulong16")
        self.functions["tan"] = c99fn("tan", ("char",), "char")
        self.functions["tan"] = c99fn("tan", ("char2",), "char2")
        self.functions["tan"] = c99fn("tan", ("char4",), "char4")
        self.functions["tan"] = c99fn("tan", ("char8",), "char8")
        self.functions["tan"] = c99fn("tan", ("char16",), "char16")
        self.functions["tan"] = c99fn("tan", ("uchar",), "uchar")
        self.functions["tan"] = c99fn("tan", ("uchar2",), "uchar2")
        self.functions["tan"] = c99fn("tan", ("uchar4",), "uchar4")
        self.functions["tan"] = c99fn("tan", ("uchar8",), "uchar8")
        self.functions["tan"] = c99fn("tan", ("uchar16",), "uchar16")
        self.functions["tan"] = c99fn("tan", ("short",), "short")
        self.functions["tan"] = c99fn("tan", ("short2",), "short2")
        self.functions["tan"] = c99fn("tan", ("short4",), "short4")
        self.functions["tan"] = c99fn("tan", ("short8",), "short8")
        self.functions["tan"] = c99fn("tan", ("short16",), "short16")
        self.functions["tan"] = c99fn("tan", ("ushort",), "ushort")
        self.functions["tan"] = c99fn("tan", ("ushort2",), "ushort2")
        self.functions["tan"] = c99fn("tan", ("ushort4",), "ushort4")
        self.functions["tan"] = c99fn("tan", ("ushort8",), "ushort8")
        self.functions["tan"] = c99fn("tan", ("ushort16",), "ushort16")
        self.functions["tan"] = c99fn("tan", ("int",), "int")
        self.functions["tan"] = c99fn("tan", ("int2",), "int2")
        self.functions["tan"] = c99fn("tan", ("int4",), "int4")
        self.functions["tan"] = c99fn("tan", ("int8",), "int8")
        self.functions["tan"] = c99fn("tan", ("int16",), "int16")
        self.functions["tan"] = c99fn("tan", ("uint",), "uint")
        self.functions["tan"] = c99fn("tan", ("uint2",), "uint2")
        self.functions["tan"] = c99fn("tan", ("uint4",), "uint4")
        self.functions["tan"] = c99fn("tan", ("uint8",), "uint8")
        self.functions["tan"] = c99fn("tan", ("uint16",), "uint16")
        self.functions["tan"] = c99fn("tan", ("long",), "long")
        self.functions["tan"] = c99fn("tan", ("long2",), "long2")
        self.functions["tan"] = c99fn("tan", ("long4",), "long4")
        self.functions["tan"] = c99fn("tan", ("long8",), "long8")
        self.functions["tan"] = c99fn("tan", ("long16",), "long16")
        self.functions["tan"] = c99fn("tan", ("ulong",), "ulong")
        self.functions["tan"] = c99fn("tan", ("ulong2",), "ulong2")
        self.functions["tan"] = c99fn("tan", ("ulong4",), "ulong4")
        self.functions["tan"] = c99fn("tan", ("ulong8",), "ulong8")
        self.functions["tan"] = c99fn("tan", ("ulong16",), "ulong16")
        self.functions["tanh"] = c99fn("tanh", ("char",), "char")
        self.functions["tanh"] = c99fn("tanh", ("char2",), "char2")
        self.functions["tanh"] = c99fn("tanh", ("char4",), "char4")
        self.functions["tanh"] = c99fn("tanh", ("char8",), "char8")
        self.functions["tanh"] = c99fn("tanh", ("char16",), "char16")
        self.functions["tanh"] = c99fn("tanh", ("uchar",), "uchar")
        self.functions["tanh"] = c99fn("tanh", ("uchar2",), "uchar2")
        self.functions["tanh"] = c99fn("tanh", ("uchar4",), "uchar4")
        self.functions["tanh"] = c99fn("tanh", ("uchar8",), "uchar8")
        self.functions["tanh"] = c99fn("tanh", ("uchar16",), "uchar16")
        self.functions["tanh"] = c99fn("tanh", ("short",), "short")
        self.functions["tanh"] = c99fn("tanh", ("short2",), "short2")
        self.functions["tanh"] = c99fn("tanh", ("short4",), "short4")
        self.functions["tanh"] = c99fn("tanh", ("short8",), "short8")
        self.functions["tanh"] = c99fn("tanh", ("short16",), "short16")
        self.functions["tanh"] = c99fn("tanh", ("ushort",), "ushort")
        self.functions["tanh"] = c99fn("tanh", ("ushort2",), "ushort2")
        self.functions["tanh"] = c99fn("tanh", ("ushort4",), "ushort4")
        self.functions["tanh"] = c99fn("tanh", ("ushort8",), "ushort8")
        self.functions["tanh"] = c99fn("tanh", ("ushort16",), "ushort16")
        self.functions["tanh"] = c99fn("tanh", ("int",), "int")
        self.functions["tanh"] = c99fn("tanh", ("int2",), "int2")
        self.functions["tanh"] = c99fn("tanh", ("int4",), "int4")
        self.functions["tanh"] = c99fn("tanh", ("int8",), "int8")
        self.functions["tanh"] = c99fn("tanh", ("int16",), "int16")
        self.functions["tanh"] = c99fn("tanh", ("uint",), "uint")
        self.functions["tanh"] = c99fn("tanh", ("uint2",), "uint2")
        self.functions["tanh"] = c99fn("tanh", ("uint4",), "uint4")
        self.functions["tanh"] = c99fn("tanh", ("uint8",), "uint8")
        self.functions["tanh"] = c99fn("tanh", ("uint16",), "uint16")
        self.functions["tanh"] = c99fn("tanh", ("long",), "long")
        self.functions["tanh"] = c99fn("tanh", ("long2",), "long2")
        self.functions["tanh"] = c99fn("tanh", ("long4",), "long4")
        self.functions["tanh"] = c99fn("tanh", ("long8",), "long8")
        self.functions["tanh"] = c99fn("tanh", ("long16",), "long16")
        self.functions["tanh"] = c99fn("tanh", ("ulong",), "ulong")
        self.functions["tanh"] = c99fn("tanh", ("ulong2",), "ulong2")
        self.functions["tanh"] = c99fn("tanh", ("ulong4",), "ulong4")
        self.functions["tanh"] = c99fn("tanh", ("ulong8",), "ulong8")
        self.functions["tanh"] = c99fn("tanh", ("ulong16",), "ulong16")
        self.functions["tanpi"] = c99fn("tanpi", ("char",), "char")
        self.functions["tanpi"] = c99fn("tanpi", ("char2",), "char2")
        self.functions["tanpi"] = c99fn("tanpi", ("char4",), "char4")
        self.functions["tanpi"] = c99fn("tanpi", ("char8",), "char8")
        self.functions["tanpi"] = c99fn("tanpi", ("char16",), "char16")
        self.functions["tanpi"] = c99fn("tanpi", ("uchar",), "uchar")
        self.functions["tanpi"] = c99fn("tanpi", ("uchar2",), "uchar2")
        self.functions["tanpi"] = c99fn("tanpi", ("uchar4",), "uchar4")
        self.functions["tanpi"] = c99fn("tanpi", ("uchar8",), "uchar8")
        self.functions["tanpi"] = c99fn("tanpi", ("uchar16",), "uchar16")
        self.functions["tanpi"] = c99fn("tanpi", ("short",), "short")
        self.functions["tanpi"] = c99fn("tanpi", ("short2",), "short2")
        self.functions["tanpi"] = c99fn("tanpi", ("short4",), "short4")
        self.functions["tanpi"] = c99fn("tanpi", ("short8",), "short8")
        self.functions["tanpi"] = c99fn("tanpi", ("short16",), "short16")
        self.functions["tanpi"] = c99fn("tanpi", ("ushort",), "ushort")
        self.functions["tanpi"] = c99fn("tanpi", ("ushort2",), "ushort2")
        self.functions["tanpi"] = c99fn("tanpi", ("ushort4",), "ushort4")
        self.functions["tanpi"] = c99fn("tanpi", ("ushort8",), "ushort8")
        self.functions["tanpi"] = c99fn("tanpi", ("ushort16",), "ushort16")
        self.functions["tanpi"] = c99fn("tanpi", ("int",), "int")
        self.functions["tanpi"] = c99fn("tanpi", ("int2",), "int2")
        self.functions["tanpi"] = c99fn("tanpi", ("int4",), "int4")
        self.functions["tanpi"] = c99fn("tanpi", ("int8",), "int8")
        self.functions["tanpi"] = c99fn("tanpi", ("int16",), "int16")
        self.functions["tanpi"] = c99fn("tanpi", ("uint",), "uint")
        self.functions["tanpi"] = c99fn("tanpi", ("uint2",), "uint2")
        self.functions["tanpi"] = c99fn("tanpi", ("uint4",), "uint4")
        self.functions["tanpi"] = c99fn("tanpi", ("uint8",), "uint8")
        self.functions["tanpi"] = c99fn("tanpi", ("uint16",), "uint16")
        self.functions["tanpi"] = c99fn("tanpi", ("long",), "long")
        self.functions["tanpi"] = c99fn("tanpi", ("long2",), "long2")
        self.functions["tanpi"] = c99fn("tanpi", ("long4",), "long4")
        self.functions["tanpi"] = c99fn("tanpi", ("long8",), "long8")
        self.functions["tanpi"] = c99fn("tanpi", ("long16",), "long16")
        self.functions["tanpi"] = c99fn("tanpi", ("ulong",), "ulong")
        self.functions["tanpi"] = c99fn("tanpi", ("ulong2",), "ulong2")
        self.functions["tanpi"] = c99fn("tanpi", ("ulong4",), "ulong4")
        self.functions["tanpi"] = c99fn("tanpi", ("ulong8",), "ulong8")
        self.functions["tanpi"] = c99fn("tanpi", ("ulong16",), "ulong16")
        self.functions["tgamma"] = c99fn("tgamma", ("char",), "char")
        self.functions["tgamma"] = c99fn("tgamma", ("char2",), "char2")
        self.functions["tgamma"] = c99fn("tgamma", ("char4",), "char4")
        self.functions["tgamma"] = c99fn("tgamma", ("char8",), "char8")
        self.functions["tgamma"] = c99fn("tgamma", ("char16",), "char16")
        self.functions["tgamma"] = c99fn("tgamma", ("uchar",), "uchar")
        self.functions["tgamma"] = c99fn("tgamma", ("uchar2",), "uchar2")
        self.functions["tgamma"] = c99fn("tgamma", ("uchar4",), "uchar4")
        self.functions["tgamma"] = c99fn("tgamma", ("uchar8",), "uchar8")
        self.functions["tgamma"] = c99fn("tgamma", ("uchar16",), "uchar16")
        self.functions["tgamma"] = c99fn("tgamma", ("short",), "short")
        self.functions["tgamma"] = c99fn("tgamma", ("short2",), "short2")
        self.functions["tgamma"] = c99fn("tgamma", ("short4",), "short4")
        self.functions["tgamma"] = c99fn("tgamma", ("short8",), "short8")
        self.functions["tgamma"] = c99fn("tgamma", ("short16",), "short16")
        self.functions["tgamma"] = c99fn("tgamma", ("ushort",), "ushort")
        self.functions["tgamma"] = c99fn("tgamma", ("ushort2",), "ushort2")
        self.functions["tgamma"] = c99fn("tgamma", ("ushort4",), "ushort4")
        self.functions["tgamma"] = c99fn("tgamma", ("ushort8",), "ushort8")
        self.functions["tgamma"] = c99fn("tgamma", ("ushort16",), "ushort16")
        self.functions["tgamma"] = c99fn("tgamma", ("int",), "int")
        self.functions["tgamma"] = c99fn("tgamma", ("int2",), "int2")
        self.functions["tgamma"] = c99fn("tgamma", ("int4",), "int4")
        self.functions["tgamma"] = c99fn("tgamma", ("int8",), "int8")
        self.functions["tgamma"] = c99fn("tgamma", ("int16",), "int16")
        self.functions["tgamma"] = c99fn("tgamma", ("uint",), "uint")
        self.functions["tgamma"] = c99fn("tgamma", ("uint2",), "uint2")
        self.functions["tgamma"] = c99fn("tgamma", ("uint4",), "uint4")
        self.functions["tgamma"] = c99fn("tgamma", ("uint8",), "uint8")
        self.functions["tgamma"] = c99fn("tgamma", ("uint16",), "uint16")
        self.functions["tgamma"] = c99fn("tgamma", ("long",), "long")
        self.functions["tgamma"] = c99fn("tgamma", ("long2",), "long2")
        self.functions["tgamma"] = c99fn("tgamma", ("long4",), "long4")
        self.functions["tgamma"] = c99fn("tgamma", ("long8",), "long8")
        self.functions["tgamma"] = c99fn("tgamma", ("long16",), "long16")
        self.functions["tgamma"] = c99fn("tgamma", ("ulong",), "ulong")
        self.functions["tgamma"] = c99fn("tgamma", ("ulong2",), "ulong2")
        self.functions["tgamma"] = c99fn("tgamma", ("ulong4",), "ulong4")
        self.functions["tgamma"] = c99fn("tgamma", ("ulong8",), "ulong8")
        self.functions["tgamma"] = c99fn("tgamma", ("ulong16",), "ulong16")
        self.functions["tunc"] = c99fn("tunc", ("char",), "char")
        self.functions["tunc"] = c99fn("tunc", ("char2",), "char2")
        self.functions["tunc"] = c99fn("tunc", ("char4",), "char4")
        self.functions["tunc"] = c99fn("tunc", ("char8",), "char8")
        self.functions["tunc"] = c99fn("tunc", ("char16",), "char16")
        self.functions["tunc"] = c99fn("tunc", ("uchar",), "uchar")
        self.functions["tunc"] = c99fn("tunc", ("uchar2",), "uchar2")
        self.functions["tunc"] = c99fn("tunc", ("uchar4",), "uchar4")
        self.functions["tunc"] = c99fn("tunc", ("uchar8",), "uchar8")
        self.functions["tunc"] = c99fn("tunc", ("uchar16",), "uchar16")
        self.functions["tunc"] = c99fn("tunc", ("short",), "short")
        self.functions["tunc"] = c99fn("tunc", ("short2",), "short2")
        self.functions["tunc"] = c99fn("tunc", ("short4",), "short4")
        self.functions["tunc"] = c99fn("tunc", ("short8",), "short8")
        self.functions["tunc"] = c99fn("tunc", ("short16",), "short16")
        self.functions["tunc"] = c99fn("tunc", ("ushort",), "ushort")
        self.functions["tunc"] = c99fn("tunc", ("ushort2",), "ushort2")
        self.functions["tunc"] = c99fn("tunc", ("ushort4",), "ushort4")
        self.functions["tunc"] = c99fn("tunc", ("ushort8",), "ushort8")
        self.functions["tunc"] = c99fn("tunc", ("ushort16",), "ushort16")
        self.functions["tunc"] = c99fn("tunc", ("int",), "int")
        self.functions["tunc"] = c99fn("tunc", ("int2",), "int2")
        self.functions["tunc"] = c99fn("tunc", ("int4",), "int4")
        self.functions["tunc"] = c99fn("tunc", ("int8",), "int8")
        self.functions["tunc"] = c99fn("tunc", ("int16",), "int16")
        self.functions["tunc"] = c99fn("tunc", ("uint",), "uint")
        self.functions["tunc"] = c99fn("tunc", ("uint2",), "uint2")
        self.functions["tunc"] = c99fn("tunc", ("uint4",), "uint4")
        self.functions["tunc"] = c99fn("tunc", ("uint8",), "uint8")
        self.functions["tunc"] = c99fn("tunc", ("uint16",), "uint16")
        self.functions["tunc"] = c99fn("tunc", ("long",), "long")
        self.functions["tunc"] = c99fn("tunc", ("long2",), "long2")
        self.functions["tunc"] = c99fn("tunc", ("long4",), "long4")
        self.functions["tunc"] = c99fn("tunc", ("long8",), "long8")
        self.functions["tunc"] = c99fn("tunc", ("long16",), "long16")
        self.functions["tunc"] = c99fn("tunc", ("ulong",), "ulong")
        self.functions["tunc"] = c99fn("tunc", ("ulong2",), "ulong2")
        self.functions["tunc"] = c99fn("tunc", ("ulong4",), "ulong4")
        self.functions["tunc"] = c99fn("tunc", ("ulong8",), "ulong8")
        self.functions["tunc"] = c99fn("tunc", ("ulong16",), "ulong16")
        self.functions["half_cos"] = c99fn("half_cos", ("char",), "char")
        self.functions["half_cos"] = c99fn("half_cos", ("char2",), "char2")
        self.functions["half_cos"] = c99fn("half_cos", ("char4",), "char4")
        self.functions["half_cos"] = c99fn("half_cos", ("char8",), "char8")
        self.functions["half_cos"] = c99fn("half_cos", ("char16",), "char16")
        self.functions["half_cos"] = c99fn("half_cos", ("uchar",), "uchar")
        self.functions["half_cos"] = c99fn("half_cos", ("uchar2",), "uchar2")
        self.functions["half_cos"] = c99fn("half_cos", ("uchar4",), "uchar4")
        self.functions["half_cos"] = c99fn("half_cos", ("uchar8",), "uchar8")
        self.functions["half_cos"] = c99fn("half_cos", ("uchar16",), "uchar16")
        self.functions["half_cos"] = c99fn("half_cos", ("short",), "short")
        self.functions["half_cos"] = c99fn("half_cos", ("short2",), "short2")
        self.functions["half_cos"] = c99fn("half_cos", ("short4",), "short4")
        self.functions["half_cos"] = c99fn("half_cos", ("short8",), "short8")
        self.functions["half_cos"] = c99fn("half_cos", ("short16",), "short16")
        self.functions["half_cos"] = c99fn("half_cos", ("ushort",), "ushort")
        self.functions["half_cos"] = c99fn("half_cos", ("ushort2",), "ushort2")
        self.functions["half_cos"] = c99fn("half_cos", ("ushort4",), "ushort4")
        self.functions["half_cos"] = c99fn("half_cos", ("ushort8",), "ushort8")
        self.functions["half_cos"] = c99fn("half_cos", ("ushort16",), "ushort16")
        self.functions["half_cos"] = c99fn("half_cos", ("int",), "int")
        self.functions["half_cos"] = c99fn("half_cos", ("int2",), "int2")
        self.functions["half_cos"] = c99fn("half_cos", ("int4",), "int4")
        self.functions["half_cos"] = c99fn("half_cos", ("int8",), "int8")
        self.functions["half_cos"] = c99fn("half_cos", ("int16",), "int16")
        self.functions["half_cos"] = c99fn("half_cos", ("uint",), "uint")
        self.functions["half_cos"] = c99fn("half_cos", ("uint2",), "uint2")
        self.functions["half_cos"] = c99fn("half_cos", ("uint4",), "uint4")
        self.functions["half_cos"] = c99fn("half_cos", ("uint8",), "uint8")
        self.functions["half_cos"] = c99fn("half_cos", ("uint16",), "uint16")
        self.functions["half_cos"] = c99fn("half_cos", ("long",), "long")
        self.functions["half_cos"] = c99fn("half_cos", ("long2",), "long2")
        self.functions["half_cos"] = c99fn("half_cos", ("long4",), "long4")
        self.functions["half_cos"] = c99fn("half_cos", ("long8",), "long8")
        self.functions["half_cos"] = c99fn("half_cos", ("long16",), "long16")
        self.functions["half_cos"] = c99fn("half_cos", ("ulong",), "ulong")
        self.functions["half_cos"] = c99fn("half_cos", ("ulong2",), "ulong2")
        self.functions["half_cos"] = c99fn("half_cos", ("ulong4",), "ulong4")
        self.functions["half_cos"] = c99fn("half_cos", ("ulong8",), "ulong8")
        self.functions["half_cos"] = c99fn("half_cos", ("ulong16",), "ulong16")
        self.functions["half_divide"] = c99fn("half_divide", ("char",), "char")
        self.functions["half_divide"] = c99fn("half_divide", ("char2",), "char2")
        self.functions["half_divide"] = c99fn("half_divide", ("char4",), "char4")
        self.functions["half_divide"] = c99fn("half_divide", ("char8",), "char8")
        self.functions["half_divide"] = c99fn("half_divide", ("char16",), "char16")
        self.functions["half_divide"] = c99fn("half_divide", ("uchar",), "uchar")
        self.functions["half_divide"] = c99fn("half_divide", ("uchar2",), "uchar2")
        self.functions["half_divide"] = c99fn("half_divide", ("uchar4",), "uchar4")
        self.functions["half_divide"] = c99fn("half_divide", ("uchar8",), "uchar8")
        self.functions["half_divide"] = c99fn("half_divide", ("uchar16",), "uchar16")
        self.functions["half_divide"] = c99fn("half_divide", ("short",), "short")
        self.functions["half_divide"] = c99fn("half_divide", ("short2",), "short2")
        self.functions["half_divide"] = c99fn("half_divide", ("short4",), "short4")
        self.functions["half_divide"] = c99fn("half_divide", ("short8",), "short8")
        self.functions["half_divide"] = c99fn("half_divide", ("short16",), "short16")
        self.functions["half_divide"] = c99fn("half_divide", ("ushort",), "ushort")
        self.functions["half_divide"] = c99fn("half_divide", ("ushort2",), "ushort2")
        self.functions["half_divide"] = c99fn("half_divide", ("ushort4",), "ushort4")
        self.functions["half_divide"] = c99fn("half_divide", ("ushort8",), "ushort8")
        self.functions["half_divide"] = c99fn("half_divide", ("ushort16",), "ushort16")
        self.functions["half_divide"] = c99fn("half_divide", ("int",), "int")
        self.functions["half_divide"] = c99fn("half_divide", ("int2",), "int2")
        self.functions["half_divide"] = c99fn("half_divide", ("int4",), "int4")
        self.functions["half_divide"] = c99fn("half_divide", ("int8",), "int8")
        self.functions["half_divide"] = c99fn("half_divide", ("int16",), "int16")
        self.functions["half_divide"] = c99fn("half_divide", ("uint",), "uint")
        self.functions["half_divide"] = c99fn("half_divide", ("uint2",), "uint2")
        self.functions["half_divide"] = c99fn("half_divide", ("uint4",), "uint4")
        self.functions["half_divide"] = c99fn("half_divide", ("uint8",), "uint8")
        self.functions["half_divide"] = c99fn("half_divide", ("uint16",), "uint16")
        self.functions["half_divide"] = c99fn("half_divide", ("long",), "long")
        self.functions["half_divide"] = c99fn("half_divide", ("long2",), "long2")
        self.functions["half_divide"] = c99fn("half_divide", ("long4",), "long4")
        self.functions["half_divide"] = c99fn("half_divide", ("long8",), "long8")
        self.functions["half_divide"] = c99fn("half_divide", ("long16",), "long16")
        self.functions["half_divide"] = c99fn("half_divide", ("ulong",), "ulong")
        self.functions["half_divide"] = c99fn("half_divide", ("ulong2",), "ulong2")
        self.functions["half_divide"] = c99fn("half_divide", ("ulong4",), "ulong4")
        self.functions["half_divide"] = c99fn("half_divide", ("ulong8",), "ulong8")
        self.functions["half_divide"] = c99fn("half_divide", ("ulong16",), "ulong16")
        self.functions["half_exp"] = c99fn("half_exp", ("char",), "char")
        self.functions["half_exp"] = c99fn("half_exp", ("char2",), "char2")
        self.functions["half_exp"] = c99fn("half_exp", ("char4",), "char4")
        self.functions["half_exp"] = c99fn("half_exp", ("char8",), "char8")
        self.functions["half_exp"] = c99fn("half_exp", ("char16",), "char16")
        self.functions["half_exp"] = c99fn("half_exp", ("uchar",), "uchar")
        self.functions["half_exp"] = c99fn("half_exp", ("uchar2",), "uchar2")
        self.functions["half_exp"] = c99fn("half_exp", ("uchar4",), "uchar4")
        self.functions["half_exp"] = c99fn("half_exp", ("uchar8",), "uchar8")
        self.functions["half_exp"] = c99fn("half_exp", ("uchar16",), "uchar16")
        self.functions["half_exp"] = c99fn("half_exp", ("short",), "short")
        self.functions["half_exp"] = c99fn("half_exp", ("short2",), "short2")
        self.functions["half_exp"] = c99fn("half_exp", ("short4",), "short4")
        self.functions["half_exp"] = c99fn("half_exp", ("short8",), "short8")
        self.functions["half_exp"] = c99fn("half_exp", ("short16",), "short16")
        self.functions["half_exp"] = c99fn("half_exp", ("ushort",), "ushort")
        self.functions["half_exp"] = c99fn("half_exp", ("ushort2",), "ushort2")
        self.functions["half_exp"] = c99fn("half_exp", ("ushort4",), "ushort4")
        self.functions["half_exp"] = c99fn("half_exp", ("ushort8",), "ushort8")
        self.functions["half_exp"] = c99fn("half_exp", ("ushort16",), "ushort16")
        self.functions["half_exp"] = c99fn("half_exp", ("int",), "int")
        self.functions["half_exp"] = c99fn("half_exp", ("int2",), "int2")
        self.functions["half_exp"] = c99fn("half_exp", ("int4",), "int4")
        self.functions["half_exp"] = c99fn("half_exp", ("int8",), "int8")
        self.functions["half_exp"] = c99fn("half_exp", ("int16",), "int16")
        self.functions["half_exp"] = c99fn("half_exp", ("uint",), "uint")
        self.functions["half_exp"] = c99fn("half_exp", ("uint2",), "uint2")
        self.functions["half_exp"] = c99fn("half_exp", ("uint4",), "uint4")
        self.functions["half_exp"] = c99fn("half_exp", ("uint8",), "uint8")
        self.functions["half_exp"] = c99fn("half_exp", ("uint16",), "uint16")
        self.functions["half_exp"] = c99fn("half_exp", ("long",), "long")
        self.functions["half_exp"] = c99fn("half_exp", ("long2",), "long2")
        self.functions["half_exp"] = c99fn("half_exp", ("long4",), "long4")
        self.functions["half_exp"] = c99fn("half_exp", ("long8",), "long8")
        self.functions["half_exp"] = c99fn("half_exp", ("long16",), "long16")
        self.functions["half_exp"] = c99fn("half_exp", ("ulong",), "ulong")
        self.functions["half_exp"] = c99fn("half_exp", ("ulong2",), "ulong2")
        self.functions["half_exp"] = c99fn("half_exp", ("ulong4",), "ulong4")
        self.functions["half_exp"] = c99fn("half_exp", ("ulong8",), "ulong8")
        self.functions["half_exp"] = c99fn("half_exp", ("ulong16",), "ulong16")
        self.functions["half_exp10"] = c99fn("half_exp10", ("char",), "char")
        self.functions["half_exp10"] = c99fn("half_exp10", ("char2",), "char2")
        self.functions["half_exp10"] = c99fn("half_exp10", ("char4",), "char4")
        self.functions["half_exp10"] = c99fn("half_exp10", ("char8",), "char8")
        self.functions["half_exp10"] = c99fn("half_exp10", ("char16",), "char16")
        self.functions["half_exp10"] = c99fn("half_exp10", ("uchar",), "uchar")
        self.functions["half_exp10"] = c99fn("half_exp10", ("uchar2",), "uchar2")
        self.functions["half_exp10"] = c99fn("half_exp10", ("uchar4",), "uchar4")
        self.functions["half_exp10"] = c99fn("half_exp10", ("uchar8",), "uchar8")
        self.functions["half_exp10"] = c99fn("half_exp10", ("uchar16",), "uchar16")
        self.functions["half_exp10"] = c99fn("half_exp10", ("short",), "short")
        self.functions["half_exp10"] = c99fn("half_exp10", ("short2",), "short2")
        self.functions["half_exp10"] = c99fn("half_exp10", ("short4",), "short4")
        self.functions["half_exp10"] = c99fn("half_exp10", ("short8",), "short8")
        self.functions["half_exp10"] = c99fn("half_exp10", ("short16",), "short16")
        self.functions["half_exp10"] = c99fn("half_exp10", ("ushort",), "ushort")
        self.functions["half_exp10"] = c99fn("half_exp10", ("ushort2",), "ushort2")
        self.functions["half_exp10"] = c99fn("half_exp10", ("ushort4",), "ushort4")
        self.functions["half_exp10"] = c99fn("half_exp10", ("ushort8",), "ushort8")
        self.functions["half_exp10"] = c99fn("half_exp10", ("ushort16",), "ushort16")
        self.functions["half_exp10"] = c99fn("half_exp10", ("int",), "int")
        self.functions["half_exp10"] = c99fn("half_exp10", ("int2",), "int2")
        self.functions["half_exp10"] = c99fn("half_exp10", ("int4",), "int4")
        self.functions["half_exp10"] = c99fn("half_exp10", ("int8",), "int8")
        self.functions["half_exp10"] = c99fn("half_exp10", ("int16",), "int16")
        self.functions["half_exp10"] = c99fn("half_exp10", ("uint",), "uint")
        self.functions["half_exp10"] = c99fn("half_exp10", ("uint2",), "uint2")
        self.functions["half_exp10"] = c99fn("half_exp10", ("uint4",), "uint4")
        self.functions["half_exp10"] = c99fn("half_exp10", ("uint8",), "uint8")
        self.functions["half_exp10"] = c99fn("half_exp10", ("uint16",), "uint16")
        self.functions["half_exp10"] = c99fn("half_exp10", ("long",), "long")
        self.functions["half_exp10"] = c99fn("half_exp10", ("long2",), "long2")
        self.functions["half_exp10"] = c99fn("half_exp10", ("long4",), "long4")
        self.functions["half_exp10"] = c99fn("half_exp10", ("long8",), "long8")
        self.functions["half_exp10"] = c99fn("half_exp10", ("long16",), "long16")
        self.functions["half_exp10"] = c99fn("half_exp10", ("ulong",), "ulong")
        self.functions["half_exp10"] = c99fn("half_exp10", ("ulong2",), "ulong2")
        self.functions["half_exp10"] = c99fn("half_exp10", ("ulong4",), "ulong4")
        self.functions["half_exp10"] = c99fn("half_exp10", ("ulong8",), "ulong8")
        self.functions["half_exp10"] = c99fn("half_exp10", ("ulong16",), "ulong16")
        self.functions["half_log"] = c99fn("half_log", ("char",), "char")
        self.functions["half_log"] = c99fn("half_log", ("char2",), "char2")
        self.functions["half_log"] = c99fn("half_log", ("char4",), "char4")
        self.functions["half_log"] = c99fn("half_log", ("char8",), "char8")
        self.functions["half_log"] = c99fn("half_log", ("char16",), "char16")
        self.functions["half_log"] = c99fn("half_log", ("uchar",), "uchar")
        self.functions["half_log"] = c99fn("half_log", ("uchar2",), "uchar2")
        self.functions["half_log"] = c99fn("half_log", ("uchar4",), "uchar4")
        self.functions["half_log"] = c99fn("half_log", ("uchar8",), "uchar8")
        self.functions["half_log"] = c99fn("half_log", ("uchar16",), "uchar16")
        self.functions["half_log"] = c99fn("half_log", ("short",), "short")
        self.functions["half_log"] = c99fn("half_log", ("short2",), "short2")
        self.functions["half_log"] = c99fn("half_log", ("short4",), "short4")
        self.functions["half_log"] = c99fn("half_log", ("short8",), "short8")
        self.functions["half_log"] = c99fn("half_log", ("short16",), "short16")
        self.functions["half_log"] = c99fn("half_log", ("ushort",), "ushort")
        self.functions["half_log"] = c99fn("half_log", ("ushort2",), "ushort2")
        self.functions["half_log"] = c99fn("half_log", ("ushort4",), "ushort4")
        self.functions["half_log"] = c99fn("half_log", ("ushort8",), "ushort8")
        self.functions["half_log"] = c99fn("half_log", ("ushort16",), "ushort16")
        self.functions["half_log"] = c99fn("half_log", ("int",), "int")
        self.functions["half_log"] = c99fn("half_log", ("int2",), "int2")
        self.functions["half_log"] = c99fn("half_log", ("int4",), "int4")
        self.functions["half_log"] = c99fn("half_log", ("int8",), "int8")
        self.functions["half_log"] = c99fn("half_log", ("int16",), "int16")
        self.functions["half_log"] = c99fn("half_log", ("uint",), "uint")
        self.functions["half_log"] = c99fn("half_log", ("uint2",), "uint2")
        self.functions["half_log"] = c99fn("half_log", ("uint4",), "uint4")
        self.functions["half_log"] = c99fn("half_log", ("uint8",), "uint8")
        self.functions["half_log"] = c99fn("half_log", ("uint16",), "uint16")
        self.functions["half_log"] = c99fn("half_log", ("long",), "long")
        self.functions["half_log"] = c99fn("half_log", ("long2",), "long2")
        self.functions["half_log"] = c99fn("half_log", ("long4",), "long4")
        self.functions["half_log"] = c99fn("half_log", ("long8",), "long8")
        self.functions["half_log"] = c99fn("half_log", ("long16",), "long16")
        self.functions["half_log"] = c99fn("half_log", ("ulong",), "ulong")
        self.functions["half_log"] = c99fn("half_log", ("ulong2",), "ulong2")
        self.functions["half_log"] = c99fn("half_log", ("ulong4",), "ulong4")
        self.functions["half_log"] = c99fn("half_log", ("ulong8",), "ulong8")
        self.functions["half_log"] = c99fn("half_log", ("ulong16",), "ulong16")
        self.functions["half_log2"] = c99fn("half_log2", ("char",), "char")
        self.functions["half_log2"] = c99fn("half_log2", ("char2",), "char2")
        self.functions["half_log2"] = c99fn("half_log2", ("char4",), "char4")
        self.functions["half_log2"] = c99fn("half_log2", ("char8",), "char8")
        self.functions["half_log2"] = c99fn("half_log2", ("char16",), "char16")
        self.functions["half_log2"] = c99fn("half_log2", ("uchar",), "uchar")
        self.functions["half_log2"] = c99fn("half_log2", ("uchar2",), "uchar2")
        self.functions["half_log2"] = c99fn("half_log2", ("uchar4",), "uchar4")
        self.functions["half_log2"] = c99fn("half_log2", ("uchar8",), "uchar8")
        self.functions["half_log2"] = c99fn("half_log2", ("uchar16",), "uchar16")
        self.functions["half_log2"] = c99fn("half_log2", ("short",), "short")
        self.functions["half_log2"] = c99fn("half_log2", ("short2",), "short2")
        self.functions["half_log2"] = c99fn("half_log2", ("short4",), "short4")
        self.functions["half_log2"] = c99fn("half_log2", ("short8",), "short8")
        self.functions["half_log2"] = c99fn("half_log2", ("short16",), "short16")
        self.functions["half_log2"] = c99fn("half_log2", ("ushort",), "ushort")
        self.functions["half_log2"] = c99fn("half_log2", ("ushort2",), "ushort2")
        self.functions["half_log2"] = c99fn("half_log2", ("ushort4",), "ushort4")
        self.functions["half_log2"] = c99fn("half_log2", ("ushort8",), "ushort8")
        self.functions["half_log2"] = c99fn("half_log2", ("ushort16",), "ushort16")
        self.functions["half_log2"] = c99fn("half_log2", ("int",), "int")
        self.functions["half_log2"] = c99fn("half_log2", ("int2",), "int2")
        self.functions["half_log2"] = c99fn("half_log2", ("int4",), "int4")
        self.functions["half_log2"] = c99fn("half_log2", ("int8",), "int8")
        self.functions["half_log2"] = c99fn("half_log2", ("int16",), "int16")
        self.functions["half_log2"] = c99fn("half_log2", ("uint",), "uint")
        self.functions["half_log2"] = c99fn("half_log2", ("uint2",), "uint2")
        self.functions["half_log2"] = c99fn("half_log2", ("uint4",), "uint4")
        self.functions["half_log2"] = c99fn("half_log2", ("uint8",), "uint8")
        self.functions["half_log2"] = c99fn("half_log2", ("uint16",), "uint16")
        self.functions["half_log2"] = c99fn("half_log2", ("long",), "long")
        self.functions["half_log2"] = c99fn("half_log2", ("long2",), "long2")
        self.functions["half_log2"] = c99fn("half_log2", ("long4",), "long4")
        self.functions["half_log2"] = c99fn("half_log2", ("long8",), "long8")
        self.functions["half_log2"] = c99fn("half_log2", ("long16",), "long16")
        self.functions["half_log2"] = c99fn("half_log2", ("ulong",), "ulong")
        self.functions["half_log2"] = c99fn("half_log2", ("ulong2",), "ulong2")
        self.functions["half_log2"] = c99fn("half_log2", ("ulong4",), "ulong4")
        self.functions["half_log2"] = c99fn("half_log2", ("ulong8",), "ulong8")
        self.functions["half_log2"] = c99fn("half_log2", ("ulong16",), "ulong16")
        self.functions["half_log10"] = c99fn("half_log10", ("char",), "char")
        self.functions["half_log10"] = c99fn("half_log10", ("char2",), "char2")
        self.functions["half_log10"] = c99fn("half_log10", ("char4",), "char4")
        self.functions["half_log10"] = c99fn("half_log10", ("char8",), "char8")
        self.functions["half_log10"] = c99fn("half_log10", ("char16",), "char16")
        self.functions["half_log10"] = c99fn("half_log10", ("uchar",), "uchar")
        self.functions["half_log10"] = c99fn("half_log10", ("uchar2",), "uchar2")
        self.functions["half_log10"] = c99fn("half_log10", ("uchar4",), "uchar4")
        self.functions["half_log10"] = c99fn("half_log10", ("uchar8",), "uchar8")
        self.functions["half_log10"] = c99fn("half_log10", ("uchar16",), "uchar16")
        self.functions["half_log10"] = c99fn("half_log10", ("short",), "short")
        self.functions["half_log10"] = c99fn("half_log10", ("short2",), "short2")
        self.functions["half_log10"] = c99fn("half_log10", ("short4",), "short4")
        self.functions["half_log10"] = c99fn("half_log10", ("short8",), "short8")
        self.functions["half_log10"] = c99fn("half_log10", ("short16",), "short16")
        self.functions["half_log10"] = c99fn("half_log10", ("ushort",), "ushort")
        self.functions["half_log10"] = c99fn("half_log10", ("ushort2",), "ushort2")
        self.functions["half_log10"] = c99fn("half_log10", ("ushort4",), "ushort4")
        self.functions["half_log10"] = c99fn("half_log10", ("ushort8",), "ushort8")
        self.functions["half_log10"] = c99fn("half_log10", ("ushort16",), "ushort16")
        self.functions["half_log10"] = c99fn("half_log10", ("int",), "int")
        self.functions["half_log10"] = c99fn("half_log10", ("int2",), "int2")
        self.functions["half_log10"] = c99fn("half_log10", ("int4",), "int4")
        self.functions["half_log10"] = c99fn("half_log10", ("int8",), "int8")
        self.functions["half_log10"] = c99fn("half_log10", ("int16",), "int16")
        self.functions["half_log10"] = c99fn("half_log10", ("uint",), "uint")
        self.functions["half_log10"] = c99fn("half_log10", ("uint2",), "uint2")
        self.functions["half_log10"] = c99fn("half_log10", ("uint4",), "uint4")
        self.functions["half_log10"] = c99fn("half_log10", ("uint8",), "uint8")
        self.functions["half_log10"] = c99fn("half_log10", ("uint16",), "uint16")
        self.functions["half_log10"] = c99fn("half_log10", ("long",), "long")
        self.functions["half_log10"] = c99fn("half_log10", ("long2",), "long2")
        self.functions["half_log10"] = c99fn("half_log10", ("long4",), "long4")
        self.functions["half_log10"] = c99fn("half_log10", ("long8",), "long8")
        self.functions["half_log10"] = c99fn("half_log10", ("long16",), "long16")
        self.functions["half_log10"] = c99fn("half_log10", ("ulong",), "ulong")
        self.functions["half_log10"] = c99fn("half_log10", ("ulong2",), "ulong2")
        self.functions["half_log10"] = c99fn("half_log10", ("ulong4",), "ulong4")
        self.functions["half_log10"] = c99fn("half_log10", ("ulong8",), "ulong8")
        self.functions["half_log10"] = c99fn("half_log10", ("ulong16",), "ulong16")
        self.functions["half_powr"] = c99fn("half_powr", ("char","char",), "char")
        self.functions["half_powr"] = c99fn("half_powr", ("char2","char2",), "char2")
        self.functions["half_powr"] = c99fn("half_powr", ("char4","char4",), "char4")
        self.functions["half_powr"] = c99fn("half_powr", ("char8","char8",), "char8")
        self.functions["half_powr"] = c99fn("half_powr", ("char16","char16",), "char16")
        self.functions["half_powr"] = c99fn("half_powr", ("uchar","uchar",), "uchar")
        self.functions["half_powr"] = c99fn("half_powr", ("uchar2","uchar2",), "uchar2")
        self.functions["half_powr"] = c99fn("half_powr", ("uchar4","uchar4",), "uchar4")
        self.functions["half_powr"] = c99fn("half_powr", ("uchar8","uchar8",), "uchar8")
        self.functions["half_powr"] = c99fn("half_powr", ("uchar16","uchar16",), "uchar16")
        self.functions["half_powr"] = c99fn("half_powr", ("short","short",), "short")
        self.functions["half_powr"] = c99fn("half_powr", ("short2","short2",), "short2")
        self.functions["half_powr"] = c99fn("half_powr", ("short4","short4",), "short4")
        self.functions["half_powr"] = c99fn("half_powr", ("short8","short8",), "short8")
        self.functions["half_powr"] = c99fn("half_powr", ("short16","short16",), "short16")
        self.functions["half_powr"] = c99fn("half_powr", ("ushort","ushort",), "ushort")
        self.functions["half_powr"] = c99fn("half_powr", ("ushort2","ushort2",), "ushort2")
        self.functions["half_powr"] = c99fn("half_powr", ("ushort4","ushort4",), "ushort4")
        self.functions["half_powr"] = c99fn("half_powr", ("ushort8","ushort8",), "ushort8")
        self.functions["half_powr"] = c99fn("half_powr", ("ushort16","ushort16",), "ushort16")
        self.functions["half_powr"] = c99fn("half_powr", ("int","int",), "int")
        self.functions["half_powr"] = c99fn("half_powr", ("int2","int2",), "int2")
        self.functions["half_powr"] = c99fn("half_powr", ("int4","int4",), "int4")
        self.functions["half_powr"] = c99fn("half_powr", ("int8","int8",), "int8")
        self.functions["half_powr"] = c99fn("half_powr", ("int16","int16",), "int16")
        self.functions["half_powr"] = c99fn("half_powr", ("uint","uint",), "uint")
        self.functions["half_powr"] = c99fn("half_powr", ("uint2","uint2",), "uint2")
        self.functions["half_powr"] = c99fn("half_powr", ("uint4","uint4",), "uint4")
        self.functions["half_powr"] = c99fn("half_powr", ("uint8","uint8",), "uint8")
        self.functions["half_powr"] = c99fn("half_powr", ("uint16","uint16",), "uint16")
        self.functions["half_powr"] = c99fn("half_powr", ("long","long",), "long")
        self.functions["half_powr"] = c99fn("half_powr", ("long2","long2",), "long2")
        self.functions["half_powr"] = c99fn("half_powr", ("long4","long4",), "long4")
        self.functions["half_powr"] = c99fn("half_powr", ("long8","long8",), "long8")
        self.functions["half_powr"] = c99fn("half_powr", ("long16","long16",), "long16")
        self.functions["half_powr"] = c99fn("half_powr", ("ulong","ulong",), "ulong")
        self.functions["half_powr"] = c99fn("half_powr", ("ulong2","ulong2",), "ulong2")
        self.functions["half_powr"] = c99fn("half_powr", ("ulong4","ulong4",), "ulong4")
        self.functions["half_powr"] = c99fn("half_powr", ("ulong8","ulong8",), "ulong8")
        self.functions["half_powr"] = c99fn("half_powr", ("ulong16","ulong16",), "ulong16")
        self.functions["half_recip"] = c99fn("half_recip", ("char",), "char")
        self.functions["half_recip"] = c99fn("half_recip", ("char2",), "char2")
        self.functions["half_recip"] = c99fn("half_recip", ("char4",), "char4")
        self.functions["half_recip"] = c99fn("half_recip", ("char8",), "char8")
        self.functions["half_recip"] = c99fn("half_recip", ("char16",), "char16")
        self.functions["half_recip"] = c99fn("half_recip", ("uchar",), "uchar")
        self.functions["half_recip"] = c99fn("half_recip", ("uchar2",), "uchar2")
        self.functions["half_recip"] = c99fn("half_recip", ("uchar4",), "uchar4")
        self.functions["half_recip"] = c99fn("half_recip", ("uchar8",), "uchar8")
        self.functions["half_recip"] = c99fn("half_recip", ("uchar16",), "uchar16")
        self.functions["half_recip"] = c99fn("half_recip", ("short",), "short")
        self.functions["half_recip"] = c99fn("half_recip", ("short2",), "short2")
        self.functions["half_recip"] = c99fn("half_recip", ("short4",), "short4")
        self.functions["half_recip"] = c99fn("half_recip", ("short8",), "short8")
        self.functions["half_recip"] = c99fn("half_recip", ("short16",), "short16")
        self.functions["half_recip"] = c99fn("half_recip", ("ushort",), "ushort")
        self.functions["half_recip"] = c99fn("half_recip", ("ushort2",), "ushort2")
        self.functions["half_recip"] = c99fn("half_recip", ("ushort4",), "ushort4")
        self.functions["half_recip"] = c99fn("half_recip", ("ushort8",), "ushort8")
        self.functions["half_recip"] = c99fn("half_recip", ("ushort16",), "ushort16")
        self.functions["half_recip"] = c99fn("half_recip", ("int",), "int")
        self.functions["half_recip"] = c99fn("half_recip", ("int2",), "int2")
        self.functions["half_recip"] = c99fn("half_recip", ("int4",), "int4")
        self.functions["half_recip"] = c99fn("half_recip", ("int8",), "int8")
        self.functions["half_recip"] = c99fn("half_recip", ("int16",), "int16")
        self.functions["half_recip"] = c99fn("half_recip", ("uint",), "uint")
        self.functions["half_recip"] = c99fn("half_recip", ("uint2",), "uint2")
        self.functions["half_recip"] = c99fn("half_recip", ("uint4",), "uint4")
        self.functions["half_recip"] = c99fn("half_recip", ("uint8",), "uint8")
        self.functions["half_recip"] = c99fn("half_recip", ("uint16",), "uint16")
        self.functions["half_recip"] = c99fn("half_recip", ("long",), "long")
        self.functions["half_recip"] = c99fn("half_recip", ("long2",), "long2")
        self.functions["half_recip"] = c99fn("half_recip", ("long4",), "long4")
        self.functions["half_recip"] = c99fn("half_recip", ("long8",), "long8")
        self.functions["half_recip"] = c99fn("half_recip", ("long16",), "long16")
        self.functions["half_recip"] = c99fn("half_recip", ("ulong",), "ulong")
        self.functions["half_recip"] = c99fn("half_recip", ("ulong2",), "ulong2")
        self.functions["half_recip"] = c99fn("half_recip", ("ulong4",), "ulong4")
        self.functions["half_recip"] = c99fn("half_recip", ("ulong8",), "ulong8")
        self.functions["half_recip"] = c99fn("half_recip", ("ulong16",), "ulong16")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("char",), "char")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("char2",), "char2")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("char4",), "char4")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("char8",), "char8")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("char16",), "char16")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("uchar",), "uchar")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("uchar2",), "uchar2")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("uchar4",), "uchar4")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("uchar8",), "uchar8")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("uchar16",), "uchar16")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("short",), "short")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("short2",), "short2")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("short4",), "short4")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("short8",), "short8")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("short16",), "short16")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("ushort",), "ushort")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("ushort2",), "ushort2")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("ushort4",), "ushort4")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("ushort8",), "ushort8")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("ushort16",), "ushort16")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("int",), "int")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("int2",), "int2")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("int4",), "int4")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("int8",), "int8")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("int16",), "int16")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("uint",), "uint")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("uint2",), "uint2")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("uint4",), "uint4")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("uint8",), "uint8")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("uint16",), "uint16")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("long",), "long")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("long2",), "long2")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("long4",), "long4")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("long8",), "long8")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("long16",), "long16")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("ulong",), "ulong")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("ulong2",), "ulong2")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("ulong4",), "ulong4")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("ulong8",), "ulong8")
        self.functions["half_rsqrt"] = c99fn("half_rsqrt", ("ulong16",), "ulong16")
        self.functions["half_sin"] = c99fn("half_sin", ("char",), "char")
        self.functions["half_sin"] = c99fn("half_sin", ("char2",), "char2")
        self.functions["half_sin"] = c99fn("half_sin", ("char4",), "char4")
        self.functions["half_sin"] = c99fn("half_sin", ("char8",), "char8")
        self.functions["half_sin"] = c99fn("half_sin", ("char16",), "char16")
        self.functions["half_sin"] = c99fn("half_sin", ("uchar",), "uchar")
        self.functions["half_sin"] = c99fn("half_sin", ("uchar2",), "uchar2")
        self.functions["half_sin"] = c99fn("half_sin", ("uchar4",), "uchar4")
        self.functions["half_sin"] = c99fn("half_sin", ("uchar8",), "uchar8")
        self.functions["half_sin"] = c99fn("half_sin", ("uchar16",), "uchar16")
        self.functions["half_sin"] = c99fn("half_sin", ("short",), "short")
        self.functions["half_sin"] = c99fn("half_sin", ("short2",), "short2")
        self.functions["half_sin"] = c99fn("half_sin", ("short4",), "short4")
        self.functions["half_sin"] = c99fn("half_sin", ("short8",), "short8")
        self.functions["half_sin"] = c99fn("half_sin", ("short16",), "short16")
        self.functions["half_sin"] = c99fn("half_sin", ("ushort",), "ushort")
        self.functions["half_sin"] = c99fn("half_sin", ("ushort2",), "ushort2")
        self.functions["half_sin"] = c99fn("half_sin", ("ushort4",), "ushort4")
        self.functions["half_sin"] = c99fn("half_sin", ("ushort8",), "ushort8")
        self.functions["half_sin"] = c99fn("half_sin", ("ushort16",), "ushort16")
        self.functions["half_sin"] = c99fn("half_sin", ("int",), "int")
        self.functions["half_sin"] = c99fn("half_sin", ("int2",), "int2")
        self.functions["half_sin"] = c99fn("half_sin", ("int4",), "int4")
        self.functions["half_sin"] = c99fn("half_sin", ("int8",), "int8")
        self.functions["half_sin"] = c99fn("half_sin", ("int16",), "int16")
        self.functions["half_sin"] = c99fn("half_sin", ("uint",), "uint")
        self.functions["half_sin"] = c99fn("half_sin", ("uint2",), "uint2")
        self.functions["half_sin"] = c99fn("half_sin", ("uint4",), "uint4")
        self.functions["half_sin"] = c99fn("half_sin", ("uint8",), "uint8")
        self.functions["half_sin"] = c99fn("half_sin", ("uint16",), "uint16")
        self.functions["half_sin"] = c99fn("half_sin", ("long",), "long")
        self.functions["half_sin"] = c99fn("half_sin", ("long2",), "long2")
        self.functions["half_sin"] = c99fn("half_sin", ("long4",), "long4")
        self.functions["half_sin"] = c99fn("half_sin", ("long8",), "long8")
        self.functions["half_sin"] = c99fn("half_sin", ("long16",), "long16")
        self.functions["half_sin"] = c99fn("half_sin", ("ulong",), "ulong")
        self.functions["half_sin"] = c99fn("half_sin", ("ulong2",), "ulong2")
        self.functions["half_sin"] = c99fn("half_sin", ("ulong4",), "ulong4")
        self.functions["half_sin"] = c99fn("half_sin", ("ulong8",), "ulong8")
        self.functions["half_sin"] = c99fn("half_sin", ("ulong16",), "ulong16")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("char",), "char")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("char2",), "char2")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("char4",), "char4")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("char8",), "char8")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("char16",), "char16")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("uchar",), "uchar")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("uchar2",), "uchar2")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("uchar4",), "uchar4")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("uchar8",), "uchar8")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("uchar16",), "uchar16")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("short",), "short")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("short2",), "short2")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("short4",), "short4")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("short8",), "short8")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("short16",), "short16")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("ushort",), "ushort")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("ushort2",), "ushort2")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("ushort4",), "ushort4")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("ushort8",), "ushort8")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("ushort16",), "ushort16")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("int",), "int")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("int2",), "int2")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("int4",), "int4")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("int8",), "int8")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("int16",), "int16")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("uint",), "uint")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("uint2",), "uint2")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("uint4",), "uint4")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("uint8",), "uint8")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("uint16",), "uint16")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("long",), "long")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("long2",), "long2")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("long4",), "long4")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("long8",), "long8")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("long16",), "long16")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("ulong",), "ulong")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("ulong2",), "ulong2")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("ulong4",), "ulong4")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("ulong8",), "ulong8")
        self.functions["half_sqrt"] = c99fn("half_sqrt", ("ulong16",), "ulong16")
        self.functions["half_tan"] = c99fn("half_tan", ("char",), "char")
        self.functions["half_tan"] = c99fn("half_tan", ("char2",), "char2")
        self.functions["half_tan"] = c99fn("half_tan", ("char4",), "char4")
        self.functions["half_tan"] = c99fn("half_tan", ("char8",), "char8")
        self.functions["half_tan"] = c99fn("half_tan", ("char16",), "char16")
        self.functions["half_tan"] = c99fn("half_tan", ("uchar",), "uchar")
        self.functions["half_tan"] = c99fn("half_tan", ("uchar2",), "uchar2")
        self.functions["half_tan"] = c99fn("half_tan", ("uchar4",), "uchar4")
        self.functions["half_tan"] = c99fn("half_tan", ("uchar8",), "uchar8")
        self.functions["half_tan"] = c99fn("half_tan", ("uchar16",), "uchar16")
        self.functions["half_tan"] = c99fn("half_tan", ("short",), "short")
        self.functions["half_tan"] = c99fn("half_tan", ("short2",), "short2")
        self.functions["half_tan"] = c99fn("half_tan", ("short4",), "short4")
        self.functions["half_tan"] = c99fn("half_tan", ("short8",), "short8")
        self.functions["half_tan"] = c99fn("half_tan", ("short16",), "short16")
        self.functions["half_tan"] = c99fn("half_tan", ("ushort",), "ushort")
        self.functions["half_tan"] = c99fn("half_tan", ("ushort2",), "ushort2")
        self.functions["half_tan"] = c99fn("half_tan", ("ushort4",), "ushort4")
        self.functions["half_tan"] = c99fn("half_tan", ("ushort8",), "ushort8")
        self.functions["half_tan"] = c99fn("half_tan", ("ushort16",), "ushort16")
        self.functions["half_tan"] = c99fn("half_tan", ("int",), "int")
        self.functions["half_tan"] = c99fn("half_tan", ("int2",), "int2")
        self.functions["half_tan"] = c99fn("half_tan", ("int4",), "int4")
        self.functions["half_tan"] = c99fn("half_tan", ("int8",), "int8")
        self.functions["half_tan"] = c99fn("half_tan", ("int16",), "int16")
        self.functions["half_tan"] = c99fn("half_tan", ("uint",), "uint")
        self.functions["half_tan"] = c99fn("half_tan", ("uint2",), "uint2")
        self.functions["half_tan"] = c99fn("half_tan", ("uint4",), "uint4")
        self.functions["half_tan"] = c99fn("half_tan", ("uint8",), "uint8")
        self.functions["half_tan"] = c99fn("half_tan", ("uint16",), "uint16")
        self.functions["half_tan"] = c99fn("half_tan", ("long",), "long")
        self.functions["half_tan"] = c99fn("half_tan", ("long2",), "long2")
        self.functions["half_tan"] = c99fn("half_tan", ("long4",), "long4")
        self.functions["half_tan"] = c99fn("half_tan", ("long8",), "long8")
        self.functions["half_tan"] = c99fn("half_tan", ("long16",), "long16")
        self.functions["half_tan"] = c99fn("half_tan", ("ulong",), "ulong")
        self.functions["half_tan"] = c99fn("half_tan", ("ulong2",), "ulong2")
        self.functions["half_tan"] = c99fn("half_tan", ("ulong4",), "ulong4")
        self.functions["half_tan"] = c99fn("half_tan", ("ulong8",), "ulong8")
        self.functions["half_tan"] = c99fn("half_tan", ("ulong16",), "ulong16")
        self.functions["native_cos"] = c99fn("native_cos", ("char",), "char")
        self.functions["native_cos"] = c99fn("native_cos", ("char2",), "char2")
        self.functions["native_cos"] = c99fn("native_cos", ("char4",), "char4")
        self.functions["native_cos"] = c99fn("native_cos", ("char8",), "char8")
        self.functions["native_cos"] = c99fn("native_cos", ("char16",), "char16")
        self.functions["native_cos"] = c99fn("native_cos", ("uchar",), "uchar")
        self.functions["native_cos"] = c99fn("native_cos", ("uchar2",), "uchar2")
        self.functions["native_cos"] = c99fn("native_cos", ("uchar4",), "uchar4")
        self.functions["native_cos"] = c99fn("native_cos", ("uchar8",), "uchar8")
        self.functions["native_cos"] = c99fn("native_cos", ("uchar16",), "uchar16")
        self.functions["native_cos"] = c99fn("native_cos", ("short",), "short")
        self.functions["native_cos"] = c99fn("native_cos", ("short2",), "short2")
        self.functions["native_cos"] = c99fn("native_cos", ("short4",), "short4")
        self.functions["native_cos"] = c99fn("native_cos", ("short8",), "short8")
        self.functions["native_cos"] = c99fn("native_cos", ("short16",), "short16")
        self.functions["native_cos"] = c99fn("native_cos", ("ushort",), "ushort")
        self.functions["native_cos"] = c99fn("native_cos", ("ushort2",), "ushort2")
        self.functions["native_cos"] = c99fn("native_cos", ("ushort4",), "ushort4")
        self.functions["native_cos"] = c99fn("native_cos", ("ushort8",), "ushort8")
        self.functions["native_cos"] = c99fn("native_cos", ("ushort16",), "ushort16")
        self.functions["native_cos"] = c99fn("native_cos", ("int",), "int")
        self.functions["native_cos"] = c99fn("native_cos", ("int2",), "int2")
        self.functions["native_cos"] = c99fn("native_cos", ("int4",), "int4")
        self.functions["native_cos"] = c99fn("native_cos", ("int8",), "int8")
        self.functions["native_cos"] = c99fn("native_cos", ("int16",), "int16")
        self.functions["native_cos"] = c99fn("native_cos", ("uint",), "uint")
        self.functions["native_cos"] = c99fn("native_cos", ("uint2",), "uint2")
        self.functions["native_cos"] = c99fn("native_cos", ("uint4",), "uint4")
        self.functions["native_cos"] = c99fn("native_cos", ("uint8",), "uint8")
        self.functions["native_cos"] = c99fn("native_cos", ("uint16",), "uint16")
        self.functions["native_cos"] = c99fn("native_cos", ("long",), "long")
        self.functions["native_cos"] = c99fn("native_cos", ("long2",), "long2")
        self.functions["native_cos"] = c99fn("native_cos", ("long4",), "long4")
        self.functions["native_cos"] = c99fn("native_cos", ("long8",), "long8")
        self.functions["native_cos"] = c99fn("native_cos", ("long16",), "long16")
        self.functions["native_cos"] = c99fn("native_cos", ("ulong",), "ulong")
        self.functions["native_cos"] = c99fn("native_cos", ("ulong2",), "ulong2")
        self.functions["native_cos"] = c99fn("native_cos", ("ulong4",), "ulong4")
        self.functions["native_cos"] = c99fn("native_cos", ("ulong8",), "ulong8")
        self.functions["native_cos"] = c99fn("native_cos", ("ulong16",), "ulong16")
        self.functions["native_divide"] = c99fn("native_divide", ("char",), "char")
        self.functions["native_divide"] = c99fn("native_divide", ("char2",), "char2")
        self.functions["native_divide"] = c99fn("native_divide", ("char4",), "char4")
        self.functions["native_divide"] = c99fn("native_divide", ("char8",), "char8")
        self.functions["native_divide"] = c99fn("native_divide", ("char16",), "char16")
        self.functions["native_divide"] = c99fn("native_divide", ("uchar",), "uchar")
        self.functions["native_divide"] = c99fn("native_divide", ("uchar2",), "uchar2")
        self.functions["native_divide"] = c99fn("native_divide", ("uchar4",), "uchar4")
        self.functions["native_divide"] = c99fn("native_divide", ("uchar8",), "uchar8")
        self.functions["native_divide"] = c99fn("native_divide", ("uchar16",), "uchar16")
        self.functions["native_divide"] = c99fn("native_divide", ("short",), "short")
        self.functions["native_divide"] = c99fn("native_divide", ("short2",), "short2")
        self.functions["native_divide"] = c99fn("native_divide", ("short4",), "short4")
        self.functions["native_divide"] = c99fn("native_divide", ("short8",), "short8")
        self.functions["native_divide"] = c99fn("native_divide", ("short16",), "short16")
        self.functions["native_divide"] = c99fn("native_divide", ("ushort",), "ushort")
        self.functions["native_divide"] = c99fn("native_divide", ("ushort2",), "ushort2")
        self.functions["native_divide"] = c99fn("native_divide", ("ushort4",), "ushort4")
        self.functions["native_divide"] = c99fn("native_divide", ("ushort8",), "ushort8")
        self.functions["native_divide"] = c99fn("native_divide", ("ushort16",), "ushort16")
        self.functions["native_divide"] = c99fn("native_divide", ("int",), "int")
        self.functions["native_divide"] = c99fn("native_divide", ("int2",), "int2")
        self.functions["native_divide"] = c99fn("native_divide", ("int4",), "int4")
        self.functions["native_divide"] = c99fn("native_divide", ("int8",), "int8")
        self.functions["native_divide"] = c99fn("native_divide", ("int16",), "int16")
        self.functions["native_divide"] = c99fn("native_divide", ("uint",), "uint")
        self.functions["native_divide"] = c99fn("native_divide", ("uint2",), "uint2")
        self.functions["native_divide"] = c99fn("native_divide", ("uint4",), "uint4")
        self.functions["native_divide"] = c99fn("native_divide", ("uint8",), "uint8")
        self.functions["native_divide"] = c99fn("native_divide", ("uint16",), "uint16")
        self.functions["native_divide"] = c99fn("native_divide", ("long",), "long")
        self.functions["native_divide"] = c99fn("native_divide", ("long2",), "long2")
        self.functions["native_divide"] = c99fn("native_divide", ("long4",), "long4")
        self.functions["native_divide"] = c99fn("native_divide", ("long8",), "long8")
        self.functions["native_divide"] = c99fn("native_divide", ("long16",), "long16")
        self.functions["native_divide"] = c99fn("native_divide", ("ulong",), "ulong")
        self.functions["native_divide"] = c99fn("native_divide", ("ulong2",), "ulong2")
        self.functions["native_divide"] = c99fn("native_divide", ("ulong4",), "ulong4")
        self.functions["native_divide"] = c99fn("native_divide", ("ulong8",), "ulong8")
        self.functions["native_divide"] = c99fn("native_divide", ("ulong16",), "ulong16")
        self.functions["native_exp"] = c99fn("native_exp", ("char",), "char")
        self.functions["native_exp"] = c99fn("native_exp", ("char2",), "char2")
        self.functions["native_exp"] = c99fn("native_exp", ("char4",), "char4")
        self.functions["native_exp"] = c99fn("native_exp", ("char8",), "char8")
        self.functions["native_exp"] = c99fn("native_exp", ("char16",), "char16")
        self.functions["native_exp"] = c99fn("native_exp", ("uchar",), "uchar")
        self.functions["native_exp"] = c99fn("native_exp", ("uchar2",), "uchar2")
        self.functions["native_exp"] = c99fn("native_exp", ("uchar4",), "uchar4")
        self.functions["native_exp"] = c99fn("native_exp", ("uchar8",), "uchar8")
        self.functions["native_exp"] = c99fn("native_exp", ("uchar16",), "uchar16")
        self.functions["native_exp"] = c99fn("native_exp", ("short",), "short")
        self.functions["native_exp"] = c99fn("native_exp", ("short2",), "short2")
        self.functions["native_exp"] = c99fn("native_exp", ("short4",), "short4")
        self.functions["native_exp"] = c99fn("native_exp", ("short8",), "short8")
        self.functions["native_exp"] = c99fn("native_exp", ("short16",), "short16")
        self.functions["native_exp"] = c99fn("native_exp", ("ushort",), "ushort")
        self.functions["native_exp"] = c99fn("native_exp", ("ushort2",), "ushort2")
        self.functions["native_exp"] = c99fn("native_exp", ("ushort4",), "ushort4")
        self.functions["native_exp"] = c99fn("native_exp", ("ushort8",), "ushort8")
        self.functions["native_exp"] = c99fn("native_exp", ("ushort16",), "ushort16")
        self.functions["native_exp"] = c99fn("native_exp", ("int",), "int")
        self.functions["native_exp"] = c99fn("native_exp", ("int2",), "int2")
        self.functions["native_exp"] = c99fn("native_exp", ("int4",), "int4")
        self.functions["native_exp"] = c99fn("native_exp", ("int8",), "int8")
        self.functions["native_exp"] = c99fn("native_exp", ("int16",), "int16")
        self.functions["native_exp"] = c99fn("native_exp", ("uint",), "uint")
        self.functions["native_exp"] = c99fn("native_exp", ("uint2",), "uint2")
        self.functions["native_exp"] = c99fn("native_exp", ("uint4",), "uint4")
        self.functions["native_exp"] = c99fn("native_exp", ("uint8",), "uint8")
        self.functions["native_exp"] = c99fn("native_exp", ("uint16",), "uint16")
        self.functions["native_exp"] = c99fn("native_exp", ("long",), "long")
        self.functions["native_exp"] = c99fn("native_exp", ("long2",), "long2")
        self.functions["native_exp"] = c99fn("native_exp", ("long4",), "long4")
        self.functions["native_exp"] = c99fn("native_exp", ("long8",), "long8")
        self.functions["native_exp"] = c99fn("native_exp", ("long16",), "long16")
        self.functions["native_exp"] = c99fn("native_exp", ("ulong",), "ulong")
        self.functions["native_exp"] = c99fn("native_exp", ("ulong2",), "ulong2")
        self.functions["native_exp"] = c99fn("native_exp", ("ulong4",), "ulong4")
        self.functions["native_exp"] = c99fn("native_exp", ("ulong8",), "ulong8")
        self.functions["native_exp"] = c99fn("native_exp", ("ulong16",), "ulong16")
        self.functions["native_exp10"] = c99fn("native_exp10", ("char",), "char")
        self.functions["native_exp10"] = c99fn("native_exp10", ("char2",), "char2")
        self.functions["native_exp10"] = c99fn("native_exp10", ("char4",), "char4")
        self.functions["native_exp10"] = c99fn("native_exp10", ("char8",), "char8")
        self.functions["native_exp10"] = c99fn("native_exp10", ("char16",), "char16")
        self.functions["native_exp10"] = c99fn("native_exp10", ("uchar",), "uchar")
        self.functions["native_exp10"] = c99fn("native_exp10", ("uchar2",), "uchar2")
        self.functions["native_exp10"] = c99fn("native_exp10", ("uchar4",), "uchar4")
        self.functions["native_exp10"] = c99fn("native_exp10", ("uchar8",), "uchar8")
        self.functions["native_exp10"] = c99fn("native_exp10", ("uchar16",), "uchar16")
        self.functions["native_exp10"] = c99fn("native_exp10", ("short",), "short")
        self.functions["native_exp10"] = c99fn("native_exp10", ("short2",), "short2")
        self.functions["native_exp10"] = c99fn("native_exp10", ("short4",), "short4")
        self.functions["native_exp10"] = c99fn("native_exp10", ("short8",), "short8")
        self.functions["native_exp10"] = c99fn("native_exp10", ("short16",), "short16")
        self.functions["native_exp10"] = c99fn("native_exp10", ("ushort",), "ushort")
        self.functions["native_exp10"] = c99fn("native_exp10", ("ushort2",), "ushort2")
        self.functions["native_exp10"] = c99fn("native_exp10", ("ushort4",), "ushort4")
        self.functions["native_exp10"] = c99fn("native_exp10", ("ushort8",), "ushort8")
        self.functions["native_exp10"] = c99fn("native_exp10", ("ushort16",), "ushort16")
        self.functions["native_exp10"] = c99fn("native_exp10", ("int",), "int")
        self.functions["native_exp10"] = c99fn("native_exp10", ("int2",), "int2")
        self.functions["native_exp10"] = c99fn("native_exp10", ("int4",), "int4")
        self.functions["native_exp10"] = c99fn("native_exp10", ("int8",), "int8")
        self.functions["native_exp10"] = c99fn("native_exp10", ("int16",), "int16")
        self.functions["native_exp10"] = c99fn("native_exp10", ("uint",), "uint")
        self.functions["native_exp10"] = c99fn("native_exp10", ("uint2",), "uint2")
        self.functions["native_exp10"] = c99fn("native_exp10", ("uint4",), "uint4")
        self.functions["native_exp10"] = c99fn("native_exp10", ("uint8",), "uint8")
        self.functions["native_exp10"] = c99fn("native_exp10", ("uint16",), "uint16")
        self.functions["native_exp10"] = c99fn("native_exp10", ("long",), "long")
        self.functions["native_exp10"] = c99fn("native_exp10", ("long2",), "long2")
        self.functions["native_exp10"] = c99fn("native_exp10", ("long4",), "long4")
        self.functions["native_exp10"] = c99fn("native_exp10", ("long8",), "long8")
        self.functions["native_exp10"] = c99fn("native_exp10", ("long16",), "long16")
        self.functions["native_exp10"] = c99fn("native_exp10", ("ulong",), "ulong")
        self.functions["native_exp10"] = c99fn("native_exp10", ("ulong2",), "ulong2")
        self.functions["native_exp10"] = c99fn("native_exp10", ("ulong4",), "ulong4")
        self.functions["native_exp10"] = c99fn("native_exp10", ("ulong8",), "ulong8")
        self.functions["native_exp10"] = c99fn("native_exp10", ("ulong16",), "ulong16")
        self.functions["native_log"] = c99fn("native_log", ("char",), "char")
        self.functions["native_log"] = c99fn("native_log", ("char2",), "char2")
        self.functions["native_log"] = c99fn("native_log", ("char4",), "char4")
        self.functions["native_log"] = c99fn("native_log", ("char8",), "char8")
        self.functions["native_log"] = c99fn("native_log", ("char16",), "char16")
        self.functions["native_log"] = c99fn("native_log", ("uchar",), "uchar")
        self.functions["native_log"] = c99fn("native_log", ("uchar2",), "uchar2")
        self.functions["native_log"] = c99fn("native_log", ("uchar4",), "uchar4")
        self.functions["native_log"] = c99fn("native_log", ("uchar8",), "uchar8")
        self.functions["native_log"] = c99fn("native_log", ("uchar16",), "uchar16")
        self.functions["native_log"] = c99fn("native_log", ("short",), "short")
        self.functions["native_log"] = c99fn("native_log", ("short2",), "short2")
        self.functions["native_log"] = c99fn("native_log", ("short4",), "short4")
        self.functions["native_log"] = c99fn("native_log", ("short8",), "short8")
        self.functions["native_log"] = c99fn("native_log", ("short16",), "short16")
        self.functions["native_log"] = c99fn("native_log", ("ushort",), "ushort")
        self.functions["native_log"] = c99fn("native_log", ("ushort2",), "ushort2")
        self.functions["native_log"] = c99fn("native_log", ("ushort4",), "ushort4")
        self.functions["native_log"] = c99fn("native_log", ("ushort8",), "ushort8")
        self.functions["native_log"] = c99fn("native_log", ("ushort16",), "ushort16")
        self.functions["native_log"] = c99fn("native_log", ("int",), "int")
        self.functions["native_log"] = c99fn("native_log", ("int2",), "int2")
        self.functions["native_log"] = c99fn("native_log", ("int4",), "int4")
        self.functions["native_log"] = c99fn("native_log", ("int8",), "int8")
        self.functions["native_log"] = c99fn("native_log", ("int16",), "int16")
        self.functions["native_log"] = c99fn("native_log", ("uint",), "uint")
        self.functions["native_log"] = c99fn("native_log", ("uint2",), "uint2")
        self.functions["native_log"] = c99fn("native_log", ("uint4",), "uint4")
        self.functions["native_log"] = c99fn("native_log", ("uint8",), "uint8")
        self.functions["native_log"] = c99fn("native_log", ("uint16",), "uint16")
        self.functions["native_log"] = c99fn("native_log", ("long",), "long")
        self.functions["native_log"] = c99fn("native_log", ("long2",), "long2")
        self.functions["native_log"] = c99fn("native_log", ("long4",), "long4")
        self.functions["native_log"] = c99fn("native_log", ("long8",), "long8")
        self.functions["native_log"] = c99fn("native_log", ("long16",), "long16")
        self.functions["native_log"] = c99fn("native_log", ("ulong",), "ulong")
        self.functions["native_log"] = c99fn("native_log", ("ulong2",), "ulong2")
        self.functions["native_log"] = c99fn("native_log", ("ulong4",), "ulong4")
        self.functions["native_log"] = c99fn("native_log", ("ulong8",), "ulong8")
        self.functions["native_log"] = c99fn("native_log", ("ulong16",), "ulong16")
        self.functions["native_log2"] = c99fn("native_log2", ("char",), "char")
        self.functions["native_log2"] = c99fn("native_log2", ("char2",), "char2")
        self.functions["native_log2"] = c99fn("native_log2", ("char4",), "char4")
        self.functions["native_log2"] = c99fn("native_log2", ("char8",), "char8")
        self.functions["native_log2"] = c99fn("native_log2", ("char16",), "char16")
        self.functions["native_log2"] = c99fn("native_log2", ("uchar",), "uchar")
        self.functions["native_log2"] = c99fn("native_log2", ("uchar2",), "uchar2")
        self.functions["native_log2"] = c99fn("native_log2", ("uchar4",), "uchar4")
        self.functions["native_log2"] = c99fn("native_log2", ("uchar8",), "uchar8")
        self.functions["native_log2"] = c99fn("native_log2", ("uchar16",), "uchar16")
        self.functions["native_log2"] = c99fn("native_log2", ("short",), "short")
        self.functions["native_log2"] = c99fn("native_log2", ("short2",), "short2")
        self.functions["native_log2"] = c99fn("native_log2", ("short4",), "short4")
        self.functions["native_log2"] = c99fn("native_log2", ("short8",), "short8")
        self.functions["native_log2"] = c99fn("native_log2", ("short16",), "short16")
        self.functions["native_log2"] = c99fn("native_log2", ("ushort",), "ushort")
        self.functions["native_log2"] = c99fn("native_log2", ("ushort2",), "ushort2")
        self.functions["native_log2"] = c99fn("native_log2", ("ushort4",), "ushort4")
        self.functions["native_log2"] = c99fn("native_log2", ("ushort8",), "ushort8")
        self.functions["native_log2"] = c99fn("native_log2", ("ushort16",), "ushort16")
        self.functions["native_log2"] = c99fn("native_log2", ("int",), "int")
        self.functions["native_log2"] = c99fn("native_log2", ("int2",), "int2")
        self.functions["native_log2"] = c99fn("native_log2", ("int4",), "int4")
        self.functions["native_log2"] = c99fn("native_log2", ("int8",), "int8")
        self.functions["native_log2"] = c99fn("native_log2", ("int16",), "int16")
        self.functions["native_log2"] = c99fn("native_log2", ("uint",), "uint")
        self.functions["native_log2"] = c99fn("native_log2", ("uint2",), "uint2")
        self.functions["native_log2"] = c99fn("native_log2", ("uint4",), "uint4")
        self.functions["native_log2"] = c99fn("native_log2", ("uint8",), "uint8")
        self.functions["native_log2"] = c99fn("native_log2", ("uint16",), "uint16")
        self.functions["native_log2"] = c99fn("native_log2", ("long",), "long")
        self.functions["native_log2"] = c99fn("native_log2", ("long2",), "long2")
        self.functions["native_log2"] = c99fn("native_log2", ("long4",), "long4")
        self.functions["native_log2"] = c99fn("native_log2", ("long8",), "long8")
        self.functions["native_log2"] = c99fn("native_log2", ("long16",), "long16")
        self.functions["native_log2"] = c99fn("native_log2", ("ulong",), "ulong")
        self.functions["native_log2"] = c99fn("native_log2", ("ulong2",), "ulong2")
        self.functions["native_log2"] = c99fn("native_log2", ("ulong4",), "ulong4")
        self.functions["native_log2"] = c99fn("native_log2", ("ulong8",), "ulong8")
        self.functions["native_log2"] = c99fn("native_log2", ("ulong16",), "ulong16")
        self.functions["native_log10"] = c99fn("native_log10", ("char",), "char")
        self.functions["native_log10"] = c99fn("native_log10", ("char2",), "char2")
        self.functions["native_log10"] = c99fn("native_log10", ("char4",), "char4")
        self.functions["native_log10"] = c99fn("native_log10", ("char8",), "char8")
        self.functions["native_log10"] = c99fn("native_log10", ("char16",), "char16")
        self.functions["native_log10"] = c99fn("native_log10", ("uchar",), "uchar")
        self.functions["native_log10"] = c99fn("native_log10", ("uchar2",), "uchar2")
        self.functions["native_log10"] = c99fn("native_log10", ("uchar4",), "uchar4")
        self.functions["native_log10"] = c99fn("native_log10", ("uchar8",), "uchar8")
        self.functions["native_log10"] = c99fn("native_log10", ("uchar16",), "uchar16")
        self.functions["native_log10"] = c99fn("native_log10", ("short",), "short")
        self.functions["native_log10"] = c99fn("native_log10", ("short2",), "short2")
        self.functions["native_log10"] = c99fn("native_log10", ("short4",), "short4")
        self.functions["native_log10"] = c99fn("native_log10", ("short8",), "short8")
        self.functions["native_log10"] = c99fn("native_log10", ("short16",), "short16")
        self.functions["native_log10"] = c99fn("native_log10", ("ushort",), "ushort")
        self.functions["native_log10"] = c99fn("native_log10", ("ushort2",), "ushort2")
        self.functions["native_log10"] = c99fn("native_log10", ("ushort4",), "ushort4")
        self.functions["native_log10"] = c99fn("native_log10", ("ushort8",), "ushort8")
        self.functions["native_log10"] = c99fn("native_log10", ("ushort16",), "ushort16")
        self.functions["native_log10"] = c99fn("native_log10", ("int",), "int")
        self.functions["native_log10"] = c99fn("native_log10", ("int2",), "int2")
        self.functions["native_log10"] = c99fn("native_log10", ("int4",), "int4")
        self.functions["native_log10"] = c99fn("native_log10", ("int8",), "int8")
        self.functions["native_log10"] = c99fn("native_log10", ("int16",), "int16")
        self.functions["native_log10"] = c99fn("native_log10", ("uint",), "uint")
        self.functions["native_log10"] = c99fn("native_log10", ("uint2",), "uint2")
        self.functions["native_log10"] = c99fn("native_log10", ("uint4",), "uint4")
        self.functions["native_log10"] = c99fn("native_log10", ("uint8",), "uint8")
        self.functions["native_log10"] = c99fn("native_log10", ("uint16",), "uint16")
        self.functions["native_log10"] = c99fn("native_log10", ("long",), "long")
        self.functions["native_log10"] = c99fn("native_log10", ("long2",), "long2")
        self.functions["native_log10"] = c99fn("native_log10", ("long4",), "long4")
        self.functions["native_log10"] = c99fn("native_log10", ("long8",), "long8")
        self.functions["native_log10"] = c99fn("native_log10", ("long16",), "long16")
        self.functions["native_log10"] = c99fn("native_log10", ("ulong",), "ulong")
        self.functions["native_log10"] = c99fn("native_log10", ("ulong2",), "ulong2")
        self.functions["native_log10"] = c99fn("native_log10", ("ulong4",), "ulong4")
        self.functions["native_log10"] = c99fn("native_log10", ("ulong8",), "ulong8")
        self.functions["native_log10"] = c99fn("native_log10", ("ulong16",), "ulong16")
        self.functions["native_powr"] = c99fn("native_powr", ("char","char",), "char")
        self.functions["native_powr"] = c99fn("native_powr", ("char2","char2",), "char2")
        self.functions["native_powr"] = c99fn("native_powr", ("char4","char4",), "char4")
        self.functions["native_powr"] = c99fn("native_powr", ("char8","char8",), "char8")
        self.functions["native_powr"] = c99fn("native_powr", ("char16","char16",), "char16")
        self.functions["native_powr"] = c99fn("native_powr", ("uchar","uchar",), "uchar")
        self.functions["native_powr"] = c99fn("native_powr", ("uchar2","uchar2",), "uchar2")
        self.functions["native_powr"] = c99fn("native_powr", ("uchar4","uchar4",), "uchar4")
        self.functions["native_powr"] = c99fn("native_powr", ("uchar8","uchar8",), "uchar8")
        self.functions["native_powr"] = c99fn("native_powr", ("uchar16","uchar16",), "uchar16")
        self.functions["native_powr"] = c99fn("native_powr", ("short","short",), "short")
        self.functions["native_powr"] = c99fn("native_powr", ("short2","short2",), "short2")
        self.functions["native_powr"] = c99fn("native_powr", ("short4","short4",), "short4")
        self.functions["native_powr"] = c99fn("native_powr", ("short8","short8",), "short8")
        self.functions["native_powr"] = c99fn("native_powr", ("short16","short16",), "short16")
        self.functions["native_powr"] = c99fn("native_powr", ("ushort","ushort",), "ushort")
        self.functions["native_powr"] = c99fn("native_powr", ("ushort2","ushort2",), "ushort2")
        self.functions["native_powr"] = c99fn("native_powr", ("ushort4","ushort4",), "ushort4")
        self.functions["native_powr"] = c99fn("native_powr", ("ushort8","ushort8",), "ushort8")
        self.functions["native_powr"] = c99fn("native_powr", ("ushort16","ushort16",), "ushort16")
        self.functions["native_powr"] = c99fn("native_powr", ("int","int",), "int")
        self.functions["native_powr"] = c99fn("native_powr", ("int2","int2",), "int2")
        self.functions["native_powr"] = c99fn("native_powr", ("int4","int4",), "int4")
        self.functions["native_powr"] = c99fn("native_powr", ("int8","int8",), "int8")
        self.functions["native_powr"] = c99fn("native_powr", ("int16","int16",), "int16")
        self.functions["native_powr"] = c99fn("native_powr", ("uint","uint",), "uint")
        self.functions["native_powr"] = c99fn("native_powr", ("uint2","uint2",), "uint2")
        self.functions["native_powr"] = c99fn("native_powr", ("uint4","uint4",), "uint4")
        self.functions["native_powr"] = c99fn("native_powr", ("uint8","uint8",), "uint8")
        self.functions["native_powr"] = c99fn("native_powr", ("uint16","uint16",), "uint16")
        self.functions["native_powr"] = c99fn("native_powr", ("long","long",), "long")
        self.functions["native_powr"] = c99fn("native_powr", ("long2","long2",), "long2")
        self.functions["native_powr"] = c99fn("native_powr", ("long4","long4",), "long4")
        self.functions["native_powr"] = c99fn("native_powr", ("long8","long8",), "long8")
        self.functions["native_powr"] = c99fn("native_powr", ("long16","long16",), "long16")
        self.functions["native_powr"] = c99fn("native_powr", ("ulong","ulong",), "ulong")
        self.functions["native_powr"] = c99fn("native_powr", ("ulong2","ulong2",), "ulong2")
        self.functions["native_powr"] = c99fn("native_powr", ("ulong4","ulong4",), "ulong4")
        self.functions["native_powr"] = c99fn("native_powr", ("ulong8","ulong8",), "ulong8")
        self.functions["native_powr"] = c99fn("native_powr", ("ulong16","ulong16",), "ulong16")
        self.functions["native_recip"] = c99fn("native_recip", ("char",), "char")
        self.functions["native_recip"] = c99fn("native_recip", ("char2",), "char2")
        self.functions["native_recip"] = c99fn("native_recip", ("char4",), "char4")
        self.functions["native_recip"] = c99fn("native_recip", ("char8",), "char8")
        self.functions["native_recip"] = c99fn("native_recip", ("char16",), "char16")
        self.functions["native_recip"] = c99fn("native_recip", ("uchar",), "uchar")
        self.functions["native_recip"] = c99fn("native_recip", ("uchar2",), "uchar2")
        self.functions["native_recip"] = c99fn("native_recip", ("uchar4",), "uchar4")
        self.functions["native_recip"] = c99fn("native_recip", ("uchar8",), "uchar8")
        self.functions["native_recip"] = c99fn("native_recip", ("uchar16",), "uchar16")
        self.functions["native_recip"] = c99fn("native_recip", ("short",), "short")
        self.functions["native_recip"] = c99fn("native_recip", ("short2",), "short2")
        self.functions["native_recip"] = c99fn("native_recip", ("short4",), "short4")
        self.functions["native_recip"] = c99fn("native_recip", ("short8",), "short8")
        self.functions["native_recip"] = c99fn("native_recip", ("short16",), "short16")
        self.functions["native_recip"] = c99fn("native_recip", ("ushort",), "ushort")
        self.functions["native_recip"] = c99fn("native_recip", ("ushort2",), "ushort2")
        self.functions["native_recip"] = c99fn("native_recip", ("ushort4",), "ushort4")
        self.functions["native_recip"] = c99fn("native_recip", ("ushort8",), "ushort8")
        self.functions["native_recip"] = c99fn("native_recip", ("ushort16",), "ushort16")
        self.functions["native_recip"] = c99fn("native_recip", ("int",), "int")
        self.functions["native_recip"] = c99fn("native_recip", ("int2",), "int2")
        self.functions["native_recip"] = c99fn("native_recip", ("int4",), "int4")
        self.functions["native_recip"] = c99fn("native_recip", ("int8",), "int8")
        self.functions["native_recip"] = c99fn("native_recip", ("int16",), "int16")
        self.functions["native_recip"] = c99fn("native_recip", ("uint",), "uint")
        self.functions["native_recip"] = c99fn("native_recip", ("uint2",), "uint2")
        self.functions["native_recip"] = c99fn("native_recip", ("uint4",), "uint4")
        self.functions["native_recip"] = c99fn("native_recip", ("uint8",), "uint8")
        self.functions["native_recip"] = c99fn("native_recip", ("uint16",), "uint16")
        self.functions["native_recip"] = c99fn("native_recip", ("long",), "long")
        self.functions["native_recip"] = c99fn("native_recip", ("long2",), "long2")
        self.functions["native_recip"] = c99fn("native_recip", ("long4",), "long4")
        self.functions["native_recip"] = c99fn("native_recip", ("long8",), "long8")
        self.functions["native_recip"] = c99fn("native_recip", ("long16",), "long16")
        self.functions["native_recip"] = c99fn("native_recip", ("ulong",), "ulong")
        self.functions["native_recip"] = c99fn("native_recip", ("ulong2",), "ulong2")
        self.functions["native_recip"] = c99fn("native_recip", ("ulong4",), "ulong4")
        self.functions["native_recip"] = c99fn("native_recip", ("ulong8",), "ulong8")
        self.functions["native_recip"] = c99fn("native_recip", ("ulong16",), "ulong16")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("char",), "char")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("char2",), "char2")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("char4",), "char4")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("char8",), "char8")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("char16",), "char16")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("uchar",), "uchar")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("uchar2",), "uchar2")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("uchar4",), "uchar4")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("uchar8",), "uchar8")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("uchar16",), "uchar16")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("short",), "short")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("short2",), "short2")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("short4",), "short4")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("short8",), "short8")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("short16",), "short16")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("ushort",), "ushort")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("ushort2",), "ushort2")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("ushort4",), "ushort4")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("ushort8",), "ushort8")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("ushort16",), "ushort16")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("int",), "int")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("int2",), "int2")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("int4",), "int4")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("int8",), "int8")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("int16",), "int16")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("uint",), "uint")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("uint2",), "uint2")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("uint4",), "uint4")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("uint8",), "uint8")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("uint16",), "uint16")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("long",), "long")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("long2",), "long2")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("long4",), "long4")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("long8",), "long8")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("long16",), "long16")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("ulong",), "ulong")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("ulong2",), "ulong2")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("ulong4",), "ulong4")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("ulong8",), "ulong8")
        self.functions["native_rsqrt"] = c99fn("native_rsqrt", ("ulong16",), "ulong16")
        self.functions["native_sin"] = c99fn("native_sin", ("char",), "char")
        self.functions["native_sin"] = c99fn("native_sin", ("char2",), "char2")
        self.functions["native_sin"] = c99fn("native_sin", ("char4",), "char4")
        self.functions["native_sin"] = c99fn("native_sin", ("char8",), "char8")
        self.functions["native_sin"] = c99fn("native_sin", ("char16",), "char16")
        self.functions["native_sin"] = c99fn("native_sin", ("uchar",), "uchar")
        self.functions["native_sin"] = c99fn("native_sin", ("uchar2",), "uchar2")
        self.functions["native_sin"] = c99fn("native_sin", ("uchar4",), "uchar4")
        self.functions["native_sin"] = c99fn("native_sin", ("uchar8",), "uchar8")
        self.functions["native_sin"] = c99fn("native_sin", ("uchar16",), "uchar16")
        self.functions["native_sin"] = c99fn("native_sin", ("short",), "short")
        self.functions["native_sin"] = c99fn("native_sin", ("short2",), "short2")
        self.functions["native_sin"] = c99fn("native_sin", ("short4",), "short4")
        self.functions["native_sin"] = c99fn("native_sin", ("short8",), "short8")
        self.functions["native_sin"] = c99fn("native_sin", ("short16",), "short16")
        self.functions["native_sin"] = c99fn("native_sin", ("ushort",), "ushort")
        self.functions["native_sin"] = c99fn("native_sin", ("ushort2",), "ushort2")
        self.functions["native_sin"] = c99fn("native_sin", ("ushort4",), "ushort4")
        self.functions["native_sin"] = c99fn("native_sin", ("ushort8",), "ushort8")
        self.functions["native_sin"] = c99fn("native_sin", ("ushort16",), "ushort16")
        self.functions["native_sin"] = c99fn("native_sin", ("int",), "int")
        self.functions["native_sin"] = c99fn("native_sin", ("int2",), "int2")
        self.functions["native_sin"] = c99fn("native_sin", ("int4",), "int4")
        self.functions["native_sin"] = c99fn("native_sin", ("int8",), "int8")
        self.functions["native_sin"] = c99fn("native_sin", ("int16",), "int16")
        self.functions["native_sin"] = c99fn("native_sin", ("uint",), "uint")
        self.functions["native_sin"] = c99fn("native_sin", ("uint2",), "uint2")
        self.functions["native_sin"] = c99fn("native_sin", ("uint4",), "uint4")
        self.functions["native_sin"] = c99fn("native_sin", ("uint8",), "uint8")
        self.functions["native_sin"] = c99fn("native_sin", ("uint16",), "uint16")
        self.functions["native_sin"] = c99fn("native_sin", ("long",), "long")
        self.functions["native_sin"] = c99fn("native_sin", ("long2",), "long2")
        self.functions["native_sin"] = c99fn("native_sin", ("long4",), "long4")
        self.functions["native_sin"] = c99fn("native_sin", ("long8",), "long8")
        self.functions["native_sin"] = c99fn("native_sin", ("long16",), "long16")
        self.functions["native_sin"] = c99fn("native_sin", ("ulong",), "ulong")
        self.functions["native_sin"] = c99fn("native_sin", ("ulong2",), "ulong2")
        self.functions["native_sin"] = c99fn("native_sin", ("ulong4",), "ulong4")
        self.functions["native_sin"] = c99fn("native_sin", ("ulong8",), "ulong8")
        self.functions["native_sin"] = c99fn("native_sin", ("ulong16",), "ulong16")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("char",), "char")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("char2",), "char2")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("char4",), "char4")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("char8",), "char8")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("char16",), "char16")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("uchar",), "uchar")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("uchar2",), "uchar2")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("uchar4",), "uchar4")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("uchar8",), "uchar8")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("uchar16",), "uchar16")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("short",), "short")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("short2",), "short2")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("short4",), "short4")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("short8",), "short8")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("short16",), "short16")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("ushort",), "ushort")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("ushort2",), "ushort2")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("ushort4",), "ushort4")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("ushort8",), "ushort8")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("ushort16",), "ushort16")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("int",), "int")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("int2",), "int2")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("int4",), "int4")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("int8",), "int8")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("int16",), "int16")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("uint",), "uint")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("uint2",), "uint2")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("uint4",), "uint4")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("uint8",), "uint8")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("uint16",), "uint16")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("long",), "long")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("long2",), "long2")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("long4",), "long4")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("long8",), "long8")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("long16",), "long16")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("ulong",), "ulong")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("ulong2",), "ulong2")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("ulong4",), "ulong4")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("ulong8",), "ulong8")
        self.functions["native_sqrt"] = c99fn("native_sqrt", ("ulong16",), "ulong16")
        self.functions["native_tan"] = c99fn("native_tan", ("char",), "char")
        self.functions["native_tan"] = c99fn("native_tan", ("char2",), "char2")
        self.functions["native_tan"] = c99fn("native_tan", ("char4",), "char4")
        self.functions["native_tan"] = c99fn("native_tan", ("char8",), "char8")
        self.functions["native_tan"] = c99fn("native_tan", ("char16",), "char16")
        self.functions["native_tan"] = c99fn("native_tan", ("uchar",), "uchar")
        self.functions["native_tan"] = c99fn("native_tan", ("uchar2",), "uchar2")
        self.functions["native_tan"] = c99fn("native_tan", ("uchar4",), "uchar4")
        self.functions["native_tan"] = c99fn("native_tan", ("uchar8",), "uchar8")
        self.functions["native_tan"] = c99fn("native_tan", ("uchar16",), "uchar16")
        self.functions["native_tan"] = c99fn("native_tan", ("short",), "short")
        self.functions["native_tan"] = c99fn("native_tan", ("short2",), "short2")
        self.functions["native_tan"] = c99fn("native_tan", ("short4",), "short4")
        self.functions["native_tan"] = c99fn("native_tan", ("short8",), "short8")
        self.functions["native_tan"] = c99fn("native_tan", ("short16",), "short16")
        self.functions["native_tan"] = c99fn("native_tan", ("ushort",), "ushort")
        self.functions["native_tan"] = c99fn("native_tan", ("ushort2",), "ushort2")
        self.functions["native_tan"] = c99fn("native_tan", ("ushort4",), "ushort4")
        self.functions["native_tan"] = c99fn("native_tan", ("ushort8",), "ushort8")
        self.functions["native_tan"] = c99fn("native_tan", ("ushort16",), "ushort16")
        self.functions["native_tan"] = c99fn("native_tan", ("int",), "int")
        self.functions["native_tan"] = c99fn("native_tan", ("int2",), "int2")
        self.functions["native_tan"] = c99fn("native_tan", ("int4",), "int4")
        self.functions["native_tan"] = c99fn("native_tan", ("int8",), "int8")
        self.functions["native_tan"] = c99fn("native_tan", ("int16",), "int16")
        self.functions["native_tan"] = c99fn("native_tan", ("uint",), "uint")
        self.functions["native_tan"] = c99fn("native_tan", ("uint2",), "uint2")
        self.functions["native_tan"] = c99fn("native_tan", ("uint4",), "uint4")
        self.functions["native_tan"] = c99fn("native_tan", ("uint8",), "uint8")
        self.functions["native_tan"] = c99fn("native_tan", ("uint16",), "uint16")
        self.functions["native_tan"] = c99fn("native_tan", ("long",), "long")
        self.functions["native_tan"] = c99fn("native_tan", ("long2",), "long2")
        self.functions["native_tan"] = c99fn("native_tan", ("long4",), "long4")
        self.functions["native_tan"] = c99fn("native_tan", ("long8",), "long8")
        self.functions["native_tan"] = c99fn("native_tan", ("long16",), "long16")
        self.functions["native_tan"] = c99fn("native_tan", ("ulong",), "ulong")
        self.functions["native_tan"] = c99fn("native_tan", ("ulong2",), "ulong2")
        self.functions["native_tan"] = c99fn("native_tan", ("ulong4",), "ulong4")
        self.functions["native_tan"] = c99fn("native_tan", ("ulong8",), "ulong8")
        self.functions["native_tan"] = c99fn("native_tan", ("ulong16",), "ulong16")
        ### End generated code ###
        
        #Valid substitutions
        self.valid_substituations = [(Type(x[0]),Type(x[1])) for x in c99_substitutions]
        
        #built-in type names
        self.types = list()
        for scalar_t in c99_scalar_types: self.types.append(scalar_t)
        for vector_t in c99_vector_types: self.types.append(vector_t)

        #Built-in type casting functions
        #qualifiers [C99 6.7.3]
        self.quals = list()
        self.quals.append("const")
        self.quals.append("restrict")
        self.quals.append("volatile")
        #,,,
        
        #storage specifiers
        self.storage = list()
        self.storage.append("typedef")
        #...
        
        #function specifiers, enforced during parsing.
        self.funcspec = ("inline","explicit","virtual")
    
    def typename_exists(self, name):
        if name in self.types:
            return True
        for n in self._g.typenames:
            if name == n.name: return True
        return False
           
    def is_valid_name(self, name):
        if name == None:
            return True
        
        if name[0] == "!":
            return False
        return True
    
    def cond_type(self):
        """ Expected type of a conditional. 
        
        To check if conditional term with type cond_type is correct, use 
        if not self._g.type_defs.sub(cond_type,self._g.type_defs.cond_type()):
            raise...
        """
        return Type("bool")
    
    def dim_type(self):
        """Expected type of a dimension for an array.
        
        To check if a dimension is correct use this functio nas one of the args
        to `equal`.
        """
        return Type("size_t")
    
    def switch_type(self):
        """Type of switch statements."""
        return None #The full switch statement shouldn't resolve to a type.
    
    def subs_type(self):
        """Subscript type."""
        return self.dim_type()
    
    def exists(self, type):
        """Raises an exception only if the type is invalid according to c99
        
        Each type is responsible  for implementing exists in terms of 
        the current definition.
        """
        type.exists(self)
    
    def return_type(self, op, lhs, rhs=None):
        """Typechecks and resolves types for ops, including assignment."""
        if(op in c99_conditional_ops):
            if rhs == None or not self.sub(lhs,rhs):
                raise TargetTypeCheckException("lhs and rhs of = should have "+
                                               "compatable types.",None)
            return self.cond_type() 
        
        if op in c99_unary_ops:
            #TODO
            return lhs
        
        if(op in c99_binops):
            if rhs == None:
                raise TargetTypeCheckException(
                            "%s is a binop but only one argument is defined."%
                            op,None)
            try:
                return Type(c99_op_pairs[lhs.name,rhs.name])
            except KeyError as e:
                raise TargetTypeCheckException("Operation between %s and %s "%
                                               (lhs.name,rhs.name)+"undefined.",
                                               None)
        if(op == "="):
            if rhs == None:
                raise TargetTypeCheckException("= is binary but only one " +
                                               "argument given",None)
            if not self.sub(lhs,rhs):
                raise TargetTypeCheckException("lhs and rhs of = should have "+
                                               "compatable types.",None)
            return lhs
    
    def sub(self, lhs, rhs):
        """Returns true if lhs and be used where rhs is expected."""
        if not isinstance(lhs, Type): return False
        if not isinstance(rhs, Type): return False
        if lhs.name == rhs.name: return True
#        for pair in self.valid_substituations:
#            if pair[0] = lhs.name and pair[1] = rhs.name: return True
        if transitive_sub(lhs.name, rhs.name): 
#            if lhs.is_array == rhs.is_array and lhs.is_ptr == rhs.is_ptr:
            return True
        return False
        
    def reserved(self):
        """Words that cannot be used as variable names."""
        reserved_words = list()
        for w in self.types: reserved_words.append(w)
        for w in self.quals: reserved_words.append(w)
        for w in self.funcspec: reserved_words.append(w)
        
        #for w in self._g.typenames: reserved_words.append(w)
        #include names of other types.
        return reserved_words
        

################################################################################
#                                        TYPES                                 #
################################################################################

class Type(object):
    """Represents a declared type. 
    
    This class Contains all the information used by TypeDefinitions, contains
    type-specific logic for entering and leaving a scope, and is 
    subclassed for structs and functions. 
    """
    def __init__(self, name):
        """Initialized a new Type; based on Decl in pycparser/c_ast.cfg
        
        name: declaration type
        quals: list of qualifiers (const, volatile)
        funcspec: list function specifiers (i.e. inline in C99)
        storage: list of storage specifiers (extern, register, etc.)
        bitsize: bit field size, or None
        """
        self.name           = name
        self.declared_name  = None
        self.quals          = list()
        self.storage        = list()
        self.funcspec       = list()
        self.bitsize        = None 
        
        #Array types
        self.is_array = False
        self.dim      = None
        
        #Ptr types
        self.is_ptr   = False

    def enter_scope(self, v, g, scope):
        """Adds `Variable` v to `Scope` scope in `Context` g
        
        Types handle scopes in a dispatch-style pattern because the result of 
        adding a `Variable` to the scope varies depending upon the type of the
        `Variable`. For example, enum types add some ints to the context, and
        structs/typedefs add new type keywords."""
        #ensure that this type exists.
        g.type_defs.exists(self)
        
        # Create the variable identifier if it doesn't already exist.
        if not g._variables.has_key(v.name):
            g._variables[v.name] = v
        
        #Add the variable to the scope.
        v.add_scope(scope, self)
    
    def leave_scope(self, v, g, scope):
        """Removes `Variable` v from `Scope` scope in `Context` g
        
        See enter_scope."""
        v.remove_scope(scope)
          
    def __str__(self):
        name = ""
        for q in self.quals:
            name = name + "%s " % q
        for s in self.storage:
            name = name + "%s " % s
        for f in self.funcspec:
            name = name + "%s " % f
        if self.is_array:
            name = name + "[%s] " % self.dim
        name = name + "%s" % self.name
        return name

    def add_qual(self, qual):
        self.quals.append(qual)
    
    def add_storage_spec(self, s):
        self.storage.append(s)
    
    def set_bitsize(self, bitsize):
        self.bitsize = bitsize
    
    def exists(self, type_defs):
        """See `TypeDefinitions.exist`"""
        if not type_defs.typename_exists(self.name):
            raise TargetTypeCheckException("Typename %s unknown"%self.name,None)
        for q in self.quals:
            if not q in type_defs.quals:
                raise TargetTypeCheckException("Qualifier %s unknown"%q,None)
        for fs in self.funcspec:
            if not fs in type_defs.funcspec:
                raise TargetTypeCheckException(
                                   "Function Specifier %s unknown"%fs,None)
        for s in self.storage:
            if not s in type_defs.storage:
                raise TargetTypeCheckException(
                                    "Storage specifier %s unknown"%s,None)
        return True
            
class StructType(Type):
    """A struct that handles type names."""
    def __init__(self, name, members):
        super(StructType, self).__init__(name)
        self.name    = name
        self.members = members
    
    def has_member(self, name):
        for n in self.members.keys():
            if n == name: return True
        return False
    
    def get_type(self, name):
        for n in self.members.keys():
            if n == name: return self.members[n]
        raise TargetTypeCheckException("Struct member %s not found"%name,None)

    def exists(self, type_defs):
        #Ensure that all member types are valid types.
        for m_type in self.members.values():
            m_type.exists(type_defs)

class TypeDef(Type):
    """A typedef."""
    def __init__(self, tagname, type):
        """Constructor.
        
        typename = the name of this type
        type     = `Type` represented by typename
        """
        super(TypeDef, self).__init__(tagname)
        self.tagname = tagname
        self.type     = type
    
    def enter_scope(self, v, g, scope):
        g.add_typename(self.tagname,scope)
        super(TypeDef,self).enter_scope(v,g,scope)

    def leave_scope(self, v, g, scope):
        pass
        
class EnumType(Type):
    """An enum type."""
    def __init__(self, name, values):
        """Constructor.
        
        name = name of variable (optional). The Type.name name of all enums is
        simply enum. the `name` passed into this constructor is only used to 
        create a variable with the correct name.
        """
        super(EnumType,self).__init__("enum")
        self._enum_name = name
        self.enum_values = values if not values == None else list()
    
    @classmethod
    def enum_value_type(cls):
        t = Type("int")
        t.add_qual("const")
        return t

    @classmethod
    def enum_name_type(cls):
        return Type("int")
        
    def enter_scope(self, v, g, scope):
        """All enum values + the name should go in and out of scope together."""
        g.type_defs.exists(self)
        
        #If a name was given to the enum, add a new typename to the scope.
        if not self._enum_name == None:
            g.add_variable(self._enum_name, self.enum_name_type(), scope)
        
        #Add each of the enum values to the context.
        for value_name in self.enum_values:            
            g.add_variable(value_name, self.enum_value_type(), scope)
    
    def leave_scope(self,v,g,scope):
        v.remove_scope(scope)
        
    def exists(self, type_defs):
        for v in self.enum_values:
            if v in type_defs.reserved():
                raise TargetTypeCheckException("Reserved word in enum def",None)
        if self._enum_name in type_defs.reserved():
            raise TargetTypeCheckException("enum name with reserved word",None)
        return True

class EllipsisType(Type):
    """A dummy type for ellipses in function arguments."""
    def __init__(self):
        super(EllipsisType,self).__init__("...")
    
    def enter_scope(self,v,g,scope):
        pass
    def leave_scope(self,v,g,scope):
        pass
    def exists(self,type_defs):
        return True

class FunctionType(Type):
    """A function type. """
    
    def __init__(self, name, param_types=list(), return_type=Type("void")):
        super(FunctionType,self).__init__(name)
        self.name          = name # Part of the type because functions aren't values.
        self.param_types   = param_types
        self.return_type    = return_type 

    def has_ellipsis(self):
        for t in self.param_types:
            if isinstance(t, EllipsisType):
                return True
        return False
    
    def enter_scope(self, v, g, scope):
        g.type_defs.exists(self)
        if not g._variables.has_key(v.name):
            g._variables[v.name] = v
        v.add_scope(scope, self)
        g.functions.append(v)
    
    def exists(self, type_defs):
        for pt in self.param_types:
            if isinstance(pt, FunctionType):
                raise TargetTypeCheckException("HOFs not support by C")
            type_defs.exists(pt)
        if isinstance(self.return_type, FunctionType):
            raise TargetTypeCheckException("HOFs not support by C")
        type_defs.exists(self.return_type)
        return True


################################################################################
#                                 IDENTIFIERS                                  #
################################################################################

#This class should be renamed to Identifier.
class Variable(object):
    """A Variable is an Identifier and a scope. 
    
    Variable has multiple Types because the same identifier can have different
    types depending on the scope.
    """
    def __init__(self, name):
        self.name = name
        self.scope = list() #stack
        self.type  = dict() #{scope : type, ...}


    def _return_type(self, type):
        if isinstance(type, TypeDef):
            return type.type
        else:
            return type

    def get_type(self):
        return self._return_type(self.type.get(self.scope[-1]))
    
    def get_type_at_scope(self, scope):
        return self._return_type( self.type[scope] )

    def add_scope(self, scope, type):
        if not isinstance(type, Type):
            raise TargetTypeCheckException(
             "Expecting an instance of Type but got %s" % type.__class__,None)    
        self.scope.append(scope)
        self.type[scope] = type
        
    def remove_scope(self, scope):
        if self.scope.count(scope) > 0:
            self.scope.remove(scope)
        if self.type.has_key(scope):
            self.type.pop(scope)


################################################################################
#                                 CONEXT                                       #
################################################################################

class TypeName(object):
    def __init__(self, name):
        self.name = name
        self.scope = list()
        
class Context(object):
    """A context for typechecking C-style programs."""
    def __init__(self):
        self.returning   = False   #True iff checker is inside a return stmt
        self.functions   = list()  #stack, determines type of returning func.
        self._variables  = dict()  #name -> `Variable`  
        self._scope      = list()  #stack.
        self._scope.append(0)
        
        self.typenames = list()  #of TypeNames
        
        #Type definitions for the context.
        self.type_defs = TypeDefinitions(self)
        
        #Context variables specific to a statement's form.
        self.switch_type = Type(None) #Type of switch condition.
    
    def get_function(self, name):
        """Returns the Type of a function."""
        if name in self._variables:
            return self.get_variable(name).get_type()
        else:
            return self.type_defs.functions[name]
            
    def is_typename(self,name):
        for t in self.typenames:
            if t.name == name: return True
        return False
    
    def get_typename_type(self, name):
        return self.get_variable(name).get_type()
            
    def add_typename(self, name, scope):
        #TODO check to make sure it's not a reserved name
        for t in self.typenames:
            if t.name == name:
                t.scope.append(scope)
                return True
        t = TypeName(name)
        t.scope.append(scope)
        self.typenames.append(t)
        return True
    
    def get_variable(self, variable_name):
        """Returns a `Variable` with variable_name as its identifier."""
        if self._variables.has_key(variable_name):
            return self._variables.get(variable_name)
        else:
            raise TargetTypeCheckException("Variable %s not in scope "
                                           % variable_name, None)     
    
    def add_variable(self, variable_name, type, node=None):
        """Adds a variable to the current scope."""
        if not self.type_defs.is_valid_name(variable_name):
            raise TargetTypeCheckException(
                            "Invalid identifier or type name: %s"%
                            variable_name, node)
        
        if not isinstance(type, Type):
            raise TargetTypeCheckException(
                                        "Expected subclass of Type but got %s"%
                                        str(type), node)
        
        if variable_name in self.type_defs.reserved():
            raise TargetTypeCheckExpceiton("%s is a reserved word."%
                                           variable_name,Node)
        
        scope = self._scope[-1] #the current scope.

        # Ensure that this variable isn't already defined for the current scope.
        if self._variables.has_key(variable_name) and \
           self._variables[variable_name].scope.count(scope) > 0:
            raise TargetTypeCheckException("Cannot redeclare %s"%variable_name + 
                " (%s) as a different symbol (%s)" % 
                (self._variables[variable_name].get_type_at_scope(scope), type),
                node)
        
        # Add the identifier to the scope.
        if variable_name in self._variables.keys():
            type.enter_scope(self._variables.get(variable_name), self,scope)
        else:    
            type.enter_scope(Variable(variable_name),self,scope)

    def change_scope(self):
        """Adds another scope. Everything previously in scope remains so."""
        self._scope.append(0 if len(self._scope) == 0  else self._scope[-1] + 1)
        
    def leave_scope(self):
        """Moves down in scope. Removes all variables that go out of scope."""
        
        scope = self._scope[-1] #the current scope.
        
        #Remove scope from all identifiers and type names.
        for v in self._variables.values():
            if scope in v.scope:
                v.get_type_at_scope(scope).leave_scope(v,self,scope)
        for t in self.typenames:
            if scope in t.scope:
                t.scope.remove(scope)
        #Remove out-of-scope identifiers from identifier list.
        for v in self._variables.values():
            if len(v.scope) == 0: self._variables.pop(v.name)
        #Removed out-of-scope typenames
        for t in self.typenames:
            if len(t.scope) == 0: 
                self.typenames.remove(t)


################################################################################
#                            UTILITY CLASSES                                   #
################################################################################
class TargetTypeCheckException(Exception):
    """Raised to indicate an error during type checking of generated code."""
    def __init__(self, message, node):
        self.message = message
        self.node = node


################################################################################
#                                TYPESCHECKING                                 #
################################################################################
        
class OpenCLTypeChecker(pycparser.c_ast.NodeVisitor):
    """Type checks OpenCL code.
    
    To use:
        tc = OpenCLTypeChecker(context)
        tc.visit(node) 
    """
    
    def __init__(self, context=Context()):
        """context = a pycparserext.typechecker.Context object."""
        self._g = Context()                                                     #To get auto-complete in my IDE... TODO remove.
        self._g = context
        
    def generic_visit(self, node):
        """Raises an error when no visit_XXX method is defined."""
        raise TargetTypeCheckException("visit_%s undefined" % 
                                       node.__class__.__name__, node)
    def visit_children(self, node):
        for c_name, c in node.children():
            self.visit(c)

    def visit_FileAST(self, node):
        self.visit_children(node)
    
    def visit_Default(self, node):
        self.visit_children(node)
    
    def visit_DoWhile(self, node):
        """Ensures conditional has correct type and statement is well-typed."""
        cond_type = self.visit(node.cond)
        if not self._g.type_defs.sub(cond_type,self._g.type_defs.cond_type()):
            raise TargetTypeCheckException(
                        "Expected condition (%s or similar) but found %s" %
                        (str(self._g.type_defs.cond_type()), str(cond_type)), 
                        node)
        self._g.change_scope()
        self.visit(node.stmt)
        self._g.leave_scope()
        
    def visit_While(self, node):
        return self.visit_DoWhile(node)

    def visit_For(self, node):
        self._g.change_scope()
                
        self.visit(node.init)
                
        cond_type = self.visit(node.cond)
        if not self._g.type_defs.sub(cond_type,self._g.type_defs.cond_type()):
            raise TargetTypeCheckException(
                        "Expected condition of for to be %s but found %s" %
                        (str(self._g.type_defs.cond_type()), 
                         str(cond_type)), node)
        
        self.visit(node.next)
        self.visit(node.stmt)
        
        self._g.leave_scope()
        
    
    def visit_Goto(self, node):
        self.visit_children(node)
    def visit_Label(self, node):
        self.visit_children(node)

    def visit_TernaryOp(self, node):
        """Ensures conditional is correct type and expression types match."""
        cond_type = self.visit(node.cond)
        if not self._g.type_defs.sub(cond_type,self._g.type_defs.cond_type()):
            raise TargetTypeCheckException(
                        "Expected condition of ternary to be %s but found %s" %
                        (str(self._g.type_defs.cond_type()), str(cond_type)), 
                        node)
        
        t_t = self.visit(node.iftrue)
        f_t = self.visit(node.iffalse)
        if not self._g.type_defs.sub(t_t,f_t):
            raise TargetTypeCheckException(
                        "Ternary condition expressions %s and %s don't match" %
                        (str(t_t), str(f_t)), node)
        
        return t_t
    
    def visit_Switch(self, node):
        """Adds switch to the context."""
        cond_type = self.visit(node.cond)
        self._g.switch_type = cond_type
#        if not cond_type == Type.get_cond_type():
#            raise TargetTypeCheckException(
#                "Expected conditional type for switch condition but found %s"% 
#                cond_type, node)
        
        #Visit each case statement.
        self.visit(node.stmt)
        self._g.switch_type = Type(None)
    
    def visit_Case(self, node):
        label_t = self.visit(node.expr)
        if not self._g.type_defs.sub(label_t,self._g.type_defs.switch_type()):
            raise TargetTypeCheckException(
                                "Case label of type %s does not reduce to %s"%
                                (str(label_t), str(self._g.switch_type)), node) 
        for s in node.stmts:
            self.visit(s)
    
    def visit_If(self, node):
        cond_type = self.visit(node.cond)
        if not self._g.type_defs.sub(cond_type,self._g.type_defs.cond_type()):
            raise TargetTypeCheckException(
                "Expected conditional type for if condition but found %s"% 
                cond_type, node)
        
        self._g.change_scope()
        self.visit(node.iftrue)
        self._g.leave_scope()
        self._g.change_scope()
        if not node.iffalse == None: #else portion is optional.
            self.visit(node.iffalse)
        self._g.leave_scope()

    def visit_FuncDef(self, node):
        """Function definition."""
        # Get the function's name and return type.
        function_name = node.decl.name
        return_type   = Type(node.decl.type.type.type.names[0])
        
        # Get the parameter names and types
        param_names = list()
        param_types = list()
        if not node.decl.type.args == None:
            for param in node.decl.type.args.params:
                t = self.visit(param)
                param_names.append(t.declared_name)
                param_types.append(t)
                #param_types.append(Type(param.type.type.names[0]))
        
        # Add the function to the enclosing scope.
        func_t = FunctionType(function_name, param_types, return_type)
        self._g.add_variable(func_t.name, func_t, node)
               
        # Create a new scope for the function defintion.
        self._g.change_scope()
        
        # Add params to the function's scope
        for n,t in zip(param_names,param_types):
            self._g.add_variable(n, t, node)
            
        # Visit expressions in the body of the function.
        self.visit(node.body)
        
        # Move out of the function definition scope.
        self._g.leave_scope()
    
    def visit_Compound(self, node): 
        self.visit_children(node)
    
    def visit_Return(self, node):
        """Ensures the returned value's type is the function's return_type."""
        self._g.returning = True
        return_type = self.visit(node.expr)
        self._g.returning = False
        
        f = self._g.functions[-1].get_type()
        if not self._g.type_defs.sub(return_type,f.return_type):
            raise TargetTypeCheckException(
                        "returning from %s expected %s but got %s" %
                        (str(f), str(f.return_type), str(return_type)), node)
    
    def visit_FuncCall(self, node):
        func_type = self._g.get_function(node.name.name)

        if not isinstance(func_type,FunctionType):
            raise TargetTypeCheckException("called '%s' is not a function"%
                            func_type.name, node)
        
        #Get the parameter types
        param_types = list()
        if not node.args == None:
            for e in node.args.exprs:
                param_types.append(self.visit(e))
        
        # Ensure that the parameter lists are the same size
        if not len(param_types) == len(func_type.param_types) \
        and (not func_type.has_ellipsis() \
             or len(param_types) < len(func_type.param_types)-1):        
            raise TargetTypeCheckException(
                    "Wrong number of arguments passed to %s" %
                    (str(func_type)), node)
        
        # Ensure that parameter types match declared parameter types.
        #Because zip uses  the smallest list, 
        for p,ep in zip(param_types, func_type.param_types):
            #Skip over the ellipsis, anything following won't be in the zip.
            if isinstance(ep, EllipsisType):
                continue
            if not self._g.type_defs.sub(p, ep):
                raise TargetTypeCheckException(
                        "Arguments to %s are incorrect: expected %s but got %s"%
                        (str(func_type),ep,p), node)
        
        # Return the return type.
        return func_type.return_type 
    
    def visit_Continue(self, node):
        pass
    
    def visit_Decl(self, node):
        """Adds a declared variable to the context."""
        name = node.name
        
        #Get the base type
        type = self.visit(node.type)

        if not isinstance(type,Type):
            raise TargetTypeCheckException("Expected Type but found %s"%
                                           type.__class__.__name__,node)
        
        #Enrich the type with c99 goodness.
        if not node.quals == None:
            for q in node.quals:
                type.add_qual(q)
        if not node.storage == None:
            for s in node.storage:
                type.add_storage_spec(s)
        if not node.bitsize == None:
            type.set_bitsize(node.bitsize)
        
        self._g.add_variable(name, type, node)
        
        
        #Ensure that type of the initial value matches the declared type.
        if node.init != None:
            #could be a list or a scalar.
            initial_value_type = self.visit(node.init)
             
            if isinstance(initial_value_type,types.ListType):
                if (type.is_array or type.is_ptr):
                    if not len(initial_value_type) == type.dim:
                        raise TargetTypeCheckException(
                        "Type %s expected dimension %s but initialized to %s"%
                            (str(type),str(type.dim),len(initial_value_type)),
                            node)
                    for t in initial_value_type:
                        if not self._g.type_defs.sub(t, type):
                            raise TargetTypeCheckException(
                            "Wrong type in initializer for %s"%str(type),node)

                elif isinstance(type, StructType):
                    if len(initial_value_type) > len(type.members.values()):
                        raise TargetTypeCheckException(
                        "Type %s expected dimension %s but initialized to %s"%
                            (str(type),len(type.members.values()),
                             len(initial_value_type)),node)
                    for t,et in zip(initial_value_type, type.members.values()):
                        if not self._g.type_defs.sub(t,et):
                            raise TargetTypeCheckException(
                            "Expected %s but found %s in struct initializer %s"%
                            (str(et),str(t),str(type)), node)
                            
                else:
                    raise TargetTypeCheckException("Assigned list to scalar %s"%
                                                   str(type),node)         
           
            else:
                if not self._g.type_defs.sub(initial_value_type,type):
                    raise TargetTypeCheckException(
                    "Incompatable types when assigning to %s (%s) from type %s"% 
                    (name, str(type), str(initial_value_type)), node)
        
        return type
        
        

    def visit_DeclList(self, node):
        self.visit_children(node)
    
    def visit_Assignment(self, node):
        """Defers to C99 spec as defined in Type"""
        #Typechecking logic handled by the types.
        return self._g.type_defs.return_type(node.op, 
                                             self.visit(node.lvalue), 
                                             self.visit(node.rvalue))
    
    def visit_UnaryOp(self, node):
        """Defers to C99 spec as defined in Type"""
        return self._g.type_defs.return_type(node.op,self.visit(node.expr))
    
    def visit_BinaryOp(self, node):
        """Defers to C99 spec as defined in Type"""
        return self._g.type_defs.return_type(node.op,self.visit(node.left),
                                          self.visit(node.right))
    
    def visit_Break(self):
        pass
        
    def visit_ID(self, node):
        """Gets the type of an already declared variable.
        
        Context does exception handling if ID isn't defined.
        """
        return self._g.get_variable(node.name).get_type()
    
    def get_ID(self, node):
        """Returns the name of the ID instead of its type."""
        return node.name
    
    def visit_Cast(self, node):
        """Returns the type to which the variable is casted."""
        return self.visit(node.to_type)
    
    def visit_Typename(self, node):
        t = self.visit(node.type)
        for q in node.quals:
            t.add_qual(q)
        return t
            
    
    
    def visit_Constant(self, node):
        return Type(node.type)
    
    def visit_TypeDecl(self, node):
        #                                                                        TODO quals?
        """Returns the Type for the base type.
        
        I believe that visit_Decl is the only way that visit_TypeDecl is ever
        called. If this is not true, then this function should add the variable
        to the context.
        """
        t = self.visit(node.type)
        t.declared_name = node.declname
        
        if not node.quals == None:
            for q in node.quals:
                t.add_qual(q)
    
        return t

    def visit_IdentifierType(self, node):
        """Returns a Type for the identifier.""" #TODO Quals?
        name = " ".join(node.names)
        
        if self._g.is_typename(name):
            return self._g.get_typename_type(name)
        else:
            return Type(name)

    def visit_PreprocessorLine(self, node):
        raise TargetTypeCheckException("Expected preprocessed code "+
                                       "but found a preprocessor line.", node)
    
    def visit_ArrayDecl(self, node):
        t = self.visit(node.type)
        dim_t = self.visit(node.dim)
        
        if not self._g.type_defs.sub(dim_t, self._g.type_defs.dim_type()):
            raise TargetTypeCheckException(
                            "Expected valid Array dimension type but found %s"%
                            str(dim_t), node)
        t.is_array = True
        t.dim = types.IntType(node.dim.value)
        return t
    
    def visit_ExprList(self, node):
        expression_types = list()
        for e in node.exprs: expression_types.append(self.visit(e))
        return expression_types
    
    def visit_ArrayRef(self, node):
        array_t = self.visit(node.name)
        
        if not array_t.is_array:
            raise TargetTypeCheckException(
                    "Attempting subscript access on a non-array type %s" %
                    str(array_t), node) 
        
        subscript_t = self.visit(node.subscript)
        if not self._g.type_defs.sub(subscript_t,self._g.type_defs.subs_type()):
            raise TargetTypeCheckException(
                                        "Arrays cannot be indexed by type %s" % 
                                        str(subscript_t), node)
        
        return array_t
    
    def visit_EmptyStatement(self, node):
        pass
    
    def visit_Enum(self, node):
        enum = EnumType(node.name,list())
        
        for e in node.values.enumerators:
            if not e.value == None:
                v_type = self.visit(e.value)
                if not self._g.type_defs.sub(v_type,EnumType.enum_value_type()):
                    raise TargetTypeCheckException(
                            "Expected enum value to be type %s but found %s" %
                            (EnumType.enum_value_type(), v_type), node)
            enum.enum_values.append(e.name)
        
        return enum
    
    def visit_Enumerator(self, node):
        raise TargetTypeCheckException("Sould be handled by visit_Enum.",node)

    def visit_EnumeratorList(self, node):
        raise TargetTypeCheckException("Sould be handled by visit_Enum.",node)

    def visit_Typedef(self, node):
        t = self.visit(node.type)
        for q in node.quals:
            t.add_qual(q)
        for s in node.storage:
            t.add_storage_spec(s)
        
        type = TypeDef(node.name, t)
        self._g.add_variable(node.name, type, node)
        return type

    def visit_Struct(self, node):
        #Capture declarations in a new context
        old_g = self._g
        self._g = Context()
        
        if not node.decls == None:
            for m in node.decls:
                self.visit(m)
        
        #Get the types and names of attributes
        members = dict()
        for v in self._g._variables.keys():
            members[v] = self._g.get_variable(v).get_type()
        
        #change to original context and create the struct type
        self._g = old_g
        t = StructType(node.name, members)
        return t
    
    def visit_StructRef(self, node):
        name = self.get_ID(node.name)
        struct = self._g.get_variable(name)
        struct_t = self._g.get_variable(name).get_type() 
        
        if not isinstance(struct_t, StructType):
            raise TargetTypeCheckException("Excpected struct type but found %s"
                                           % str(struct.get_type()), node)
        
        #Ensure correct type argument is used
        if (struct_t.is_ptr and node.type == ".") \
        or (not struct_t.is_ptr and node.type == "->"):
            raise TargetTypeCheckException(
                                    "Invalid type argument of '%s' (have '%s')"%
                                           (node.type,str(struct_t)), node)
        
        return struct.get_type().get_type(self.get_ID(node.field))
        
    def visit_PtrDecl(self, node):
        t = self.visit(node.type)
        t.is_ptr = True
        for q in node.quals:
            t.add_qual(q)
        return t
            
    def visit_Union(self, node):
        """A Union."""
        if self._g.is_typename(node.name):
            return self._g.get_typename_type(node.name)
        else:
            #Treat unions that haven't already been declared like structs.
            if node.decls == None:
                raise TargetTypeCheckException("Storage size of %s unknown"%
                                               node.name,node)
            struct_t =  self.visit_Struct(node)
            type = TypeDef(node.name, struct_t)
            self._g.add_variable(node.name, type, node)
            return struct_t
    
    def visit_EllipsisParam(self, node):
        return EllipsisType()
