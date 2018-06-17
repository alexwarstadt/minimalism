from typing import *
from .definitions import LexicalItem
from .features import *

# for xml parsing of imported lexicon
import os
from xml.etree import ElementTree


class Lexicon(object):
    """
    Definition 3: A lexicon is a finite set of lexical items.
    """
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
            phon_set = set([Phon_Feature(f) for f in w.find('phon').text.strip().split()])
            sem_set = set([Sem_Feature(f) for f in w.find('sem').text.strip().split()])
            sel_features = w.findall('syn/sel')
            if sel_features != None:
                sel_set = {Trigger_Feature(f.text.strip()) for f in sel_features}
            else:
                sel_set = set()
            cat_set = set([Cat_Feature(f) for f in w.find('syn/cat').text.strip().split()])
            syn_set = sel_set.union(cat_set)
            new_word = LexicalItem(syn_set, sem_set, phon_set)
            self.lex.add(new_word)
