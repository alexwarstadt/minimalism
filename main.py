from derivations import *
from structures import *

def main():
    lexicon = Lexicon()
    counter = 0
    lex_array_list = []
    for w in lexicon.lex:
        new_token = LexicalItemToken(w, counter)
        lex_array_list.append(new_token)
        counter += 1
    lex_array = LexicalArray(lex_array_list)
    ug = UniversalGrammar(set(), set(), set()) # todo: add feature import to UG
    i_lang = ILanguage(lexicon, ug)
    derivation = Derivation(i_lang, lex_array=lex_array)
    derivation.derive()






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