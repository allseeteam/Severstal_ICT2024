from extract import *  # noqa
from search.text import normalize_string
from search.rank import calc_factors, factors_to_list, rank
from search.entity import normalize_entity
from collections import defaultdict
from math import log


class SearchEngine:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self._index: dict[str, dict[str, int]] = defaultdict(self.default_dict)
        self._documents: dict[str, str] = {}
        self.k1 = k1
        self.b = b

    def default_dict(self):
        return defaultdict(int)

    @staticmethod
    def update_url_scores(old: dict[str, float], new: dict[str, float]):
        for url, score in new.items():
            if url in old:
                old[url] += score
            else:
                old[url] = score
        return old

    @property
    def posts(self) -> list[str]:
        return list(self._documents.keys())

    @property
    def number_of_documents(self) -> int:
        return len(self._documents)

    @property
    def avdl(self) -> float:
        # todo: refactor this. it can be slow to compute it every time. compute it once and cache it
        return sum(len(d) for d in self._documents.values()) / len(self._documents)

    def get_candidates(self, words: list[str]):
        candidates = set()
        for word in words:
            new_candi = set(self.get_urls(word).keys())
            candidates = candidates.union(new_candi)
        return candidates

    def idf(self, kw: str) -> float:
        N = self.number_of_documents
        n_kw = len(self.get_urls(kw))
        return log((N - n_kw + 0.5) / (n_kw + 0.5) + 1)

    def bm25(self, kw: str) -> dict[str, float]:
        result = {}
        idf_score = self.idf(kw)
        avdl = self.avdl
        for url, freq in self.get_urls(kw).items():
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (
                1 - self.b + self.b * len(self._documents[url]) / avdl
            )
            result[url] = idf_score * numerator / denominator
        return result

    def calc_bm25_factor(self, words, entity):
        url_scores: dict[str, float] = {}
        for kw in words:
            kw_urls_score = self.bm25(kw)
            url_scores = self.update_url_scores(url_scores, kw_urls_score)

    def smart_search(self, query, page=1, page_size=10):
        keywords = normalize_string(query).split()
        candidates = self.get_candidates(keywords)
        candidates_to_rank = []
        for candidate in candidates:
            doc = self._documents[candidate]
            factors = calc_factors(keywords, doc)
            factors = factors_to_list(query, candidate, factors)
            candidates_to_rank.append(factors)

        ranked_candidates = rank(candidates_to_rank)
        ranked_candidates = ranked_candidates[(
            (page - 1) * page_size):page * page_size]
        return ranked_candidates

    def search(self, query: str, page=1, page_size=10) -> dict[str, float]:
        keywords = normalize_string(query).split()
        url_scores: dict[str, float] = {}
        for kw in keywords:
            kw_urls_score = self.bm25(kw)
            url_scores = self.update_url_scores(url_scores, kw_urls_score)

        url_scores = sorted(url_scores.items(),
                            key=lambda x: x[1], reverse=True)
        url_scores = url_scores[((page - 1) * page_size):page * page_size]
        return url_scores

    def index(self, url: str, content: str, entity) -> None:
        self._documents[url] = entity
        words = content.split()
        for word in words:
            self._index[word][url] += 1

    def index_entity(self, entity):
        entity_id = get_entity_id(entity)
        search_content = normalize_entity(entity)
        self.index(entity_id, search_content, entity)

    def bulk_index_entities(self, entities: list[dict]):
        for entity in entities:
            self.index_entity(entity)

    def get_urls(self, keyword: str) -> dict[str, int]:
        keyword = normalize_string(keyword)
        return self._index[keyword]
