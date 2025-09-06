#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Set

import pandas as pd


def setup_logging(level: str) -> None:
    lvl = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=lvl,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def validate_source(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Input file is empty: {path}")


def iter_json_chunks(
    source: Path,
    chunksize: int,
    dtypes: Dict[str, str],
) -> Iterable[pd.DataFrame]:
    # Yelp review file is NDJSON (one JSON object per line)
    for chunk in pd.read_json(  # pyright: ignore[reportCallIssue]
        source,
        lines=True,
        chunksize=chunksize,
        dtype=dtypes,  # pyright: ignore[reportArgumentType]
    ):
        yield chunk


def pass1_count_authors(
    source: Path,
    chunksize: int,
    min_review_length: int,
    required_cols: List[str],
) -> Counter[str]:
    logger = logging.getLogger(__name__)
    counts: Counter[str] = Counter()
    total_rows = 0
    total_len_filtered = 0
    cols_verified = False

    for i, chunk in enumerate(
        iter_json_chunks(
            source, chunksize, dtypes={"user_id": "string", "text": "string"}
        )
    ):
        if not cols_verified:
            missing = [c for c in required_cols if c not in chunk.columns]
            if missing:
                raise KeyError(f"Missing required columns in input: {missing}")
            cols_verified = True

        orig_rows = len(chunk)
        total_rows += orig_rows

        # Keep only needed fields and apply length filter
        chunk = chunk.loc[:, required_cols].dropna()
        chunk = chunk[chunk["text"].str.len().ge(min_review_length)]
        len_rows = len(chunk)
        total_len_filtered += len_rows

        # Update per-author counts
        counts.update(chunk["user_id"].tolist())

        if (i + 1) % 5 == 0 or orig_rows == 0:
            logger.info(
                "Pass 1 | chunks=%d rows=%s len>= %d rows=%s unique_authors=%s",
                i + 1,
                f"{total_rows:,}",
                min_review_length,
                f"{total_len_filtered:,}",
                f"{len(counts):,}",
            )

    logger.info(
        "Pass 1 complete | total_rows=%s len>= %d rows=%s unique_authors=%s",
        f"{total_rows:,}",
        min_review_length,
        f"{total_len_filtered:,}",
        f"{len(counts):,}",
    )
    return counts


def pass2_write_csv(
    source: Path,
    out_csv: Path,
    chunksize: int,
    min_review_length: int,
    keep_authors: Set[str],
    required_cols: List[str],
) -> int:
    logger = logging.getLogger(__name__)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    # Estimate total rows to write for progress (sum of kept author counts after length filter)
    # Note: caller can compute this from pass1 counts; we re-derive during writing to keep it simple.
    total_written_estimate = None  # optional; will be set by caller if provided

    first = True
    written = 0
    processed = 0
    cols_verified = False

    for i, chunk in enumerate(
        iter_json_chunks(
            source, chunksize, dtypes={"user_id": "string", "text": "string"}
        )
    ):
        if not cols_verified:
            missing = [c for c in required_cols if c not in chunk.columns]
            if missing:
                raise KeyError(f"Missing required columns in input: {missing}")
            cols_verified = True

        processed += len(chunk)

        chunk = chunk.loc[:, required_cols].dropna()
        chunk = chunk[chunk["text"].str.len().ge(min_review_length)]
        if not keep_authors:
            # Nothing to keep; short-circuit
            continue
        chunk = chunk[chunk["user_id"].isin(keep_authors)]
        if chunk.empty:
            if (i + 1) % 5 == 0:
                logger.info(
                    "Pass 2 | chunks=%d processed_rows=%s written_rows=%s",
                    i + 1,
                    f"{processed:,}",
                    f"{written:,}",
                )
            continue

        chunk = chunk.rename(columns={"user_id": "author"})
        chunk.to_csv(out_csv, mode="w" if first else "a", header=first, index=False)
        first = False

        written += len(chunk)

        if (i + 1) % 5 == 0:
            pct = ""
            if total_written_estimate:
                pct = f" ({written / total_written_estimate:.1%})"
            logger.info(
                "Pass 2 | chunks=%d processed_rows=%s written_rows=%s%s",
                i + 1,
                f"{processed:,}",
                f"{written:,}",
                pct,
            )

    logger.info("Pass 2 complete | written_rows=%s -> %s", f"{written:,}", out_csv)
    return written


def compute_keep_authors(counts: Counter[str], min_review_count: int) -> Set[str]:
    keep = {a for a, c in counts.items() if c >= min_review_count}
    logging.getLogger(__name__).info(
        "Authors meeting min_review_count=%d: %s", min_review_count, f"{len(keep):,}"
    )
    return keep


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prepare Yelp reviews CSV with low memory.")
    p.add_argument(
        "--source",
        type=Path,
        default=Path("data/raw/yelp_academic_dataset_review.json"),
    )
    p.add_argument("--out", type=Path, default=Path("data/yelp_reviews.csv"))
    p.add_argument("--min-review-count", type=int, default=3)
    p.add_argument("--min-review-length", type=int, default=200)
    p.add_argument("--chunksize", type=int, default=1_000_000)
    p.add_argument(
        "--log-level", type=str, default="DEBUG", help="DEBUG, INFO, WARNING, ERROR"
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    logger.info(
        "Config | source=%s out=%s min_count=%d min_length=%d chunksize=%s",
        args.source,
        args.out,
        args.min_review_count,
        args.min_review_length,
        f"{args.chunksize:,}",
    )

    validate_source(args.source)

    # Pass 1: count reviews per author after length filter
    counts = pass1_count_authors(
        source=args.source,
        chunksize=args.chunksize,
        min_review_length=args.min_review_length,
        required_cols=["user_id", "text"],
    )

    # Determine which authors to keep and how many rows we expect to write
    keep_authors = compute_keep_authors(counts, args.min_review_count)
    expected_rows = sum(counts[a] for a in keep_authors)
    logger.info("Expected rows to write (after filters): %s", f"{expected_rows:,}")

    # Pass 2: write filtered rows
    written = pass2_write_csv(
        source=args.source,
        out_csv=args.out,
        chunksize=args.chunksize,
        min_review_length=args.min_review_length,
        keep_authors=keep_authors,
        required_cols=["user_id", "text"],
    )

    if written != expected_rows:
        logger.warning(
            "Wrote %s rows, but expected %s. Differences can occur due to NA handling.",
            f"{written:,}",
            f"{expected_rows:,}",
        )

    logger.info("Done.")


if __name__ == "__main__":
    main()
