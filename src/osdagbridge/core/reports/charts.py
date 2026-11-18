"""Render report charts from design and quantity data."""

from math import isfinite
from pathlib import Path

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from .styles import (
    CHART_BAR_COLOR,
    CHART_DPI,
    CHART_LIMIT_COLOR,
    QUANTITY_CHART_SIZE,
    UR_CHART_SIZE,
    chart_figure,
)


def report_number(value):
    """Return a finite, non-negative value or None for missing report data."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if isfinite(number) and number >= 0 else None


def _bar_panel(ax, labels, values, ylabel, limit=None):
    positions = range(len(labels))
    bars = ax.bar(positions, [value or 0 for value in values], color=CHART_BAR_COLOR)
    decimals = 3 if limit is not None else 2
    for bar, value in zip(bars, values):
        label = "N/A" if value is None else f"{value:.{decimals}f}"
        ax.annotate(label, (bar.get_x() + bar.get_width() / 2, value or 0),
                    xytext=(0, 5), textcoords="offset points", ha="center")
    if limit is not None:
        ax.axhline(limit, color=CHART_LIMIT_COLOR, linestyle="--", label=f"UR = {limit:.1f}")
        ax.legend(loc="upper right")
    ax.set_xticks(list(positions), labels)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, max(limit or 0, max((v or 0 for v in values)), 0.01) * 1.25)
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)


def utilization_chart(ratios, image_dir):
    figure = Figure(figsize=UR_CHART_SIZE, layout="constrained")
    FigureCanvasAgg(figure)
    _bar_panel(figure.subplots(),
               ["Steel plate\ngirders", "Concrete\ndeck slab", "Cross\nbracing", "End\ndiaphragms"],
               ratios, "Utilization ratio", limit=1.0)
    path = Path(image_dir) / "utilization.png"
    figure.savefig(path, dpi=CHART_DPI)
    return chart_figure(path, "Governing utilization ratio by component (N/A: no result)")


def material_charts(steel, concrete, reinforcement, image_dir):
    figure = Figure(figsize=QUANTITY_CHART_SIZE, layout="constrained")
    FigureCanvasAgg(figure)
    _bar_panel(figure.subplots(), ["Girders", "Cross bracing", "End diaphragms"],
               steel, "Structural steel (t)")
    steel_path = Path(image_dir) / "structural_steel.png"
    figure.savefig(steel_path, dpi=CHART_DPI)

    figure = Figure(figsize=QUANTITY_CHART_SIZE, layout="constrained")
    FigureCanvasAgg(figure)
    concrete_ax, reinforcement_ax = figure.subplots(ncols=2)
    _bar_panel(concrete_ax, ["Deck concrete"], [concrete], "Concrete volume (m³)")
    _bar_panel(reinforcement_ax, ["Deck reinforcement"], [reinforcement], "Reinforcement steel (t)")
    deck_path = Path(image_dir) / "deck_materials.png"
    figure.savefig(deck_path, dpi=CHART_DPI)

    return "\n".join((
        chart_figure(steel_path, "Structural steel mass by component in tonnes (t)"),
        chart_figure(deck_path, "Deck concrete volume in cubic metres and reinforcement mass in tonnes"),
    ))
