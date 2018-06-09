from derivations import *
from structures import *

def main():
    lexicon = Lexicon()
    counter = 0
    # word_list = lexicon.lex
    # for w in lexicon.lex:
    #     word_list.ap
    # lex_array = LexicalArray(lex_array_list)
    ug = UniversalGrammar(set(), set(), set()) # todo: add feature import to UG
    i_lang = ILanguage(lexicon, ug)
    derivation = Derivation(i_lang, word_list=list(i_lang.lexicon.lex))
    derivation.derive()

main()