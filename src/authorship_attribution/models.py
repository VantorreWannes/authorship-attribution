from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import numpy as np
from joblib import dump, load
from sklearn.linear_model import LogisticRegression

from authorship_attribution.features import FeatureExtractor
from authorship_attribution.utils import ModelMeta


def pairwise_features(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """
    Construct pairwise features from two embedding sets.

    Accepts:
      - u: (D,) and v: (D,)            -> returns (2D + 3,)
      - u: (N, D) and v: (N, D)        -> returns (N, 2D + 3)

    Features:
      - |u - v|
      - u * v
      - cosine similarity
      - mean L1 distance
      - mean L2 distance
    """
    U = np.atleast_2d(u).astype(np.float32, copy=False)
    V = np.atleast_2d(v).astype(np.float32, copy=False)
    if U.shape != V.shape:
        raise ValueError(f"u and v shape mismatch: {U.shape} vs {V.shape}")
    if U.ndim != 2:
        raise ValueError("u and v must be 1D or 2D arrays")

    # normalize for cosine
    U_norm = U / (np.linalg.norm(U, axis=1, keepdims=True) + 1e-8)
    V_norm = V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-8)
    cos = np.sum(U_norm * V_norm, axis=1, keepdims=True)

    diff = np.abs(U - V)
    prod = U * V
    l1 = np.mean(np.abs(U - V), axis=1, keepdims=True)
    l2 = np.sqrt(np.mean((U - V) ** 2, axis=1, keepdims=True))
    out = np.hstack([diff, prod, cos, l1, l2]).astype(np.float32, copy=False)
    if u.ndim == 1:
        return out[0]
    return out


@dataclass
class ModelBundle:
    extractor: FeatureExtractor
    classifier: LogisticRegression
    threshold: float
    meta: ModelMeta

    _FORMAT_VERSION: int = 2  # bump if on-disk structure changes

    def save(self, path: str) -> None:
        """
        Save a stable dict (not raw dataclass) for forward compatibility.
        """
        payload: Dict[str, Any] = {
            "format_version": self._FORMAT_VERSION,
            "extractor": self.extractor,
            "classifier": self.classifier,
            "threshold": float(self.threshold),
            "meta": self.meta,
        }
        dump(payload, path)

    @staticmethod
    def load(path: str) -> "ModelBundle":
        obj = load(path)
        # Backward compatibility: if older dumps saved the dataclass directly
        if isinstance(obj, ModelBundle):
            return obj
        if isinstance(obj, dict) and "format_version" in obj:
            return ModelBundle(
                extractor=obj["extractor"],
                classifier=obj["classifier"],
                threshold=float(obj["threshold"]),
                meta=obj["meta"],
            )
        raise ValueError("Unknown model file format.")


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
        pf = pairwise_features(XA, XB)
        prob = clf.predict_proba(pf)[0, 1]
        return float(prob)

    def verify(self, text_a: str, text_b: str) -> Dict[str, Any]:
        prob = self.score_proba(text_a, text_b)
        same = prob >= self.bundle.threshold
        return {
            "probability_same_author": float(prob),
            "same_author": bool(same),
            "threshold": float(self.bundle.threshold),
        }
