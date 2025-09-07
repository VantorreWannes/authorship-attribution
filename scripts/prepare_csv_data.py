#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def prepare_csv_data(
    source: Path,
    out_csv: Path,
    author_col: str = "userName",
    text_col: str = "reviewText",
    min_review_count: int = 3,
    min_review_length: int = 200,
) -> int:
    """
    Prepare CSV review data by filtering authors and reviews.

    - Keeps rows with non-null author/text.
    - Keeps authors with at least `min_review_count` reviews.
    - Keeps texts of length >= `min_review_length`.
    - Writes a CSV with columns: author, text.

    Returns:
        Number of rows written.
    """
    if not source.is_file():
        raise FileNotFoundError(f"Input file not found: {source}")

    usecols = [author_col, text_col]
    df = pd.read_csv(source, usecols=usecols, dtype="string")  # type: ignore[arg-type]
    df = df.dropna(subset=usecols).copy()
    df = df.rename(columns={author_col: "author", text_col: "text"})
    df["text"] = df["text"].astype(str)

    counts = df["author"].value_counts()
    keep_authors = set(counts[counts >= min_review_count].index)
    df = df[df["author"].isin(keep_authors)].copy()
    df = df[df["text"].str.len().ge(min_review_length)].copy()

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    return len(df)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prepare CSV review data.")
    p.add_argument(
        "--source",
        type=Path,
        default=Path("data/raw/raw_amazon_reviews.csv"),
    )
    p.add_argument("--out", type=Path, default=Path("data/amazon_reviews.csv"))
    p.add_argument("--author-col", type=str, default="userName")
    p.add_argument("--text-col", type=str, default="reviewText")
    p.add_argument("--min-review-count", type=int, default=3)
    p.add_argument("--min-review-length", type=int, default=200)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    written = prepare_csv_data(
        source=args.source,
        out_csv=args.out,
        author_col=args.author_col,
        text_col=args.text_col,
        min_review_count=args.min_review_count,
        min_review_length=args.min_review_length,
    )
    print(f"Wrote {written} rows to {args.out}")


if __name__ == "__main__":
    main()
