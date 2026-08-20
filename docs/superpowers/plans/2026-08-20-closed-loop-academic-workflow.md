# Closed-loop academic workflow implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement truthful PDF indexing, evidence-backed study and exam records, postmortem card decisions, and five visible academic commands in Ravmax and the publishable Primer distribution.

**Architecture:** Deterministic Python utilities own source states, record schemas, IDs, validation, and card decisions. Markdown prompts orchestrate those utilities and existing specialist instructions. Ravmax is implemented first; Primer receives the same contracts with generic fixtures and distribution documentation.

**Tech stack:** Python 3 standard library, Markdown with YAML front matter, Pi prompt/skill discovery, Obsidian notes and Bases, `unittest`, Primer release verifier.

**Spec:** `docs/superpowers/specs/2026-08-20-closed-loop-academic-workflow-design.md`

## Global constraints

- Expose exactly `/study`, `/capture`, `/research`, `/exam`, and `/doctor` as prompt files.
- Preserve all 25 specialist instruction bodies as internal references; do not leave compatibility aliases in `.pi/prompts/`.
- A study or exam turn may write only its selected target note.
- Keep dynamic mastery evidence out of `LEARNER.md`.
- Use only the eight error labels and four card actions specified in the design.
- Zero pages must not imply OCR.
- Primer must contain no Ravmax path, course, source, credential, or learner data.
- Do not stage Ravmax `.pi/settings.json`, `.pi/npm/`, or modified lecture notes.
- Use test-first red-green cycles for Python behavior and verifier behavior.

---

### Task 1: Truthful PDF status model in Ravmax

**Files:**
- Create: `C:/Users/ravin/My Drive/Ravmax/.pi/lib/__init__.py`
- Create: `C:/Users/ravin/My Drive/Ravmax/.pi/lib/vault.py`
- Modify: `C:/Users/ravin/My Drive/Ravmax/.pi/skills/pdf-search/index.py`
- Modify: `C:/Users/ravin/My Drive/Ravmax/.pi/skills/pdf-search/SKILL.md`
- Create: `C:/Users/ravin/My Drive/Ravmax/.pi/tests/test_pdf_index.py`

**Interfaces:**
- Produces `find_vault(start: Path | None = None) -> Path` in `.pi/lib/vault.py`.
- Produces `SourceStatus(StrEnum)` with `indexed`, `missing_target`, `unsupported_uri`, `unreadable`, `no_text_layer`, `ocr_pending`, and `failed`.
- Produces `Resolution(status: SourceStatus | None, path: Path | None, failure_reason: str | None)`.
- Produces `ExtractionResult(status: SourceStatus, pages: int, text_pages: int, chars: int, backend: str | None, failure_reason: str | None)`.
- Produces `build_manifest_record(source: Path, resolution: Resolution, extraction: ExtractionResult | None) -> dict[str, object]`.
- Adds CLI subcommand `doctor` that reads the manifest, reports status counts and blocking records, and returns nonzero for blocking or legacy records without mutating files.

- [ ] **Step 1: Write failing resolution and status tests**

Create tests using temporary directories and imported real script code. Cover a percent-decoded `file:///` URI, missing target, unsupported `https:` URI, readable text PDF through a patched extraction boundary, no-text result, backend failure, complete manifest keys, and legacy-record doctor failure.

```python
self.assertEqual(result.status, index.SourceStatus.MISSING_TARGET)
self.assertIsNone(result.path)
self.assertEqual(record["status"], "missing_target")
self.assertIn("content_hash", record)
self.assertNotEqual(index.doctor(manifest), 0)
```

- [ ] **Step 2: Run the tests and verify the expected failures**

Run:

```text
python -m unittest .pi.tests.test_pdf_index -v
```

Expected: failures because `SourceStatus`, provenance fields, portable vault discovery, and `doctor` do not exist.

- [ ] **Step 3: Port the portable vault resolver**

Copy Primer’s `.pi/lib/vault.py` behavior without Primer-specific paths. Add `.pi/lib/__init__.py`. Update `index.py` to import `find_vault` after adding `.pi` to `sys.path` relative to `__file__`.

- [ ] **Step 4: Implement explicit resolution and extraction results**

