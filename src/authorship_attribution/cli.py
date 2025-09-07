from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

from authorship_attribution.models import Verifier
from authorship_attribution.train import train


def train_main() -> int:
    p = argparse.ArgumentParser(description="Train an authorship verification model.")
    p.add_argument("--csv", required=True, help="Path to CSV with columns: author,text")
    p.add_argument("--text-col", default="text")
    p.add_argument("--author-col", default="author")
    p.add_argument("--out-dir", default="aa_model")
    p.add_argument("--max-pos-per-author", type=int, default=100)
    p.add_argument("--negatives-per-positive", type=int, default=3)
    p.add_argument("--char-min", type=int, default=3)
    p.add_argument("--char-max", type=int, default=6)
    p.add_argument("--max-char-features", type=int, default=100000)
    p.add_argument("--svd-dim", type=int, default=512)
    p.add_argument(
        "--char-min-df",
        type=float,
        default=5,
        help="min_df for char TF-IDF (int>=1 or fraction in (0,1)",
    )
    p.add_argument("--no-function-words", action="store_true")
    p.add_argument("--no-lowercase", action="store_true")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--no-cache", action="store_true", help="Disable caching.")
    p.add_argument(
        "--cache-dir", type=str, default=None, help="Custom cache directory."
    )
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
        char_min_df=args.char_min_df,
        seed=args.seed,
        use_cache=not args.no_cache,
        cache_dir=args.cache_dir,
    )
    print(json.dumps(res, indent=2))
    return 0


def eval_main() -> int:
    print("Use aa-train to see validation metrics and a saved model.")
    return 0


def _read_text_arg(text: Optional[str], file: Optional[str]) -> str:
    if text is not None:
        return text
    if file is None:
        raise ValueError("Either a text or a file path must be provided.")
    path = Path(file)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file}")
    return path.read_text(encoding="utf-8")


def verify_main() -> int:
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

    text_a = _read_text_arg(args.text_a, args.file_a)
    text_b = _read_text_arg(args.text_b, args.file_b)

    verifier = Verifier.from_path(args.model)
    res = verifier.verify(text_a, text_b)
    print(json.dumps(res, indent=2))
    return 0
