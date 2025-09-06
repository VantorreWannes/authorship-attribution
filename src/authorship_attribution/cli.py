from __future__ import annotations
import argparse
import json

from authorship_attribution.models import Verifier
from authorship_attribution.train import train


def train_main():
    p = argparse.ArgumentParser(description="Train an authorship verification model.")
    p.add_argument("--csv", required=True, help="Path to CSV with columns: author,text")
    p.add_argument("--text-col", default="text")
    p.add_argument("--author-col", default="author")
    p.add_argument("--out-dir", default="aa_model")
    p.add_argument("--max-pos-per-author", type=int, default=100)
    p.add_argument("--negatives-per-positive", type=int, default=1)
    p.add_argument("--char-min", type=int, default=3)
    p.add_argument("--char-max", type=int, default=5)
    p.add_argument("--max-char-features", type=int, default=40000)
    p.add_argument("--svd-dim", type=int, default=256)
    p.add_argument("--no-function-words", action="store_true")
    p.add_argument("--no-lowercase", action="store_true")
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    res = train(
        csv_path=args.csv,
        text_col=args.text_col,
        author_col=args.author_col,
        out_dir=args.out_dir,
        max_pos_per_author=args.max_pos_per_author
        if args.max_pos_per_author > 0
        else None,
        negatives_per_positive=args.negatives_per_positive,
        char_ngram_range=(args.char_min, args.char_max),
        max_char_features=args.max_char_features,
        svd_dim=args.svd_dim,
        use_function_words=not args.no_function_words,
        text_lowercase=not args.no_lowercase,
        seed=args.seed,
    )
    print(json.dumps(res, indent=2))


def eval_main():
    # For now eval is identical to train's validation report; users can retrain or split externally.
    print("Use aa-train to see validation metrics and a saved model.")
    return 0


def verify_main():
    p = argparse.ArgumentParser(
        description="Verify if two texts are by the same author."
    )
    p.add_argument("--model", required=True, help="Path to aa_model.joblib")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--text-a", help="Text A as string")
    g.add_argument("--file-a", help="Path to file for Text A")
    h = p.add_mutually_exclusive_group(required=True)
    h.add_argument("--text-b", help="Text B as string")
    h.add_argument("--file-b", help="Path to file for Text B")
    args = p.parse_args()

    if args.text_a is not None:
        text_a = args.text_a
    else:
        text_a = open(args.file_a, "r", encoding="utf-8").read()

    if args.text_b is not None:
        text_b = args.text_b
    else:
        text_b = open(args.file_b, "r", encoding="utf-8").read()

    verifier = Verifier.from_path(args.model)
    res = verifier.verify(text_a, text_b)
    print(json.dumps(res, indent=2))
