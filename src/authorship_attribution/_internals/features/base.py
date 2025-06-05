from abc import ABC, abstractmethod
import json
import re
import string
from typing import Any, Generator

from nltk import pos_tag, sent_tokenize, word_tokenize
from authorship_attribution._internals.types.aliases import Json, Sentence, Text


def ngrams(sequence: list[str], n: int, join_char: str = "") -> list[str]:
    if n <= 0:
        return []
    if len(sequence) < n:
        return []
    return [join_char.join(sequence[i : i + n]) for i in range(len(sequence) - n + 1)]


class Feature(ABC):
    @classmethod
    def name(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    @classmethod
    def file_name(cls) -> str:
        return f"{cls.name()}.json"

    def to_json(self) -> Json:
        return dict[str, Any](self)

    @classmethod
    def from_json(cls, data: Json) -> "Feature":
        return cls(**data)

    def to_file(self, path: str) -> None:
        json_data: Json = self.to_json()
        with open(path, "w") as file:
            json.dump(json_data, file, indent=4)

    @classmethod
    def from_file(cls, file_path: str) -> "Feature":
        with open(file_path, "r") as file:
            json_data = json.load(file)
            return cls.from_json(json_data)

    def __iter__(self) -> Generator[tuple[str, Any], Any, None]:
        for key in self.__dict__:
            yield key, getattr(self, key)


class FeatureExtractor(ABC):
    @abstractmethod
    def feature(self) -> Feature:
        pass


class TextFeatureExtractor(FeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__()
        self.text: Text = text


class SentencesFeatureExtractor(TextFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.sentences: list[Sentence] = sent_tokenize(text)


class WordsFeatureExtractor(TextFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.words = word_tokenize(text)


class PosTagFeatureExtractor(WordsFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.part_of_speech_tags = [tag for _, tag in pos_tag(self.words)]


class CharacterNgramsFeatureExtractor(TextFeatureExtractor):
    def __init__(self, text: Text, ngram_size: int) -> None:
        super().__init__(text)
        self.ngrams = ngrams(list[str](self.text), ngram_size)


class WordNgramsFeatureExtractor(WordsFeatureExtractor):
    def __init__(self, text: Text, ngram_size: int) -> None:
        super().__init__(text)
        self.ngrams = ngrams(self.words, ngram_size)


class PunctuationFeatureExtractor(TextFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.punctuations = [char for char in self.text if char in string.punctuation]
