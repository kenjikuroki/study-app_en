from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from studyapp_next_cycle_runner import CYCLE_ORDER
from studyapp_pipeline import ROOT, output_path, write_json


ARTEFACT_GROUPS = [
    "ir",
    "ir_audit_reports",
    "generated_questions",
    "question_audit_reports",
    "revision_proposals",
    "final_questions",
]


def cycle_file_path(group: str, app_id: str, category: str, cycle: str) -> Path:
    suffix_map = {
        "ir": f"{cycle}_ir.json",
        "ir_audit_reports": f"{cycle}_ir_audit.json",
        "generated_questions": f"{cycle}_questions.json",
        "question_audit_reports": f"{cycle}_question_audit.json",
        "revision_proposals": f"{cycle}_revisions.json",
        "final_questions": f"{cycle}_final_questions.json",
    }
    return output_path(group, app_id, category, suffix_map[group])


def cycle_log_paths(app_id: str, category: str, cycle: str) -> list[Path]:
    logs_dir = output_path("logs", app_id, category)
    return [
        logs_dir / f"{cycle}_log.json",
        logs_dir / f"{cycle}_shuffle_log.json",
        logs_dir / f"{cycle}_failure_report.json",
        logs_dir / "pipeline_run_log.json",
        logs_dir / "next_cycle_runner_log.json",
    ]


def artefacts_for_cycles(app_id: str, category: str, start_cycle: str) -> list[Path]:
    start_index = CYCLE_ORDER.index(start_cycle)
    selected = CYCLE_ORDER[start_index:]
    files: list[Path] = []
    for cycle in selected:
        for group in ARTEFACT_GROUPS:
            path = cycle_file_path(group, app_id, category, cycle)
            if path.exists():
                files.append(path)
        for path in cycle_log_paths(app_id, category, cycle):
            if path.exists() and path not in files:
                files.append(path)
    return files


def move_to_backup(files: list[Path], backup_root: Path) -> None:
    for path in files:
        relative = path.relative_to(ROOT)
        target = backup_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(target))


def run_next_cycle_until_stop(app_id: str, category: str, today: str) -> list[dict[str, str]]:
    runner = ROOT / "scripts" / "studyapp_next_cycle_runner.py"
    steps: list[dict[str, str]] = []
    for _ in range(4):
        result = subprocess.run(
            [sys.executable, str(runner), "--app-id", app_id, "--category", category, "--date", today],
            cwd=ROOT,
            check=False,
        )
        status = "success" if result.returncode == 0 else "failed"
        steps.append({"step": "run_next_cycle", "status": status})
        if result.returncode != 0:
            break
        next_log = output_path("logs", app_id, category, "next_cycle_runner_log.json")
        if next_log.exists():
            payload = json.loads(next_log.read_text(encoding="utf-8"))
            if payload.get("status") == "skipped":
                break
    return steps


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive existing later-cycle outputs and rebuild from a chosen cycle.")
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--start-cycle", required=True, choices=CYCLE_ORDER)
    parser.add_argument("--date", default="2026-06-06")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    files = artefacts_for_cycles(args.app_id, args.category, args.start_cycle)
    report = {
        "app_id": args.app_id,
        "category": args.category,
        "start_cycle": args.start_cycle,
        "dry_run": args.dry_run,
        "artefacts_found": [str(path.relative_to(ROOT)).replace("\\", "/") for path in files],
        "backup_root": "",
        "steps": [],
    }

    if args.dry_run:
        report["steps"].append({"step": "inspect", "status": "success", "reason": "Dry run only. No files were moved and no cycles were rerun."})
        write_json(output_path("logs", args.app_id, args.category, "rebuild_runner_log.json"), report)
        return 0

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = ROOT / "backups" / "rebuild_runs" / timestamp / args.app_id / args.category
    report["backup_root"] = str(backup_root).replace("\\", "/")
    move_to_backup(files, backup_root)
    report["steps"].append({"step": "archive_existing_outputs", "status": "success", "reason": f"Moved {len(files)} files into backup storage."})
    report["steps"].extend(run_next_cycle_until_stop(args.app_id, args.category, args.date))
    write_json(output_path("logs", args.app_id, args.category, "rebuild_runner_log.json"), report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
