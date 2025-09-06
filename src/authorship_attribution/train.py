from __future__ import annotations
from typing import Dict, Any
import os
import logging
import numpy as np
from sklearn.linear_model import LogisticRegression

from .data import load_author_corpus, group_split_by_author, sample_pairs
from .features import FeatureExtractor
from .models import ModelBundle, pairwise_features
from .utils import find_best_threshold, metrics_at_threshold, roc_auc, ModelMeta


def build_pair_matrix(embeddings: np.ndarray, pairs: np.ndarray) -> np.ndarray:
    feats = []
    for i, j in pairs:
        u = embeddings[i]
        v = embeddings[j]
        feats.append(pairwise_features(u, v))
    return np.vstack(feats).astype(np.float32)


def train(
    csv_path: str,
    text_col: str = "text",
    author_col: str = "author",
    out_dir: str = "aa_model",
    max_pos_per_author: int | None = 200,
    negatives_per_positive: int = 1,
    char_ngram_range: tuple[int, int] = (3, 5),
    max_char_features: int = 50000,
    svd_dim: int = 256,
    use_function_words: bool = True,
    text_lowercase: bool = True,
    seed: int = 42,
) -> Dict[str, Any]:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    os.makedirs(out_dir, exist_ok=True)
    # 1) Load data
    logging.info(f"Loading data from {csv_path}...")
    df, texts, authors = load_author_corpus(
        csv_path,
        text_col=text_col,
        author_col=author_col,
        min_text_len=50,
        min_texts_per_author=2,
    )
    logging.info(f"Loaded {len(texts)} texts from {len(set(authors))} authors.")

    idx_train, idx_val = group_split_by_author(authors, train_frac=0.8, seed=seed)
    texts_train = [texts[i] for i in idx_train]
    texts_val = [texts[i] for i in idx_val]
    authors_train = [authors[i] for i in idx_train]
    authors_val = [authors[i] for i in idx_val]

    # 2) Fit feature extractor on train texts only
    logging.info("Fitting feature extractor...")
    extractor = FeatureExtractor(
        char_ngram_range=char_ngram_range,
        max_char_features=max_char_features,
        svd_dim=svd_dim,
        text_lowercase=text_lowercase,
        use_function_words=use_function_words,
        random_state=seed,
    )
    extractor.fit(texts_train)

    # 3) Precompute embeddings
    logging.info("Transforming texts to embeddings...")
    X_train = extractor.transform(texts_train)
    X_val = extractor.transform(texts_val)

    # 4) Create pair datasets (author-disjoint)
    logging.info("Creating training and validation pairs...")
    pairs_train, y_train = sample_pairs(
        authors_train,
        max_pos_per_author=max_pos_per_author,
        negatives_per_positive=negatives_per_positive,
        seed=seed,
    )
    pairs_val, y_val = sample_pairs(
        authors_val,
        max_pos_per_author=max_pos_per_author,
        negatives_per_positive=negatives_per_positive,
        seed=seed + 1,
    )
    logging.info(
        f"Created {len(pairs_train)} training pairs and {len(pairs_val)} validation pairs."
    )

    # Remap pair indices to split subarray indices
    logging.info("Building pair matrices...")
    Pf_train = build_pair_matrix(X_train, pairs_train)
    Pf_val = build_pair_matrix(X_val, pairs_val)

    # 5) Train classifier
    logging.info("Training classifier...")
    clf = LogisticRegression(max_iter=2000, class_weight="balanced", solver="lbfgs")
    clf.fit(Pf_train, y_train)

    # 6) Calibrate threshold on val
    logging.info("Calibrating threshold on validation set...")
    val_probs = clf.predict_proba(Pf_val)[:, 1]
    threshold = find_best_threshold(y_val, val_probs)

    # 7) Evaluate
    logging.info("Evaluating model...")
    auc = roc_auc(y_val, val_probs)
    m = metrics_at_threshold(y_val, val_probs, threshold=threshold)
    logging.info(
        f"Validation AUC: {auc:.4f}, Accuracy: {m['accuracy']:.4f}, F1: {m['f1']:.4f} at threshold {threshold:.4f}"
    )

    # 8) Save model
    logging.info("Saving model bundle...")
    bundle = ModelBundle(
        extractor=extractor,
        classifier=clf,
        threshold=float(threshold),
        meta=ModelMeta(
            feature_dim=int(X_train.shape[1]),
            svd_dim=svd_dim,
            char_ngram_range=char_ngram_range,
            max_char_features=max_char_features,
            use_function_words=use_function_words,
            text_lowercase=text_lowercase,
            tokenizer="regex_word",
            notes="Pairwise logistic on |u-v|, u*v plus cos/L1/L2 from char n-gram SVD + function words",
        ),
    )
    model_path = os.path.join(out_dir, "aa_model.joblib")
    bundle.save(model_path)
    logging.info(f"Model saved to {model_path}")

    return {
        "model_path": model_path,
        "val_auc": auc,
        "val_accuracy": m["accuracy"],
        "val_f1": m["f1"],
        "threshold": float(threshold),
        "n_train_pairs": int(len(Pf_train)),
        "n_val_pairs": int(len(Pf_val)),
        "n_train_texts": int(len(texts_train)),
        "n_val_texts": int(len(texts_val)),
    }


def load_model(path: str) -> ModelBundle:
    return ModelBundle.load(path)
