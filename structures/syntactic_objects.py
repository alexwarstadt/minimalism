from typing import *
from .features import *

class SyntacticObject(object):
    """
    Defintion 7: X i sa syntactic object iff
        (i) X is a lexical item token, or 
        (ii) X is a set of syntactic objects.
    Abstract class, never instantiated. 
    Has two subclasses, base case (i), recursive case (ii)
    """

    def __init__(self, idx: int):
        self.idx = idx


    def immediately_contains(self, a):
        """
        DEFINITION 8: Let A and B be syntactic objects, then B immediately contains A iff A 2 B.
        """
        if type(self) is SyntacticObjectSet:
            return a in self.syntactic_object_set
        else:
            return False

    def contains(self, a):
        """
        DEFINITION 9: Let A and B be syntactic objects, then B contains A iff
            (i) B immediately contains A, or 
            (ii) for some syntactic object C, B immediately contains C and C contains A.
            
        Returns True if self contains a, False otherwise
        """
        if type(self) is SyntacticObjectSet:
            if self.immediately_contains(a):
                return True
            else:
                to_return = False
                for daughter in self.syntactic_object_set:
                    if type(daughter) is SyntacticObjectSet:
                        to_return = to_return or daughter.contains(a)
                return to_return
        else:
            return False

    def merge(self, a, idx: int):
        """:return: a syntactic object with the index idx, containing self and a"""
        new_so = SyntacticObjectSet(set([self, a]), idx)
        return new_so


    def find(self, idx: int):
        """:return: the syntactic object within self at idx, or else None """
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
        """
        DEFINITION 16:
        The position of SO_n in SO_1 is a path, 
        a sequence of syntactic objects < SO_1,SO_2,...,SO_n > where for all 0 < i < n, SO_{i+1} is in SO_i.
        :return: all paths to self starting at so 
        """
        if so == self:
            return [self]
        else:
            if type(so) is LexicalItemToken:
                return []
            elif type(so) is SyntacticObjectSet:
                return set([self.paths(x).append(x) for x in so.syntactic_object_set])





class LexicalItem(object):
    """
    DEFINITION 2:
    A lexical item is a triple: LI = < SEM,SYN,PHON >
    where SEM and SYN are finite sets such that SEM ⊆ SEM-F, SYN ⊆ SYN-F, and PHON 2 PHON-F*
    """
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
    """See DEFINTION 7 (ii)"""
    def __init__(self, the_set: Set[SyntacticObject], idx: int):
        super(SyntacticObjectSet, self).__init__(idx)
        self.syntactic_object_set: Set[SyntacticObject] = the_set

    def __str__(self):
        set_strings = {str(obj) for obj in self.syntactic_object_set}
        rep = "< " + str(self.idx) + ": " + ", ".join(set_strings) + " >"
        return rep


class LexicalItemToken(SyntacticObject):
    """
    Definition 5: A lexical item token is a pair 〈LI,k〉 where LI is a lexical item and k is an integer.
    """
    def __init__(self, lexical_item: LexicalItem, idx: int):
        super(LexicalItemToken, self).__init__(idx)
        self.lexical_item = lexical_item

    def __str__(self):
        rep = "< " + str(self.idx) + ": " + str(self.lexical_item) + " >"
        return rep