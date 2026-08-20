# Closed-loop academic workflow design

## Goal

Turn the existing Pi and Obsidian toolkit into a small, evidence-driven academic loop. The implementation covers six selected capabilities: truthful PDF status, one `/study` orchestrator, evidence-backed concept state, a fixed assessment-error taxonomy, postmortem-driven card actions, and five visible command entrypoints.

## Scope

The visible commands are:

- `/study <course> <minutes> [target-note]`
- `/capture [source]`
- `/research <question-or-topic>`
- `/exam <course> [question-or-paper]`
- `/doctor`

The existing specialist prompt instructions remain available as internal workflow references. Pi must not discover them as top-level slash commands.

This release does not add a general health system, course registry, vector database, sync transaction layer, mobile capture automation, model router, or new Obsidian community plugins.

## Distribution boundary

Ravmax is the live vault. It may contain vault-relative configuration and real academic notes, but this implementation must not rewrite existing learner notes while installing the workflow.

Primer is the publishable distribution. It contains generic prompts, skills, schemas, fixtures, verifier rules, setup documentation, workflow documentation, demo content, and changelog entries. It must not contain Ravmax paths, course names, source manifests, credentials, or learner evidence.

The two repositories receive intentional, separate commits. Existing unrelated Ravmax changes remain unstaged.

## PDF status model

The PDF index assigns exactly one status to every source record:

- `indexed`: extraction produced searchable text.
- `missing_target`: a local path or decoded `file://` URI does not exist.
- `unsupported_uri`: the source URI scheme cannot resolve to a local file.
- `unreadable`: the target exists but cannot be opened or read.
- `no_text_layer`: the target is readable and has pages, but text extraction produced no text.
- `ocr_pending`: a readable document without text has been explicitly queued for OCR.
- `failed`: the selected extraction backend raised an error that is not represented by another state.

Zero pages alone must not imply OCR. Missing targets and unsupported URIs must never enter the OCR queue.

Each manifest record includes:

- `kind`
- `source`
- `resolved_path`
- `status`
- `pages`
- `text_pages`
- `chars`
- `content_hash`
- `extraction_backend`
- `extracted_at`
- `source_stamp`
- `failure_reason`

Optional values use JSON `null`, not placeholder strings. Status selection and URI decoding are deterministic and testable without invoking an LLM.

`/doctor` reports counts by status, lists blocking records, identifies stale legacy records, and exits without changing sources or indexes.

## Learning evidence model

`LEARNER.md` remains limited to stable preferences, goals, accommodations, and constraints. Dynamic mastery claims are derived from evidence stored in the note currently being studied.

Machine-readable records use fenced JSONL blocks with these markers:

```text
academic-evidence
```

Each record has a `record_type` and stable ID. The supported records are:

### Study session

Required fields:

- `record_type: "study_session"`
- `session_id`
- `started_at`
- `course_id`
- `planned_minutes`
- `target_note`
- `concept_ids`
- `source_refs`
- `next_action`

### Assessment attempt

Required fields:

- `record_type: "assessment_attempt"`
- `attempt_id`
- `question_id`
- `attempted_at`
- `course_id`
- `concept_ids`
- `marks_awarded`
- `marks_available`
- `time_seconds`
- `confidence_before`
- `grading_source`
- `grading_confidence`
- `error_types`
- `feedback`
- `card_action`

IDs are derived from normalized identity inputs plus a timestamp or content digest. Re-running validation must not mutate IDs.

The evidence utility supports validation, latest-evidence lookup by concept, attempt recording, and deterministic card-action selection. It uses the Python standard library only.

## Assessment error taxonomy

`error_types` is a non-empty subset of:

- `recall`
- `concept`
- `translation`
- `procedure`
- `calculation`
- `misread`
- `incomplete-justification`
- `time-management`

Unknown labels fail validation. Multiple labels are allowed. Every recorded error must be supported by feedback describing the observed answer or step; the system must not infer a permanent learner trait.

## Postmortem-driven card actions

The deterministic card decision returns one of:

- `create`
- `revise`
- `suspend`
- `none`

Decision rules:

1. `recall` or `concept` on the first supported failure returns `create` when no related card exists.
2. A repeated `recall` or `concept` failure with a related card returns `revise`.
3. `translation`, `procedure`, `calculation`, `misread`, `incomplete-justification`, or `time-management` alone returns `none`; the postmortem records a practice intervention instead of manufacturing a recall card.
4. A card demonstrated to be misleading or to encode a corrected misconception returns `suspend` until revised.
5. Passing attempts without a supported retrieval failure return `none`.

The agent proposes the resulting card content or intervention in the target note. It must not bulk-create cards or update unrelated notes.

## `/study` workflow

`/study` owns the daily learning loop:

1. Resolve course, duration, and one target note. Ask only when the target remains ambiguous.
2. Run PDF-status checks for cited sources.
3. Read recent concept evidence from the target note.
4. Probe before teaching.
5. Teach only the demonstrated gap.
6. Require retrieval or application.
7. Grade against an explicit source or rubric.
8. Record error evidence when present.
9. Run the card-action decision.
10. Append one validated session record and any attempt record to the target note.
11. End with one concrete `next_action`.

A turn may write only the target note. The command must not update `LEARNER.md` with dynamic mastery.

## `/exam` workflow

`/exam` selects or accepts a stable question identity, captures time and pre-answer confidence, grades against an explicit source, applies the fixed error taxonomy, records the attempt, and runs the card-action decision. Missing grading evidence must reduce `grading_confidence`; it must not be represented as authoritative marking.

## `/capture` and `/research`

`/capture` and `/research` are front doors over existing specialist instructions. `/capture` routes source ingestion and note normalization. `/research` routes Zotero, web, PDF, synthesis, and citation behavior. Both preserve existing source-grounding and one-note write rules.

## Internal workflow references

The current specialist prompts move from `.pi/prompts/` into `.pi/skills/academic-workflow/references/`. Their filenames and instruction bodies remain stable where possible. The `academic-workflow` skill maps each of the five front doors to those references and states which deterministic utility to run.

References in `CLAUDE.md`, `APPEND_SYSTEM.md`, `PLAN.md`, `LEARNER.md`, help text, verifier rules, and tests must use the new visible commands or the internal reference paths. No compatibility aliases remain in `.pi/prompts/`.

## Verification

Automated tests cover:

- URI decoding and missing-target classification
- No-text versus extraction-failure classification
- Complete manifest provenance fields
- Legacy manifest detection
- Evidence-schema validation
- Stable IDs
- Error-label rejection
- Every card-action rule
- Exactly five discoverable prompt files
- No stale references to removed top-level specialist commands
- No Ravmax-specific values in Primer

Smoke verification runs the actual index doctor, evidence validator, `/study` prompt discovery, `/exam` prompt discovery, and Primer release verifier. Both repositories must be clean except for known pre-existing Ravmax changes before their respective intentional commits.
