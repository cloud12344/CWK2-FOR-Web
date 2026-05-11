# Coursework 2: Search Engine Tool

This repository contains a staged implementation of the COMP/XJCO3011 coursework.

Current status: **Stage 0 + Stage 1 completed**
- Stage 0: project structure and command-line skeleton
- Stage 1: website crawler with politeness window and basic error handling

## Project Structure

- `src/crawler.py`: crawler implementation
- `src/indexer.py`: placeholder for inverted index (next stage)
- `src/search.py`: placeholder for search logic (next stage)
- `src/main.py`: CLI entry point (`build`, `load`, `print`, `find`)
- `tests/`: unit tests
- `data/`: generated output files (crawl/index)

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

### Useful build options

```bash
python src/main.py build --max-pages 5
python src/main.py build --base-url https://quotes.toscrape.com/
```

## Testing

```bash
pytest -q
```

## Notes

- The crawler enforces a politeness delay of at least 6 seconds between requests by default.
- Full inverted index build and real search behaviour will be implemented in the next stage.
