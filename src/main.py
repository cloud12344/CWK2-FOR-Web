"""Command-line interface for the coursework search tool."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from crawler import crawl_site

DEFAULT_BASE_URL = "https://quotes.toscrape.com/"
DEFAULT_INDEX_PATH = Path("data") / "index.json"


def handle_build(args: argparse.Namespace) -> None:
    """Stage 1 build command: crawl only, save raw page dump."""
    pages = crawl_site(base_url=args.base_url, max_pages=args.max_pages)

    payload: Dict[str, Any] = {
        "stage": "stage-1-crawl-only",
        "base_url": args.base_url,
        "page_count": len(pages),
        "pages": pages,
    }

    args.index_path.parent.mkdir(parents=True, exist_ok=True)
    args.index_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Build completed (stage 1). Crawled pages: {len(pages)}")
    print(f"Saved crawl output to: {args.index_path}")


def handle_load(args: argparse.Namespace) -> None:
    if not args.index_path.exists():
        print(f"Index file not found: {args.index_path}")
        return

    data = json.loads(args.index_path.read_text(encoding="utf-8"))
    print("Load completed.")
    print(f"File: {args.index_path}")
    print(f"Stored pages: {data.get('page_count', 0)}")


def handle_print(args: argparse.Namespace) -> None:
    print(f"print command placeholder. Requested word: {args.word}")


def handle_find(args: argparse.Namespace) -> None:
    if not args.terms:
        print("Empty query is not allowed.")
        return
    print(f"find command placeholder. Requested terms: {' '.join(args.terms)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Coursework 2 Search Engine Tool")
    parser.add_argument("--index-path", type=Path, default=DEFAULT_INDEX_PATH)

    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser_cmd = subparsers.add_parser("build", help="Crawl site and build index")
    build_parser_cmd.add_argument("--base-url", default=DEFAULT_BASE_URL)
    build_parser_cmd.add_argument("--max-pages", type=int, default=None)
    build_parser_cmd.set_defaults(func=handle_build)

    load_parser_cmd = subparsers.add_parser("load", help="Load index from disk")
    load_parser_cmd.set_defaults(func=handle_load)

    print_parser_cmd = subparsers.add_parser("print", help="Print index data for a word")
    print_parser_cmd.add_argument("word")
    print_parser_cmd.set_defaults(func=handle_print)

    find_parser_cmd = subparsers.add_parser("find", help="Find pages matching terms")
    find_parser_cmd.add_argument("terms", nargs="*")
    find_parser_cmd.set_defaults(func=handle_find)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
