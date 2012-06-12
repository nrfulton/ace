import clq
import cypy
import cypy.astx as astx
import clq.extensions.regex as regex

def get_singleton_language_type(cls,backend,regex_str):
    """ returns the singleton type associated with a backend and all equivalent regular expressions. """
    
    if not hasattr(get_singleton_language_type, "regex_list"): 
        get_singleton_language_type.regex_list = dict()
    
    leftNFA = regex.NFA.parse(regex.Pattern(regex_str).get_regex())
    
    for [cmp_backend,cmp_regex_str] in get_singleton_language_type.regex_list.keys():
        if cmp_backend != backend: continue
        #Using the set theoretic definition of equivalence; an isomorphism test might be faster.
        cmpNFA = regex.NFA.parse(regex.Pattern(cmp_regex_str).get_regex())
        if leftNFA.included_in(cmpNFA) and cmpNFA.included_in(leftNFA):
            return get_singleton_language_type.regex_list[frozenset({cmp_backend,cmp_regex_str})]
    
    #create a new language type.
    new_lang_key = frozenset([backend,regex_str])
    
    LangType = type("Lang_" + Language.regex_to_name(regex_str), (Language,backend.string_type(),), {})
    g = LangType(None)
    g._backend = backend
    g._regex = regex_str
    g.name = Language.regex_to_name(g._regex)
    
    get_singleton_language_type.regex_list[new_lang_key] = g
    return g
    
#@cypy.intern
class Language(clq.Type):

    @classmethod
    def regex_to_name(cls, name):
        ret_val = ""
        for c in name:
            if c == ".":
                ret_val += "Dot"
            elif c == "+":
                ret_val += "Plus"
            elif c == "*":
                ret_val += "Kleene"
            elif c == "?":
                ret_val += "Question"
            elif c == "(":
                ret_val += "LP"
            elif c == ")":
                ret_val += "RP"
            else:
                ret_val += c
        return ret_val
    
    @classmethod
    def factory(cls, backend, regex_str):
        """ This function returns the single instance of a language type associated with
            the backend and the class of equivalent regular expressions. """
        return get_singleton_language_type(cls,backend,regex_str)
        
    def includes(self, right):
        """ Returns true iff this language includes the right language. """
        if not isinstance(right, Language):
            return False
        
        leftNFA  = regex.NFA.parse(regex.Pattern(self._regex).get_regex())
        rightNFA = regex.NFA.parse(regex.Pattern(right._regex).get_regex())
        return rightNFA.included_in(leftNFA)
    
    def is_subtype(self, candidate_subtype):
        return self.includes(candidate_subtype)

    #generate is implemented in the backend.
    def resolve_BinOp(self,context,node):
        right_type = node.right.unresolved_type.resolve(context)
        if not isinstance(right_type, Language):
            raise clq.TypeResolutionError("Must be a language",node)
        return Language.factory(self.backend, "(%s)(%s)" % (self._regex,right_type._regex))
        
    def get_coerced(self, supertype):
        if self == supertype:
            return self
        
        if(supertype.is_subtype(self)):
            new_type = Language.factory(self._backend, supertype._regex)
            return new_type
        else:
            return None