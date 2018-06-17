import structures as s
from nltk.tree import Tree

from typing import *

def tree(so):
    tr = None
    if type(so) is s.definitions.LexicalItemToken:
        li = so.lexical_item
        cat = [ x for x in li.syn if type(x) is s.features.Cat_Feature ]
        assert len(cat) == 1

        ph = [ y for y in li.phon if type(y) is s.features.Phon_Feature ]
        assert len(ph) == 1
        cat_label = cat[0].label
        ph_label = ph[0].label
        tr = Tree(cat_label + "," + str(so.idx), [ph_label])
    elif type (so) is s.definitions.SyntacticObjectSet:
        cat_label = so.category.label
        obj_set = so.syntactic_object_set
        tr = Tree(str(so.idx) + "," + cat_label, [ tree(x) for x in obj_set ])
    return tr

