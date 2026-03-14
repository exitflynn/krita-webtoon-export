# Krita-Webtoon-Export

Krita-Webtoon-Export helps artists export long-scroll comic pages into Webtoon-ready image slices.

Webtoon has strict upload constraints, including 800px output width and per-image size limitations. The goal of this project is to provide a Krita-native workflow so artists can export directly from their document without relying on third-party conversion tools.

## V1 Scope

V1 focuses on one workflow:

- Single long canvas in Krita -> multiple Webtoon-ready slices.
- Output width fixed to 800px.
- Configurable max slice height.
- Per-slice JPEG size targeting using adaptive quality.
- Optional smart cut around hard split boundaries.

## Current Project Layout

- `src/krita_webtoon_export/core/`: Pure Python processing pipeline.
- `src/krita_webtoon_export/plugin/`: Krita plugin integration scaffold.
- `src/krita_webtoon_export/cli.py`: Local CLI for development and testing.
- `tests/`: Unit tests for resize, split, encode, and end-to-end pipeline behavior.

## Getting Started

Requirements:

- Python 3.10+

Install in editable mode with dev tools:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run local CLI export:

```bash
webtoon-export path/to/input.png path/to/output-dir
```

Example with explicit options:

```bash
webtoon-export path/to/input.png path/to/output-dir \
  --width 800 \
  --max-height 1280 \
  --max-bytes 2097152 \
  --quality-min 55 \
  --quality-max 92 \
  --smart-window 80 \
  --prefix episode1
```

## Notes

- Smart cut currently uses a local low-detail heuristic near each hard boundary.