Use `urllib.parse.urlparse` and `unquote` for URI handling, `Path.exists()` and `Path.is_file()` for target classification, `hashlib.sha256()` for readable source hashes, UTC ISO-8601 timestamps, and `null`-compatible `None` values. Preserve existing extraction backends behind `extract()`; translate outcomes into `ExtractionResult` once.

- [ ] **Step 5: Implement manifest migration and doctor**

Write every new index record with the complete key set. Treat records missing `status`, `resolved_path`, `content_hash`, `extraction_backend`, `extracted_at`, `text_pages`, or `failure_reason` as legacy. `doctor` prints deterministic JSON and does not rewrite the manifest.

- [ ] **Step 6: Run PDF tests**

Run:

```text
python -m unittest .pi.tests.test_pdf_index -v
```

Expected: all PDF status tests pass.

- [ ] **Step 7: Commit Ravmax PDF changes**

Stage only the five paths listed for this task and commit:

```text
git commit -m "feat: add truthful PDF source states"
```

### Task 2: Evidence and postmortem engine in Ravmax

**Files:**
- Create: `C:/Users/ravin/My Drive/Ravmax/.pi/skills/academic-workflow/SKILL.md`
- Create: `C:/Users/ravin/My Drive/Ravmax/.pi/skills/academic-workflow/learning_state.py`
- Create: `C:/Users/ravin/My Drive/Ravmax/.pi/tests/test_learning_state.py`

**Interfaces:**
- Produces `ERROR_TYPES: frozenset[str]` containing exactly `recall`, `concept`, `translation`, `procedure`, `calculation`, `misread`, `incomplete-justification`, and `time-management`.
- Produces `CARD_ACTIONS: frozenset[str]` containing exactly `create`, `revise`, `suspend`, and `none`.
- Produces `stable_id(prefix: str, identity: Mapping[str, object]) -> str` using canonical JSON and SHA-256.
- Produces `validate_record(record: Mapping[str, object]) -> list[str]`; an empty list means valid.
- Produces `load_records(note: Path) -> list[dict[str, object]]` for every `academic-evidence` fenced block.
- Produces `append_record(note: Path, record: Mapping[str, object]) -> str`, appending one fenced JSON line and returning its stable ID.
- Produces `latest_for_concept(records: Sequence[Mapping[str, object]], concept_id: str) -> Mapping[str, object] | None`.
- Produces `decide_card_action(*, error_types: Collection[str], passed: bool, has_related_card: bool, repeated_failure: bool, misleading_card: bool) -> str`.
- Provides CLI subcommands `validate`, `latest`, `append`, and `decide-card`.

- [ ] **Step 1: Write failing schema and card-decision tests**

Cover stable IDs under key reordering, required session fields, required attempt fields, unknown error rejection, non-empty feedback when errors exist, marks bounds, confidence bounds, fenced-record round trip, latest concept selection, and every decision rule.

```python
self.assertEqual(
    state.decide_card_action(
        error_types={"recall"}, passed=False, has_related_card=False,
        repeated_failure=False, misleading_card=False,
    ),
    "create",
)
```

- [ ] **Step 2: Run tests and verify expected failures**

Run:

```text
python -m unittest .pi.tests.test_learning_state -v
```

Expected: import or symbol failures because the evidence engine does not exist.

- [ ] **Step 3: Implement constants, IDs, and validation**

Use `json.dumps(..., sort_keys=True, separators=(",", ":"))`, `hashlib.sha256`, `datetime.fromisoformat`, and explicit field validators. Reject booleans where integer marks or seconds are required. Validation returns all errors in deterministic field order.

- [ ] **Step 4: Implement fenced-record parsing and append**

