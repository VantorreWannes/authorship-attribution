from authorship_attribution import (
    BookId,
    AuthorId,
    DateRange,
    BaseDataClass,
    Author,
    Book,
    Json,
    Sentence,
    Word,
    Feature,
    PrimitiveFeature,
    AverageWordLengthFeature,
    FeatureExtractor,
    LexicalFeatureExtractor,
    WordFeatureExtractor,
    SentenceFeatureExtractor,
    AverageWordLengthFeatureExtractor,
)


def test_imports():
    assert BookId is not None
    assert AuthorId is not None
    assert DateRange is not None
    assert BaseDataClass is not None
    assert Author is not None
    assert Book is not None
    assert Json is not None
    assert Sentence is not None
    assert Word is not None
    assert Feature is not None
    assert PrimitiveFeature is not None
    assert AverageWordLengthFeature is not None
    assert FeatureExtractor is not None
    assert LexicalFeatureExtractor is not None
    assert WordFeatureExtractor is not None
    assert SentenceFeatureExtractor is not None
    assert AverageWordLengthFeatureExtractor is not None
