"""Settings model shared by UI and pipeline mapping."""

from __future__ import annotations

from dataclasses import dataclass

from krita_webtoon_export.core.pipeline import ExportSettings


@dataclass
class PluginSettings:
    """Persisted plugin defaults for MVP."""

    target_width: int = 800
    max_slice_height: int = 1280
    max_bytes: int = 2 * 1024 * 1024
    quality_min: int = 55
    quality_max: int = 92
    smart_cut: bool = True
    smart_cut_window: int = 80
    output_prefix: str = "webtoon"

    def to_export_settings(self) -> ExportSettings:
        return ExportSettings(
            target_width=self.target_width,
            max_slice_height=self.max_slice_height,
            max_bytes=self.max_bytes,
            quality_min=self.quality_min,
            quality_max=self.quality_max,
            smart_cut=self.smart_cut,
            smart_cut_window=self.smart_cut_window,
            output_prefix=self.output_prefix,
        )
