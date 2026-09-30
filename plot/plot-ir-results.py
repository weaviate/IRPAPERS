"""Grouped bar chart of retrieval results from the README leaderboard.

Each Recall@k metric is a group on the x-axis; within a group there is one bar
per retriever, colored consistently and identified in the legend.

    uv run python3 plot/plot-ir-results.py [--config plot/config.yaml] [--show]
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

from leaderboard import (
    PALETTE, SURFACE, TEXT_PRIMARY, TEXT_SECONDARY,
    load_config, parse_value, read_table, select_rows, style_axes, clean_name,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", default=None, help="Path to config.yaml")
    parser.add_argument("--show", action="store_true", help="Open an interactive window")
    args = parser.parse_args()

    config = load_config(args.config)
    cfg = config["ir"]
    readme = config["_dir"] / config["readme"]

    rows = read_table(readme, cfg["section"])
    selected = select_rows(rows, cfg["name_column"], cfg["retrievers"])
    metrics = cfg["metrics"]

    n = len(selected)
    group_width = 0.8
    bar_width = group_width / n
    x = np.arange(len(metrics))

    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=SURFACE)
    style_axes(ax)

    for i, row in enumerate(selected):
        values = [parse_value(row[m]) for m in metrics]
        offsets = x - group_width / 2 + bar_width * (i + 0.5)
        bars = ax.bar(
            offsets, values, width=bar_width,
            color=PALETTE[i], edgecolor=SURFACE, linewidth=1.5,  # gap between adjacent bars
            label=clean_name(row[cfg["name_column"]]),
        )
        # Values in text ink, so pale or near-identical bar colors never carry the number alone
        ax.bar_label(bars, fmt="%.0f", padding=2, color=TEXT_SECONDARY, fontsize=8)

    ax.set_xticks(x, metrics, fontsize=12, color=TEXT_PRIMARY)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.set_ylabel("Recall", color=TEXT_SECONDARY)
    ax.set_title(cfg["title"], loc="left", fontsize=14, color=TEXT_PRIMARY, pad=12)

    legend = ax.legend(
        loc="upper left", bbox_to_anchor=(0, -0.08), ncol=2, frameon=False,
        labelcolor=TEXT_PRIMARY, fontsize=9, title="Retriever", alignment="left",
        title_fontproperties={"weight": "bold", "size": 10},
    )
    legend.get_title().set_color(TEXT_PRIMARY)

    fig.tight_layout()
    out_dir = config["_dir"] / config["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / cfg["output"]
    fig.savefig(out_path, dpi=200, facecolor=SURFACE, bbox_inches="tight")
    print(f"Saved {out_path}")

    if args.show:
        plt.show()


if __name__ == "__main__":
    main()
