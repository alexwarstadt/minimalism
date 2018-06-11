from derivations import *
from structures import *

def main():
    lexicon = Lexicon()
    counter = 0
    ug = UniversalGrammar(set(), set(), set()) # todo: add feature import to UG
    i_lang = ILanguage(lexicon, ug)
    derivation = Derivation(i_lang, word_list=list(i_lang.lexicon.lex))
    derivation.derive()


    # kate_token1 = LexicalItemToken(list(lexicon.lex)[0], 0)
    # kate_token2 = LexicalItemToken(list(lexicon.lex)[0], 1)
    # kate_runs = kate_token1.merge(kate_token2, 2)
    # tr = tree(kate_runs)
    # tr.pretty_print()


main()