Recognize only fences whose opening line is exactly ```` ```academic-evidence ````. Parse one JSON object per nonblank line. Append one complete fenced block after a blank line. Validate before writing; invalid records leave the note unchanged.

- [ ] **Step 5: Implement card decisions and CLI**

Apply the design rules in precedence order: misleading card → `suspend`; passed → `none`; supported recall/concept with existing or repeated evidence → `revise`; first supported recall/concept without a card → `create`; all other cases → `none`. CLI JSON output is deterministic and nonzero on invalid input.

- [ ] **Step 6: Run learning-state tests**

Run:

```text
python -m unittest .pi.tests.test_learning_state -v
```

Expected: all tests pass.

- [ ] **Step 7: Commit Ravmax evidence engine**

Stage only the new skill and test paths and commit:

```text
git commit -m "feat: add evidence-backed learning state"
```

### Task 3: Five-command Ravmax workflow

**Files:**
- Move these 25 files from `.pi/prompts/` to `.pi/skills/academic-workflow/references/`: `lecture-video.md`, `lecture.md`, `probe.md`, `teach.md`, `classify.md`, `overview.md`, `mock.md`, `postmortem.md`, `weakspots.md`, `review.md`, `cards.md`, `cram.md`, `cite.md`, `gap.md`, `exercises.md`, `feynman.md`, `paper.md`, `worked.md`, `source.md`, `find.md`, `synth.md`, `summary.md`, `predict.md`, `paper-review.md`, `crosswalk.md`.
- Create: `.pi/prompts/study.md`
- Create: `.pi/prompts/capture.md`
- Create: `.pi/prompts/research.md`
- Create: `.pi/prompts/exam.md`
- Create: `.pi/prompts/doctor.md`
- Modify: `.pi/skills/academic-workflow/SKILL.md`
- Modify: `.pi/APPEND_SYSTEM.md`
- Modify: `.pi/PLAN.md`
- Modify: `.pi/LEARNER.md`
- Modify: `.pi/agents/academic.md`
- Modify relevant references in `.pi/skills/canvas-gen/`, `.pi/skills/past-papers/`, `.pi/skills/pdf-search/`, `.pi/skills/spaced-repetition/`, `.pi/skills/vault-syntax/`, root `README.md`, and root `CLAUDE.md` only where they name removed commands.
- Create: `.pi/tests/test_workflow_prompts.py`

**Interfaces:**
- `/study` calls the internal probe, teach, exercises/worked, postmortem, and cards references and requires `learning_state.py validate` before one target-note write.
- `/exam` calls mock/paper, classify/crosswalk, postmortem, and cards references and records time, confidence, grading evidence, exact error labels, and card action.
- `/capture` routes lecture, lecture-video, source, summary, and find references.
- `/research` routes find, source, cite, synth, summary, gap, and paper-review references.
- `/doctor` runs `pdf-search/index.py doctor` and reports without writing.

- [ ] **Step 1: Write failing prompt-discovery tests**

Test that `.pi/prompts` contains exactly the five names, each has `description` and `argument-hint`, every internal reference exists, no top-level prompt references `/teach` or another removed command, `/study` and `/exam` mention the evidence validator, and `/doctor` invokes the PDF doctor.

- [ ] **Step 2: Run tests and verify expected failures**

Run:

```text
python -m unittest .pi.tests.test_workflow_prompts -v
```

Expected: failure because 25 old prompts remain and the five front doors are absent.

- [ ] **Step 3: Move specialist prompts into internal references**

Use filesystem moves so git records renames. Preserve front matter and bodies in internal references; revise only stale top-level slash-command calls and the old three-label postmortem/card rules.

- [ ] **Step 4: Write the five front-door prompts**

Use the existing front-matter convention. Each prompt names its allowed references, deterministic commands, inputs, ambiguity behavior, write limit, and completion record. `/study` uses `$ARGUMENTS` as `<course> <minutes> [target-note]`; `/exam` uses `<course> [question-or-paper]`.

- [ ] **Step 5: Update skill and system references**

Document the five-command map in `academic-workflow/SKILL.md`. Replace stale user-facing command names in system and skill docs. Keep historical command names only when describing internal reference filenames, not callable slash commands. Remove the unavailable `@academic` fan-out from synthesis instructions.

- [ ] **Step 6: Run Ravmax tests and prompt smoke checks**

Run:

```text
python -m unittest discover -s .pi/tests -v
python .pi/skills/pdf-search/index.py doctor
python .pi/skills/academic-workflow/learning_state.py --help
```

Expected: tests pass; doctor reports truthful current manifest blockers without changing the manifest; evidence CLI lists all four subcommands.

- [ ] **Step 7: Commit Ravmax workflow changes**

Stage exact `.pi/prompts`, `.pi/skills/academic-workflow`, updated named docs/skills, and `.pi/tests/test_workflow_prompts.py`. Confirm `.pi/settings.json`, `.pi/npm/`, and lecture notes are not staged. Commit:

```text
git commit -m "feat: unify academic workflows around evidence"
```

### Task 4: Port the generic distribution to Primer

**Files:**
- Modify: `vault/.pi/skills/pdf-search/index.py`
- Modify: `vault/.pi/skills/pdf-search/SKILL.md`
- Create: `vault/.pi/skills/academic-workflow/SKILL.md`
- Create: `vault/.pi/skills/academic-workflow/learning_state.py`
- Move the same 25 prompt files from `vault/.pi/prompts/` to `vault/.pi/skills/academic-workflow/references/`.
- Create the same five front-door files under `vault/.pi/prompts/`.
- Modify stale references under `vault/.pi/`, `vault/README.md`, `vault/START HERE.md`, and `vault/CLAUDE.md`.
- Modify: `scripts/verify.py`
- Modify: `tests/test_runtime_scripts.py`
- Modify: `tests/test_verify.py`
- Create focused tests if runtime tests become unclear: `tests/test_pdf_index.py`, `tests/test_learning_state.py`, `tests/test_workflow_prompts.py`.
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/setup.md`
- Modify: `docs/workflows.md`
- Modify: `docs/customization.md`
- Modify: `docs/troubleshooting.md`

