from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Sequence

import numpy as np
from sklearn.metrics import accuracy_score, f1_score as sk_f1_score, roc_auc_score


def find_best_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    *,
    n_steps: int = 200,
) -> float:
    """
    Pick threshold (by percentiles of y_prob) that maximizes F1.
    """
    if y_true.ndim != 1 or y_prob.ndim != 1 or y_true.shape[0] != y_prob.shape[0]:
        raise ValueError("y_true and y_prob must be 1D arrays of the same length.")
    if n_steps <= 1:
        return 0.5

    # Avoid degenerate candidates by deduplicating
    candidates = np.unique(np.percentile(y_prob, np.linspace(0, 100, n_steps)))
    best_t, best_f1 = 0.5, -1.0
    for t in candidates:
        y_pred = (y_prob >= t).astype(int)
        f1 = sk_f1_score(y_true, y_pred, zero_division=0)  # pyright: ignore[reportArgumentType]
        if f1 > best_f1:
            best_f1 = f1
            best_t = float(t)
    return best_t


def metrics_at_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float,
) -> Dict[str, float]:
    """
    Compute accuracy/F1 at a fixed threshold using sklearn metrics.
    """
    y_pred = (y_prob >= threshold).astype(int)
    acc = float(accuracy_score(y_true, y_pred))
    f1 = float(sk_f1_score(y_true, y_pred, zero_division=0))  # pyright: ignore[reportArgumentType]
    return {"accuracy": acc, "f1": f1, "threshold": float(threshold)}


def roc_auc(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """
    Compute ROC AUC via sklearn. Returns NaN if not defined.
    """
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    pos = int(np.sum(y_true == 1))
    neg = int(np.sum(y_true == 0))
    if pos == 0 or neg == 0:
        return float("nan")
    return float(roc_auc_score(y_true, y_prob))


@dataclass
class ModelMeta:
    feature_dim: int
    svd_dim: int
    char_ngram_range: tuple[int, int]
    max_char_features: int
    use_function_words: bool
    text_lowercase: bool
    tokenizer: str
    notes: str = ""
    version: str = "1.0.0"


# ------------- caching helpers ------------- #


def sha256_update(obj: bytes | str, h: hashlib._Hash) -> None:
    if isinstance(obj, str):
        h.update(obj.encode("utf-8"))
    else:
        h.update(obj)


def file_sha256(path: str | Path, chunk_size: int = 1 << 20) -> str:
    """
    Streaming SHA-256 of a file's content.
    """
    p = Path(path)
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def texts_sha256(texts: Sequence[str]) -> str:
    """
    Hash a sequence of texts deterministically (length-prefixed).
    """
    h = hashlib.sha256()
    for t in texts:
        b = t.encode("utf-8", errors="replace")
        sha256_update(str(len(b)), h)
        h.update(b)
        sha256_update("|", h)
    return h.hexdigest()


def params_sha256(params: Any) -> str:
    """
    Hash an arbitrary JSON-serializable structure deterministically.
    """
    s = json.dumps(params, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
