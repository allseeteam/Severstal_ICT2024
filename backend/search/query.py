from ruwordnet import RuWordNet
from search import normalize_string
import pymorphy3
from functools import reduce
wn = RuWordNet()
morph = pymorphy3.MorphAnalyzer()


def enrich_word(word):
    return set([lexeme.word for lexeme in morph.parse(word)[0].lexeme])


def enrich_word_set(new_words_list):
    word_set = set()
    for new_word in new_words_list:
        new_word_set = set(normalize_string(new_word.title).split())
        word_set = word_set.union(new_word_set)
    return word_set


def enrich_query(query):
    query = normalize_string(query).split()
    senses = []
    for word in query:
        new_senses = wn.get_senses(word)
        for sense in new_senses:
            senses.append(sense)

    query_enrichment = set()

    for sense in senses:
        synset = sense.synset

        word_set = set(normalize_string(synset.title).split())
        query_enrichment = query_enrichment | word_set
        query_enrichment = query_enrichment | enrich_word_set(
            synset.pos_synonyms)
        query_enrichment = query_enrichment | enrich_word_set(synset.holonyms)
        query_enrichment = query_enrichment | enrich_word_set(synset.hypernyms)
    query = list(map(enrich_word, query_enrichment | set(query)))
    query = reduce(lambda a, b: a.union(b), query)
    return list(query)
