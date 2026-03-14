"""CLI entry point for local testing outside Krita."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from .core.pipeline import ExportSettings, run_export_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export a long image into Webtoon slices")
    parser.add_argument("input", type=Path, help="Path to input image")
    parser.add_argument("output", type=Path, help="Output directory")
    parser.add_argument("--width", type=int, default=800, help="Target output width")
    parser.add_argument("--max-height", type=int, default=1280, help="Max slice height")
    parser.add_argument(
        "--max-bytes", type=int, default=2 * 1024 * 1024, help="Max bytes per slice"
    )
    parser.add_argument("--quality-min", type=int, default=55, help="Minimum JPEG quality")
    parser.add_argument("--quality-max", type=int, default=92, help="Maximum JPEG quality")
    parser.add_argument("--no-smart-cut", action="store_true", help="Disable smart cut")
    parser.add_argument("--smart-window", type=int, default=80, help="Smart cut window (px)")
    parser.add_argument("--prefix", default="webtoon", help="Output file prefix")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    settings = ExportSettings(
        target_width=args.width,
        max_slice_height=args.max_height,
        max_bytes=args.max_bytes,
        quality_min=args.quality_min,
        quality_max=args.quality_max,
        smart_cut=not args.no_smart_cut,
        smart_cut_window=args.smart_window,
        output_prefix=args.prefix,
    )

    source = Image.open(args.input)
    result = run_export_pipeline(source_image=source, output_dir=args.output, settings=settings)
    print(f"Exported {len(result.slices)} slices to {result.output_dir}")


if __name__ == "__main__":
    main()
