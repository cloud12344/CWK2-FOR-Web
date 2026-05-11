"""Tests for indexer module."""

from __future__ import annotations

from src.indexer import build_inverted_index, index_summary, tokenize


def test_tokenize_is_case_insensitive() -> None:
    text = "Good good FRIENDS"
    assert tokenize(text) == ["good", "good", "friends"]


def test_build_inverted_index_stores_freq_and_positions() -> None:
    pages = [
        {
            "url": "https://quotes.toscrape.com/page/1",
            "html": """
                <html><body>
                  <div class='quote'>
                    <span class='text'>Good friends good books</span>
                    <small class='author'>Alice</small>
                  </div>
                </body></html>
            """,
        },
        {
            "url": "https://quotes.toscrape.com/page/2",
            "html": """
                <html><body>
                  <div class='quote'>
                    <span class='text'>Friends are good</span>
                    <small class='author'>Bob</small>
                  </div>
                </body></html>
            """,
        },
    ]

    index = build_inverted_index(pages)

    assert index["good"]["doc_freq"] == 2
    assert index["good"]["pages"]["https://quotes.toscrape.com/page/1"]["freq"] == 2
    assert index["good"]["pages"]["https://quotes.toscrape.com/page/1"]["positions"] == [0, 2]

    assert index["friends"]["doc_freq"] == 2
    assert index["friends"]["pages"]["https://quotes.toscrape.com/page/2"]["positions"] == [0]


def test_index_summary_counts_terms_and_postings() -> None:
    index = {
        "good": {"doc_freq": 2, "pages": {"u1": {"freq": 1, "positions": [0]}, "u2": {"freq": 1, "positions": [2]}}},
        "friends": {"doc_freq": 1, "pages": {"u1": {"freq": 1, "positions": [1]}}},
    }

    term_count, posting_count = index_summary(index)
    assert term_count == 2
    assert posting_count == 3
