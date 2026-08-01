#!/usr/bin/env python3
"""Overlay the oxide-thickness and 5e16-doping ID-VG curves."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt


WORKSPACE = Path(__file__).resolve().parents[2]
DEFAULT_CURVES = (
    (
        WORKSPACE / "sweep/oxide/IDVG_thickness_20.log",
        "20 nm",
    ),
    (
        WORKSPACE / "doping_5e16/IDVG_5e16.log",
        "30 nm",
    ),
)


def read_atlas_idvg(path: Path) -> tuple[list[float], list[float]]:
    """Read gate voltage and absolute drain current from an ATLAS log."""
    gate_voltage: list[float] = []
    drain_current: list[float] = []

    with path.open(encoding="utf-8") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            fields = line.split()
            if not fields or fields[0] != "d":
                continue
            if len(fields) < 10:
                raise ValueError(
                    f"{path}:{line_number}: expected nine ATLAS data values"
                )

            try:
                # Data columns are grouped by source, gate, and drain.
                gate_voltage.append(float(fields[4]))
                drain_current.append(abs(float(fields[9])))
            except ValueError as error:
                raise ValueError(
                    f"{path}:{line_number}: invalid numeric data"
                ) from error

    if not gate_voltage:
        raise ValueError(f"{path}: no ATLAS data records found")

    return gate_voltage, drain_current


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "oxide_doping_overlay.png",
        help="output PNG path",
    )
    parser.add_argument("--show", action="store_true", help="open the plot window")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    fig, ax = plt.subplots(figsize=(7.2, 5.0))

    for path, label in DEFAULT_CURVES:
        vg, current = read_atlas_idvg(path)
        ax.semilogy(vg, current, linewidth=2, label=label)

    ax.set_xlabel("Gate voltage, $V_G$ (V)")
    ax.set_ylabel("Absolute drain current, $|I_D|$ (A)")
    ax.set_title("ID–VG Curve Comparison")
    ax.grid(True, which="both", linestyle=":", alpha=0.55)
    
    ax.legend()
    fig.tight_layout()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=300)
    print(f"Saved overlay plot to {args.output}")

    if args.show:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    main()
