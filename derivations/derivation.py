from typing import *
from structures import *


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
        """
        Contains main loop, prompts user for actions
        side effects only: adds to self.stages for each successful action
        """
        while (True):
            self.print_derivation()
            instruction = input("Select (s) or Merge (m)? ")
            try:
                if instruction == "m":
                    self.merge_step()
                elif instruction == "s":
                    self.select_step()
                elif instruction == "debug":
                    self.debug()
                elif instruction == "exit":
                    break
                else:
                    raise InteractionError("Please type either 's' for Select or 'm' for Merge")
            except InteractionError as interaction_error:
                print(interaction_error)

    def merge_step(self):
        last_stage = self.stages[-1]
        try:
            index1 = int(input("Enter the index of the first syntactic object you would like to Merge: "))
            index2 = int(input("Enter the index of the second syntactic object you would like to Merge: "))
        except ValueError:
            raise InteractionError("Merge requires an index (an integer).")
        if last_stage.workspace.is_root(index1) or last_stage.workspace.is_root(index2):
            new_stage = last_stage.merge_stage(index1, index2)
            self.stages.append(new_stage)
        else:
            raise InteractionError("Merge(A,B) requires either A or B to be a root.")

    def select_step(self):
        last_stage = self.stages[-1]
        try:
            index = int(input("Enter the index of the token you would like to Select: "))
            lexical_item_token = last_stage.lexical_array.find_lexical_array(index)
            if lexical_item_token is None:
                raise InteractionError("There is no lexical item in the lexical array th that index.")
            new_stage = last_stage.select_stage(lexical_item_token)
            self.stages.append(new_stage)
        except ValueError:
            raise InteractionError("Select requires an index (an integer).")


    def print_derivation(self):
        last_stage = self.stages[-1]
        print(last_stage.lexical_array.__str__())
        print(last_stage.workspace.__str__(), '\n')
        tr_list = [tree(x) for x in last_stage.workspace.w]
        for tr in tr_list:
            tr.pretty_print()

    def debug(self):
        pass