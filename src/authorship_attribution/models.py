from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any
from sklearn.linear_model import LogisticRegression
from joblib import dump, load

from authorship_attribution.features import FeatureExtractor
from authorship_attribution.utils import ModelMeta


def pairwise_features(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """
    Create pairwise features from two embeddings.
    Returns: [|u-v|, u*v, cosine_sim, l1_mean, l2_mean]
    """

    # normalize to compute cosine
    def safe_norm(x):
        n = np.linalg.norm(x) + 1e-8
        return x / n

    u_n = safe_norm(u)
    v_n = safe_norm(v)
    cos = np.dot(u_n, v_n)
    diff = np.abs(u - v)
    prod = u * v
    l1 = float(np.mean(np.abs(u - v)))
    l2 = float(np.sqrt(np.mean((u - v) ** 2)))
    return np.hstack([diff, prod, [cos, l1, l2]]).astype(np.float32)


@dataclass
class ModelBundle:
    extractor: FeatureExtractor
    classifier: LogisticRegression
    threshold: float
    meta: ModelMeta

    def save(self, path: str):
        dump(self, path)

    @staticmethod
    def load(path: str) -> "ModelBundle":
        return load(path)


class Verifier:
    """
    High-level API for inference.
    """

    def __init__(self, bundle: ModelBundle):
        self.bundle = bundle

    @staticmethod
    def from_path(path: str) -> "Verifier":
        return Verifier(ModelBundle.load(path))

    def score_proba(self, text_a: str, text_b: str) -> float:
        extractor = self.bundle.extractor
        clf = self.bundle.classifier
        XA = extractor.transform([text_a])
        XB = extractor.transform([text_b])
        u = XA[0]
        v = XB[0]
        pf = pairwise_features(u, v).reshape(1, -1)
        proba = clf.predict_proba(pf)[0, 1]
        return float(proba)

    def verify(self, text_a: str, text_b: str) -> Dict[str, Any]:
        prob = self.score_proba(text_a, text_b)
        same = prob >= self.bundle.threshold
        return {
            "probability_same_author": prob,
            "same_author": bool(same),
            "threshold": self.bundle.threshold,
        }
