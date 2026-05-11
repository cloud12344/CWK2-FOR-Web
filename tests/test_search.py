"""Tests for search module."""

from __future__ import annotations

from src.search import find_query, print_word


def _sample_index() -> dict:
    return {
        "good": {
            "doc_freq": 2,
            "pages": {
                "u1": {"freq": 2, "positions": [0, 2]},
                "u2": {"freq": 1, "positions": [1]},
            },
        },
        "friends": {
            "doc_freq": 2,
            "pages": {
                "u1": {"freq": 1, "positions": [1]},
                "u3": {"freq": 1, "positions": [0]},
            },
        },
    }


def test_print_word_is_case_insensitive() -> None:
    index = _sample_index()
    result = print_word(index=index, word="GOOD")
    assert result is not None
    assert result["doc_freq"] == 2


def test_print_word_returns_none_for_empty_input() -> None:
    index = _sample_index()
    assert print_word(index=index, word="   ") is None


def test_find_query_single_term() -> None:
    index = _sample_index()
    assert find_query(index=index, terms=["good"]) == ["u1", "u2"]


def test_find_query_multi_term_intersection() -> None:
    index = _sample_index()
    assert find_query(index=index, terms=["good", "friends"]) == ["u1"]


def test_find_query_returns_empty_if_any_term_missing() -> None:
    index = _sample_index()
    assert find_query(index=index, terms=["good", "missing"]) == []
