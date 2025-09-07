from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import numpy as np
import pandas as pd
from collections import defaultdict


@dataclass(frozen=True)
class AuthorCorpus:
    df: pd.DataFrame
    texts: List[str]
    authors: List[str]


def load_author_corpus(
    path: str,
    text_col: str = "text",
    author_col: str = "author",
    min_text_len: int = 50,
    min_texts_per_author: int = 2,
) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """
    Load a CSV of author-text rows and apply minimal filtering.
    """
    df = pd.read_csv(path)
    if text_col not in df.columns or author_col not in df.columns:
        raise ValueError(f"CSV must have '{author_col}' and '{text_col}' columns.")
    df = df.dropna(subset=[text_col, author_col]).copy()
    df[text_col] = df[text_col].astype(str)
    df["__len__"] = df[text_col].str.len()
    df = df[df["__len__"] >= min_text_len].copy()
    df.drop(columns=["__len__"], inplace=True)

    counts = df[author_col].value_counts()  # pyright: ignore[reportAttributeAccessIssue]
    keep_authors = set(counts[counts >= min_texts_per_author].index)  # pyright: ignore[reportAttributeAccessIssue]
    df = df[df[author_col].isin(keep_authors)].reset_index(drop=True)  # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]

    texts = df[text_col].tolist()
    authors = df[author_col].tolist()
    return df, texts, authors  # pyright: ignore[reportReturnType]


def group_split_by_author(
    authors: Sequence[str], train_frac: float = 0.8, seed: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Split indices by whole-author groups to avoid leakage.
    """
    if not 0.0 < train_frac < 1.0:
        raise ValueError("train_frac must be in (0, 1).")
    rng = np.random.default_rng(seed)
    unique_authors = np.array(sorted(set(authors)))
    rng.shuffle(unique_authors)
    if len(unique_authors) == 1:
        idx = np.arange(len(authors))
        return idx, idx[:0]  # all train, no val
    n_train = max(1, int(len(unique_authors) * train_frac))
    train_authors = set(unique_authors[:n_train])
    idx = np.arange(len(authors))
    train_mask = np.array([a in train_authors for a in authors], dtype=bool)
    val_mask = ~train_mask
    return idx[train_mask], idx[val_mask]


def sample_pairs(
    authors: Sequence[str],
    max_pos_per_author: int | None = 200,
    negatives_per_positive: int = 1,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build (i,j) pairs and labels.

    Returns:
      pairs: (N, 2) indices
      labels: (N,) with 1 for same author, 0 otherwise
    """
    if negatives_per_positive < 1:
        raise ValueError("negatives_per_positive must be >= 1")
    rng = np.random.default_rng(seed)

    author_to_indices: Dict[str, List[int]] = defaultdict(list)
    for i, a in enumerate(authors):
        author_to_indices[a].append(i)

    # Positive pairs
    pos_pairs: List[Tuple[int, int]] = []
    for idxs in author_to_indices.values():
        if len(idxs) < 2:
            continue
        # generate all unordered pairs
        all_pairs = [
            (idxs[i], idxs[j])
            for i in range(len(idxs))
            for j in range(i + 1, len(idxs))
        ]
        if max_pos_per_author is not None and len(all_pairs) > max_pos_per_author:
            picks = rng.choice(len(all_pairs), size=max_pos_per_author, replace=False)
            pos_pairs.extend(all_pairs[k] for k in picks)
        else:
            pos_pairs.extend(all_pairs)

    if not pos_pairs:
        raise ValueError(
            "Not enough positive (same-author) pairs. Provide more texts per author."
        )
    pos_pairs_arr = np.asarray(pos_pairs, dtype=int)

    # Negative pairs: for each positive anchor i, sample negatives_per_positive j' with different author
    n = len(authors)
    all_indices = np.arange(n)
    authors_arr = np.asarray(authors)
    neg_pairs: List[Tuple[int, int]] = []
    for i, _ in pos_pairs_arr:
        a_i = authors[i]
        candidates = all_indices[authors_arr != a_i]
        k = negatives_per_positive
        # allow replace if candidate pool is smaller
        replace = k > len(candidates)
        js = rng.choice(candidates, size=k, replace=replace)
        for j in js:
            neg_pairs.append((int(i), int(j)))
    neg_pairs_arr = np.asarray(neg_pairs, dtype=int)

    pairs = np.vstack([pos_pairs_arr, neg_pairs_arr])
    labels = np.hstack(
        [
            np.ones(len(pos_pairs_arr), dtype=int),
            np.zeros(len(neg_pairs_arr), dtype=int),
        ]
    )

    # Shuffle
    p = rng.permutation(len(pairs))
    return pairs[p], labels[p]
