"""Encoding helpers for size-constrained exports."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Tuple

from PIL import Image


@dataclass(frozen=True)
class EncodeOptions:
    """Controls JPEG encoding and size targeting."""

    max_bytes: int = 2 * 1024 * 1024
    quality_min: int = 55
    quality_max: int = 92
    optimize: bool = True


def encode_jpeg_to_size(image: Image.Image, options: EncodeOptions) -> Tuple[bytes, int]:
    """Encode image to JPEG under max bytes using quality search."""
    if options.max_bytes <= 0:
        raise ValueError("max_bytes must be greater than 0")

    quality_min = max(1, min(options.quality_min, 100))
    quality_max = max(1, min(options.quality_max, 100))
    if quality_min > quality_max:
        raise ValueError("quality_min cannot exceed quality_max")

    rgb_image = image.convert("RGB")

    best_data = None
    best_quality = quality_min
    left, right = quality_min, quality_max

    while left <= right:
        quality = (left + right) // 2
        candidate = _encode_jpeg(rgb_image, quality, options.optimize)
        if len(candidate) <= options.max_bytes:
            best_data = candidate
            best_quality = quality
            left = quality + 1
        else:
            right = quality - 1

    if best_data is not None:
        return best_data, best_quality

    fallback = _encode_jpeg(rgb_image, quality_min, options.optimize)
    return fallback, quality_min


def _encode_jpeg(image: Image.Image, quality: int, optimize: bool) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=quality, optimize=optimize, progressive=True)
    return buffer.getvalue()
