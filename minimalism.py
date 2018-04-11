from typing import *

class UniversalGrammar:
    def __init__(self):
        phon_F: Set[Phon_Feature]
        syn_F: Set[Feature]
        sem_F: Set[Feature]

    def select(self):
        pass

    def merge(self):
        pass

    def transfer(self):
        pass


class Lexicon:
    def __init__(self):
        lex: Set[LexicalItem]

class ILanguage:
    def __init__(self, lexicon, ug):
        self.lexicon = lexicon
        self.ug = ug

class SyntacticObject:
    """Abstract class, never instantiated. Has two subtypes, base case, recursive case"""
    def __init__(self, idx: int):
        self.idx = idx

    def i_contains(self, a):
        """self immediately contains a if a is an element of self"""
        if self is SyntacticObjectSet:
            return a in self.syntactic_object_set
        else:
            return False

    def contains(self, a):
        """self contains a if self immediately contains a, or some daughter of self contains a"""
        if self is SyntacticObjectSet:
            if self.i_contains(a):
                return True
            else:
                to_return = False
                for daughter in a.syntactic_object_set:
                    to_return = to_return or daughter.contains(a)
                return to_return
        else:
            return False

    def merge(self, a, counter: int):
        new_so = SyntacticObjectSet(set(self, a), counter)
        return new_so


class LexicalItem:
    def __init__(self, syn, sem, phon):
        self.syn: Set[Feature] = syn
        self.sem: Set[Feature] = sem
        self.phon: List[Set[Feature]] = phon


class SyntacticObjectSet(SyntacticObject):
    def __init__(self, the_set, idx):
        super(SyntacticObjectSet, self).__init__(idx)
        self.syntactic_object_set: Set[SyntacticObject] = the_set


class LexicalItemToken(SyntacticObject):
    """Alex: this annoys me. Why can't this just be a singleton set, and unify the two types of SOs?"""
    # todo: counter for initializing lexical item tokens
    def __init__(self, lexical_item, idx):
        super(LexicalItemToken).__init__(idx)
        self.lexical_item = lexical_item


class LexicalArray:
    def __init__(self, the_list):
        self.the_list: Set[LexicalItemToken] = the_list

    def __copy__(self):
        return LexicalArray(self.the_list)


class Workspace:
    def __init__(self, w: Set[SyntacticObject]):
        self.w = w

    def __sub__(self, other):
        new_set = set(self.w)
        new_set.remove(other)
        return Workspace(new_set)

    def __add__(self, other):
        new_set = set(self.w)
        new_set.add(other)
        return Workspace(new_set)

    def __copy__(self):
        return Workspace(set(self.w))


class Stage:
    def __init__(self, lexical_array: LexicalArray, w: Workspace):
        self.lexical_array = lexical_array
        self.w = w

    def is_root(self, x: SyntacticObject):
        return x in self.w

    def select(self, a: LexicalItemToken):
        if a not in self.lexical_array:
            raise Exception("The lexical array does not contain this lexical item.")
        else:
            new_LI_set = self.lexical_array.the_list.copy()
            new_LI_set.remove(a)
            new_LA = LexicalArray(new_LI_set)
            new_w = self.w.syntactic_object_set.copy()
            new_w = new_w.union(set(a))
            new_stage = Stage(self.lexical_array, new_w)
            return new_stage

    def merge(self, A, B):
        new_so = A.merge(B)
        new_workspace = self.w.__copy__()
        new_workspace -= A
        new_workspace -= B
        new_workspace += new_so
        new_stage = Stage(self.lexical_array.__copy__(), new_workspace)
        return new_stage


class Derivation:
    def __init__(self, stages: List[Stage], i_lang: ILanguage):
        self.stages = stages
        self.i_lang = i_lang


    # def verify(self):
        # todo: finish from definition 14 in C&S
        # for lex_tok in self.stages[0].lexical_array.the_list:
        #     if lex_tok not in self.i_lang.lexicon:
        #         raise Exception(str(lex_tok) + ":  this word is not in the lexicon.")
        # if (len(self.stages[0].w.syntactic_object_set) != 0):
        #     raise Exception("The initial workspace is not empty.")
        # consider whether verifying constraints on valid derivations in necessary

    def derive(self):
        """side effects only. Modifies self.stages"""
        last_stage = self.stages[-1]
        print(last_stage.lexical_array)
        print(last_stage.w)
        while(True):
            instruction = input("Select (s) or Merge (m)? ")
            if instruction == "m":
                index1 = int(input("Enter the index of the first syntactic object you would like to Merge"))
                index2 = int(input("Enter the index of the second syntactic object you would like to Merge"))
                A = last_stage.w.find(index1)
                B = last_stage.w.find(index2)
                new_stage = last_stage.merge(A, B)
                self.stages.append(new_stage)
                break
            if instruction == "s":
                index = int(input("Enter the index of the token you would like to Select"))
                lexical_item_token = last_stage.lexical_array.find(index)
                new_stage = last_stage.select(lexical_item_token)
                self.stages.append(new_stage)
                break




        



class Feature:
    """what are these?"""

class Phon_Feature(Feature):
    def __init__(self, feature_name, value):
        self.feature_name = feature_name
        self.value = value
