"""Bar chart of question answering results from the README leaderboard.

    uv run python3 plot/plot-qa-results.py [--config plot/config.yaml] [--show]
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np

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
    cfg = config["qa"]
    readme = config["_dir"] / config["readme"]

    rows = read_table(readme, cfg["section"])
    selected = select_rows(rows, cfg["name_column"], cfg["systems"])
    names = [clean_name(r[cfg["name_column"]]) for r in selected]
    values = [parse_value(r[cfg["metric"]]) for r in selected]

    fig, ax = plt.subplots(figsize=(8, 5), facecolor=SURFACE)
    style_axes(ax)

    x = np.arange(len(selected))
    bars = ax.bar(x, values, width=0.6, color=PALETTE[: len(selected)], label=names)
    ax.bar_label(bars, fmt="%.2f", padding=3, color=TEXT_SECONDARY, fontsize=9)

    ax.set_xticks(x, names, rotation=20, ha="right", color=TEXT_PRIMARY)
    ax.set_ylim(0, 1)
    ax.set_ylabel(cfg["metric"], color=TEXT_SECONDARY)
    ax.set_title(cfg["title"], loc="left", fontsize=14, color=TEXT_PRIMARY, pad=12)

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
