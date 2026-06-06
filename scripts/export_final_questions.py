from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FINAL_ROOT = ROOT / "output" / "final_questions"
EXPORT_ROOT = ROOT / "output" / "exports"
CYCLE_ORDER = ["cycle_01", "cycle_02", "cycle_03", "cycle_04"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def app_config_path(app_id: str) -> Path:
    return ROOT / "apps" / "active_apps" / app_id / "app_config.json"


def categories_for_app(app_id: str) -> list[dict[str, Any]]:
    config = load_json(app_config_path(app_id))
    return config.get("categories", [])


def export_app(app_id: str) -> Path:
    categories = categories_for_app(app_id)
    config = load_json(app_config_path(app_id))
    export_categories: list[dict[str, Any]] = []
    all_questions: list[dict[str, Any]] = []

    for category in categories:
        category_id = category["category_id"]
        category_name = category.get("category_name", category_id)
        category_questions: list[dict[str, Any]] = []
        cycle_summaries: list[dict[str, Any]] = []

        for cycle in CYCLE_ORDER:
            cycle_path = FINAL_ROOT / app_id / category_id / f"{cycle}_final_questions.json"
            payload = load_json(cycle_path)
            cycle_questions = payload.get("questions", [])
            category_questions.extend(cycle_questions)
            cycle_summaries.append(
                {
                    "cycle": cycle,
                    "total_final_questions": payload["summary"]["total_final_questions"],
                    "true_count": payload["summary"]["true_count"],
                    "false_count": payload["summary"]["false_count"],
                }
            )

        export_categories.append(
            {
                "category_id": category_id,
                "category_name": category_name,
                "question_count": len(category_questions),
                "cycles": cycle_summaries,
                "questions": category_questions,
            }
        )
        all_questions.extend(category_questions)

    export_payload = {
        "app_id": app_id,
        "app_name": config.get("app_name", app_id),
        "language": config.get("language", "en"),
        "export_type": "final_questions_bundle",
        "total_questions": len(all_questions),
        "categories": export_categories,
        "questions": all_questions,
    }

    destination = EXPORT_ROOT / app_id / f"{app_id}_final_questions_bundle.json"
    write_json(destination, export_payload)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description="Bundle final StudyApp questions into one JSON file for app consumption.")
    parser.add_argument("--app-id", required=True)
    args = parser.parse_args()
    path = export_app(args.app_id)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
