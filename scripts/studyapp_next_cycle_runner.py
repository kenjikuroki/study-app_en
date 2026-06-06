from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from studyapp_pipeline import ROOT, app_config_path, load_json, output_path, write_failure_report, write_json


CYCLE_ORDER = ["cycle_01", "cycle_02", "cycle_03", "cycle_04"]
CYCLE_SIZES = {
    "cycle_01": 30,
    "cycle_02": 30,
    "cycle_03": 30,
    "cycle_04": 10,
}


def final_questions_path(app_id: str, category: str, cycle: str) -> Path:
    return output_path("final_questions", app_id, category, f"{cycle}_final_questions.json")


def cycle_bank_path(app_id: str, category: str, cycle: str) -> Path:
    return ROOT / "data" / "cycle_banks" / app_id / category / f"{cycle}.json"


def category_target(app_id: str, category: str) -> int:
    config = load_json(app_config_path(app_id))
    for item in config.get("categories", []):
        if item["category_id"] == category:
            return int(item.get("target_question_count", config.get("target_question_count_per_category", 100)))
    raise ValueError(f"Category '{category}' not found in app config.")


def completed_cycles(app_id: str, category: str) -> list[str]:
    done: list[str] = []
    for cycle in CYCLE_ORDER:
        if final_questions_path(app_id, category, cycle).exists():
            done.append(cycle)
    return done


def next_cycle_from_completed(done: list[str]) -> str | None:
    for cycle in CYCLE_ORDER:
        if cycle not in done:
            return cycle
    return None


def total_final_count(app_id: str, category: str) -> int:
    total = 0
    for cycle in completed_cycles(app_id, category):
        payload = load_json(final_questions_path(app_id, category, cycle))
        total += int(payload["summary"]["total_final_questions"])
    return total


def validate_cycle_bank(app_id: str, category: str, cycle: str) -> tuple[bool, str]:
    bank_path = cycle_bank_path(app_id, category, cycle)
    if not bank_path.exists():
        return False, f"Missing curated cycle bank: {bank_path}"
    payload = load_json(bank_path)
    question_specs = payload.get("question_specs", [])
    expected = CYCLE_SIZES[cycle]
    if len(question_specs) != expected:
        return False, f"Curated cycle bank has {len(question_specs)} questions, expected {expected}: {bank_path}"
    return True, f"Curated cycle bank is ready: {bank_path}"


def try_auto_curate_cycle_bank(app_id: str, category: str, cycle: str, today: str) -> tuple[bool, str]:
    curator_script = ROOT / "scripts" / "studyapp_cycle_curator.py"
    result = subprocess.run(
        [
            sys.executable,
            str(curator_script),
            "--app-id",
            app_id,
            "--category",
            category,
            "--cycle",
            cycle,
            "--date",
            today,
        ],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        return False, f"Automatic cycle curation failed for {app_id}/{category}/{cycle}."
    return validate_cycle_bank(app_id, category, cycle)


def run_next_cycle(app_id: str, category: str, today: str) -> int:
    target = category_target(app_id, category)
    done = completed_cycles(app_id, category)
    total = total_final_count(app_id, category)
    next_cycle = next_cycle_from_completed(done)
    log_path = output_path("logs", app_id, category, "next_cycle_runner_log.json")

    log = {
        "app_id": app_id,
        "category": category,
        "completed_cycles": done,
        "current_total_final_questions": total,
        "target_question_count": target,
        "next_cycle": next_cycle or "",
        "status": "",
        "reason": "",
    }

    if next_cycle is None:
        log["status"] = "skipped"
        log["reason"] = "No next cycle is available because all configured cycles are already complete."
        write_json(log_path, log)
        return 0

    if total >= target:
        log["status"] = "skipped"
        log["reason"] = "No next cycle is needed because the category target is already satisfied."
        write_json(log_path, log)
        return 0

    if next_cycle != "cycle_01":
        previous_cycle = CYCLE_ORDER[CYCLE_ORDER.index(next_cycle) - 1]
        previous_path = final_questions_path(app_id, category, previous_cycle)
        if not previous_path.exists():
            reason = f"Previous cycle is not complete: {previous_path}"
            log["status"] = "failed"
            log["reason"] = reason
            write_json(log_path, log)
            write_failure_report(app_id, category, next_cycle, "next_cycle_runner", reason, ["read_app_config"], ["pipeline_runner"])
            return 1
        ok, reason = validate_cycle_bank(app_id, category, next_cycle)
        if not ok:
            ok, reason = try_auto_curate_cycle_bank(app_id, category, next_cycle, today)
            if not ok:
                log["status"] = "failed"
                log["reason"] = reason
                write_json(log_path, log)
                write_failure_report(app_id, category, next_cycle, "next_cycle_runner", reason, ["read_app_config"], ["pipeline_runner"])
                return 1

    pipeline_script = ROOT / "scripts" / "studyapp_pipeline.py"
    result = subprocess.run(
        [
            sys.executable,
            str(pipeline_script),
            "--app-id",
            app_id,
            "--category",
            category,
            "--cycle",
            next_cycle,
            "--date",
            today,
        ],
        cwd=ROOT,
        check=False,
    )
    if result.returncode == 0:
        log["status"] = "success"
        log["reason"] = f"Started and completed {next_cycle}."
    else:
        log["status"] = "failed"
        log["reason"] = f"Pipeline runner failed for {next_cycle}."
    write_json(log_path, log)
    return result.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the next StudyApp cycle when it is ready.")
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--date", default="2026-06-06")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_next_cycle(args.app_id, args.category, args.date)


if __name__ == "__main__":
    sys.exit(main())
