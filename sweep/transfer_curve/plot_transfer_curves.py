#!/usr/bin/env python3
"""Overlay all IDVG_VD*.log transfer curves in one figure."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt


SCRIPT_DIR = Path(__file__).resolve().parent
VD_PATTERN = re.compile(r"IDVG_VD([+-]?(?:\d+(?:\.\d*)?|\.\d+))", re.IGNORECASE)


def drain_voltage(path: Path) -> float:
    """Extract the drain voltage from a name such as IDVG_VD25.log."""
    match = VD_PATTERN.search(path.stem)
    if not match:
        raise ValueError(f"Cannot determine VD from filename: {path.name}")
    return float(match.group(1))


def read_idvg(path: Path) -> tuple[list[float], list[float]]:
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
                # ATLAS columns: source (V, auxiliary, I),
                # gate (V, auxiliary, I), drain (V, auxiliary, I).
                gate_voltage.append(float(fields[4]))
                drain_current.append(abs(float(fields[9])))
            except ValueError as error:
                raise ValueError(
                    f"{path}:{line_number}: invalid numeric data"
                ) from error

    if not gate_voltage:
        raise ValueError(f"{path}: no data records found")

    return gate_voltage, drain_current


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Overlay Silvaco IDVG transfer curves for multiple VD values."
    )
    parser.add_argument(
        "--directory",
        type=Path,
        default=SCRIPT_DIR,
        help="directory containing the log files (default: script directory)",
    )
    parser.add_argument(
        "--pattern",
        default="IDVG_VD*.log",
        help="log filename pattern (default: IDVG_VD*.log)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=SCRIPT_DIR / "IDVG_transfer_curves.png",
        help="output image path",
    )
    parser.add_argument("--show", action="store_true", help="open the plot window")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    files = sorted(args.directory.glob(args.pattern), key=drain_voltage)

    if not files:
        raise SystemExit(
            f"No files matching {args.pattern!r} found in {args.directory}"
        )

    fig, ax = plt.subplots(figsize=(7.4, 5.2))

    for path in files:
        voltage = drain_voltage(path)
        vg, current = read_idvg(path)
        ax.semilogy(vg, current, linewidth=2, label=f"$V_D$ = {voltage:g} V")

    ax.set_xlabel("Gate voltage, $V_G$ (V)")
    ax.set_ylabel("Absolute drain current, $|I_D|$ (A)")
    ax.set_title("Transfer Characteristics")
    ax.grid(True, which="both", linestyle=":", alpha=0.55)
    ax.legend()
    fig.tight_layout()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=300)
    print(f"Plotted {len(files)} curves")
    print(f"Saved plot to {args.output}")

    if args.show:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    main()
