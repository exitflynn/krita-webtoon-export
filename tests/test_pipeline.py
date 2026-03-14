from pathlib import Path

from PIL import Image

from krita_webtoon_export.core.pipeline import ExportSettings, run_export_pipeline


def test_pipeline_exports_expected_slices(tmp_path: Path) -> None:
    img = Image.new("RGB", (1200, 4000), color="white")
    result = run_export_pipeline(
        source_image=img,
        output_dir=tmp_path,
        settings=ExportSettings(
            target_width=800,
            max_slice_height=1280,
            max_bytes=500_000,
            quality_min=55,
            quality_max=92,
            smart_cut=False,
            output_prefix="episode1",
        ),
    )

    assert len(result.slices) == 3
    assert result.slices[0].file_path.name == "episode1_001.jpg"
    assert result.slices[0].width == 800
    assert result.slices[0].height == 1280
    assert result.slices[0].bytes_written <= 500_000

    for item in result.slices:
        assert item.file_path.exists()
