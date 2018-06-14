from typing import *
from .features import *
from .syntacticobjects import *
from .trees import tree


class UniversalGrammar(object):
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
    def __init__(self, lexicon, ug):
        self.lexicon = lexicon
        self.ug = ug

class LexicalArray(object):
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

    """ calls SyntacticObject.find() in module 'syntacticobjects.py' """
    def find_workspace(self, idx: int):
        for syn_obj in self.w:
            found = syn_obj.find(idx)
            if found != None:
                return found
        raise Exception("There is no syntactic object with this index in the workspace.")

    def is_root(self, idx: int):
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
    def __init__(self, lexical_array: LexicalArray, w: Workspace, counter):
        self.lexical_array = lexical_array
        self.workspace = w
        self.counter = counter


    def select_stage(self, a: LexicalItemToken):
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
        if i == j:
            raise MergeError("\nERROR: Self-Merge is undefined.\n")
        old_workspace = self.workspace
        new_workspace = old_workspace.merge_workspace(i, j, self.counter)
        self.counter += 1
        new_stage = Stage(self.lexical_array.__copy__(), new_workspace, self.counter)
        return new_stage


class Derivation(object):
    def __init__(self, i_lang: ILanguage, stages: List[Stage] = None, word_list: List[LexicalItem] = None):
        """
        To initialize from a pre-existing derivation pass in list of stages.
        To initialize a new derivation, pass in a lexical array.
        """
        self.i_lang = i_lang
        if stages is None:
            if word_list is None:
                raise Exception("You must pass in either a list of stages or a word list to initialize a derivation.")
            w_zero = Workspace(set())
            counter = 0
            lexical_array = []
            for w in word_list:
                assert w in i_lang.lexicon.lex
                lexical_array.append(LexicalItemToken(w, counter))
                counter += 1
            stage_zero = Stage(LexicalArray(lexical_array), w_zero, counter)
            self.stages = [stage_zero]
        else:
            assert word_list is None
            self.stages = stages


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
        while (True):
            self.print_derivation()
            instruction = input("Select (s) or Merge (m)? ")
            if instruction == "m":
                self.merge_step()
            elif instruction == "s":
                self.select_step()
            elif instruction == "debug":
                self.debug()
            elif instruction == "exit":
                break
            else:
                print("Please type either 's' for Select or 'm' for Merge".upper(), '\n')
                pass

    def merge_step(self):
        last_stage = self.stages[-1]
        index1 = int(input("Enter the index of the first syntactic object you would like to Merge: "))
        index2 = int(input("Enter the index of the second syntactic object you would like to Merge: "))
        if last_stage.workspace.is_root(index1) or last_stage.workspace.is_root(index2):
            try:
                new_stage = last_stage.merge_stage(index1, index2)
                self.stages.append(new_stage)
            except MergeError as inst:
                print(inst.message)
        else:
            print("One of the syntactic objects must be a root of some tree in the workspace")

    def select_step(self):
        last_stage = self.stages[-1]
        index = -1
        lexical_item_token = None
        while (lexical_item_token is None):
            index = int(input("Enter the index of the token you would like to Select: "))
            lexical_item_token = last_stage.lexical_array.find_lexical_array(index)
        new_stage = last_stage.select_stage(lexical_item_token)
        self.stages.append(new_stage)

    def print_derivation(self):
        last_stage = self.stages[-1]
        print(last_stage.lexical_array.__str__())
        print(last_stage.workspace.__str__(), '\n')
        tr_list = [tree(x) for x in last_stage.workspace.w]
        for tr in tr_list:
            tr.pretty_print()

    def debug(self):
        pass


class MergeError(Exception):
    def __init__(self, message):
        self.message = message

