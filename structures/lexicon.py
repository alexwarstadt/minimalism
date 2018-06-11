from typing import *
from .definitions import LexicalItem
from .features import *

# for xml parsing of imported lexicon
import os
from xml.etree import ElementTree


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
            syn_set = syn_set.union(sel_set)
            syn_set = syn_set.union(cat_set)
            new_word = LexicalItem(syn_set, sem_set, phon_set)
            self.lex.add(new_word)
