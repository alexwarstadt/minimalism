from typing import *

class Feature(object):
    def __init__(self):
        pass


class Syn_Feature(Feature):
    def __init__(self):
        super(Syn_Feature, self).__init__()
        pass


class Sem_Feature(Feature):
    def __init__(self, label: str):
        super(Sem_Feature, self).__init__()
        self.label = label


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
        rep = self.label
        return rep
