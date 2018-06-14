from typing import *
from .features import *
from .syntactic_objects import *
from .trees import tree


class UniversalGrammar(object):
    """
    Definition 1: Universal Grammar is a 6-tuple: 〈PHON-F,SYN-F,SEM-F,Select,Merge,Transfer.
    Attributes: @syn_f, @sem_F, @phon_F
    """
    def __init__(self, syn_F, sem_F, phon_F):
        self.syn_F: Set[Syn_Feature] = syn_F
        self.sem_F: Set[Sem_Feature] = sem_F
        self.phon_F: Set[Phon_Feature] = phon_F

    def select(self):
        pass

    def merge(self):
        pass

    def transfer(self):
        pass


class ILanguage(object):
    """
    Definition 4: An I-language is a pair 〈Lex,UG〉 where Lex is a lexicon and UG is Universal Grammar    
    """
    def __init__(self, lexicon, ug):
        self.lexicon = lexicon
        self.ug = ug

class LexicalArray(object):
    """
    Definition 6: A lexical array (LA) is a finite set of lexical item tokens.
    """
    def __init__(self, the_list):
        self.the_list: Set[LexicalItemToken] = the_list

    def __copy__(self):
        return LexicalArray(self.the_list)

    def __str__(self):
        set_strings = {str(token) for token in self.the_list}
        rep = "Lex Array: \n" + "\n".join(set_strings)
        return rep

    def find_lexical_array(self, idx):
        s_objs_with_idx = [x for x in self.the_list if x.idx == idx]
        if len(s_objs_with_idx) == 1:
            return s_objs_with_idx[0]
        else:
            return None


class Workspace(object):
    def __init__(self, w: Set[SyntacticObject]):
        self.w = w

    def __sub__(self, other):
        new_set = set(self.w)
        new_set.remove(other)
        return Workspace(new_set)

    def __add__(self, other: SyntacticObject):
        new_set = set()
        if type(other) is SyntacticObjectSet:
            new_set = self.w.union(other.syntactic_object_set)
        if type(other) is LexicalItemToken:
            word_set = set([other])
            new_set = self.w.union(word_set)
        else:
            Exception("you added something that isn't a syntactic object to the workspace")
        return Workspace(new_set)

    def __copy__(self):
        return Workspace(set(self.w))

    def __str__(self):
        if not self.w:
            return "Workspace: (empty)"
        else:
            set_strings = {str(obj) for obj in self.w}
            rep = "Workspace: " + str(set_strings)
            return rep

    def find_workspace(self, idx: int):
        """ calls SyntacticObject.find() in module 'syntacticobjects.py' """
        for syn_obj in self.w:
            found = syn_obj.find(idx)
            if found is not None:
                return found
        raise InteractionError("There is no syntactic object with this index in the workspace.")


    def is_root(self, idx: int):
        """
        DEFINITION 11:
        For any syntactic object X and any stage S =〈LA,W〉with workspace W, 
        if X is in W, X isa root in W.
        """
        results = [x for x in self.w if x.idx == idx]
        if len(results) == 1:
            return True
        elif len(results) == 0:
            return False
        else:
            raise Exception("There are multiple tree roots with the given index.")

    # Omar: this is new, uses indices to merge objects
    def merge_workspace(self, i: int, j: int, idx):
        A = self.find_workspace(i)
        B = self.find_workspace(j)
        new_obj = A.merge(B, idx)
        new_set = self.w
        new_set.add(new_obj)
        if self.is_root(i):
            new_set.remove(A)
        if self.is_root(j):
            new_set.remove(B)
        return Workspace(new_set)


class Stage(object):
    """
    DEFINITION 10:
    A stage is a pair S = < LA,W >, where
        LA is a lexical array and 
        W is a set of syntactic objects. 
    We call W the workspace of S.
    """
    def __init__(self, lexical_array: LexicalArray, w: Workspace, counter):
        self.lexical_array = lexical_array
        self.workspace = w
        self.counter = counter


    def select_stage(self, a: LexicalItemToken):
        """
        DEFINITION 12:
        Let S be a stage in a derivation S = < LA,W >. 
        If lexical token A is in LA, then Select(A,S)  =  < LA - {A}, W ∪ {A} >
        :return: the stage resulting from Select(a,self)
        """
        if a not in self.lexical_array.the_list:
            raise Exception("The lexical array does not contain this lexical item.")
        else:
            new_LI_set = self.lexical_array.the_list.copy()
            new_LI_set.remove(a)
            new_LA = LexicalArray(new_LI_set)
            new_w = self.workspace.__copy__()
            new_w = new_w.__add__(a)
            new_stage = Stage(new_LA, new_w, self.counter)
            return new_stage

    # Omar: Stage.merge() now calls Workspace.merge(),
    # I'm passing indices instead of objects to get around
    # object equality testing bug
    def merge_stage(self, i, j):
        """
        DEFINITION 13:
        Given any two distinct syntactic objects A, B, Merge(A,B) = {A,B}.
        ( comment: for parallelism with Select, consider the following definition:
            Let S be a stage in a derivation S = < LA,W >. 
            If A and B are distinct syntactic objects s.t.
                a) A or B is a root in W
                b) if A or B is not a root in W, it is contained within a root in W
            Merge(A,B,S) = < LA, (W - (A∪B)) ∪ {A,B} > )
        :return: the stage resulting from Merge
        """
        if i == j:
            raise InteractionError("Self-Merge is undefined.")
        old_workspace = self.workspace
        new_workspace = old_workspace.merge_workspace(i, j, self.counter)
        self.counter += 1
        new_stage = Stage(self.lexical_array.__copy__(), new_workspace, self.counter)
        return new_stage





class InteractionError(Exception):
    """
    Raise whenever a user's input is uninterpretable or violates requirements from definitions
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "\nALERT: %s\n" % self.message
