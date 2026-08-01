#!/usr/bin/env python3
"""Overlay two ID-VG curves stored in Silvaco ATLAS log files."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt


SCRIPT_DIR = Path(__file__).resolve().parent


def read_atlas_idvg(path: Path) -> tuple[list[float], list[float]]:
    """Return gate voltage and absolute drain current from an ATLAS log."""
    gate_voltage: list[float] = []
    drain_current: list[float] = []

    with path.open(encoding="utf-8") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            fields = line.split()
            if not fields or fields[0] != "d":
                continue

            # The `p` record in these logs maps the nine data columns as:
            # source (V, auxiliary, I), gate (V, auxiliary, I),
            # drain (V, auxiliary, I).
            if len(fields) < 10:
                raise ValueError(
                    f"{path}:{line_number}: expected 9 values in data record"
                )

            try:
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
    parser = argparse.ArgumentParser(
        description="Overlay IDVG_O100 and IDVG_O100_src ATLAS curves."
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        default=[
            SCRIPT_DIR / "IDVG_O100.log",
            SCRIPT_DIR / "IDVG_O100_src.log",
        ],
        help="ATLAS log files (defaults to the two logs beside this script)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=SCRIPT_DIR / "IDVG_O100_overlap.png",
        help="output image path",
    )
    parser.add_argument("--show", action="store_true", help="open the plot window")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if len(args.files) != 2:
        raise SystemExit("Please provide exactly two ATLAS log files.")

    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    for path in args.files:
        vg, drain_current = read_atlas_idvg(path)
        label = path.stem.removeprefix("IDVG_")
        ax.semilogy(vg, drain_current, linewidth=2, label=label)

    ax.set_xlabel("Gate voltage, $V_G$ (V)")
    ax.set_ylabel("Absolute drain current, $|I_D|$ (A)")
    ax.set_title("ID–VG Overlap")
    ax.grid(True, which="both", linestyle=":", alpha=0.55)
    ax.legend()
    fig.tight_layout()
    
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=300)
    print(f"Saved overlap plot to {args.output}")

    if args.show:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    main()
