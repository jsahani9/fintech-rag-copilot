from unittest.mock import MagicMock
from src.rag import format_context, answer, answer_with_sources


def _make_doc(text, source="test.pdf", page=1):
    doc = MagicMock()
    doc.page_content = text
    doc.metadata = {"source": source, "page": page}
    return doc


def test_format_context_basic():
    docs = [_make_doc("Capital requirements are set at 8%.")]
    result = format_context(docs)
    assert "[1]" in result
    assert "Capital requirements" in result
    assert "test.pdf" in result


def test_format_context_multiple_docs():
    docs = [
        _make_doc("Liquidity coverage ratio must exceed 100%.", source="basel.pdf", page=3),
        _make_doc("Operational risk must be managed proactively.", source="osfi.pdf", page=7),
    ]
    result = format_context(docs)
    assert "[1]" in result
    assert "[2]" in result
    assert "Liquidity" in result
    assert "Operational" in result


def test_format_context_truncates_at_max_chars():
    long_text = "A" * 6000
    docs = [_make_doc(long_text), _make_doc(long_text), _make_doc(long_text)]
    result = format_context(docs, max_chars=12000)
    # Should not exceed roughly max_chars + one block header overhead
    assert len(result) < 14000


def test_format_context_empty():
    assert format_context([]) == ""


def test_answer_calls_retrieve_and_claude(monkeypatch):
    mock_docs = [_make_doc("Board oversight is required.", source="gov.pdf", page=2)]
    monkeypatch.setattr("src.rag.retrieve", lambda q, k: mock_docs)
    monkeypatch.setattr("src.rag.ask_claude", lambda q, ctx: "Board must oversee risk [1].")

    result = answer("What does the board do?", k=3)
    assert result == "Board must oversee risk [1]."


def test_answer_with_sources_returns_text_and_sources(monkeypatch):
    mock_docs = [
        _make_doc("Capital at 8%.", source="basel.pdf", page=5),
        _make_doc("Liquidity coverage.", source="osfi.pdf", page=2),
    ]
    monkeypatch.setattr("src.rag.retrieve", lambda q, k: mock_docs)
    monkeypatch.setattr("src.rag.ask_claude", lambda q, ctx: "Capital must be 8% [1].")

    text, sources = answer_with_sources("What is capital?", k=2)
    assert text == "Capital must be 8% [1]."
    assert sources == [
        {"source": "basel.pdf", "page": 5},
        {"source": "osfi.pdf", "page": 2},
    ]
