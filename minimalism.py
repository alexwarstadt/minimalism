from typing import *

# for xml parsing of imported lexicon
import os
from xml.etree import ElementTree

class UniversalGrammar(object):
    def __init__(self, syn_F, sem_F, phon_F):
        self.syn_F: Set[Feature] = syn_F
        self.sem_F: Set[Feature] = sem_F
        self.phon_F: Set[Phon_Feature] = phon_F

    def select(self):
        pass

    def merge(self):
        pass

    def transfer(self):
        pass


class Lexicon(object):
    def __init__(self):
        self.lex: Set[LexicalItem] = set()
        # get the file path to lexicon data
        file_name = "lexicon.xml"
        full_file = os.path.abspath(os.path.join("data", file_name))
        # create xml tree
        dom = ElementTree.parse(full_file)
        # extract data and create lexical items
        words = dom.findall('word')
        for w in words:
            # extract word data
            phon = w.find('phon').text
            cat = w.find('syn/cat').text
            sel = w.find('syn/sel').text
            sem = w.find('sem').text
            # create phon features
            phon = phon.strip()
            phon_list = phon.split()
            phon_set = set()
            for f in phon_list:
                new_feat = Phon_Feature(f)
                phon_set.add(new_feat)
            # create sem features
            sem = sem.strip()
            sem_list = sem.split()
            sem_set = set()
            for f in sem_list:
                new_feat = Sem_Feature(f)
                sem_set.add(new_feat)
            # create cat features
            cat = cat.strip()
            cat_list = cat.split()
            cat_set = set()
            for f in cat_list:
                new_feat = Cat_Feature(f)
                cat_set.add(new_feat)
            # create sel features
            sel = sel.strip()
            sel_list = sel.split()
            sel_set = set()
            for f in sel_list:
                new_feat = Sel_Feature(f)
                sel_set.add(new_feat)
            syn_set = set()
            syn_set.union(sel_set)
            syn_set.union(cat_set)
            new_word = LexicalItem(syn_set, sem_set, phon_set)
            self.lex.add(new_word)

class ILanguage(object):
    def __init__(self, lexicon, ug):
        self.lexicon = lexicon
        self.ug = ug

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

    def merge(self, a, counter: int):
        new_so = SyntacticObjectSet(set([self, a]), counter)
        counter += 1
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



class LexicalItem(object):
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
    def __init__(self, lexical_item, idx: int):
        super(LexicalItemToken, self).__init__(idx)
        self.lexical_item = lexical_item


class LexicalArray(object):
    def __init__(self, the_list):
        self.the_list: Set[LexicalItemToken] = the_list

    def __copy__(self):
        return LexicalArray(self.the_list)

    def find(self, idx):
        s_objs_with_idx = [x for x in self.the_list if x.idx == idx]
        if len(s_objs_with_idx) == 1:
            return s_objs_with_idx[0]
        else:
            raise Exception("The lexical array should contain exactly 1 element with the given index")



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

    def find(self, idx: int):
        for syn_obj in self.w:
            found = syn_obj.find(idx)
            if found != None:
                return found
        raise Exception("There is no syntactic object with this index in the workspace.")



class Stage(object):
    def __init__(self, lexical_array: LexicalArray, w: Workspace):
        self.lexical_array = lexical_array
        self.workspace = w

    def is_root(self, x: SyntacticObject):
        return x in self.workspace.w

    def select(self, a: LexicalItemToken):
        if a not in self.lexical_array.the_list:
            raise Exception("The lexical array does not contain this lexical item.")
        else:
            new_LI_set = self.lexical_array.the_list.copy()
            new_LI_set.remove(a)
            new_LA = LexicalArray(new_LI_set)
            new_w = self.workspace.__copy__()
            new_w = new_w.__add__(a)
            new_stage = Stage(self.lexical_array, new_w)
            return new_stage

    def merge(self, A, B):
        new_so = A.merge(B,counter)
        new_workspace = self.workspace.__copy__()
        new_workspace -= A
        new_workspace -= B
        new_workspace += new_so
        new_stage = Stage(self.lexical_array.__copy__(), new_workspace)
        return new_stage


class Derivation(object):
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
        print(last_stage.lexical_array.__str__())
        print(last_stage.workspace.__str__())
        while(True):
            instruction = input("Select (s) or Merge (m)? ")
            if instruction == "m":
                index1 = int(input("Enter the index of the first syntactic object you would like to Merge"))
                index2 = int(input("Enter the index of the second syntactic object you would like to Merge"))
                A = last_stage.workspace.find(index1)
                B = last_stage.workspace.find(index2)
                if last_stage.is_root(A) or last_stage.is_root(B):
                    new_stage = last_stage.merge(A, B)
                    self.stages.append(new_stage)
                    break
                else:
                    print("One of the syntactic objects must be a root of some tree in the workspace")
            elif instruction == "s":
                index = int(input("Enter the index of the token you would like to Select"))
                lexical_item_token = last_stage.lexical_array.find(index)
                new_stage = last_stage.select(lexical_item_token)
                self.stages.append(new_stage)
                break


def first_stage(lexical_array):
    w_zero = Workspace(set())
    return Stage(lexical_array, w_zero)
    
    

counter = 100



class Feature(object):
    def __init__(self):
        pass
    """what are these?"""

class Syn_Feature(Feature):
    def __init__(self):
        super(Syn_Feature, self).__init__()
        pass

class Cat_Feature(Syn_Feature):
    def __init__(self, label):
        super(Cat_Feature, self).__init__()
        self.label = label

class Sel_Feature(Syn_Feature):
    def __init__(self, label):
        super(Sel_Feature, self).__init__()
        self.label = label

class Phon_Feature(Feature):
    def __init__(self, label):
        self.label = label

class Sem_Feature(Feature):
    def __init__(self, label):
        super(Feature, self).__init__()
        self.label = label

def main():
    '''
    nouncat = Cat_Feature("N")
    nounsel = Sel_Feature("N")
    k = Phon_Feature("K8")
    verbcat = Cat_Feature("V")
    r = Phon_Feature("runs")
    kate = LexicalItem(set([nouncat]), set(), set([k]))
    runs = LexicalItem(set([verbcat, nounsel]), set(), set([r]))
    kate_token = LexicalItemToken(kate, 1)
    runs_token = LexicalItemToken(runs, 2)
    
    lexicon = Lexicon(set([kate, runs]))
    ug = UniversalGrammar(set([nouncat, nounsel, verbcat]), set(), set([k, r]))
    i_lang = ILanguage(lexicon, ug)
    lex_array = LexicalArray([kate_token, runs_token])
    derivation = Derivation([first_stage(lex_array)], i_lang)

    while (True):
        derivation.derive()
    '''

    lexicon = Lexicon()
    print('The Lexicon:')
    for w in lexicon.lex:
        for f in w.phon:
            print(f.label)
    
    
    
    

main()
