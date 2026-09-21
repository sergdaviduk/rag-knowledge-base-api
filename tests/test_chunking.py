from app.services import split_text


def test_short_text_is_one_chunk():
    assert split_text("hello world") == ["hello world"]


def test_long_text_is_split_with_overlap():
    chunks = split_text("a" * 2000, chunk_size=500, overlap=50)
    assert len(chunks) > 1
    assert all(len(chunk) <= 500 for chunk in chunks)


def test_whitespace_is_normalized():
    assert split_text("hello\n\n   world") == ["hello world"]
