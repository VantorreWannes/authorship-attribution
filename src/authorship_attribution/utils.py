from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any


def find_best_threshold(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    # Maximize F1; search over percentiles of predicted probabilities
    candidates = np.unique(np.percentile(y_prob, np.linspace(0, 100, 200)))
    best_t = 0.5
    best_f1 = -1.0
    for t in candidates:
        y_pred = (y_prob >= t).astype(int)
        f1 = f1_score(y_true, y_pred)
        if f1 > best_f1:
            best_f1 = f1
            best_t = t
    return float(best_t)


def f1_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    if tp + fp == 0 or tp + fn == 0:
        return 0.0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def metrics_at_threshold(
    y_true: np.ndarray, y_prob: np.ndarray, threshold: float
) -> Dict[str, Any]:
    y_pred = (y_prob >= threshold).astype(int)
    acc = float(np.mean(y_pred == y_true))
    f1 = f1_score(y_true, y_pred)
    return {"accuracy": acc, "f1": f1, "threshold": threshold}


def roc_auc(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    # Simple AUC computation without sklearn dependency beyond core
    # Sort by probability descending
    order = np.argsort(-y_prob)
    y = y_true[order]
    pos = np.sum(y == 1)
    neg = np.sum(y == 0)
    if pos == 0 or neg == 0:
        return float("nan")
    tpr = 0.0
    fpr = 0.0
    last_prob = None
    auc = 0.0
    tp = 0
    fp = 0
    for i, yi in enumerate(y):
        if yi == 1:
            tp += 1
        else:
            fp += 1
        # add area when probability changes or at the end
        prob = y_prob[order[i]]
        if last_prob is None:
            last_prob = prob
        if prob != last_prob or i == len(y) - 1:
            auc += (fp / neg - fpr) * (tp / pos + tpr) / 2.0
            fpr = fp / neg
            tpr = tp / pos
            last_prob = prob
    return float(auc)


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
