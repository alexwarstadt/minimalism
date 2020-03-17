from typing import *
from .features import *
from .errors import *

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


    def category(self):
        if type(self) is LexicalItemToken:
            result = [ f for f in self.lexical_item.syn if type(f) is Cat_Feature ]
            assert len(result) == 1
        elif type(self) is SyntacticObjectSet:
            result = None
        return result

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

    # def merge(self, a, idx: int):
        """:return: a syntactic object with the index idx, containing self and a"""
    #     new_so = SyntacticObjectSet(set([self, a]), set(), None, idx)
    #     return new_so

    def merge(self, a, idx: int):
        """ new merge, works with trigger features 
        :param: takes two syntactic objects and an index
        :return: a syntactic object with the index idx, containing self and a"""
        if self.triggers == set():
            raise InteractionError("First argument of merge has no trigger features.")
        elif a.triggers != set():
            raise InteractionError("Second argument of merge has illicit trigger features.")
        else:
            matching_triggers = [ f for f in self.triggers if f.label == a.category.label ]
            if matching_triggers == []:
                raise InteractionError("The trigger feature of the head does not match the category of the complement.")
            trigger = matching_triggers[0]
            new_triggers = { f for f in self.triggers if f != trigger }
            new_so = SyntacticObjectSet(set([self, a]), new_triggers, self.category, idx)
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
        def path_finder(self, other, current_path, paths):
            """Helper Function"""
            if type(other) is SyntacticObjectSet:
                for x in other.syntactic_object_set:
                    if x is self:
                        new_path = current_path.copy() + [x]
                        paths.add(tuple(new_path)) # Crucial: Use "add" for a new path, if it's only one.

                    elif type(x) is SyntacticObjectSet:
                        if x.contains(self):
                            new_path = current_path.copy() + [x]
                            paths.union(path_finder(self, x, new_path, paths))
                        
            return paths
        
        if type(so) is SyntacticObjectSet:
            if so.contains(self) is True:
                startpath = [so]
                initialset = set()
                return path_finder(self, so, startpath, initialset)
        elif so is self:
            return {self}
        else: return {}

    def c_commands(self, other, in_sos):
        """
        DEFINITION 21:
        Let A and B be syntactic objects, then A c-commands B in D, iff there is
        a syntactic object C, such that:
            i) C is a sister of A in D, and
            ii) either B == C, or C contains B
        """
        
        def sister_finder(self, container, sisterset = set()):
            for daughter in container.syntactic_object_set:
                if daughter.idx == self.idx:
                    newsister = container.syntactic_object_set - {daughter}
                    sisterset.add(newsister.pop())
                else:
                    if type(daughter) is SyntacticObjectSet:
                        if daughter.contains(self):
                            sisterset.union(sister_finder(self, daughter, sisterset))
            return sisterset
                        
            
        if in_sos.contains(self) and in_sos.contains(other):
            sisterset = sister_finder(self, in_sos)
            to_return = False
#            print(sisterset) # debug
            for sister in sisterset:
                if sister.contains(other) or sister.idx == other.idx:
                    to_return = True
            return to_return
        else:
            return False
        
    def asymmetric_c_command(self, other, in_sos):
        """
        DEFINITION 21
        A asymmetrically c-commands B in C, if A c-commands B in C, and A and B are not sisters
        """
        def sister_finder(self, container, sisterset = set()):
            for daughter in container.syntactic_object_set:
                if daughter.idx == self.idx:
                    newsister = container.syntactic_object_set - {daughter}
                    sisterset.add(newsister.pop())
                else:
                    if type(daughter) is SyntacticObjectSet:
                        if daughter.contains(self):
                            sisterset.union(sister_finder(self, daughter, sisterset))
            return sisterset
                        
            
        if in_sos.contains(self) and in_sos.contains(other):
            sisterset = sister_finder(self, in_sos)
            to_return = False
            if not other in sisterset:
                for sister in sisterset:
                    if sister.contains(other) or sister.idx == other.idx:
                        to_return = True
            return to_return
        else:
            return False

    def is_derivable(self, lexicon): # Not implemented
        """
        DEFINITION 15:
        A syntactic object A is derivable from lexicon L iff there is a derivation
        〈〈LA_1,W_1〉,. . .,〈LA_n,W_n〉〉, where LA_n = {} and W_n = {A}.

        :param L:
        :return: True/False
        """

        pass

    def does_occur(self, so): # Not implemented
        """
        DEFINITION 17:
        B occurs in A at position P iff P = 〈A,. . .,B〉. We also say B has an occurrence in A at position P (written B_P).

        :param so:
        :return: True/False
        """
        pass

    def occurrence(self, so): # Not done
        """
        DEFINITION 17:
        B occurs in A at position P iff P = 〈A,. . .,B〉. We also say B has an occurrence in A at position P (written B_P).

        :param so:
        :return: Path/Position B_P
        """
        pass
        # Should check if does_occur is true, and if so, return the path.

    def are_sisters(self, soA, soB):
        """
        Let A, B, C be syntactic objects (where A != B), then A and B are sisters in C iff A, B are in C.
        :param A:
        :param B:
        :return:
        """
        if soA == soB:
            raise Exception("An object cannot be its own sister.")
        if self.immediately_contains(soA) and self.immediately_contains(soB):
            return True
        else:
            return False

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
        syn_features = [str(f) for f in self.syn]
        phon_features = {str(f) for f in self.phon}
        rep = "( Syn: " + str(syn_features) + ", Phon: " + str(phon_features) + " )"
        return rep


class SyntacticObjectSet(SyntacticObject):
    """See DEFINTION 7 (ii)"""
    def __init__(self, the_set: Set[SyntacticObject], triggers, category, idx: int):
        super(SyntacticObjectSet, self).__init__(idx)
        self.syntactic_object_set: Set[SyntacticObject] = the_set
        # can edit this inside merge, or add it to init, either way
        self.triggers = triggers
        self.category = category

    def __str__(self):
        set_strings = {str(obj) for obj in self.syntactic_object_set}
        rep = "< " + str(self.idx) + "," + str(self.category) + "," + str([str(t) for t in self.triggers]) + ": " + ", ".join(set_strings) + " >"
        return rep


class LexicalItemToken(SyntacticObject):
    """
    Definition 5: A lexical item token is a pair 〈LI,k〉 where LI is a lexical item and k is an integer.
    """
    def __init__(self, lexical_item: LexicalItem, idx: int):
        super(LexicalItemToken, self).__init__(idx)
        self.lexical_item = lexical_item
        self.triggers = { f for f in self.lexical_item.syn if type(f) is Trigger_Feature }
        cat_features = { f for f in self.lexical_item.syn if type(f) is Cat_Feature }
        assert len(cat_features) == 1
        (category, ) = cat_features
        self.category = category

    def __str__(self):
        rep = "< " + str(self.idx) + "," + str(self.category) + ": " + str(self.lexical_item) + " >"
        return rep