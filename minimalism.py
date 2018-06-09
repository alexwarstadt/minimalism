from typing import *

# for xml parsing of imported lexicon
import os
from xml.etree import ElementTree


class Feature(object):
    def __init__(self):
        pass

class Syn_Feature(Feature):
    def __init__(self):
        super(Syn_Feature, self).__init__()
        pass

class Sem_Feature(Feature):
    def __init__(self,label: str):
        super(Sem_Feature, self).__init__()
        self.label = label

class Cat_Feature(Syn_Feature):
    def __init__(self, label: str):
        super(Syn_Feature, self).__init__()
        pass

class Cat_Feature(Syn_Feature):
    def __init__(self, label):
        super(Cat_Feature, self).__init__()
        self.label = label
        
    def __str__(self):
        rep = self.label
        return rep

class Sel_Feature(Syn_Feature):
    def __init__(self, label: str):
        super(Sel_Feature, self).__init__()
        self.label = label
    
    def __str__(self):
        rep = "_" + self.label
        return rep

class Phon_Feature(Feature):
    def __init__(self, label: str):
        self.label = label

    def __str__(self):
        rep = self.value
        return rep

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
        self.syn: Set[Syn_Feature] = syn
        self.sem: Set[Sem_Feature] = sem
        self.phon: Set[Phon_Feature] = phon

    def __str__(self):
        syn_features = { str(f) for f in self.syn }
        phon_features = { str(f) for f in self.phon }
        rep = "( Syn: " + str(syn_features) + ", Phon: " + str(phon_features) + " )"
        return rep


class SyntacticObjectSet(SyntacticObject):
    def __init__(self, the_set: Set[SyntacticObject], idx: int):
        super(SyntacticObjectSet, self).__init__(idx)
        self.syntactic_object_set: Set[SyntacticObject] = the_set

    def __str__(self):
        set_strings = { str(obj)  for obj in self.syntactic_object_set }
        rep = "< " + str(self.idx) + ": " + str(set_strings) + " >"
        return str(rep)


class LexicalItemToken(SyntacticObject):
    """Alex: this annoys me. Why can't this just be a singleton set, and unify the two types of SOs?"""
    # todo: counter for initializing lexical item tokens
    def __init__(self, lexical_item: LexicalItem, idx: int):
        super(LexicalItemToken, self).__init__(idx)
        self.lexical_item = lexical_item
    
    def __str__(self):
        rep = "< " + str(self.idx) + ": " + str(self.lexical_item) + " >"
        return rep


class LexicalArray(object):
    def __init__(self, the_list):
        self.the_list: Set[LexicalItemToken] = the_list

    def __copy__(self):
        return LexicalArray(self.the_list)
    
    def __str__(self):
        set_strings = { str(token) for token in self.the_list }
        rep = "Lex Array: " + str(set_strings)
        return rep

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

    def __str__(self):
        if not self.w:
            return "Workspace: (empty)"
        else:
            set_strings = { str(obj) for obj in self.w }
            rep = "Workspace: " + str(set_strings)
            return rep

    """ TODO: add recursive find for internal merge """
    def find(self, idx: int):
        for syn_obj in self.w:
            found = syn_obj.find(idx)
            if found != None:
                return found
        raise Exception("There is no syntactic object with this index in the workspace.")

    def is_root(self, idx: int):
        results = [ x for x in self.w if x.idx == idx]
        if len(results) == 1:
            return True
        elif len(results) == 0:
            return False  
        else:
            raise Exception("There are multiple tree roots with the given index.")

    # Omar: this is new, uses indices to merge objects
    def merge(self, i: int, j: int):
        A = self.find(i)
        B = self.find(j)
        new_obj = A.merge(B,counter)
        new_set = self.w
        new_set.add(new_obj)
        new_set.remove(A)
        new_set.remove(B)
        return Workspace(new_set)



class Stage(object):
    def __init__(self, lexical_array: LexicalArray, w: Workspace):
        self.lexical_array = lexical_array
        self.workspace = w

    def is_root(self, idx: int):
        return self.workspace.is_root(idx)

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

    # Omar: Stage.merge() now calls Workspace.merge(),
    # I'm passing indices instead of objects to get around 
    # object equality testing bug
    def merge(self, i, j):
        old_workspace = self.workspace
        new_workspace = old_workspace.merge(i,j)
        new_stage = Stage(self.lexical_array.__copy__(), new_workspace)
        return new_stage

'''         Old version didn't work
    def merge(self, A, B):
        new_so = A.merge(B,counter)
        new_workspace = self.workspace.__copy__()
        new_workspace -= A
        new_workspace -= B
        new_workspace += new_so
        new_stage = Stage(self.lexical_array.__copy__(), new_workspace)
        return new_stage
'''


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
                if last_stage.is_root(index1) or last_stage.is_root(index2):
                    new_stage = last_stage.merge(index1, index2)
                    self.stages.append(new_stage)
                    break
                else:
                    print("One of the syntactic objects must be a root of some tree in the workspace")

                '''             This didn't work
                A = last_stage.workspace.find(index1)
                B = last_stage.workspace.find(index2)
                if last_stage.is_root(A) or last_stage.is_root(B):
                    new_stage = last_stage.merge(A, B)
                    self.stages.append(new_stage)
                    break
                '''
            elif instruction == "s":
                index = int(input("Enter the index of the token you would like to Select"))
                lexical_item_token = last_stage.lexical_array.find(index)
                new_stage = last_stage.select(lexical_item_token)
                self.stages.append(new_stage)
                break


# Global stuff

def first_stage(lexical_array):
    w_zero = Workspace(set())
    return Stage(lexical_array, w_zero)
    
    

counter = 100

# for xml parsing of imported lexicon


# for xml parsing of imported lexicon
# Chris: xml parsing done in the lexicon constructor

def main():
    # prints the phonological features of each member of the lexicon
    lexicon = Lexicon()
    print('The Lexicon:')
    for w in lexicon.lex:
        for f in w.phon:
            print(f.label)

'''
# main that runs Omar's new merge
def main():

    # Syntactic fragment
    ncat = Cat_Feature("N")
    nsel = Sel_Feature("N")
    k = Phon_Feature("K8")
    vcat = Cat_Feature("V")
    r = Phon_Feature("runs")
    e = Phon_Feature("eats")
    a = Phon_Feature("apples")
    kate = LexicalItem(set([ncat]), set(), set([k]))
    runs = LexicalItem(set([vcat, nsel]), set(), set([r]))
    eats = LexicalItem(set([vcat, nsel, nsel]), set(), set([e]))
    apples = LexicalItem(set([ncat]), set(), set([a]))
    kate1 = LexicalItemToken(kate, 1)
    runs2 = LexicalItemToken(runs, 2)
    eats3 = LexicalItemToken(eats, 3)
    apples4 = LexicalItemToken(apples, 4)

    # Intransitive verb merge test
    lexicon = Lexicon(set([kate, runs]))
    ug = UniversalGrammar(set([ncat, nsel, vcat]), set(), set([k, r]))
    i_lang = ILanguage(lexicon, ug)
    lex_array = LexicalArray([kate1, runs2])
    initial = first_stage(lex_array)
    derivation = Derivation([initial], i_lang)
    # testing merge
    # wksp = Workspace(set([kate_token, runs_token]))
    # print(wksp)
    # new_wksp = wksp.merge(1,2)
    # print(new_wksp)

    while (True):
        derivation.derive()

'''
    

main()