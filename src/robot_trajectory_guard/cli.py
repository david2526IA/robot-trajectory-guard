from __future__ import annotations

import argparse
import json
from pathlib import Path

from .validator import validate_trajectory


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a robot joint trajectory offline.")
    parser.add_argument("trajectory", type=Path, help="JSON trajectory samples")
    parser.add_argument("limits", type=Path, help="JSON per-joint limits")
    parser.add_argument("--output", type=Path, default=Path("trajectory_report.json"))
    args = parser.parse_args()
    report = validate_trajectory(json.loads(args.trajectory.read_text()), json.loads(args.limits.read_text()))
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"valid": report["valid"], "violations": len(report["violations"])}))
