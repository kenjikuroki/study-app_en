from __future__ import annotations

import argparse
from pathlib import Path

from studyapp_bank_builder import build_cycle_payload, write_json
from studyapp_next_cycle_runner import CYCLE_ORDER, CYCLE_SIZES
from studyapp_pipeline import ROOT, output_path


def cycle_bank_path(app_id: str, category: str, cycle: str) -> Path:
    return ROOT / "data" / "cycle_banks" / app_id / category / f"{cycle}.json"


def curation_evidence_path(app_id: str, category: str, cycle: str) -> Path:
    return output_path("logs", app_id, category, f"{cycle}_curation_evidence.json")


def final_questions_exist(app_id: str, category: str, cycle: str) -> bool:
    return output_path("final_questions", app_id, category, f"{cycle}_final_questions.json").exists()


def curate_cycle(app_id: str, category: str, cycle: str, today: str) -> int:
    if cycle != "cycle_01" and not final_questions_exist(app_id, category, "cycle_01"):
        raise RuntimeError("cycle_01 final output must exist before automated curation for later cycles.")

    if cycle == "all":
        for cycle_name in CYCLE_ORDER:
            payload, evidence = build_cycle_payload(app_id, category, cycle_name, today)
            expected = CYCLE_SIZES[cycle_name]
            if len(payload["question_specs"]) != expected:
                raise RuntimeError(f"{category} {cycle_name} has {len(payload['question_specs'])} questions, expected {expected}.")
            write_json(cycle_bank_path(app_id, category, cycle_name), payload)
            write_json(curation_evidence_path(app_id, category, cycle_name), {
                "app_id": app_id,
                "category": category,
                "cycle": cycle_name,
                "items": evidence,
            })
    else:
        payload, evidence = build_cycle_payload(app_id, category, cycle, today)
        expected = CYCLE_SIZES[cycle]
        if len(payload["question_specs"]) != expected:
            raise RuntimeError(f"{category} {cycle} has {len(payload['question_specs'])} questions, expected {expected}.")
        write_json(cycle_bank_path(app_id, category, cycle), payload)
        write_json(curation_evidence_path(app_id, category, cycle), {
            "app_id": app_id,
            "category": category,
            "cycle": cycle,
            "items": evidence,
        })
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build curated cycle bank files for StudyApp.")
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--cycle", required=True, choices=CYCLE_ORDER + ["all"])
    parser.add_argument("--date", default="2026-06-06")
    args = parser.parse_args()
    return curate_cycle(args.app_id, args.category, args.cycle, args.date)


if __name__ == "__main__":
    raise SystemExit(main())
