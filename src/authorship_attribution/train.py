from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import numpy as np
from joblib import dump, load
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from .data import group_split_by_author, load_author_corpus, sample_pairs
from .features import FeatureExtractor
from .models import ModelBundle, pairwise_features
from .utils import (
    ModelMeta,
    ensure_dir,
    find_best_threshold,
    metrics_at_threshold,
    params_sha256,
    roc_auc,
    file_sha256,
    texts_sha256,
)


def build_pair_matrix(embeddings: np.ndarray, pairs: np.ndarray) -> np.ndarray:
    """
    Vectorized pairwise feature construction.
    embeddings: (N, D)
    pairs: (K, 2) with index pairs into embeddings
    returns: (K, 2D+3)
    """
    U = embeddings[pairs[:, 0]]
    V = embeddings[pairs[:, 1]]
    return pairwise_features(U, V)


@dataclass(frozen=True)
class TrainingConfig:
    csv_path: str
    text_col: str = "text"
    author_col: str = "author"
    out_dir: str = "aa_model"
    max_pos_per_author: int | None = 200
    negatives_per_positive: int = 1
    char_ngram_range: tuple[int, int] = (3, 5)
    max_char_features: int = 50_000
    svd_dim: int = 256
    use_function_words: bool = True
    text_lowercase: bool = True
    char_min_df: int = 2
    seed: int = 42
    use_cache: bool = True
    cache_dir: str | None = None


def _cache_paths(
    cfg: TrainingConfig, data_key: str, train_key: str, texts_key: str
) -> Dict[str, Path]:
    cache_root = Path(cfg.cache_dir or Path(cfg.out_dir) / "cache")
    ensure_dir(cache_root)
    extractor_key = params_sha256(
        {
            "data_key": data_key,
            "train_key": train_key,
            "char_ngram_range": list(cfg.char_ngram_range),
            "max_char_features": cfg.max_char_features,
            "svd_dim": cfg.svd_dim,
            "use_function_words": cfg.use_function_words,
            "text_lowercase": cfg.text_lowercase,
            "min_df": cfg.char_min_df,
            "seed": cfg.seed,
            "extractor_class": "FeatureExtractor",
        }
    )
    emb_all_key = params_sha256(
        {
            "extractor_key": extractor_key,
            "texts_key": texts_key,
        }
    )
    return {
        "extractor": cache_root / f"extractor_{extractor_key}.joblib",
        "emb_all": cache_root / f"emb_all_{emb_all_key}.npz",
        # pairs also depend on seed and sampling params, build per split below
    }


def _pairs_paths(
    cfg: TrainingConfig,
    split_name: str,
    authors_hash: str,
) -> Path:
    cache_root = Path(cfg.cache_dir or Path(cfg.out_dir) / "cache")
    ensure_dir(cache_root)
    key = params_sha256(
        {
            "split": split_name,
            "authors_hash": authors_hash,
            "max_pos_per_author": cfg.max_pos_per_author,
            "negatives_per_positive": cfg.negatives_per_positive,
            "seed": cfg.seed if split_name == "train" else cfg.seed + 1,
        }
    )
    return cache_root / f"pairs_{split_name}_{key}.npz"


