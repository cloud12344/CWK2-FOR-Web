"""Search and query logic for inverted index."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Set

from indexer import tokenize


def load_index_file(index_path: Path) -> Dict[str, Any]:
    """Load serialized index payload from disk."""
    data = json.loads(index_path.read_text(encoding="utf-8"))
    return data


def print_word(index: Dict[str, Any], word: str) -> Dict[str, Any] | None:
    """Return posting details for a word (case-insensitive)."""
    normalized = word.lower().strip()
    if not normalized:
        return None
    return index.get(normalized)


def find_query(index: Dict[str, Any], terms: List[str]) -> List[str]:
    """Find URLs containing all query terms (AND semantics)."""
    normalized_terms = _normalize_query_terms(terms)
    if not normalized_terms:
        return []

    page_sets: List[Set[str]] = []
    for term in normalized_terms:
        posting = index.get(term)
        if not posting:
            return []
        page_sets.append(set(posting["pages"].keys()))

    matched = set.intersection(*page_sets) if page_sets else set()
    return sorted(matched)


def _normalize_query_terms(terms: List[str]) -> List[str]:
    """Normalize query terms using the same tokenization as indexing."""
    joined = " ".join(terms).strip().lower()
    if not joined:
        return []
    return tokenize(joined)
