import pycparserext.typechecker as type_checker

class TypeCorrespondence(object):
    """ Converted between typechecker types, ace types and ocl types.
    
    tc_t  = a clq.pycparserext.type_checker.Type
    ace_t = an ace type
    ocl_t = an opencl type (string)
    """
    
    @classmethod
    def ace_to_tc(self, ace_t):
        name = ace_t.name
        t = type_checker.Type(ace_t.name)
        if t.name.endswith("*"):
            t.name = t.name.replace("*","")
            t.is_ptr = True
        return t
    
    @classmethod
    def tc_to_ace(self, tc_t):
        return str(tc_t)