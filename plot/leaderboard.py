"""Shared helpers for reading the README leaderboards and loading plot config."""

import re
from pathlib import Path

import yaml

PLOT_DIR = Path(__file__).resolve().parent

# Categorical palette, assigned in fixed order (never cycled). The order keeps
# the two near-identical navies apart so adjacent bars stay distinguishable.
PALETTE = [
    "#0C1429",  # navy
    "#61BD73",  # mid green
    "#172037",  # navy (lighter)
    "#38D611",  # bright green
    "#057201",  # dark green
    "#C5EFA4",  # pale green
]

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")


def load_config(path=None):
    path = Path(path) if path else PLOT_DIR / "config.yaml"
    with open(path) as f:
        config = yaml.safe_load(f)
    config["_dir"] = path.resolve().parent
    return config


def clean_name(cell):
    """Strip markdown links and footnote asterisks: '[Foo](url)*' -> 'Foo'."""
    return _LINK.sub(r"\1", cell).rstrip("*").strip()


def parse_value(cell):
    """'64%' -> 64.0, '56%**' -> 56.0, '0.82' -> 0.82, '6,022' -> 6022.0, '—' -> None."""
    cell = cell.strip().rstrip("*").rstrip("%").replace(",", "")
    try:
        return float(cell)
    except ValueError:
        return None


def read_table(readme_path, heading):
    """Return the rows of the first markdown table under a `## heading` section.

    Each row is a dict keyed by column header. The name column is cleaned so it
    can be matched against the names listed in config.yaml.
    """
    lines = Path(readme_path).read_text().splitlines()
    start = next(
        (i for i, l in enumerate(lines) if l.startswith("## ") and heading in l),
        None,
    )
    if start is None:
        raise ValueError(f"No section containing {heading!r} in {readme_path}")

    table = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if line.strip().startswith("|"):
            table.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif table:
            break

    header, rows = table[0], table[2:]  # skip the |---| separator row
    return [dict(zip(header, row)) for row in rows]


def select_rows(rows, name_column, names):
    """Pick rows by name, in the order given in config (so colors stay stable)."""
    by_name = {clean_name(r[name_column]): r for r in rows}
    missing = [n for n in names if n not in by_name]
    if missing:
        available = "\n  ".join(by_name)
        raise KeyError(
            f"Not found in leaderboard: {missing}\nAvailable names:\n  {available}"
        )
    if len(names) > len(PALETTE):
        raise ValueError(
            f"{len(names)} series selected; at most {len(PALETTE)} can be told apart "
            "by color. Split them across multiple plots."
        )
    return [by_name[n] for n in names]


def style_axes(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    ax.tick_params(colors=TEXT_SECONDARY, length=0)
    ax.yaxis.grid(True, color=GRIDLINE, linewidth=0.8)
    ax.set_axisbelow(True)
