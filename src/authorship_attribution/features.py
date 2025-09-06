from __future__ import annotations
import numpy as np
import re
from typing import List, Tuple
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# Simple tokenization
_word_re = re.compile(r"[A-Za-z']+")

FUNCTION_WORDS = [
    # Common English function words (subset)
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "if",
    "then",
    "else",
    "when",
    "while",
    "because",
    "so",
    "as",
    "than",
    "that",
    "which",
    "who",
    "whom",
    "whose",
    "this",
    "these",
    "those",
    "there",
    "here",
    "where",
    "why",
    "how",
    "what",
    "such",
    "many",
    "much",
    "few",
    "more",
    "most",
    "less",
    "least",
    "i",
    "you",
    "he",
    "she",
    "it",
    "we",
    "they",
    "me",
    "him",
    "her",
    "us",
    "them",
    "my",
    "your",
    "his",
    "its",
    "our",
    "their",
    "mine",
    "yours",
    "hers",
    "ours",
    "theirs",
    "myself",
    "yourself",
    "himself",
    "herself",
    "itself",
    "ourselves",
    "themselves",
    "is",
    "am",
    "are",
    "was",
    "were",
    "be",
    "being",
    "been",
    "do",
    "does",
    "did",
    "doing",
    "have",
    "has",
    "had",
    "having",
    "will",
    "would",
    "shall",
    "should",
    "can",
    "could",
    "may",
    "might",
    "must",
    "ought",
    "of",
    "to",
    "in",
    "on",
    "at",
    "by",
    "for",
    "from",
    "with",
    "about",
    "into",
    "over",
    "after",
    "before",
    "between",
    "through",
    "up",
    "down",
    "out",
    "off",
    "above",
    "below",
    "under",
    "again",
    "further",
    "once",
    "not",
    "no",
    "nor",
    "only",
    "just",
    "also",
    "too",
    "very",
    "ever",
    "never",
    "always",
    "often",
    "sometimes",
    "usually",
    "rarely",
    "seldom",
    "than",
    "rather",
    "quite",
    "almost",
    "nearly",
    "already",
    "yet",
    "still",
]


def simple_tokenize(text: str, lowercase: bool = True) -> List[str]:
    t = text.lower() if lowercase else text
    return _word_re.findall(t)


@dataclass
class FeatureExtractor:
    char_ngram_range: Tuple[int, int] = (3, 5)
    max_char_features: int = 50000
    svd_dim: int = 256
    text_lowercase: bool = True
    use_function_words: bool = True
    random_state: int = 42

    def __post_init__(self):
        self.char_vec = TfidfVectorizer(
            analyzer="char",
            ngram_range=self.char_ngram_range,
            lowercase=self.text_lowercase,
            min_df=2,
            max_features=self.max_char_features,
            sublinear_tf=True,
            dtype=np.float32,  # pyright: ignore[reportArgumentType]
        )
        self.svd = TruncatedSVD(
            n_components=self.svd_dim,
            random_state=self.random_state,
            algorithm="randomized",
        )
        self._fw_mean = None
        self._fw_std = None

    def fit(self, texts: List[str]):
        X_char = self.char_vec.fit_transform(texts)
        X_svd = self.svd.fit_transform(X_char)
        _ = X_svd

        if self.use_function_words:
            fw = self._function_word_features_batch(texts)
            # standardize
            self._fw_mean = fw.mean(axis=0, keepdims=True)
            self._fw_std = fw.std(axis=0, keepdims=True) + 1e-6  # avoid div by zero

        return self

    def transform(self, texts: List[str]) -> np.ndarray:
        X_char = self.char_vec.transform(texts)
        X_svd = self.svd.transform(X_char)
        if self.use_function_words:
            fw = self._function_word_features_batch(texts)
            if self._fw_mean is None or self._fw_std is None:
                raise RuntimeError(
                    "Function-word stats not initialized; call fit first."
                )
            fw = (fw - self._fw_mean) / self._fw_std
            return np.hstack([X_svd, fw]).astype(np.float32)
        else:
            return X_svd.astype(np.float32)

    def _function_word_features_batch(self, texts: List[str]) -> np.ndarray:
        vocab = {w: i for i, w in enumerate(FUNCTION_WORDS)}
        M = len(texts)
        F = len(vocab)
        # F + 6 existing + 8 new light features = F + 14
        X = np.zeros((M, F + 14), dtype=np.float32)
        for m, text in enumerate(texts):
            toks = simple_tokenize(text, lowercase=True)
            n = len(toks)
            if n == 0:
                continue
            counts = {}
            for t in toks:
                if t in vocab:
                    counts[t] = counts.get(t, 0) + 1
            for w, c in counts.items():
                X[m, vocab[w]] = c / n

            avg_word_len = np.mean([len(t) for t in toks]) if toks else 0.0
            type_token_ratio = len(set(toks)) / n if n > 0 else 0.0
            punct = count_selected_punct(text)
            upper_ratio = sum(1 for ch in text if ch.isupper()) / max(1, len(text))
            digit_ratio = sum(1 for ch in text if ch.isdigit()) / max(1, len(text))

            # Existing 6
            X[m, F + 0] = avg_word_len
            X[m, F + 1] = type_token_ratio
            X[m, F + 2] = punct["comma"]
            X[m, F + 3] = punct["period"]
            X[m, F + 4] = upper_ratio
            X[m, F + 5] = digit_ratio

            # New cheap extras (8)
            txt_len = max(1, len(text))
            X[m, F + 6] = text.count("!") / txt_len
            X[m, F + 7] = text.count("?") / txt_len
            X[m, F + 8] = text.count(";") / txt_len
            X[m, F + 9] = text.count(":") / txt_len
            X[m, F + 10] = text.count("-") / txt_len
            X[m, F + 11] = (text.count('"') + text.count("'")) / txt_len
            X[m, F + 12] = (text.count("(") + text.count(")")) / txt_len
            X[m, F + 13] = text.count("...") / txt_len  # ellipsis approx

        return X


def count_selected_punct(text: str) -> dict:
    n = max(1, len(text))
    return {
        "comma": text.count(",") / n,
        "period": text.count(".") / n,
    }