**Interfaces:**
- Primer exposes the same statuses, record schemas, card decisions, CLI subcommands, five prompts, and internal reference map as Ravmax.
- `scripts/verify.py::verify_repository` rejects a distribution with any top-level prompt outside the five-command set, missing internal reference, unknown error label, missing runtime script, Ravmax path, or stale callable command reference.

- [ ] **Step 1: Copy tests first and verify they fail in Primer**

Port the Ravmax behavior tests to Primer paths and extend verifier tests with a fixture containing an extra top-level prompt and a missing internal reference.

Run:

```text
python -m unittest discover -s tests -v
```

Expected: failures for missing statuses, evidence engine, five-command prompt set, and verifier rules.

- [ ] **Step 2: Port deterministic utilities and prompt layout**

Port behavior, not Ravmax data. Keep Primer’s existing `find_vault` import. Move its 25 prompt files, add the five front doors, and port the academic-workflow skill and learning-state utility.

- [ ] **Step 3: Strengthen the release verifier**

Validate the exact visible prompt set, internal reference set, required runtime scripts, generic-path constraint, and absence of removed callable command references. Return actionable path-specific errors.

- [ ] **Step 4: Update distribution documentation**

Document installation, the five-command workflow, evidence blocks, PDF statuses, customization points, doctor troubleshooting, demo/start behavior, and migration from specialist slash commands. Add a changelog entry for this release without claiming unverified behavior.

- [ ] **Step 5: Run Primer verification**

Run:

```text
python -m unittest discover -s tests -v
python scripts/verify.py
```

Expected: all tests pass and verifier exits zero.

- [ ] **Step 6: Scan Primer for private values and stale commands**

Search tracked distribution files for `C:/Users/ravin`, `C:\\Users\\ravin`, `Ravmax`, `@academic`, and callable forms of the 25 removed commands. Historical migration tables may name old commands; executable prompt or system instructions may not call them.

- [ ] **Step 7: Commit Primer implementation**

Stage the plan, runtime, prompts, skills, verifier, tests, and docs. Commit:

```text
git commit -m "feat: publish closed-loop academic workflow"
```

### Task 5: Final cross-repository verification

**Files:**
- No production changes unless a failing verification identifies a defect, in which case return to the owning task’s red-green cycle.

- [ ] **Step 1: Verify Ravmax working state**

Run the full Ravmax tests, PDF doctor, evidence CLI help, and a fresh Pi prompt-discovery smoke test. Confirm unrelated changes remain unstaged.

- [ ] **Step 2: Verify Primer release state**

Run the full Primer unittest suite and release verifier from a clean checkout state after the implementation commit.

- [ ] **Step 3: Inspect both commit histories and working trees**

Confirm Ravmax has only intentional feature commits plus pre-existing unstaged user changes. Confirm Primer has the design commit and implementation commit with no untracked generated files.

- [ ] **Step 4: Report observed behavior**

Report exact test counts, doctor status counts, commit hashes, retained Ravmax user changes, and any current-data blockers. Do not claim live note migration because this implementation installs contracts without rewriting learner notes.
