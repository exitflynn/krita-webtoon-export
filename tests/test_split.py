from PIL import Image, ImageDraw

from krita_webtoon_export.core.split import SplitOptions, compute_slices


def test_split_without_smart_cut_uses_hard_bounds() -> None:
    img = Image.new("RGB", (800, 3000), color="white")
    bounds = compute_slices(
        img, SplitOptions(max_slice_height=1280, smart_cut=False, smart_cut_window=80)
    )
    assert bounds == [(0, 1280), (1280, 2560), (2560, 3000)]


def test_split_with_smart_cut_prefers_quiet_band() -> None:
    img = Image.new("RGB", (800, 2700), color="white")
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 1230, 799, 1255), fill="black")
    draw.rectangle((0, 1282, 799, 1304), fill="white")
    draw.rectangle((0, 1310, 799, 1350), fill="black")

    bounds = compute_slices(
        img, SplitOptions(max_slice_height=1280, smart_cut=True, smart_cut_window=40)
    )
    first_top, first_bottom = bounds[0]
    assert first_top == 0
    assert 1278 <= first_bottom <= 1305
