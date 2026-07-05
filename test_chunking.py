from main import chunk_text


def test_short_text_returns_one_chunk():
    """Text well under the limit should produce exactly one chunk."""
    text = "This is a short sentence."
    result = chunk_text(text)
    assert len(result) == 1


def test_long_text_returns_multiple_chunks():
    """Text over the limit should split into more than one chunk."""
    text = "word " * 1000
    result = chunk_text(text)
    assert len(result) > 1


def test_no_chunk_exceeds_the_limit():
    """Every chunk must be at or under max_chars."""
    text = "word " * 1000
    result = chunk_text(text, max_chars=3000)
    for chunk in result:
        assert len(chunk) <= 3000


def test_empty_text_returns_empty_list():
    """Empty input should give an empty list, not [''] ."""
    result = chunk_text("")
    assert result == []


def test_no_words_are_lost():
    """Splitting then recounting should preserve every word."""
    text = "word " * 1000
    result = chunk_text(text)
    total_words = 0
    for chunk in result:
        total_words += len(chunk.split())
    assert total_words == 1000