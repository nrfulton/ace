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
    return FunctionType(name,
                        [Type(t_name) for t_name in args],
                        Type(return_type))

c99_binops = ("+","-")
c99_conditional_ops = ("==","!=","<","<=",">",">=")

op_pairs = {
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
        """Todo populate from OCL spec""" 
        #The context
        self._g = context
        
        #built-in functions
        self.functions = dict()
        self.functions["tanh"] = c99fn("tanh", ("double",), "double")
        self.functions["tanhf"] = c99fn("tanh", ("float",), "float")
        self.functions["tanhl"] = c99fn("tanh", ("long double",), "long double")
        
        #built-in type names
        self.types = ("uchar", "char",
         "ushort", "short",
         "uint", "int",
         "ulong", "long",
         "uintptr_t", "intptr_t",
         "size_t", "ptrdiff_t",
         "half", "float", "double",
         "void", "bool",
         "long double") #TODO find all the combinations...

        #qualifiers
        self.quals = list()
        self.quals.append("const")
        #,,,
        
        #storage specifiers
        self.storage = list()
        self.storage.append("typedef")
        #...
        
        #OpenCL function specifiers
        self.funcspec = list()
        #...
    
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
        return Type("int") #TODO change to size_t
    
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
        
        if(op in c99_binops):
            try:
                return op_pairs[lhs.name,rhs.name]
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
        """Returns true if lhs and be used where rhs is expected per c99."""
        #TODO take into account typenames.
        if not isinstance(lhs, Type): return False
        if not isinstance(rhs, Type): return False
        return lhs.name == rhs.name
    
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
