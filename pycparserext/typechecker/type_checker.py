import pycparser
from pycparserext.ext_c_parser import OpenCLCParser
from pycparserext.ext_c_generator import OpenCLCGenerator
#import cypy

################################################################################
#                      TYPING CHECKING RULES                                   #
################################################################################
class TypeDefinitions(object):
    def __init__(self):       
        """Todo populate from OCL spec""" 
        #built-in types
        self.types = list()
        self.types.append("int")
        self.types.append("char")
        
        self.tags = dict() #tagname -> Type
        
        #qualifiers
        self.quals = list()
        self.quals.append("const")
        
        #storage specifiers
        self.storage = list()
        
        #function specifiers
        self.funcspec = list()
    
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
        return Type("int")
    
    def switch_type(self):
        """Type of switch statements."""
        return None #The full switch statement shouldn't resolve to a type.
    
    def subs_type(self):
        return self.dim_type()
    
    def exists(self, type):
        """Raises an exception if type doesn't exist. Returns true."""
        if not type.name in self.types:
            raise TargetTypeCheckException("Typename %s unknown"%type.name,node)
        for q in type.quals:
            if not q in self.quals:
                raise TargetTypeCheckException("Qualifier %s unknown"%q,node)
        for fs in type.funcspec:
            if not fs in self.funcspec:
                raise TargetTypeCheckException(
                                   "Function Specifier %s unknown"%fs,node)
        for s in type.storage:
            if not s in self.storage:
                raise TargetTypeCheckException(
                                    "Storage specifier %s unknown"%s,node)
        return True
    
    def return_type(self, op, lhs, rhs=None):
        """Typechecks and resolves types for ops, including assignment."""
        if(op == "=="):
            return self.cond_type()
        return lhs
    
    def sub(self, lhs, rhs):
        """Returns true if lhs and be used where rhs is expected per c99."""
        if not isinstance(lhs, Type): return False
        if not isinstance(rhs, Type): return False
        return lhs.name == rhs.name

################################################################################
#                                        TYPES                                 #
################################################################################

class Type(object):
    """An OpenCL Type."""
    def __init__(self, name):
        """Initialized a new Type; based on Decl in pycparser/c_ast.cfg
        
        name: declaration type
        quals: list of qualifiers (const, volatile)
        funcspec: list function specifiers (i.e. inline in C99)
        storage: list of storage specifiers (extern, register, etc.)
        bitsize: bit field size, or None
        """
        self.name     = name
        self.quals    = list()
        self.storage  = list()
        self.funcspec = list()
        self.bitsize  = None 
        
        #Array types
        self.is_array = False
        self.dim      = None

    def enter_scope(self, v, g, scope):
        """Adds `Variable` v to `Scope` scope in `Context` g
        
        Types handle scopes in a dispatch-style pattern because the result of 
        adding a `Variable` to the scope varies depending upon the type of the
        `Variable`. For example, enum types add some ints to the context, and
        structs/typedefs add new type keywords."""
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

class TypeDef(Type):
    """A typedef."""
    def __init__(self, typename, type):
        """Constructor.
        
        typename = the name of this type
        type     = `Type` represented by typename
        """
        super(TypeDef, self).__init__(type.name)
        self.typename = name
        self.type     = type
    
    
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
        #If a name was given to the enum, add a new variable to the scope.
        if not self.name == None:
            v.name = self._enum_name #TODO-nf
            self.enum_name_type().enter_scope(v, g, scope)
        
        #Add each of the enum values to the context.
        for value_name in self.enum_values:            
            g.add_variable(value_name, self.enum_value_type(), None)

class FunctionType(Type):
    """A function type in the target language. 

    The function name is part of the type, and function Variables are given
    the name variable_name(name) in the Context.
    """
    
    @classmethod
    def variable_name(cls, name):
        return "!%s" % name 
    
    def __init__(self, name, param_types=list(),
                 return_type=Type("void")):
        self.name          = name # Part of the type because functions aren't values.
        self.param_types   = param_types
        self.return_type    = return_type 
    
    def get_variable_name(self):
        return self.variable_name(self.name)

    def enter_scope(self, v, g, scope):
        if not g._variables.has_key(v.name):
            g._variables[v.name] = v
        v.add_scope(scope, self)
        g.functions.append(v)


################################################################################
#                                 IDENTIFIERS                                  #
################################################################################

class Variable(object):
    """A variable or function identifier. 
    
    Variable has multiple Types because the same identifier can have different
    types depending on the scope.
    """
    def __init__(self, name):
        self.name = name
        self.scope = list() #stack
        self.type  = dict() #{scope : type, ...}

    def get_type(self):
        return self.type.get(self.scope[-1])
    
    def get_type_at_scope(self, scope):
        return self.type[scope]

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