def train(
    csv_path: str,
    text_col: str = "text",
    author_col: str = "author",
    out_dir: str = "aa_model",
    max_pos_per_author: int | None = 200,
    negatives_per_positive: int = 1,
    char_ngram_range: tuple[int, int] = (3, 5),
    max_char_features: int = 50_000,
    svd_dim: int = 256,
    use_function_words: bool = True,
    text_lowercase: bool = True,
    char_min_df: int = 2,
    seed: int = 42,
    use_cache: bool = True,
    cache_dir: str | None = None,
) -> Dict[str, Any]:
    """
    Train an authorship verification model and save a serialized bundle.
    Now includes pairwise feature scaling and LR(C) tuning on validation split.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)

    cfg = TrainingConfig(
        csv_path=csv_path,
        text_col=text_col,
        author_col=author_col,
        out_dir=out_dir,
        max_pos_per_author=max_pos_per_author,
        negatives_per_positive=negatives_per_positive,
        char_ngram_range=char_ngram_range,
        max_char_features=max_char_features,
        svd_dim=svd_dim,
        use_function_words=use_function_words,
        text_lowercase=text_lowercase,
        char_min_df=char_min_df,
        seed=seed,
        use_cache=use_cache,
        cache_dir=cache_dir,
    )

    os.makedirs(cfg.out_dir, exist_ok=True)

    # 1) Load and minimally filter data
    logger.info("Loading data from %s", cfg.csv_path)
    df, texts, authors = load_author_corpus(
        cfg.csv_path,
        text_col=cfg.text_col,
        author_col=cfg.author_col,
        min_text_len=50,
        min_texts_per_author=2,
    )
    logger.info("Loaded %d texts from %d authors.", len(texts), len(set(authors)))

    # Data-level fingerprints
    data_key = params_sha256(
        {
            "file_sha256": file_sha256(cfg.csv_path),
            "text_col": cfg.text_col,
            "author_col": cfg.author_col,
            "min_text_len": 50,
            "min_texts_per_author": 2,
        }
    )
    texts_key = texts_sha256(texts)

    # 2) Author-disjoint split (deterministic for seed)
    idx_train, idx_val = group_split_by_author(authors, train_frac=0.8, seed=cfg.seed)
    texts_train = [texts[i] for i in idx_train]
    texts_val = [texts[i] for i in idx_val]
    authors_train = [authors[i] for i in idx_train]
    authors_val = [authors[i] for i in idx_val]

    train_key = texts_sha256(texts_train)
    paths = _cache_paths(
        cfg, data_key=data_key, train_key=train_key, texts_key=texts_key
    )

    # 3) Fit or load feature extractor (fit on train only; no leakage)
    if cfg.use_cache and paths["extractor"].is_file():
        logger.info("Cache hit: loading extractor from %s", paths["extractor"])
        extractor: FeatureExtractor = load(paths["extractor"])
    else:
        logger.info("Fitting feature extractor...")
        extractor = FeatureExtractor(
            char_ngram_range=cfg.char_ngram_range,
            max_char_features=cfg.max_char_features,
            svd_dim=cfg.svd_dim,
            text_lowercase=cfg.text_lowercase,
            use_function_words=cfg.use_function_words,
            random_state=cfg.seed,
            min_df=cfg.char_min_df,
        ).fit(texts_train)
        if cfg.use_cache:
            logger.info("Cache save: extractor -> %s", paths["extractor"])
            dump(extractor, paths["extractor"])

    # 4) Transform texts to embeddings (reuse for all texts if cached)
    if cfg.use_cache and paths["emb_all"].is_file():
        logger.info("Cache hit: loading all embeddings from %s", paths["emb_all"])
        X_all = np.load(paths["emb_all"])["X"]
    else:
        logger.info("Transforming texts to embeddings (all)...")
        X_all = extractor.transform(texts)
        if cfg.use_cache:
            logger.info("Cache save: embeddings -> %s", paths["emb_all"])
            np.savez_compressed(paths["emb_all"], X=X_all)

    X_train = X_all[idx_train]
    X_val = X_all[idx_val]

    # 5) Pairs (author-disjoint), cache per split
    train_pairs_path = _pairs_paths(
        cfg, "train", authors_hash=texts_sha256(authors_train)
    )
    val_pairs_path = _pairs_paths(cfg, "val", authors_hash=texts_sha256(authors_val))

    if cfg.use_cache and train_pairs_path.is_file():
        logger.info("Cache hit: loading train pairs from %s", train_pairs_path)
        with np.load(train_pairs_path) as npz:
            pairs_train = npz["pairs"]
            y_train = npz["labels"]
    else:
        logger.info("Creating training pairs...")
        pairs_train, y_train = sample_pairs(
            authors_train,
            max_pos_per_author=cfg.max_pos_per_author,
            negatives_per_positive=cfg.negatives_per_positive,
            seed=cfg.seed,
        )
        if cfg.use_cache:
            logger.info("Cache save: train pairs -> %s", train_pairs_path)
            np.savez_compressed(train_pairs_path, pairs=pairs_train, labels=y_train)

    if cfg.use_cache and val_pairs_path.is_file():
        logger.info("Cache hit: loading val pairs from %s", val_pairs_path)
        with np.load(val_pairs_path) as npz:
            pairs_val = npz["pairs"]
            y_val = npz["labels"]
    else:
        logger.info("Creating validation pairs...")
        pairs_val, y_val = sample_pairs(
            authors_val,
            max_pos_per_author=cfg.max_pos_per_author,
            negatives_per_positive=cfg.negatives_per_positive,
            seed=cfg.seed + 1,
        )
        if cfg.use_cache:
            logger.info("Cache save: val pairs -> %s", val_pairs_path)
            np.savez_compressed(val_pairs_path, pairs=pairs_val, labels=y_val)

    logger.info(
        "Prepared %d train pairs and %d val pairs.",
        len(pairs_train),
        len(pairs_val),
    )

    # 6) Build pairwise feature matrices
    logger.info("Building pair feature matrices...")
    Pf_train = build_pair_matrix(X_train, pairs_train)
    Pf_val = build_pair_matrix(X_val, pairs_val)

    # 7) Standardize pairwise features
    logger.info("Fitting StandardScaler for pairwise features...")
    pair_scaler = StandardScaler().fit(Pf_train)
    Pf_train = pair_scaler.transform(Pf_train)
    Pf_val = pair_scaler.transform(Pf_val)

    # 8) Tune LogisticRegression C on validation (no class weighting; pairs are balanced)
    logger.info("Tuning LogisticRegression(C) on validation set...")
    C_grid = [0.1, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
    best = {
        "auc": -1.0,
        "f1": -1.0,
        "C": None,
        "clf": None,
        "threshold": 0.5,
        "val_probs": None,
    }
    for C in C_grid:
        clf_tmp = LogisticRegression(
            max_iter=2000,
            class_weight=None,
            solver="lbfgs",
            random_state=cfg.seed,
            C=C,
        )
        clf_tmp.fit(Pf_train, y_train)
        val_probs_tmp = clf_tmp.predict_proba(Pf_val)[:, 1]
        auc_tmp = roc_auc(y_val, val_probs_tmp)
        thr_tmp = find_best_threshold(y_val, val_probs_tmp)
        m_tmp = metrics_at_threshold(y_val, val_probs_tmp, threshold=thr_tmp)
        logger.info(
            "C=%.3g | AUC=%.4f | F1@bestThr=%.4f thr=%.4f",
            C,
            auc_tmp,
            m_tmp["f1"],
            thr_tmp,
        )
        # Select by AUC, tie-break by F1
        if (auc_tmp > best["auc"]) or (
            np.isclose(auc_tmp, best["auc"]) and m_tmp["f1"] > best["f1"]
        ):
            best.update(
                {
                    "auc": float(auc_tmp),
                    "f1": float(m_tmp["f1"]),
                    "C": float(C),
                    "clf": clf_tmp,
                    "threshold": float(thr_tmp),
                    "val_probs": val_probs_tmp,
                }
            )

    clf = best["clf"]  # type: ignore[assignment]
    assert clf is not None
    val_probs = best["val_probs"]  # type: ignore[assignment]
    assert val_probs is not None
    threshold = float(best["threshold"])
    auc = float(best["auc"])
    m = metrics_at_threshold(y_val, val_probs, threshold=threshold)

    logger.info(
        "Selected C=%.3g | Validation AUC: %.4f, Accuracy: %.4f, F1: %.4f at threshold %.4f",
        best["C"],
        auc,
        m["accuracy"],
        m["f1"],
        threshold,
    )

    # 9) Save model bundle
    logger.info("Saving model bundle...")
    bundle = ModelBundle(
        extractor=extractor,
        classifier=clf,  # tuned
        threshold=float(threshold),
        meta=ModelMeta(
            feature_dim=int(X_train.shape[1]),
            svd_dim=cfg.svd_dim,
            char_ngram_range=cfg.char_ngram_range,
            max_char_features=cfg.max_char_features,
            use_function_words=cfg.use_function_words,
            text_lowercase=cfg.text_lowercase,
            tokenizer="regex_word",
            notes="Pairwise logistic on |u-v|, u*v + cosine + L1 + L2 from char n-gram SVD (+ function words). Pairwise features standardized.",
        ),
        pair_scaler=pair_scaler,
    )
    model_path = os.path.join(cfg.out_dir, "aa_model.joblib")
    bundle.save(model_path)
    logger.info("Model saved to %s", model_path)

    return {
        "model_path": model_path,
        "val_auc": auc,
        "val_accuracy": m["accuracy"],
        "val_f1": m["f1"],
        "threshold": float(threshold),
        "best_C": float(best["C"]) if best["C"] is not None else None,
        "n_train_pairs": int(len(Pf_train)),
        "n_val_pairs": int(len(Pf_val)),
        "n_train_texts": int(len(texts_train)),
        "n_val_texts": int(len(texts_val)),
        "cache": {
            "used": bool(cfg.use_cache),
            "cache_dir": str(Path(cfg.cache_dir or Path(cfg.out_dir) / "cache")),
        },
    }


def load_model(path: str) -> ModelBundle:
    return ModelBundle.load(path)
