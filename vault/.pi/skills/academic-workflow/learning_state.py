#!/usr/bin/env python3
"""Validate and append evidence records inside one academic note."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Collection, Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any

ERROR_TYPES = frozenset(
    {
        "recall",
        "concept",
        "translation",
        "procedure",
        "calculation",
        "misread",
        "incomplete-justification",
        "time-management",
    }
)
CARD_ACTIONS = frozenset({"create", "revise", "suspend", "none"})
FENCE_OPEN = "```academic-evidence"
FENCE_CLOSE = "```"
ID_RE = re.compile(r"^[a-z][a-z0-9-]*-[0-9a-f]{16}$")

SESSION_FIELDS = (
    "record_type",
    "session_id",
    "started_at",
    "course_id",
    "planned_minutes",
    "target_note",
    "concept_ids",
    "source_refs",
    "next_action",
)
ATTEMPT_FIELDS = (
    "record_type",
    "attempt_id",
    "question_id",
    "attempted_at",
    "course_id",
    "concept_ids",
    "marks_awarded",
    "marks_available",
    "time_seconds",
    "confidence_before",
    "grading_source",
    "grading_confidence",
    "error_types",
    "feedback",
    "card_action",
)


def canonical_json(value: Mapping[str, object]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_id(prefix: str, identity: Mapping[str, object]) -> str:
    normalized_prefix = re.sub(r"[^a-z0-9]+", "-", prefix.lower()).strip("-")
    if not normalized_prefix or not normalized_prefix[0].isalpha():
        raise ValueError("ID prefix must start with a letter")
    digest = hashlib.sha256(canonical_json(identity).encode("utf-8")).hexdigest()[:16]
    return "%s-%s" % (normalized_prefix, digest)


def _is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_timestamp(field: str, value: object, errors: list[str]) -> None:
    if not _is_nonempty_string(value):
        errors.append("%s must be a non-empty ISO-8601 timestamp" % field)
        return
    try:
        datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        errors.append("%s must be an ISO-8601 timestamp" % field)


def _validate_string_list(field: str, value: object, errors: list[str], *, allow_empty: bool = False) -> None:
    if not isinstance(value, list):
        errors.append("%s must be a list" % field)
        return
    if not allow_empty and not value:
        errors.append("%s must not be empty" % field)
    if any(not _is_nonempty_string(item) for item in value):
        errors.append("%s must contain only non-empty strings" % field)


def _require_fields(record: Mapping[str, object], fields: Sequence[str], errors: list[str]) -> None:
    for field in fields:
        if field not in record:
            errors.append("missing required field: %s" % field)


def validate_record(record: Mapping[str, object]) -> list[str]:
    errors: list[str] = []
    record_type = record.get("record_type")
    if record_type == "study_session":
        _require_fields(record, SESSION_FIELDS, errors)
        if errors:
            return errors
        for field in ("session_id", "course_id", "target_note", "next_action"):
            if not _is_nonempty_string(record[field]):
                errors.append("%s must be a non-empty string" % field)
        _validate_timestamp("started_at", record["started_at"], errors)
        planned = record["planned_minutes"]
        if not isinstance(planned, int) or isinstance(planned, bool) or planned <= 0:
            errors.append("planned_minutes must be a positive integer")
        _validate_string_list("concept_ids", record["concept_ids"], errors)
        _validate_string_list("source_refs", record["source_refs"], errors, allow_empty=True)
        return errors

    if record_type == "assessment_attempt":
        _require_fields(record, ATTEMPT_FIELDS, errors)
        if errors:
            return errors
        for field in ("attempt_id", "question_id", "course_id", "grading_source", "feedback"):
            if not isinstance(record[field], str):
                errors.append("%s must be a string" % field)
        for field in ("attempt_id", "question_id", "course_id", "grading_source"):
            if isinstance(record[field], str) and not record[field].strip():
                errors.append("%s must not be empty" % field)
        _validate_timestamp("attempted_at", record["attempted_at"], errors)
        _validate_string_list("concept_ids", record["concept_ids"], errors)

        awarded = record["marks_awarded"]
        available = record["marks_available"]
        if not isinstance(available, int) or isinstance(available, bool) or available <= 0:
            errors.append("marks_available must be a positive integer")
        if not isinstance(awarded, int) or isinstance(awarded, bool) or awarded < 0:
            errors.append("marks_awarded must be a non-negative integer")
        elif isinstance(available, int) and not isinstance(available, bool) and awarded > available:
            errors.append("marks_awarded must not exceed marks_available")

        seconds = record["time_seconds"]
        if not isinstance(seconds, int) or isinstance(seconds, bool) or seconds <= 0:
            errors.append("time_seconds must be a positive integer")
        for field in ("confidence_before", "grading_confidence"):
            value = record[field]
            if not _is_number(value) or not 0 <= float(value) <= 1:
                errors.append("%s must be a number from 0 to 1" % field)

        error_types = record["error_types"]
        _validate_string_list("error_types", error_types, errors, allow_empty=True)
        if isinstance(error_types, list):
            unknown = sorted(set(error_types) - ERROR_TYPES)
            if unknown:
                errors.append("unknown error_types: %s" % ", ".join(unknown))
            if error_types and not _is_nonempty_string(record["feedback"]):
                errors.append("feedback must describe observed evidence when error_types are present")

        action = record["card_action"]
        if action not in CARD_ACTIONS:
            errors.append("card_action must be one of: %s" % ", ".join(sorted(CARD_ACTIONS)))
        return errors

    return ["record_type must be study_session or assessment_attempt"]


def load_records(note: Path) -> list[dict[str, object]]:
    lines = note.read_text(encoding="utf-8").splitlines()
    records: list[dict[str, object]] = []
    inside = False
    for line_number, line in enumerate(lines, 1):
        if not inside and line == FENCE_OPEN:
            inside = True
            continue
        if inside and line == FENCE_CLOSE:
            inside = False
            continue
        if not inside or not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError("invalid academic-evidence JSON on line %d: %s" % (line_number, error)) from error
        if not isinstance(value, dict):
            raise ValueError("academic-evidence line %d must be a JSON object" % line_number)
        records.append(value)
    if inside:
        raise ValueError("unclosed academic-evidence fence")
    return records


def record_id(record: Mapping[str, object]) -> str:
    if record.get("record_type") == "study_session":
        value = record.get("session_id")
    elif record.get("record_type") == "assessment_attempt":
        value = record.get("attempt_id")
    else:
        raise ValueError("unknown record_type")
    if not _is_nonempty_string(value):
        raise ValueError("record ID is missing")
    return str(value)


def append_record(note: Path, record: Mapping[str, object]) -> str:
    errors = validate_record(record)
    if errors:
        raise ValueError("; ".join(errors))
    if not note.is_file():
        raise FileNotFoundError(note)
    identifier = record_id(record)
    existing = load_records(note)
    if any(record_id(item) == identifier for item in existing):
        raise ValueError("record ID already exists: %s" % identifier)

    original = note.read_text(encoding="utf-8")
    separator = "" if original.endswith("\n\n") else ("\n" if original.endswith("\n") else "\n\n")
    block = "%s\n%s\n%s\n" % (FENCE_OPEN, canonical_json(record), FENCE_CLOSE)
    note.write_text(original + separator + block, encoding="utf-8")
    return identifier


def _record_time(record: Mapping[str, object]) -> datetime:
    raw = record.get("attempted_at") or record.get("started_at")
    if not isinstance(raw, str):
        return datetime.min
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min


def latest_for_concept(
    records: Sequence[Mapping[str, object]], concept_id: str
) -> Mapping[str, object] | None:
    matches = [record for record in records if concept_id in record.get("concept_ids", [])]
    return max(matches, key=_record_time) if matches else None


def decide_card_action(
    *,
    error_types: Collection[str],
    passed: bool,
    has_related_card: bool,
    repeated_failure: bool,
    misleading_card: bool,
) -> str:
    unknown = set(error_types) - ERROR_TYPES
    if unknown:
        raise ValueError("unknown error types: %s" % ", ".join(sorted(unknown)))
    if misleading_card:
        return "suspend"
    if passed:
        return "none"
    supports_card = bool({"recall", "concept"} & set(error_types))
    if not supports_card:
        return "none"
    if has_related_card or repeated_failure:
        return "revise"
    return "create"


def _load_record_argument(raw: str) -> dict[str, object]:
    value: Any
    if raw == "-":
        value = json.load(sys.stdin)
    else:
        value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("record must be a JSON object")
    return value


def command_validate(note: Path) -> int:
    failures = []
    try:
        records = load_records(note)
    except (OSError, ValueError) as error:
        print(json.dumps({"errors": [str(error)], "valid": False}, sort_keys=True))
        return 1
    for index, record in enumerate(records):
        for error in validate_record(record):
            failures.append({"record": index + 1, "error": error})
    print(json.dumps({"errors": failures, "records": len(records), "valid": not failures}, sort_keys=True))
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    validate = commands.add_parser("validate", help="validate evidence blocks in one note")
    validate.add_argument("note", type=Path)

    latest = commands.add_parser("latest", help="print latest evidence for a concept")
    latest.add_argument("note", type=Path)
    latest.add_argument("concept_id")

    append = commands.add_parser("append", help="append one validated JSON record")
    append.add_argument("note", type=Path)
    append.add_argument("record_json", help="JSON object or - for stdin")

    decide = commands.add_parser("decide-card", help="choose a deterministic postmortem card action")
    decide.add_argument("--errors", default="")
    decide.add_argument("--passed", action="store_true")
    decide.add_argument("--has-related-card", action="store_true")
    decide.add_argument("--repeated-failure", action="store_true")
    decide.add_argument("--misleading-card", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "validate":
            return command_validate(args.note)
        if args.command == "latest":
            result = latest_for_concept(load_records(args.note), args.concept_id)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        if args.command == "append":
            identifier = append_record(args.note, _load_record_argument(args.record_json))
            print(json.dumps({"record_id": identifier}, sort_keys=True))
            return 0
        errors = frozenset(value for value in args.errors.split(",") if value)
        action = decide_card_action(
            error_types=errors,
            passed=args.passed,
            has_related_card=args.has_related_card,
            repeated_failure=args.repeated_failure,
            misleading_card=args.misleading_card,
        )
        print(json.dumps({"card_action": action}, sort_keys=True))
        return 0
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({"error": str(error)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
