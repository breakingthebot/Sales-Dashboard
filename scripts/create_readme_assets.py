# scripts/create_readme_assets.py
# Generates README visual assets for the Streamlit dashboard workflow.
# Connects to: README.md, docs/assets/
# Created: 2026-06-08

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle


ASSET_PATH = Path("docs/assets/streamlit-workflow.png")
CANVAS_SIZE = (15, 8.2)
BACKGROUND = "#F8FAFC"
INK = "#111827"
MUTED = "#6B7280"
LINE = "#E5E7EB"
BLUE = "#2563EB"
GREEN = "#059669"
ORANGE = "#D97706"


def draw_card(ax: plt.Axes, xy: tuple[float, float], width: float, height: float, title: str, body: str) -> None:
    """Draw a rounded workflow card.

    Parameters:
        ax: Matplotlib axes to draw on.
        xy: Lower-left card coordinate.
        width: Card width.
        height: Card height.
        title: Card title text.
        body: Card body text.

    Returns:
        None.
    """

    card = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.035,rounding_size=0.08",
        linewidth=1.1,
        edgecolor=LINE,
        facecolor="#FFFFFF",
    )
    ax.add_patch(card)
    ax.text(xy[0] + 0.22, xy[1] + height - 0.35, title, fontsize=14, fontweight="bold", color=INK)
    wrapped_body = "\n".join(textwrap.wrap(body, width=26))
    ax.text(xy[0] + 0.22, xy[1] + height - 0.74, wrapped_body, fontsize=10.5, color=MUTED, linespacing=1.35)


def draw_button(ax: plt.Axes, xy: tuple[float, float], width: float, label: str, color: str) -> None:
    """Draw a compact button-style element.

    Parameters:
        ax: Matplotlib axes to draw on.
        xy: Lower-left button coordinate.
        width: Button width.
        label: Button text.
        color: Button fill color.

    Returns:
        None.
    """

    button = FancyBboxPatch(
        xy,
        width,
        0.34,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        linewidth=0,
        facecolor=color,
    )
    ax.add_patch(button)
    ax.text(xy[0] + 0.12, xy[1] + 0.105, label, fontsize=8.8, color="#FFFFFF", fontweight="bold")


def draw_bar_chart(ax: plt.Axes) -> None:
    """Draw a lightweight chart preview.

    Parameters:
        ax: Matplotlib axes to draw on.

    Returns:
        None.
    """

    x_start = 8.05
    y_start = 1.35
    widths = [0.35, 0.58, 0.46, 0.8, 0.68]
    for index, width in enumerate(widths):
        ax.add_patch(Rectangle((x_start, y_start + index * 0.28), width, 0.16, color=GREEN, alpha=0.9))


def generate_streamlit_workflow_asset(output_path: Path = ASSET_PATH) -> Path:
    """Generate the Streamlit workflow README image.

    Parameters:
        output_path: Destination image path.

    Returns:
        Generated image path.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=CANVAS_SIZE)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.2)
    ax.axis("off")

    ax.text(0.55, 7.48, "Sales Dashboard Streamlit Workflow", fontsize=25, fontweight="bold", color=INK)
    ax.text(
        0.58,
        7.08,
        "Generate sample data, upload a CSV, inspect quality checks, filter sales, and export results.",
        fontsize=12.5,
        color=MUTED,
    )

    draw_card(ax, (0.7, 4.75), 4.2, 1.7, "1. Prepare CSV", "Download a template or generated sample.")
    draw_button(ax, (0.95, 5.0), 1.55, "Template CSV", BLUE)
    draw_button(ax, (2.75, 5.0), 1.55, "Sample CSV", GREEN)

    draw_card(ax, (5.25, 4.75), 4.2, 1.7, "2. Upload + Map", "Upload a CSV or map custom headers.")
    draw_button(ax, (5.5, 5.0), 1.05, "Upload", BLUE)
    draw_button(ax, (6.75, 5.0), 1.42, "Column map", ORANGE)

    draw_card(ax, (9.8, 4.75), 4.2, 1.7, "3. Validate", "Review data quality before charts render.")
    draw_button(ax, (10.05, 5.0), 1.55, "Quality report", GREEN)

    draw_card(ax, (0.7, 1.05), 6.4, 2.8, "Interactive Dashboard", "Filters update KPIs, charts, and tables.")
    metrics = [("Revenue", "$128K"), ("Orders", "100"), ("Units", "1,047")]
    for index, (label, value) in enumerate(metrics):
        x_pos = 1.0 + index * 1.65
        ax.text(x_pos, 2.94, label, fontsize=9.5, color=MUTED)
        ax.text(x_pos, 2.62, value, fontsize=16, color=INK, fontweight="bold")
    for index, height in enumerate([0.35, 0.7, 0.52, 1.0, 0.82]):
        ax.add_patch(Rectangle((1.05 + index * 0.58, 1.55), 0.28, height, color=BLUE, alpha=0.9))
    ax.text(1.0, 1.28, "Monthly revenue", fontsize=10.5, color=MUTED)

    draw_card(ax, (7.65, 1.05), 6.35, 2.8, "Exports", "Download CSV tables and chart PNG files.")
    draw_bar_chart(ax)
    draw_button(ax, (10.3, 1.35), 1.1, "CSV", BLUE)
    draw_button(ax, (11.65, 1.35), 1.1, "PNG", GREEN)

    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


if __name__ == "__main__":
    path = generate_streamlit_workflow_asset()
    print(f"README asset written to: {path}")
