# src/models/artifacts.py
# Defines generated dashboard artifact metadata.
# Connects to: src/main.py, src/services/dashboard.py
# Created: 2026-06-08

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DashboardArtifacts:
    """Generated files returned after a dashboard build.

    Parameters:
        output_dir: Folder where dashboard files were written.
        charts: Mapping of chart names to generated image paths.
        report_path: Generated HTML report path.
    """

    output_dir: Path
    charts: dict[str, Path]
    report_path: Path
