import pycparser
from pycparserext.ext_c_parser import OpenCLCParser
from pycparserext.ext_c_generator import OpenCLCGenerator
import cypy

################################################################################
#                                        TYPES                                 #
################################################################################
class Type:
    """ An OpenCL Type """
    def __init__(self, name):
        self.name = name

    def eq(self, other):
        """ This is incorrect. TODO. """
        if not isinstance(other, Type): return False
        return str(self.name) == str(other.name)
    
    def __eq__(self, other):
        return self.eq(other)
    def __cmp__(self,other):
        return self.eq(other)

class FunctionType(Type):
    """ A function type in the target language. 
        The function name is part of the type.
        Function "Variables" are given the name ![name] in the Context."""
    
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


################################################################################
#                                 CONTEXT HANDLING                             #
################################################################################

class Variable(object):
    """ A variable. """
    def __init__(self, name):
        self.name = name
        self.scope = list() #stack
        self.type  = dict() #{scope : type, ...}
        
    def add_scope(self, scope, type):
        if not isinstance(type, Type):
            raise TargetTypeCheckException("type must by a Type.", node)    
        self.scope.append(scope)
        self.type[scope] = type

    def get_type(self):
        return self.type.get(self.scope[-1])
    
    def get_type_at_scope(self, scope):
        return self.type[scope]

    def remove_scope(self, scope):
        if self.scope.count(scope) > 0:
            self.scope.remove(scope)
        if self.type.has_key(scope):
            self.type.pop(scope)
    
class Context(object):
    """ A context for typechecking C-style programs.
        The scope is a stack. """
    def __init__(self):
        self.returning  = False   #True iff checker is inside a return stmt
        self.functions  = list()  #stack, determines type of returning func.  
        self._variables = dict()  #name -> Variable
        self._scope     = list()  #stack.
        self._scope.append(0)
    
    def get_variable(self, variable_name):
        if self._variables.has_key(variable_name):
            return self._variables.get(variable_name)
        else:
            raise TargetTypeCheckException("Variable %s not in scope "
                                           % variable_name, None)     
    
    def add_variable(self, variable_name, type, node=None):
        """ Adds a variable to the current scope.
            An error is raised if the variable is already defined in scope. """
        scope = self._scope[-1] #the current scope.

        # Ensure that this variable isn't already defined for the current scope.
        if self._variables.has_key(variable_name) and \
           self._variables[variable_name].scope.has_key(scope):
            raise TargetTypeCheckException("Cannot define variable %s " +
                            "twice in the same context" % variable_name, node)
        
        # Add the variable to this scope.
        if not self._variables.has_key(variable_name):
            self._variables[variable_name] = Variable(variable_name)
            self._variables[variable_name].add_scope(scope,type)
            if isinstance(type, FunctionType):
                self.functions.append(self._variables[variable_name])

    def change_scope(self):
        """ Adds another scope. Everything previously in scope remains so. """
        self._scope.append(0 if len(self._scope) == 0  else self._scope[-1] + 1)
        
    def leave_scope(self):
        """ Moves down in scope. Removes all variables that go out of scope. """
        scope = self._scope[-1] #the current scope.
        for v in self._variables.values():
            if scope in v.scope:
                v.remove_scope(scope)
            if len(v.scope) == 0:
                self._variables.pop(v.name)


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
    """ Type checks OpenCL code.
        To use:
            tc = OpenCLTypeChecker(context)
            tc.visit(node) """
    
    def __init__(self, context=Context()):
        """ context = a pycparserext.typechecker.Context object. """
        self._g = Context() #To get auto-complete... TODO remove.
        self._g = context

    def visit_FileAST(self, node):
        self.visit_children(node)
    
#    def visit_ParamList(self, node):
#        self.visit_children(node)
        
    def visit_FuncDef(self, node):
        """ Function definition. """
        # Get the function's name and return type.
        function_name = node.decl.name
        return_type   = Type(node.decl.type.type.type.names[0])
        
        # Get the parameter names and types
        param_names = list()
        param_types = list()
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
        """ TODO? """
        self.visit_children(node)
    
    def visit_Return(self, node):
        """ Checks that the value returned has the same type as the enclosing 
            function. """
        self._g.returning = True
        return_type = self.visit(node.expr)
        self._g.returning = False
        
        f = self._g.functions[-1].get_type()
        if not return_type == f.return_type:
            raise TargetTypeCheckException(
                                    "returning from %s expected %s but got %s" %
                                    (f.name, f.return_type.name, return_type.name), node)
    
    def visit_FuncCall(self, node):
        func_type = self._g.get_variable(
                          FunctionType.variable_name(node.name.name)).get_type()
        
        #Get the parameter types
        param_types = list()
        for e in node.args.exprs:
            param_types.append(self.visit(e))
        
        # Ensure that the parameter lists are the same size
        if not len(param_types) == len(func_type.param_types):
            raise TargetTypeCheckException(
                    "Wrong number of arguments passed to %s" %
                    (func_type.name), node)
        
        # Ensure that parameter types match declared parameter types.
        for p,ep in zip(param_types, func_type.param_types):
            if not p == ep:
                raise TargetTypeCheckException(
                        "Arguments to %s are incorrect: expected %s but got %s"%
                        (func_type.name,p,ep), node)
        
        # Return the return type.
        return func_type.return_type 
    
    
    def generic_visit(self, node):
        """ Raises an error when no visit_XXX method is defined. """
        raise TargetTypeCheckException("visit_%s undefined" % 
                                       node.__class__.__name__, ast)
    def visit_children(self, node):
        for c_name, c in node.children():
            self.visit(c)


#Testing...
p = OpenCLCParser()
ast = p.parse("__kernel int plus(int a, int b) {return plus(a + b, 1);}")
try:
    tc = OpenCLTypeChecker(Context())
    tc.visit(ast)
except TargetTypeCheckException as e:
    print e.message
    raise e

#ast.show()

#def type_check_OpenCL(g, ast):
#    """ Type checks OpenCL code generated by Ace 
#        g(amma) = current context
#        ast     = current AST 
#        Returns a new context. """
#    if isinstance(ast, pycparser.c_ast.FileAST):
#        for child in ast.ext:
#            g = type_check_OpenCL(g, child)
#    if isinstance(ast, pycparser.c_ast.FuncDef):
#        pass
#        #for child in ast.ext:
#        #    g = type_cehck_OpenCL(g, child)
#    else:
#        raise TargetTypeCheckException("Node type is unknown %s" % ast.__class__,
#                                   ast)