from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BANK_ROOT = ROOT / "data" / "question_banks" / "linux"

CATEGORIES = [
    "basic_commands",
    "filesystem",
    "permissions",
    "users_groups",
    "processes",
    "package_management",
    "networking",
    "shell_scripting",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_text(text: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = text.replace("¶", " ")
    return " ".join(text.split())


def normalize_statement(text: str) -> str:
    text = " ".join(text.split())
    return text.rstrip(".")


def command_from_path(path_str: str) -> str:
    stem = Path(path_str).stem
    stem = stem.replace("-invocation", "")
    if stem.endswith(".8") or stem.endswith(".7"):
        stem = stem.rsplit(".", 1)[0]
    return stem.replace("-", " ")


def render_command(command: str) -> str:
    return f"`{command}`" if command else "the command"


def statement_from_option(command: str, option: str, description: str) -> str:
    desc = normalize_statement(description)
    if desc and desc[0].islower():
        desc = desc[0].lower() + desc[1:]
    return f"The {render_command(command)} {option} option {desc}."


def sentence_split(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [item.strip() for item in parts if len(item.strip()) > 20]


def is_usable_sentence(text: str) -> bool:
    lowered = text.lower()
    banned = [
        "next:",
        "previous:",
        "up:",
        "[ contents ]",
        "[ index ]",
        "table of contents",
        "copyright",
        "permission is granted",
    ]
    return not any(token in lowered for token in banned)


def parse_option_facts(path: Path, category: str) -> list[dict[str, Any]]:
    html_text = path.read_text(encoding="utf-8", errors="ignore")
    command = command_from_path(str(path))
    title = path.stem
    items: list[dict[str, Any]] = []
    seen: set[str] = set()

    for match in re.finditer(r"<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>.*?<p>(.*?)</p>", html_text, re.S | re.I):
        dt = clean_text(match.group(1))
        dd = clean_text(match.group(2))
        option_match = re.search(r"(--?[A-Za-z0-9][A-Za-z0-9=\[\]_-]*|[A-Za-z](?=\s|$))", dt)
        if not option_match or len(dd) < 20:
            continue
        opt = option_match.group(1)
        if not opt.startswith("-"):
            if len(opt) == 1:
                opt = f"-{opt}"
            else:
                continue
        sentences = sentence_split(dd)
        if not sentences:
            continue
        desc = sentences[0]
        if not is_usable_sentence(desc):
            continue
        statement = statement_from_option(command, opt, desc)
        key = normalize_statement(statement)
        if key in seen:
            continue
        seen.add(key)
        items.append({
            "topic": f"{command} {opt}",
            "category": category,
            "fact_type": "option",
            "statement": statement,
            "conditions": [],
            "examples": [f"{command} {opt}".strip()],
            "source": "Official source document",
            "source_document_path": str(path).replace("\\", "/"),
            "source_url": "",
            "source_title": title,
            "source_version": "current",
            "source_last_checked": "2026-06-06",
            "source_section": title,
            "source_quote_or_summary": desc,
            "confidence": "high",
            "question_potential": "high",
            "notes": "",
        })
    return items


def parse_paragraph_facts(path: Path, category: str) -> list[dict[str, Any]]:
    html_text = path.read_text(encoding="utf-8", errors="ignore")
    command = command_from_path(str(path))
    title = path.stem
    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for paragraph in re.findall(r"<p>(.*?)</p>", html_text, re.S | re.I):
        text = clean_text(paragraph)
        if len(text) < 40:
            continue
        for sentence in sentence_split(text)[:2]:
            if not is_usable_sentence(sentence):
                continue
            normalized = normalize_statement(sentence)
            if command and normalized.lower().startswith(command.lower() + " "):
                statement = f"The {render_command(command)} command {normalized[len(command):].strip()}."
            elif command and normalized.lower().startswith(f"{command} is "):
                statement = f"The {render_command(command)} command {normalized[len(command):].strip()}."
            else:
                statement = normalized + "."
            key = normalize_statement(statement)
            if key in seen:
                continue
            seen.add(key)
            items.append({
                "topic": f"{command} paragraph",
                "category": category,
                "fact_type": "behavior",
                "statement": statement,
                "conditions": [],
                "examples": [command] if command else [],
                "source": "Official source document",
                "source_document_path": str(path).replace("\\", "/"),
                "source_url": "",
                "source_title": title,
                "source_version": "current",
                "source_last_checked": "2026-06-06",
                "source_section": title,
                "source_quote_or_summary": normalized,
                "confidence": "high",
                "question_potential": "medium",
                "notes": "",
            })
            if len(items) >= 20:
                break
        if len(items) >= 20:
            break
    return items


def subject_predicate(statement: str) -> tuple[str, str]:
    trimmed = normalize_statement(statement)
    match = re.match(r"(The\s+`[^`]+`(?:\s+\S+)?)(\s+.+)", trimmed)
    if match:
        return match.group(1), match.group(2).strip()
    parts = trimmed.split(" ", 3)
    if len(parts) >= 4:
        return " ".join(parts[:3]), parts[3]
    return trimmed, trimmed


def explanation_from_statement(statement: str) -> str:
    return normalize_statement(statement) + "."


def build_false_question(statement: str, peer_statement: str) -> str:
    subject, predicate = subject_predicate(statement)
    _, peer_predicate = subject_predicate(peer_statement)
    if predicate == peer_predicate:
        if " does not " in statement:
            return normalize_statement(statement.replace(" does not ", " does ", 1)) + "."
        if " is not " in statement:
            return normalize_statement(statement.replace(" is not ", " is ", 1)) + "."
        if " cannot " in statement:
            return normalize_statement(statement.replace(" cannot ", " can ", 1)) + "."
        return normalize_statement(statement.replace(" always ", " never ", 1) if " always " in statement else f"It is false that {statement[0].lower() + statement[1:]}") + "."
    return f"{subject} {peer_predicate.rstrip('.')}."


def supplemental_true_question(statement: str) -> str:
    normalized = normalize_statement(statement)
    lowered = normalized[0].lower() + normalized[1:]
    return f"According to the official source, {lowered}."


def generate_bank(category: str) -> dict[str, Any]:
    ir_path = ROOT / "output" / "ir" / "linux" / category / "cycle_01_ir.json"
    q_path = ROOT / "output" / "generated_questions" / "linux" / category / "cycle_01_questions.json"
    base_irs = load_json(ir_path)["items"]
    base_questions = load_json(q_path)["questions"]

    existing_statements = {normalize_statement(item["statement"]) for item in base_irs}
    next_ir_index = len(base_irs)
    new_irs: list[dict[str, Any]] = []
    category_dir = ROOT / "input" / "source_documents" / "linux" / category
    for html_path in sorted(category_dir.glob("*.html")):
        for parser in (parse_option_facts, parse_paragraph_facts):
            for item in parser(html_path, category):
                normalized = normalize_statement(item["statement"])
                if normalized in existing_statements:
                    continue
                existing_statements.add(normalized)
                next_ir_index += 1
                item["id"] = f"linux_{category}_ir_{next_ir_index:04d}"
                new_irs.append(item)

    all_irs = base_irs + new_irs
    ir_by_id = {item["id"]: item for item in all_irs}

    question_specs = [
        {
            "id": item["id"],
            "source_ir_id": item["source_ir_id"],
            "question": item["question"],
            "answer": item["answer"],
            "explanation": item["explanation"],
            "difficulty": item["difficulty"],
        }
        for item in base_questions
    ]

    grouped_ids: dict[str, list[str]] = defaultdict(list)
    for item in all_irs:
        grouped_ids[item["source_document_path"]].append(item["id"])

    supplemental_slots: list[str] = [item["id"] for item in new_irs]
    if len(supplemental_slots) < 35:
        reusable = [item["id"] for item in base_irs]
        while len(supplemental_slots) < 35:
            supplemental_slots.extend(reusable)
        supplemental_slots = supplemental_slots[:35]
    else:
        supplemental_slots = supplemental_slots[:35]

    next_q_index = len(question_specs)
    for slot_ir_id in supplemental_slots:
        ir_item = ir_by_id[slot_ir_id]
        peer_ids = [candidate for candidate in grouped_ids[ir_item["source_document_path"]] if candidate != slot_ir_id]
        if not peer_ids:
            peer_ids = [candidate for candidate in ir_by_id if candidate != slot_ir_id]
        peer_item = ir_by_id[peer_ids[next_q_index % len(peer_ids)]]

        next_q_index += 1
        question_specs.append({
            "id": f"linux_{category}_q_{next_q_index:04d}",
            "source_ir_id": slot_ir_id,
            "question": supplemental_true_question(ir_item["statement"]),
            "answer": True,
            "explanation": explanation_from_statement(ir_item["statement"]),
            "difficulty": "intermediate",
        })

        next_q_index += 1
        question_specs.append({
            "id": f"linux_{category}_q_{next_q_index:04d}",
            "source_ir_id": slot_ir_id,
            "question": build_false_question(ir_item["statement"], peer_item["statement"]),
            "answer": False,
            "explanation": explanation_from_statement(ir_item["statement"]),
            "difficulty": "intermediate",
        })

    question_specs = question_specs[:100]
    required_ids = {item["source_ir_id"] for item in question_specs}
    bank_irs = [item for item in all_irs if item["id"] in required_ids]
    return {"ir_specs": bank_irs, "question_specs": question_specs}


def main() -> None:
    for category in CATEGORIES:
        payload = generate_bank(category)
        write_json(BANK_ROOT / f"{category}.json", payload)
        print(category, len(payload["ir_specs"]), len(payload["question_specs"]))


if __name__ == "__main__":
    main()
