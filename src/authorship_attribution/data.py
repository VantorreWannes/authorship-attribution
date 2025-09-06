from __future__ import annotations
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict
from collections import defaultdict


def load_author_corpus(
    path: str,
    text_col: str = "text",
    author_col: str = "author",
    min_text_len: int = 50,
    min_texts_per_author: int = 2,
) -> Tuple[pd.DataFrame, List[str], List[str]]:
    df = pd.read_csv(path)
    if text_col not in df.columns or author_col not in df.columns:
        raise ValueError(f"CSV must have '{author_col}' and '{text_col}' columns.")
    df = df.dropna(subset=[text_col, author_col]).copy()
    df[text_col] = df[text_col].astype(str)
    df["len"] = df[text_col].str.len()
    df = df[df["len"] >= min_text_len]
    df.drop(columns=["len"], inplace=True)

    # filter authors with at least min_texts_per_author
    counts = df[author_col].value_counts()
    keep_authors = set(counts[counts >= min_texts_per_author].index)
    df = df[df[author_col].isin(keep_authors)].reset_index(drop=True)

    texts = df[text_col].tolist()
    authors = df[author_col].tolist()
    return df, texts, authors


def group_split_by_author(
    authors: List[str], train_frac: float = 0.8, seed: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    unique_authors = np.array(sorted(set(authors)))
    rng.shuffle(unique_authors)
    n_train = max(1, int(len(unique_authors) * train_frac))
    train_authors = set(unique_authors[:n_train])
    idx = np.arange(len(authors))
    train_mask = np.array([a in train_authors for a in authors], dtype=bool)
    val_mask = ~train_mask
    return idx[train_mask], idx[val_mask]


def sample_pairs(
    authors: List[str],
    max_pos_per_author: int | None = 200,
    negatives_per_positive: int = 1,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns:
      pairs: (N, 2) indices
      labels: (N,) 1 for same author, 0 for different
    """
    rng = np.random.default_rng(seed)
    author_to_indices: Dict[str, List[int]] = defaultdict(list)
    for i, a in enumerate(authors):
        author_to_indices[a].append(i)

    pos_pairs = []
    for a, idxs in author_to_indices.items():
        if len(idxs) < 2:
            continue
        # all combinations or sample
        all_pairs = []
        for i in range(len(idxs)):
            for j in range(i + 1, len(idxs)):
                all_pairs.append((idxs[i], idxs[j]))
        if max_pos_per_author is not None and len(all_pairs) > max_pos_per_author:
            pos_pairs.extend(
                rng.choice(
                    np.array(all_pairs), size=max_pos_per_author, replace=False
                ).tolist()
            )
        else:
            pos_pairs.extend(all_pairs)

    pos_pairs = np.array(pos_pairs, dtype=int)
    n_pos = len(pos_pairs)
    if n_pos == 0:
        raise ValueError(
            "Not enough positive (same-author) pairs. Provide more texts per author."
        )

    # negatives: sample pairs with different authors
    all_indices = np.arange(len(authors))
    labels = np.array(authors)
    neg_pairs = []
    for i, j in pos_pairs:
        # sample j' with a different author than authors[i]
        a_i = authors[i]
        # candidate pool: indices whose author != a_i
        mask = labels != a_i
        candidates = all_indices[mask]
        jj = int(rng.choice(candidates))
        neg_pairs.append((i, jj))
    neg_pairs = np.array(neg_pairs, dtype=int)

    # balance negatives_per_positive
    if negatives_per_positive > 1:
        extra_neg = []
        for i, _ in pos_pairs:
            a_i = authors[i]
            mask = labels != a_i
            candidates = all_indices[mask]
            picks = rng.choice(
                candidates, size=negatives_per_positive - 1, replace=False
            )
            for jj in picks:
                extra_neg.append((i, int(jj)))
        if extra_neg:
            neg_pairs = np.vstack([neg_pairs, np.array(extra_neg, dtype=int)])

    pairs = np.vstack([pos_pairs, neg_pairs])
    labels_bin = np.hstack([
        np.ones(len(pos_pairs), dtype=int),
        np.zeros(len(neg_pairs), dtype=int),
    ])
    # shuffle
    shuf = rng.permutation(len(pairs))
    return pairs[shuf], labels_bin[shuf]
