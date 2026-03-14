"""Orchestrates resize, split, and encode steps."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from PIL import Image

from .encode import EncodeOptions, encode_jpeg_to_size
from .resize import resize_to_width
from .split import SplitOptions, compute_slices


@dataclass(frozen=True)
class ExportSettings:
    """User-facing export settings."""

    target_width: int = 800
    max_slice_height: int = 1280
    max_bytes: int = 2 * 1024 * 1024
    quality_min: int = 55
    quality_max: int = 92
    smart_cut: bool = True
    smart_cut_window: int = 80
    output_prefix: str = "webtoon"


@dataclass(frozen=True)
class ExportedSlice:
    """Metadata for one exported slice."""

    file_path: Path
    width: int
    height: int
    bytes_written: int
    quality: int


@dataclass(frozen=True)
class ExportResult:
    """Metadata describing export output."""

    output_dir: Path
    slices: List[ExportedSlice]


def run_export_pipeline(
    source_image: Image.Image, output_dir: Path, settings: ExportSettings
) -> ExportResult:
    """Export a single long image into Webtoon-ready JPEG slices."""
    output_dir.mkdir(parents=True, exist_ok=True)

    resized = resize_to_width(source_image, settings.target_width)
    split_options = SplitOptions(
        max_slice_height=settings.max_slice_height,
        smart_cut=settings.smart_cut,
        smart_cut_window=settings.smart_cut_window,
    )
    bounds = compute_slices(resized, split_options)
    encode_options = EncodeOptions(
        max_bytes=settings.max_bytes,
        quality_min=settings.quality_min,
        quality_max=settings.quality_max,
    )

    exported: List[ExportedSlice] = []
    for index, (top, bottom) in enumerate(bounds, start=1):
        piece = resized.crop((0, top, resized.width, bottom))
        data, quality = encode_jpeg_to_size(piece, encode_options)
        file_name = f"{settings.output_prefix}_{index:03d}.jpg"
        file_path = output_dir / file_name
        file_path.write_bytes(data)

        exported.append(
            ExportedSlice(
                file_path=file_path,
                width=piece.width,
                height=piece.height,
                bytes_written=len(data),
                quality=quality,
            )
        )

    return ExportResult(output_dir=output_dir, slices=exported)
