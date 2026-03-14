from PIL import Image

from krita_webtoon_export.core.encode import EncodeOptions, encode_jpeg_to_size


def test_encode_returns_bytes_and_quality() -> None:
    img = Image.new("RGB", (800, 800), color="white")
    data, quality = encode_jpeg_to_size(
        img,
        EncodeOptions(max_bytes=250_000, quality_min=55, quality_max=92),
    )
    assert isinstance(data, bytes)
    assert 55 <= quality <= 92
    assert len(data) <= 250_000
