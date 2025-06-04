def ngrams(collection: list[str], ngram_size: int) -> list[str]:
    return [
        "".join(collection[i : i + ngram_size])
        for i in range(len(collection))
        if i + ngram_size < len(collection)
    ]
