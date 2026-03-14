from PIL import Image

from krita_webtoon_export.core.resize import resize_to_width


def test_resize_to_target_width() -> None:
    img = Image.new("RGB", (1600, 3200), color="white")
    resized = resize_to_width(img, 800)
    assert resized.width == 800
    assert resized.height == 1600
