from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from studyapp_next_cycle_runner import CYCLE_ORDER, completed_cycles
from studyapp_pipeline import ROOT, app_config_path, load_json, output_path, write_json


def run_command(args: list[str]) -> int:
    result = subprocess.run(args, cwd=ROOT, check=False)
    return result.returncode


def ensure_cycle_bank(app_id: str, category: str, cycle: str, today: str) -> int:
    return run_command(
        [
            sys.executable,
            str(ROOT / "scripts" / "studyapp_cycle_curator.py"),
            "--app-id",
            app_id,
            "--category",
            category,
            "--cycle",
            cycle,
            "--date",
            today,
        ]
    )


def next_cycle_log(app_id: str, category: str) -> dict[str, str] | None:
    path = output_path("logs", app_id, category, "next_cycle_runner_log.json")
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def category_exists(app_id: str, category: str) -> bool:
    config = load_json(app_config_path(app_id))
    return any(item["category_id"] == category for item in config.get("categories", []))


def run_full_cycle(app_id: str, category: str, today: str) -> int:
    if not app_config_path(app_id).exists():
        raise FileNotFoundError(f"Missing app config: {app_config_path(app_id)}")
    if not category_exists(app_id, category):
        raise ValueError(f"Category '{category}' is not defined in {app_config_path(app_id)}")

    log_path = output_path("logs", app_id, category, "full_cycle_runner_log.json")
    steps: list[dict[str, str]] = []

    cycle_01_final = output_path("final_questions", app_id, category, "cycle_01_final_questions.json")
    if not cycle_01_final.exists():
        cycle_01_bank = ROOT / "data" / "cycle_banks" / app_id / category / "cycle_01.json"
        if not cycle_01_bank.exists():
            rc = ensure_cycle_bank(app_id, category, "cycle_01", today)
            steps.append(
                {
                    "step": "curate_cycle_01",
                    "status": "success" if rc == 0 else "failed",
                    "reason": "Built a curated cycle_01 bank from source documents." if rc == 0 else "cycle_01 curation failed.",
                }
            )
            if rc != 0:
                write_json(
                    log_path,
                    {
                        "app_id": app_id,
                        "category": category,
                        "steps": steps,
                        "completed_cycles": completed_cycles(app_id, category),
                        "status": "failed",
                    },
                )
                return rc
        rc = run_command(
            [
                sys.executable,
                str(ROOT / "scripts" / "studyapp_pipeline.py"),
                "--app-id",
                app_id,
                "--category",
                category,
                "--cycle",
                "cycle_01",
                "--date",
                today,
            ]
        )
        steps.append(
            {
                "step": "cycle_01",
                "status": "success" if rc == 0 else "failed",
                "reason": "Ran cycle_01 directly through studyapp_pipeline.py." if rc == 0 else "cycle_01 failed.",
            }
        )
        if rc != 0:
            write_json(
                log_path,
                {
                    "app_id": app_id,
                    "category": category,
                    "steps": steps,
                    "completed_cycles": completed_cycles(app_id, category),
                    "status": "failed",
                },
            )
            return rc
    else:
        steps.append({"step": "cycle_01", "status": "skipped", "reason": "cycle_01 final output already exists."})

    for cycle in CYCLE_ORDER[1:]:
        if output_path("final_questions", app_id, category, f"{cycle}_final_questions.json").exists():
            steps.append({"step": cycle, "status": "skipped", "reason": f"{cycle} final output already exists."})
            continue

        rc = run_command(
            [
                sys.executable,
                str(ROOT / "scripts" / "studyapp_next_cycle_runner.py"),
                "--app-id",
                app_id,
                "--category",
                category,
                "--date",
                today,
            ]
        )
        log = next_cycle_log(app_id, category) or {}
        status = "success" if rc == 0 and log.get("status") == "success" else "failed"
        reason = log.get("reason", f"{cycle} did not complete.")
        steps.append({"step": cycle, "status": status, "reason": reason})
        if status != "success":
            write_json(
                log_path,
                {
                    "app_id": app_id,
                    "category": category,
                    "steps": steps,
                    "completed_cycles": completed_cycles(app_id, category),
                    "status": "failed",
                },
            )
            return 1

    write_json(
        log_path,
        {
            "app_id": app_id,
            "category": category,
            "steps": steps,
            "completed_cycles": completed_cycles(app_id, category),
            "status": "success",
        },
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run StudyApp category cycles from cycle_01 to cycle_04 in sequence.")
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--date", default="2026-06-06")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_full_cycle(args.app_id, args.category, args.date)


if __name__ == "__main__":
    sys.exit(main())
