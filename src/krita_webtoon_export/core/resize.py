"""Image resize helpers."""

from __future__ import annotations

from PIL import Image


def resize_to_width(image: Image.Image, target_width: int) -> Image.Image:
    """Resize image to target width while preserving aspect ratio."""
    if target_width <= 0:
        raise ValueError("target_width must be greater than 0")

    if image.width == target_width:
        return image.copy()

    scale = target_width / image.width
    target_height = max(1, int(round(image.height * scale)))
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS)
