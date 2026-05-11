# Coursework 2: Search Engine Tool

Python command-line search tool for `https://quotes.toscrape.com/`.

## Coursework Scope Implemented

- Website crawling with same-domain link discovery
- Politeness window between requests (default: 6 seconds)
- Inverted index creation with per-word statistics:
  - document frequency (`doc_freq`)
  - per-page frequency (`freq`)
  - token positions (`positions`)
- Search commands:
  - `build`
  - `load`
  - `print <word>`
  - `find <one or more words>`

## Project Structure

- `src/crawler.py` - crawling logic
- `src/indexer.py` - tokenization and inverted index construction
- `src/search.py` - query and retrieval logic
- `src/main.py` - CLI entry point
- `tests/` - unit tests for crawler/indexer/search
- `data/` - generated index output

## Setup

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

Run from project root:

```bash
python src/main.py build
python src/main.py load
python src/main.py print nonsense
python src/main.py find good friends
```

Build options:

```bash
python src/main.py build --max-pages 5
python src/main.py build --base-url https://quotes.toscrape.com/
python src/main.py --index-path data/index.json build
```

## Output Data Format

`build` saves a JSON payload at `data/index.json` by default:

- `page_count`: number of crawled pages
- `term_count`: number of unique indexed terms
- `posting_count`: total number of postings
- `index`: inverted index map

## Testing

Install test dependency via `requirements.txt` and run:

```bash
python -m pytest -q
```

Recommended (with coverage):

```bash
python -m pytest --maxfail=1 --disable-warnings -q
```

### Current test focus

- URL normalization and domain filtering
- Crawler continuation on network failure
- Tokenization and case-insensitive indexing
- Frequency/position correctness in inverted index
- Single-term and multi-term query behaviour
- Missing terms and empty-query handling

## Notes

- Search is case-insensitive.
- `find` currently uses AND semantics for multi-word queries (all words must exist in the page).
- Keep at least a 6-second politeness window for real target-site crawling.
