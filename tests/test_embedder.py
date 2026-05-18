import numpy as np
import pytest

from embedder.embedder import Embedder

@pytest.fixture(scope="module")
def embedder():
    return Embedder()

def test_embed_returns_numpy_array(embedder):
    result = embedder.embed("test sentence")
    assert isinstance(result, np.ndarray)

def test_embed_returns_correct_shape(embedder):
    result = embedder.embed("hello world")
    assert result.shape == (384,)

def test_embed_returns_float32(embedder):
    result = embedder.embed("another sentence")
    assert result.dtype == np.float32

def test_embed_many_returns_correct_shape(embedder):
    texts = ["first sentence", "second sentence", "third sentence"]
    result = embedder.embed_many(texts)
    assert result.shape == (3, 384)

def test_embed_many_returns_float32(embedder):
    result = embedder.embed_many(["a", "b"])
    assert result.dtype == np.float32

def test_same_text_produces_same_vector(embedder):
    text = "deterministic embedding test"
    v1 = embedder.embed(text)
    v2 = embedder.embed(text)
    np.testing.assert_array_equal(v1, v2)

def test_different_texts_produce_different_vectors(embedder):
    v1 = embedder.embed("the sky is blue")
    v2 = embedder.embed("database replication")
    assert not np.allclose(v1, v2)