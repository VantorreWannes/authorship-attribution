from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np
import re
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

_word_re = re.compile(r"[A-Za-z']+")

# Subset of common English function words (can be extended)
FUNCTION_WORDS: List[str] = [
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


def count_selected_punct(text: str) -> dict:
    n = max(1, len(text))
    return {
        "comma": text.count(",") / n,
        "period": text.count(".") / n,
    }


@dataclass
class FeatureExtractor:
    """
    Feature extractor combining:
    - Char n-gram TF-IDF + SVD (compact stylometric signal)
    - Lightweight function-word and stylistic statistics (optionally scaled)

    Notes:
      - fit() learns TF-IDF vocab, SVD basis, and function-word scaler.
      - transform() returns float32 features for efficiency.
    """

    char_ngram_range: Tuple[int, int] = (3, 5)
    max_char_features: int = 50_000
    svd_dim: int = 256
    text_lowercase: bool = True
    use_function_words: bool = True
    random_state: int = 42

    # Internal components (initialized in __post_init__)
    char_vec: TfidfVectorizer = field(init=False, repr=False)
    svd: TruncatedSVD = field(init=False, repr=False)
    fw_scaler: StandardScaler | None = field(default=None, init=False, repr=False)

    # Cached dims
    _fw_dim: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        self.char_vec = TfidfVectorizer(
            analyzer="char",
            ngram_range=self.char_ngram_range,
            lowercase=self.text_lowercase,
            min_df=2,
            max_features=self.max_char_features,
            sublinear_tf=True,
            dtype=np.float32,  # type: ignore[arg-type]
        )
        self.svd = TruncatedSVD(
            n_components=self.svd_dim,
            random_state=self.random_state,
            algorithm="randomized",
        )
        if self.use_function_words:
            # number of function words + 14 light features
            self._fw_dim = len(FUNCTION_WORDS) + 14
        else:
            self._fw_dim = 0

    @property
    def output_dim(self) -> int:
        """
        Number of output features after transform().
        """
        return self.svd_dim + self._fw_dim

    def fit(self, texts: List[str]) -> "FeatureExtractor":
        # Fit TF-IDF + SVD without creating an intermediate dense array
        X_char = self.char_vec.fit_transform(texts)
        self.svd.fit(X_char)

        if self.use_function_words:
            fw = self._function_word_features_batch(texts)
            self.fw_scaler = StandardScaler().fit(fw)

        return self

    def transform(self, texts: List[str]) -> np.ndarray:
        X_char = self.char_vec.transform(texts)
        X_svd = self.svd.transform(X_char)

        if self.use_function_words:
            fw = self._function_word_features_batch(texts)
            if self.fw_scaler is None:
                raise RuntimeError(
                    "Function-word scaler not initialized; call fit() first."
                )
            fw = self.fw_scaler.transform(fw)
            out = np.hstack([X_svd, fw])
        else:
            out = X_svd
        return out.astype(np.float32, copy=False)

    # -------- internals -------- #
    def _function_word_features_batch(self, texts: List[str]) -> np.ndarray:
        vocab = {w: i for i, w in enumerate(FUNCTION_WORDS)}
        M = len(texts)
        F = len(vocab)
        X = np.zeros((M, F + 14), dtype=np.float32)
        for m, text in enumerate(texts):
            toks = simple_tokenize(text, lowercase=True)
            n = len(toks)
            if n == 0:
                # leave zeros
                continue

            # function word relative frequencies
            for t in toks:
                idx = vocab.get(t)
                if idx is not None:
                    X[m, idx] += 1.0
            X[m, :F] /= max(1, n)

            avg_word_len = float(np.mean([len(t) for t in toks])) if toks else 0.0
            type_token_ratio = float(len(set(toks)) / n) if n > 0 else 0.0
            punct = count_selected_punct(text)
            upper_ratio = sum(1 for ch in text if ch.isupper()) / max(1, len(text))
            digit_ratio = sum(1 for ch in text if ch.isdigit()) / max(1, len(text))

            # Six existing features
            X[m, F + 0] = avg_word_len
            X[m, F + 1] = type_token_ratio
            X[m, F + 2] = punct["comma"]
            X[m, F + 3] = punct["period"]
            X[m, F + 4] = upper_ratio
            X[m, F + 5] = digit_ratio

            # Eight new light features
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