class Context(object):
    """A context for typechecking C-style programs.
    
    The primary reason this is C-style is that the scope is a stack, and 
    functions aren't treated a values. 
    """
    def __init__(self):
        self.returning   = False   #True iff checker is inside a return stmt
        self.functions   = list()  #stack, determines type of returning func.  
        self._variables  = dict()  #name -> Variable
        self._scope      = list()  #stack.
        self._scope.append(0)
        
        #Type definitions for thie context (typenames, etc.)
        self.type_defs = TypeDefinitions()
        
        #Context variables specific to a statement's form.
        self.switch_type = Type(None) #Type of switch condition.
    
    def get_variable(self, variable_name):
        if self._variables.has_key(variable_name):
            return self._variables.get(variable_name)
        else:
            raise TargetTypeCheckException("Variable %s not in scope "
                                           % variable_name, None)     
    
    def add_variable(self, variable_name, type, node=None):
        """Adds a variable to the current scope."""
        if not isinstance(type, Type):
            raise TargetTypeCheckException(
                                        "Expected subclass of Type but got %s"%
                                        str(type), node)
        
        scope = self._scope[-1] #the current scope.

        # Ensure that this variable isn't already defined for the current scope.
        if self._variables.has_key(variable_name) and \
           self._variables[variable_name].scope.count(scope) > 0:
            raise TargetTypeCheckException("Cannot redeclare %s"%variable_name + 
                " (%s) as a different symbol (%s)" % 
                (self._variables[variable_name].get_type_at_scope(scope), type),
                node)
        
        # Add the identifier to the scope.
        type.enter_scope(Variable(variable_name),self,scope)

    def change_scope(self):
        """Adds another scope. Everything previously in scope remains so."""
        self._scope.append(0 if len(self._scope) == 0  else self._scope[-1] + 1)
        
    def leave_scope(self):
        """Moves down in scope. Removes all variables that go out of scope."""
        scope = self._scope[-1] #the current scope.
        for v in self._variables.values():
            if scope in v.scope:
                v.get_type_at_scope(scope).leave_scope(v,self,scope)
        #Remove out-of-scope identifiers from identifier list.
        for v in self._variables.values():
            if len(v.scope) == 0: self._variables.pop(v.name)


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
                        (str(Type.get_cond_type()), str(cond_type)), node)
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
                        (str(Type.get_cond_type()), str(cond_type)), node)
        
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
                param_names.append(param.type.declname)
                param_types.append(Type(param.type.type.names[0]))
        
        # Add the function to the enclosing scope.
        func_t = FunctionType(function_name, param_types, return_type)
        self._g.add_variable(func_t.get_variable_name(), func_t, node)
               
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
        """TODO? """
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
        func_type = self._g.get_variable(
                          FunctionType.variable_name(node.name.name)).get_type()
        
        #Get the parameter types
        param_types = list()
        if not node.args == None:
            for e in node.args.exprs:
                param_types.append(self.visit(e))
        
        # Ensure that the parameter lists are the same size
        if not len(param_types) == len(func_type.param_types):
            raise TargetTypeCheckException(
                    "Wrong number of arguments passed to %s" %
                    (str(func_type)), node)
        
        # Ensure that parameter types match declared parameter types.
        for p,ep in zip(param_types, func_type.param_types):
            if not self._g.type_defs.sub(p, ep):
                raise TargetTypeCheckException(
                        "Arguments to %s are incorrect: expected %s but got %s"%
                        (str(func_type),p,ep), node)
        
        # Return the return type.
        return func_type.return_type 
    
    def visit_Continue(self, node):
        pass
    
    def visit_Decl(self, node):
        """Adds a declared variable to the context."""
        name = node.name

        #Get the base type
        type = self.visit(node.type)
        
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
            initial_value_type = self.visit(node.init) 
            if not self._g.type_defs.sub(type , initial_value_type):
                raise TargetTypeCheckException(
                "Incompatable types when assigning to %s (type: %s) from type %s" % 
                (name, str(type), str(initial_value_type)), node)
        
        

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
    
    def visit_Cast(self, node):
        """Returns the type to which the variable is casted."""
        return self.visit(node.to_type)
    
    def visit_Typename(self, node):
        return self.visit(node.type)
    
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
        if not node.quals == None:
            for q in node.quals:
                t.add_qual(q)
        
        
        
        return t

    def visit_IdentifierType(self, node):
        """Returns a Type for the identifier."""
        return Type(node.names[0])                                              #TODO quals?

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
        t.dim = node.dim
        return t
    
    def visit_ExprList(self, node):
        #TODO do the right thing.
        """Returns an Array of the last expr's type. TODO"""
        t = None #the type
        for e in node.exprs:
            if t == None:
                t = self.visit(e)
            else:
                e_t = self.visit(e)
                if not self._g.type_defs.sub(t, e_t):
                    raise TargetTypeCheckException(
                     "Expected all expressions to have type %s, but found %s"%
                     (str(t), str(e_t)), node)
        t.is_array = True
        t.dim = len(node.exprs)
        return t
    
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

#    def visit_Typedef(self, node):
#        node.show()
        