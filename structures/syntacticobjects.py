from typing import *

class SyntacticObject(object):
    """Abstract class, never instantiated. Has two subtypes, base case, recursive case"""

    def __init__(self, idx: int):
        self.idx = idx


    def i_contains(self, a):
        """self immediately contains a if a is an element of self"""
        if type(self) is SyntacticObjectSet:
            return a in self.syntactic_object_set
        else:
            return False

    def contains(self, a):
        """self contains a if self immediately contains a, or some daughter of self contains a"""
        if type(self) is SyntacticObjectSet:
            if self.i_contains(a):
                return True
            else:
                to_return = False
                for daughter in a.syntactic_object_set:
                    to_return = to_return or daughter.contains(a)
                return to_return
        else:
            return False

    def merge(self, a, idx: int):
        new_so = SyntacticObjectSet(set([self, a]), idx)
        return new_so

    def find(self, idx: int):
        if self.idx == idx:
            return self
        else:
            if type(self) is LexicalItemToken:
                return None
            elif type(self) is SyntacticObjectSet:
                for syn_obj in self.syntactic_object_set:
                    found = syn_obj.find(idx)
                    if found != None:
                        return found
                return None

    def paths(self, so):
        """ returns all paths to self starting at so """
        if so == self:
            return [self]
        else:
            if type(so) is LexicalItemToken:
                return []
            elif type(so) is SyntacticObjectSet:
                return set([self.paths(x).append(x) for x in so.syntactic_object_set])





class LexicalItem(object):
    def __init__(self, syn, sem, phon):
        self.syn: Set[Syn_Feature] = syn
        self.sem: Set[Sem_Feature] = sem
        self.phon: Set[Phon_Feature] = phon

    def __str__(self):
        syn_features = {str(f) for f in self.syn}
        phon_features = {str(f) for f in self.phon}
        rep = "( Syn: " + str(syn_features) + ", Phon: " + str(phon_features) + " )"
        return rep


class SyntacticObjectSet(SyntacticObject):
    def __init__(self, the_set: Set[SyntacticObject], idx: int):
        super(SyntacticObjectSet, self).__init__(idx)
        self.syntactic_object_set: Set[SyntacticObject] = the_set

    def __str__(self):
        set_strings = {str(obj) for obj in self.syntactic_object_set}
        rep = "< " + str(self.idx) + ": " + ", ".join(set_strings) + " >"
        return rep


class LexicalItemToken(SyntacticObject):

    def __init__(self, lexical_item: LexicalItem, idx: int):
        super(LexicalItemToken, self).__init__(idx)
        self.lexical_item = lexical_item

    def __str__(self):
        rep = "< " + str(self.idx) + ": " + str(self.lexical_item) + " >"
        return rep