import pandas as pd
from pandas import DataFrame, Series
from typing import cast, List

MIN_REVIEW_COUNT = 3
MIN_REVIEW_LENGTH = 200

df: DataFrame = cast(
    DataFrame,
    pd.read_csv(  # pyright: ignore[reportCallIssue]
        "data/raw/raw_amazon_reviews.csv",
        usecols=["userName", "reviewText"],  # pyright: ignore[reportArgumentType]
    ),
)
df = df.loc[:, ["userName", "reviewText"]].dropna().copy()
df = df.rename(columns={"userName": "author", "reviewText": "text"})

counts: Series = df["author"].value_counts()
keep_authors: List[str] = counts.loc[counts >= MIN_REVIEW_COUNT].index.to_list()
df = df.loc[df["author"].isin(keep_authors)].copy()

df = df.loc[df["text"].str.len().ge(MIN_REVIEW_LENGTH)].copy()

df.to_csv("data/reviews.csv", index=False)
