def ngrams(sequence: list[str], n: int, join_char: str = "") -> list[str]:
    if n <= 0:
        return []
    if len(sequence) < n:
        return []
    return [join_char.join(sequence[i : i + n]) for i in range(len(sequence) - n + 1)]
