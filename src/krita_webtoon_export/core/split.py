"""Image splitting logic for Webtoon slices."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from PIL import Image, ImageStat


@dataclass(frozen=True)
class SplitOptions:
    """Controls splitting behavior."""

    max_slice_height: int = 1280
    smart_cut: bool = True
    smart_cut_window: int = 80


def compute_slices(image: Image.Image, options: SplitOptions) -> List[Tuple[int, int]]:
    """Return list of (top, bottom) crop bounds."""
    if options.max_slice_height <= 0:
        raise ValueError("max_slice_height must be greater than 0")

    bounds: List[Tuple[int, int]] = []
    top = 0
    while top < image.height:
        hard_bottom = min(top + options.max_slice_height, image.height)
        if hard_bottom >= image.height:
            bounds.append((top, image.height))
            break

        bottom = hard_bottom
        if options.smart_cut:
            bottom = _choose_smart_cut(
                image=image, top=top, hard_bottom=hard_bottom, window=options.smart_cut_window
            )

        if bottom <= top:
            bottom = hard_bottom
        bounds.append((top, bottom))
        top = bottom

    return bounds


def _choose_smart_cut(image: Image.Image, top: int, hard_bottom: int, window: int) -> int:
    """Pick low-detail row near hard boundary."""
    search_min = max(top + 1, hard_bottom - max(1, window))
    search_max = min(image.height - 1, hard_bottom + max(1, window))

    best_row = hard_bottom
    best_score = None
    grayscale = image.convert("L")

    for row in range(search_min, search_max + 1):
        band_top = max(top, row - 1)
        band_bottom = min(image.height, row + 2)
        band = grayscale.crop((0, band_top, grayscale.width, band_bottom))
        stat = ImageStat.Stat(band)
        variance = stat.var[0] if stat.var else 0.0
        distance_penalty = abs(row - hard_bottom) * 0.5
        score = variance + distance_penalty

        if best_score is None or score < best_score:
            best_score = score
            best_row = row

    return best_row
