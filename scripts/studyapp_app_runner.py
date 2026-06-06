from __future__ import annotations

import argparse
import subprocess
import sys

from studyapp_pipeline import ROOT, app_config_path, load_json, output_path, write_json


def categories_for_app(app_id: str) -> list[str]:
    config_path = app_config_path(app_id)
    if not config_path.exists():
        raise FileNotFoundError(f"Missing app config: {config_path}")
    config = load_json(config_path)
    return [item["category_id"] for item in config.get("categories", [])]


def total_final_questions(app_id: str, category: str) -> int:
    total = 0
    final_dir = output_path("final_questions", app_id, category, "")
    for cycle in ("cycle_01", "cycle_02", "cycle_03", "cycle_04"):
        path = output_path("final_questions", app_id, category, f"{cycle}_final_questions.json")
        if path.exists():
            payload = load_json(path)
            total += int(payload.get("summary", {}).get("total_final_questions", 0))
    return total


def run_app(app_id: str, today: str) -> int:
    categories = categories_for_app(app_id)
    log_path = output_path("logs", app_id, "_app", "app_runner_log.json")
    steps: list[dict[str, str]] = []

    for category in categories:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "studyapp_full_cycle_runner.py"),
                "--app-id",
                app_id,
                "--category",
                category,
                "--date",
                today,
            ],
            cwd=ROOT,
            check=False,
        )
        steps.append(
            {
                "category": category,
                "status": "success" if result.returncode == 0 else "failed",
                "reason": "All four cycles completed." if result.returncode == 0 else "Category run failed before all four cycles completed.",
            }
        )
        if result.returncode != 0:
            write_json(
                log_path,
                {
                    "app_id": app_id,
                    "status": "failed",
                    "steps": steps,
                    "total_final_questions": sum(total_final_questions(app_id, category_name) for category_name in categories),
                },
            )
            return result.returncode

    write_json(
        log_path,
        {
            "app_id": app_id,
            "status": "success",
            "steps": steps,
            "total_final_questions": sum(total_final_questions(app_id, category) for category in categories),
        },
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run StudyApp for all categories in an app through cycle_01 to cycle_04.")
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--date", default="2026-06-06")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_app(args.app_id, args.date)


if __name__ == "__main__":
    raise SystemExit(main())
