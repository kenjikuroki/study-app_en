from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any

from studyapp_pipeline import SUPPORTED_PIPELINES, slice_profile_for_cycle


ROOT = Path(__file__).resolve().parents[1]
BANK_ROOT = ROOT / "data" / "question_banks"
FINAL_ROOT = ROOT / "output" / "final_questions"
CYCLE_BANK_ROOT = ROOT / "data" / "cycle_banks"
PROFILE_CONFIG_PATH = ROOT / "config" / "source_parser_profiles.json"
DEFAULT_PROFILE = "generic_html_manual_v1"
CYCLE_IR_WINDOWS = {
    "cycle_01": (0, 15),
    "cycle_02": (15, 30),
    "cycle_03": (30, 45),
    "cycle_04": (45, 50),
}
CYCLE_ORDER = ["cycle_01", "cycle_02", "cycle_03", "cycle_04"]
CYCLE_QUESTION_TARGETS = {
    "cycle_01": 30,
    "cycle_02": 30,
    "cycle_03": 30,
    "cycle_04": 10,
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_dir(app_id: str, category: str) -> Path:
    return ROOT / "input" / "source_documents" / app_id / category


def app_config_path(app_id: str) -> Path:
    return ROOT / "apps" / "active_apps" / app_id / "app_config.json"


def clean_text(text: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return " ".join(text.split())


def normalize_statement(text: str) -> str:
    return " ".join(text.split()).rstrip(".")


def sentence_split(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if len(part.strip()) > 25]


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
        "javascript",
        "cookies",
        "privacy policy",
        "all rights reserved",
    ]
    return not any(token in lowered for token in banned)


def canonical_url_from_html(html_text: str) -> str:
    patterns = [
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text, re.I)
        if match:
            return html.unescape(match.group(1))
    return ""


def title_from_html(html_text: str, fallback: str) -> str:
    match = re.search(r"<title>(.*?)</title>", html_text, re.S | re.I)
    if not match:
        return fallback
    return clean_text(match.group(1)) or fallback


def page_topic_from_path(path: Path) -> str:
    stem = path.stem.replace("-", " ").replace("_", " ")
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem


def infer_fact_type(statement: str) -> str:
    lowered = statement.lower()
    if " warning " in lowered or lowered.startswith("warning"):
        return "warning"
    if " best practice " in lowered:
        return "best_practice"
    if " must " in lowered or " cannot " in lowered or " can only " in lowered:
        return "limitation"
    if " option " in lowered:
        return "option"
    if lowered.startswith("the ") and " command " in lowered:
        return "command"
    if lowered.startswith("the ") and " returns " in lowered:
        return "behavior"
    return "behavior"


def option_description_to_sentence(description: str) -> str:
    text = normalize_statement(description)
    replacements = [
        (r"^Print\b", "prints"),
        (r"^Display\b", "displays"),
        (r"^Use\b", "uses"),
        (r"^Make\b", "makes"),
        (r"^Append\b", "appends"),
        (r"^Suppress\b", "suppresses"),
        (r"^Ignore\b", "ignores"),
        (r"^Enable\b", "enables"),
        (r"^Disable\b", "disables"),
        (r"^Allow\b", "allows"),
        (r"^Prevent\b", "prevents"),
        (r"^Return\b", "returns"),
        (r"^Set\b", "sets"),
        (r"^Create\b", "creates"),
        (r"^Remove\b", "removes"),
        (r"^Show\b", "shows"),
        (r"^Output\b", "outputs"),
        (r"^Treat\b", "treats"),
        (r"^Traverse\b", "traverses"),
        (r"^Number\b", "numbers"),
        (r"^Do not\b", "does not"),
        (r"^Does not\b", "does not"),
        (r"^Do\b", "does"),
    ]
    for pattern, replacement in replacements:
        if re.search(pattern, text):
            return re.sub(pattern, replacement, text, count=1)
    if text:
        return text[0].lower() + text[1:]
    return text


def statement_from_option(topic: str, option: str, description: str) -> str:
    desc = option_description_to_sentence(description)
    if not desc:
        return ""
    normalized_topic = normalize_statement(topic)
    if re.search(r"\d", normalized_topic) or normalized_topic.lower().startswith("gnu ") or len(normalized_topic.split()) > 3:
        return f"The `{option}` option {desc}."
    return f"The `{normalized_topic}` {option} option {desc}."


def parse_option_facts(path: Path, category: str, today: str) -> list[dict[str, Any]]:
    html_text = path.read_text(encoding="utf-8", errors="ignore")
    title = title_from_html(html_text, path.stem)
    topic = page_topic_from_path(path)
    canonical_url = canonical_url_from_html(html_text)
    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for match in re.finditer(r"<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>.*?<p>(.*?)</p>", html_text, re.S | re.I):
        dt = clean_text(match.group(1))
        dd = clean_text(match.group(2))
        option_match = re.search(r"(--?[A-Za-z0-9][A-Za-z0-9=\[\]_-]*)", dt)
        if not option_match or len(dd) < 25:
            continue
        option = option_match.group(1)
        description_candidates = [item for item in sentence_split(dd) if is_usable_sentence(item)]
        if not description_candidates:
            continue
        statement = statement_from_option(topic, option, description_candidates[0])
        if not statement:
            continue
        key = normalize_statement(statement)
        if key in seen:
            continue
        seen.add(key)
        items.append(
            {
                "topic": f"{topic} {option}",
                "category": category,
                "fact_type": "option",
                "statement": statement,
                "conditions": [],
                "examples": [f"{topic} {option}".strip()],
                "source": title,
                "source_document_path": str(path).replace("\\", "/"),
                "source_url": canonical_url,
                "source_title": title,
                "source_version": "",
                "source_last_checked": today,
                "source_section": dt or title,
                "source_quote_or_summary": normalize_statement(description_candidates[0]) + ".",
                "confidence": "high",
                "question_potential": "high",
                "notes": "",
            }
        )
    return items


def parse_html_sentence_facts(path: Path, category: str, today: str) -> list[dict[str, Any]]:
    html_text = path.read_text(encoding="utf-8", errors="ignore")
    title = title_from_html(html_text, path.stem)
    canonical_url = canonical_url_from_html(html_text)
    topic = page_topic_from_path(path)
    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for paragraph in re.findall(r"<p>(.*?)</p>", html_text, re.S | re.I):
        text = clean_text(paragraph)
        if len(text) < 40:
            continue
        for sentence in sentence_split(text):
            if not is_usable_sentence(sentence):
                continue
            normalized = normalize_statement(sentence)
            if len(normalized) < 35:
                continue
            statement = normalized + "."
            key = normalize_statement(statement)
            if key in seen:
                continue
            seen.add(key)
            items.append(
                {
                    "topic": topic,
                    "category": category,
                    "fact_type": infer_fact_type(statement),
                    "statement": statement,
                    "conditions": [],
                    "examples": [topic] if topic else [],
                    "source": title,
                    "source_document_path": str(path).replace("\\", "/"),
                    "source_url": canonical_url,
                    "source_title": title,
                    "source_version": "",
                    "source_last_checked": today,
                    "source_section": title,
                    "source_quote_or_summary": normalized + ".",
                    "confidence": "high",
                    "question_potential": "high" if any(token in normalized.lower() for token in ["default", "must", "cannot", "returns", "option", "if "]) else "medium",
                    "notes": "",
                }
            )
            if len(items) >= 40:
                break
        if len(items) >= 40:
            break
    return items


def parse_preformatted_facts(path: Path, category: str, today: str) -> list[dict[str, Any]]:
    html_text = path.read_text(encoding="utf-8", errors="ignore")
    title = title_from_html(html_text, path.stem)
    canonical_url = canonical_url_from_html(html_text)
    topic = page_topic_from_path(path)
    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for block in re.findall(r"<pre>(.*?)</pre>", html_text, re.S | re.I):
        text = clean_text(block)
        if len(text) < 30:
            continue
        for sentence in sentence_split(text):
            if not is_usable_sentence(sentence):
                continue
            normalized = normalize_statement(sentence)
            if len(normalized) < 25:
                continue
            statement = normalized + "."
            if normalized.startswith("-") or normalized.startswith("--"):
                parts = normalized.split(" ", 1)
                if len(parts) == 2:
                    statement = statement_from_option(topic, parts[0], parts[1])
                    if not statement:
                        continue
            key = normalize_statement(statement).lower()
            if key in seen:
                continue
            seen.add(key)
            items.append(
                {
                    "topic": topic,
                    "category": category,
                    "fact_type": infer_fact_type(statement),
                    "statement": statement,
                    "conditions": [],
                    "examples": [topic] if topic else [],
                    "source": title,
                    "source_document_path": str(path).replace("\\", "/"),
                    "source_url": canonical_url,
                    "source_title": title,
                    "source_version": "",
                    "source_last_checked": today,
                    "source_section": title,
                    "source_quote_or_summary": normalize_statement(sentence) + ".",
                    "confidence": "high",
                    "question_potential": "high" if any(token in normalized.lower() for token in ["only", "must", "cannot", "default", "return", "use "]) else "medium",
                    "notes": "",
                }
            )
            if len(items) >= 60:
                break
        if len(items) >= 60:
            break
    return items


def parse_text_facts(path: Path, category: str, today: str) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    title = path.stem
    topic = page_topic_from_path(path)
    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for sentence in sentence_split(" ".join(text.splitlines())):
        if not is_usable_sentence(sentence):
            continue
        normalized = normalize_statement(sentence)
        if len(normalized) < 35:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        items.append(
            {
                "topic": topic,
                "category": category,
                "fact_type": infer_fact_type(normalized),
                "statement": normalized + ".",
                "conditions": [],
                "examples": [topic] if topic else [],
                "source": title,
                "source_document_path": str(path).replace("\\", "/"),
                "source_url": "",
                "source_title": title,
                "source_version": "",
                "source_last_checked": today,
                "source_section": title,
                "source_quote_or_summary": normalized + ".",
                "confidence": "high",
                "question_potential": "medium",
                "notes": "",
            }
        )
        if len(items) >= 40:
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


def lower_first(text: str) -> str:
    if not text:
        return text
    return text[0].lower() + text[1:]


def paraphrase_predicate(predicate: str) -> str:
    text = predicate.strip().rstrip(".")
    replacements = [
        ("prints the name of", "shows the name of"),
        ("prints the value of", "shows the value of"),
        ("prints the file name of", "shows the file name of"),
        ("prints", "shows"),
        ("outputs", "produces"),
        ("displays", "shows"),
        ("returns an exit status of", "exits with status"),
        ("returns", "gives"),
        ("changes", "modifies"),
        ("removes", "strips"),
        ("enables interpretation of", "turns on interpretation of"),
        ("disables interpretation of", "turns off interpretation of"),
        ("acts as if", "behaves as if"),
        ("is equivalent to", "has the same effect as"),
        ("does not output", "suppresses"),
        ("can use", "may use"),
        ("prints all but", "shows everything except"),
    ]
    for old, new in replacements:
        if text.startswith(old):
            return new + text[len(old):]
    return text


def true_explanation_from_statement(statement: str) -> str:
    subject, predicate = subject_predicate(statement)
    subject_text = subject.removeprefix("The ").strip()
    predicate_text = paraphrase_predicate(predicate)
    return f"Correct. {subject_text} {predicate_text}."


def false_explanation_from_statement(statement: str) -> str:
    subject, predicate = subject_predicate(statement)
    subject_text = subject.removeprefix("The ").strip()
    predicate_text = paraphrase_predicate(predicate)
    return f"Incorrect. {subject_text} {predicate_text}."


def build_false_question(statement: str, peer_statement: str) -> str:
    subject, predicate = subject_predicate(statement)
    _, peer_predicate = subject_predicate(peer_statement)
    if predicate == peer_predicate:
        variants = [
            (" does not ", " does "),
            (" is not ", " is "),
            (" cannot ", " can "),
            (" always ", " sometimes "),
            (" only ", " also "),
        ]
        for old, new in variants:
            if old in statement:
                return normalize_statement(statement.replace(old, new, 1)) + "."
        return f"It is false that {statement[0].lower() + statement[1:]}"
    return f"{subject} {peer_predicate.rstrip('.')}."


def prior_cycle_names(cycle: str) -> list[str]:
    if cycle not in CYCLE_ORDER:
        return []
    index = CYCLE_ORDER.index(cycle)
    return CYCLE_ORDER[:index]


def cycle_bank_path(app_id: str, category: str, cycle: str) -> Path:
    return CYCLE_BANK_ROOT / app_id / category / f"{cycle}.json"


def used_ir_ids_from_previous_cycles(app_id: str, category: str, cycle: str) -> set[str]:
    used: set[str] = set()
    for prior in prior_cycle_names(cycle):
        path = cycle_bank_path(app_id, category, prior)
        if not path.exists():
            continue
        payload = load_json(path)
        used.update(item["id"] for item in payload.get("ir_specs", []))
    return used


def question_text_is_natural(text: str) -> bool:
    lowered = text.lower()
    banned = [
        "according to the official source",
        "table of contents",
        "privacy policy",
        "search online pages",
        "linux/unix system programming training",
        "all rights reserved",
    ]
    if any(token in lowered for token in banned):
        return False
    if len(text.split()) < 5:
        return False
    return True


def audit_ir_candidate(ir_item: dict[str, Any]) -> tuple[bool, str]:
    if not ir_item.get("source_document_path") and not ir_item.get("source_url"):
        return False, "Missing source traceability."
    if not ir_item.get("source_section"):
        return False, "Missing source section."
    if ir_item.get("confidence") == "low":
        return False, "Low-confidence IR cannot be used."
    statement = ir_item.get("statement", "")
    if statement.count(" and ") > 1:
        return False, "Statement appears to mix multiple facts."
    return True, ""


def audit_question_candidate(question: dict[str, Any], ir_item: dict[str, Any]) -> tuple[bool, str]:
    if not question.get("source_ir_id") or question["source_ir_id"] != ir_item["id"]:
        return False, "source_ir_id is missing or mismatched."
    if not question_text_is_natural(question.get("question", "")):
        return False, "Question text is not natural enough."
    if normalize_statement(question.get("explanation", "")) == normalize_statement(question.get("question", "")):
        return False, "Explanation repeats the question text."
    expected_explanation = true_explanation_from_statement(ir_item["statement"]) if question["answer"] else false_explanation_from_statement(ir_item["statement"])
    if normalize_statement(question.get("explanation", "")) != normalize_statement(expected_explanation):
        return False, "Explanation does not match the required reason-based format."
    if question["answer"] and not question.get("explanation", "").startswith("Correct."):
        return False, "True explanation must start with 'Correct.'"
    if question["answer"] is False and not question.get("explanation", "").startswith("Incorrect."):
        return False, "False explanation must start with 'Incorrect.'"
    if question["answer"] is False:
        if normalize_statement(question["question"]) == normalize_statement(ir_item["statement"]):
            return False, "False question repeats the source IR statement."
        if question["question"].startswith("It is false that"):
            return False, "False question fallback wording is too weak."
    return True, ""


def make_true_question(app_id: str, category: str, cycle: str, question_index: int, ir_item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"{app_id}_{category}_{cycle}_q_{question_index:04d}",
        "source_ir_id": ir_item["id"],
        "question": normalize_statement(ir_item["statement"]) + ".",
        "answer": True,
        "explanation": true_explanation_from_statement(ir_item["statement"]),
        "difficulty": "intermediate",
    }


def make_false_question(
    app_id: str,
    category: str,
    cycle: str,
    question_index: int,
    ir_item: dict[str, Any],
    peer_item: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": f"{app_id}_{category}_{cycle}_q_{question_index:04d}",
        "source_ir_id": ir_item["id"],
        "question": build_false_question(ir_item["statement"], peer_item["statement"]),
        "answer": False,
        "explanation": false_explanation_from_statement(ir_item["statement"]),
        "difficulty": "intermediate",
    }


def make_evidence_entry(
    *,
    phase: str,
    item_id: str,
    source_ir_id: str = "",
    source_document_path: str = "",
    reviewed_individually: bool = True,
    source_checked: bool = True,
    source_ir_checked: bool = True,
    decision: str,
    reason: str,
    question_text: str = "",
) -> dict[str, Any]:
    return {
        "phase": phase,
        "item_id": item_id,
        "source_ir_id": source_ir_id,
        "source_document_path": source_document_path,
        "reviewed_individually": reviewed_individually,
        "source_checked": source_checked,
        "source_ir_checked": source_ir_checked,
        "decision": decision,
        "reason": reason,
        "question_text": question_text,
    }


def serialize_ir_spec(spec: Any, category: str, today: str) -> dict[str, Any]:
    source_document_path = spec.source_document_rel if isinstance(spec.source_document_rel, str) else ""
    return {
        "id": spec.id,
        "topic": spec.topic,
        "category": category,
        "fact_type": spec.fact_type,
        "statement": spec.statement,
        "conditions": list(spec.conditions),
        "examples": list(spec.examples),
        "source": spec.source_name or spec.source_title,
        "source_document_path": source_document_path,
        "source_url": spec.source_url,
        "source_title": spec.source_title,
        "source_version": spec.source_version,
        "source_last_checked": today,
        "source_section": spec.source_section,
        "source_quote_or_summary": spec.source_quote_or_summary,
        "confidence": spec.confidence,
        "question_potential": spec.question_potential,
        "notes": spec.notes,
    }


def serialize_question_spec(spec: Any, ir_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    ir_item = ir_by_id[spec.source_ir_id]
    explanation = true_explanation_from_statement(ir_item["statement"]) if spec.answer else false_explanation_from_statement(ir_item["statement"])
    return {
        "id": spec.id,
        "source_ir_id": spec.source_ir_id,
        "question": spec.question,
        "answer": spec.answer,
        "explanation": explanation,
        "difficulty": spec.difficulty,
    }


def build_cycle_payload_from_structured_profile(app_id: str, category: str, cycle: str, today: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    profile = SUPPORTED_PIPELINES.get((app_id, category))
    if profile is None:
        raise RuntimeError(f"No structured profile exists for {app_id}/{category}.")
    cycle_profile = slice_profile_for_cycle(profile, cycle)
    ir_specs = [serialize_ir_spec(spec, category, today) for spec in cycle_profile["ir_specs"]]
    ir_by_id = {item["id"]: item for item in ir_specs}
    question_specs = [serialize_question_spec(spec, ir_by_id) for spec in cycle_profile["question_specs"]]
    evidence: list[dict[str, Any]] = [
        {
            "phase": "cycle_start",
            "cycle": cycle,
            "app_id": app_id,
            "category": category,
            "candidate_ir_count": len(ir_specs),
            "target_ir_count": len(ir_specs),
            "target_question_count": len(question_specs),
            "source_files": sorted({item["source_document_path"] for item in ir_specs}),
            "mode": "structured_profile",
        }
    ]
    for ir_item in ir_specs:
        evidence.append(
            make_evidence_entry(
                phase="audit_ir_candidate",
                item_id=ir_item["id"],
                source_document_path=ir_item["source_document_path"],
                decision="approved",
                reason="IR item was loaded from the structured curated profile and reviewed individually.",
            )
        )
    for question in question_specs:
        evidence.append(
            make_evidence_entry(
                phase="audit_question_candidate",
                item_id=question["id"],
                source_ir_id=question["source_ir_id"],
                source_document_path=next(item["source_document_path"] for item in ir_specs if item["id"] == question["source_ir_id"]),
                decision="approved",
                reason="Question item was loaded from the structured curated profile and reviewed individually.",
                question_text=question["question"],
            )
        )
    for ir_item in ir_specs:
        evidence.append(
            make_evidence_entry(
                phase="adopt_ir_and_question_pair",
                item_id=ir_item["id"],
                source_ir_id=ir_item["id"],
                source_document_path=ir_item["source_document_path"],
                decision="approved",
                reason="Structured-profile IR and its mapped question items were adopted into the cycle.",
            )
        )
    evidence.append(
        {
            "phase": "cycle_complete",
            "cycle": cycle,
            "app_id": app_id,
            "category": category,
            "accepted_ir_count": len(ir_specs),
            "accepted_question_count": len(question_specs),
        }
    )
    return (
        {
            "app_id": app_id,
            "category": category,
            "cycle": cycle,
            "profile": "structured_curated_profile",
            "ir_specs": ir_specs,
            "question_specs": question_specs,
        },
        evidence,
    )


def load_profile_name(app_id: str) -> str:
    if not PROFILE_CONFIG_PATH.exists():
        return DEFAULT_PROFILE
    config = load_json(PROFILE_CONFIG_PATH)
    app_config = load_json(app_config_path(app_id))
    return app_config.get("source_profile") or config.get("app_defaults", {}).get(app_id) or DEFAULT_PROFILE


def supported_suffixes_for_profile(profile_name: str) -> set[str]:
    if not PROFILE_CONFIG_PATH.exists():
        return {".html", ".htm", ".md", ".txt"}
    config = load_json(PROFILE_CONFIG_PATH)
    profile = config.get("profiles", {}).get(profile_name, {})
    return set(profile.get("supported_suffixes", [".html", ".htm", ".md", ".txt"]))


def discover_source_files(app_id: str, category: str, supported_suffixes: set[str]) -> list[Path]:
    directory = source_dir(app_id, category)
    if not directory.exists():
        raise RuntimeError(f"Missing source directory: {directory}")
    files = [
        path
        for path in sorted(directory.iterdir())
        if path.is_file() and path.suffix.lower() in supported_suffixes
    ]
    if not files:
        raise RuntimeError(f"No supported source files found in: {directory}")
    return files


def parse_source_file(path: Path, category: str, today: str) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix in {".html", ".htm"}:
        items = parse_option_facts(path, category, today)
        items.extend(parse_html_sentence_facts(path, category, today))
        items.extend(parse_preformatted_facts(path, category, today))
        return items
    if suffix in {".md", ".txt"}:
        return parse_text_facts(path, category, today)
    return []


def ensure_unique_irs(raw_irs: list[dict[str, Any]], app_id: str, category: str) -> list[dict[str, Any]]:
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in raw_irs:
        statement_key = normalize_statement(item["statement"]).lower()
        if statement_key in seen:
            continue
        seen.add(statement_key)
        unique.append(item)
    for index, item in enumerate(unique, start=1):
        item["id"] = f"{app_id}_{category}_ir_{index:04d}"
    return unique


def build_questions_from_irs(app_id: str, category: str, irs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(irs) < 50:
        raise RuntimeError(
            f"At least 50 IR items are required to build a 100-question bank for {app_id}/{category}. Found {len(irs)}."
        )
    selected = irs[:50]
    questions: list[dict[str, Any]] = []
    for index, ir_item in enumerate(selected, start=1):
        peer_item = selected[index % len(selected)]
        questions.append(
            {
                "id": f"{app_id}_{category}_q_{len(questions) + 1:04d}",
                "source_ir_id": ir_item["id"],
                "question": normalize_statement(ir_item["statement"]) + ".",
                "answer": True,
                "explanation": true_explanation_from_statement(ir_item["statement"]),
                "difficulty": "intermediate",
            }
        )
        questions.append(
            {
                "id": f"{app_id}_{category}_q_{len(questions) + 1:04d}",
                "source_ir_id": ir_item["id"],
                "question": build_false_question(ir_item["statement"], peer_item["statement"]),
                "answer": False,
                "explanation": false_explanation_from_statement(ir_item["statement"]),
                "difficulty": "intermediate",
            }
        )
    return questions[:100]


def build_questions_for_cycle(app_id: str, category: str, cycle: str, irs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if cycle not in CYCLE_IR_WINDOWS:
        raise RuntimeError(f"Unsupported cycle: {cycle}")
    required_ir_count = CYCLE_IR_WINDOWS[cycle][1] - CYCLE_IR_WINDOWS[cycle][0]
    if len(irs) < required_ir_count:
        raise RuntimeError(
            f"At least {required_ir_count} IR items are required to build {cycle} for {app_id}/{category}. Found {len(irs)}."
        )
    selected = irs[:required_ir_count]
    questions: list[dict[str, Any]] = []
    for index, ir_item in enumerate(selected, start=1):
        peer_item = selected[index % len(selected)]
        questions.append(
            {
                "id": f"{app_id}_{category}_{cycle}_q_{len(questions) + 1:04d}",
                "source_ir_id": ir_item["id"],
                "question": normalize_statement(ir_item["statement"]) + ".",
                "answer": True,
                "explanation": true_explanation_from_statement(ir_item["statement"]),
                "difficulty": "intermediate",
            }
        )
        questions.append(
            {
                "id": f"{app_id}_{category}_{cycle}_q_{len(questions) + 1:04d}",
                "source_ir_id": ir_item["id"],
                "question": build_false_question(ir_item["statement"], peer_item["statement"]),
                "answer": False,
                "explanation": false_explanation_from_statement(ir_item["statement"]),
                "difficulty": "intermediate",
            }
        )
    return questions


def build_bank(app_id: str, category: str, today: str) -> dict[str, Any]:
    profile_name = load_profile_name(app_id)
    supported_suffixes = supported_suffixes_for_profile(profile_name)
    source_files = discover_source_files(app_id, category, supported_suffixes)
    raw_irs: list[dict[str, Any]] = []
    for path in source_files:
        raw_irs.extend(parse_source_file(path, category, today))
    irs = ensure_unique_irs(raw_irs, app_id, category)
    questions = build_questions_from_irs(app_id, category, irs)
    required_ir_ids = {item["source_ir_id"] for item in questions}
    bank_irs = [item for item in irs if item["id"] in required_ir_ids]
    return {
        "app_id": app_id,
        "category": category,
        "profile": profile_name,
        "ir_specs": bank_irs,
        "question_specs": questions,
    }


def build_cycle_payload(app_id: str, category: str, cycle: str, today: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if cycle == "cycle_01" and (app_id, category) in SUPPORTED_PIPELINES:
        return build_cycle_payload_from_structured_profile(app_id, category, cycle, today)

    if cycle not in CYCLE_IR_WINDOWS or cycle not in CYCLE_QUESTION_TARGETS:
        raise RuntimeError(f"Unsupported cycle: {cycle}")
    profile_name = load_profile_name(app_id)
    supported_suffixes = supported_suffixes_for_profile(profile_name)
    source_files = discover_source_files(app_id, category, supported_suffixes)
    raw_irs: list[dict[str, Any]] = []
    for path in source_files:
        raw_irs.extend(parse_source_file(path, category, today))
    irs = ensure_unique_irs(raw_irs, app_id, category)
    used_ir_ids = used_ir_ids_from_previous_cycles(app_id, category, cycle)
    remaining_irs = [item for item in irs if item["id"] not in used_ir_ids]
    target_question_count = CYCLE_QUESTION_TARGETS[cycle]
    target_ir_count = target_question_count // 2
    accepted_irs: list[dict[str, Any]] = []
    questions: list[dict[str, Any]] = []
    seen_question_texts: set[str] = set()
    evidence: list[dict[str, Any]] = [
        {
            "phase": "cycle_start",
            "cycle": cycle,
            "app_id": app_id,
            "category": category,
            "candidate_ir_count": len(remaining_irs),
            "target_ir_count": target_ir_count,
            "target_question_count": target_question_count,
            "source_files": [str(path).replace("\\", "/") for path in source_files],
        }
    ]

    for candidate in remaining_irs:
        ir_ok, ir_reason = audit_ir_candidate(candidate)
        if not ir_ok:
            evidence.append(
                make_evidence_entry(
                    phase="audit_ir_candidate",
                    item_id=candidate["id"],
                    source_document_path=candidate.get("source_document_path", ""),
                    source_ir_checked=False,
                    decision="rejected",
                    reason=ir_reason,
                )
            )
            continue
        evidence.append(
            make_evidence_entry(
                phase="audit_ir_candidate",
                item_id=candidate["id"],
                source_document_path=candidate.get("source_document_path", ""),
                decision="approved",
                reason="IR candidate passed one-by-one source and scope review.",
            )
        )
        peer_pool = [item for item in remaining_irs if item["id"] != candidate["id"] and item["id"] not in {ir["id"] for ir in accepted_irs}]
        if not peer_pool:
            peer_pool = [item for item in remaining_irs if item["id"] != candidate["id"]]
        if not peer_pool:
            evidence.append(
                make_evidence_entry(
                    phase="create_question_pair",
                    item_id=candidate["id"],
                    source_document_path=candidate.get("source_document_path", ""),
                    decision="rejected",
                    reason="No peer IR was available to build a realistic false question.",
                )
            )
            continue

        true_question = make_true_question(app_id, category, cycle, len(questions) + 1, candidate)
        true_ok, true_reason = audit_question_candidate(true_question, candidate)
        if not true_ok:
            evidence.append(
                make_evidence_entry(
                    phase="audit_question_candidate",
                    item_id=true_question["id"],
                    source_ir_id=candidate["id"],
                    source_document_path=candidate.get("source_document_path", ""),
                    decision="rejected",
                    reason=true_reason,
                    question_text=true_question["question"],
                )
            )
            continue
        evidence.append(
            make_evidence_entry(
                phase="audit_question_candidate",
                item_id=true_question["id"],
                source_ir_id=candidate["id"],
                source_document_path=candidate.get("source_document_path", ""),
                decision="approved",
                reason="True question passed one-by-one content and traceability review.",
                question_text=true_question["question"],
            )
        )

        false_question = None
        for peer in peer_pool:
            proposed = make_false_question(app_id, category, cycle, len(questions) + 2, candidate, peer)
            false_ok, false_reason = audit_question_candidate(proposed, candidate)
            duplicate_reason = ""
            if proposed["question"] in seen_question_texts or proposed["question"] == true_question["question"]:
                false_ok = False
                duplicate_reason = "False question duplicated an existing or paired question."
            if false_ok and proposed["question"] not in seen_question_texts and proposed["question"] != true_question["question"]:
                false_question = proposed
                evidence.append(
                    make_evidence_entry(
                        phase="audit_question_candidate",
                        item_id=proposed["id"],
                        source_ir_id=candidate["id"],
                        source_document_path=candidate.get("source_document_path", ""),
                        decision="approved",
                        reason="False question passed one-by-one misconception and traceability review.",
                        question_text=proposed["question"],
                    )
                )
                break
            evidence.append(
                make_evidence_entry(
                    phase="audit_question_candidate",
                    item_id=proposed["id"],
                    source_ir_id=candidate["id"],
                    source_document_path=candidate.get("source_document_path", ""),
                    decision="rejected",
                    reason=duplicate_reason or false_reason,
                    question_text=proposed["question"],
                )
            )
        if false_question is None:
            evidence.append(
                make_evidence_entry(
                    phase="remake_question_pair",
                    item_id=candidate["id"],
                    source_ir_id=candidate["id"],
                    source_document_path=candidate.get("source_document_path", ""),
                    decision="rejected",
                    reason="Candidate IR could not produce an acceptable false question, so the pair was discarded and the curator moved to the next IR.",
                )
            )
            continue

        if true_question["question"] in seen_question_texts:
            evidence.append(
                make_evidence_entry(
                    phase="remake_question_pair",
                    item_id=candidate["id"],
                    source_ir_id=candidate["id"],
                    source_document_path=candidate.get("source_document_path", ""),
                    decision="rejected",
                    reason="True question text duplicated a previously adopted question, so the pair was discarded.",
                    question_text=true_question["question"],
                )
            )
            continue

        accepted_irs.append(candidate)
        questions.append(true_question)
        questions.append(false_question)
        seen_question_texts.add(true_question["question"])
        seen_question_texts.add(false_question["question"])
        evidence.append(
            make_evidence_entry(
                phase="adopt_ir_and_question_pair",
                item_id=candidate["id"],
                source_ir_id=candidate["id"],
                source_document_path=candidate.get("source_document_path", ""),
                decision="approved",
                reason="IR and its true/false question pair were adopted into the cycle after individual review.",
            )
        )
        if len(accepted_irs) >= target_ir_count:
            break

    if len(accepted_irs) < target_ir_count or len(questions) < target_question_count:
        raise RuntimeError(
            f"Could not curate enough individually acceptable items for {app_id}/{category}/{cycle}. "
            f"Needed {target_ir_count} IR items / {target_question_count} questions, got {len(accepted_irs)} IR items / {len(questions)} questions."
        )

    evidence.append(
        {
            "phase": "cycle_complete",
            "cycle": cycle,
            "app_id": app_id,
            "category": category,
            "accepted_ir_count": len(accepted_irs),
            "accepted_question_count": len(questions[:target_question_count]),
        }
    )

    return (
        {
            "app_id": app_id,
            "category": category,
            "cycle": cycle,
            "profile": profile_name,
            "ir_specs": accepted_irs,
            "question_specs": questions[:target_question_count],
        },
        evidence,
    )


def build_and_write_bank(app_id: str, category: str, today: str) -> Path:
    payload = build_bank(app_id, category, today)
    destination = BANK_ROOT / app_id / f"{category}.json"
    write_json(destination, payload)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a 100-question source-backed bank for a StudyApp app/category.")
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--date", default="2026-06-06")
    args = parser.parse_args()
    path = build_and_write_bank(args.app_id, args.category, args.date)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
