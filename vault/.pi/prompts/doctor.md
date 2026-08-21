---
description: Report PDF index health and truthful source blockers without repairs
argument-hint: ""
---

Run the selected read-only academic health check:

```bash
python .pi/skills/pdf-search/index.py doctor
```

Report status counts, legacy records, and each blocking source with its reason.
Explain the required class of action:

- `missing_target`: restore or remap the source.
- `unsupported_uri`: replace with a supported local file reference.
- `unreadable`: repair or replace the source file.
- `no_text_layer`: OCR may be appropriate.
- `ocr_pending`: finish or inspect the queued OCR work.
- `failed`: repair the named extraction backend failure.
- `indexed`: no action.

Do not write, modify, repair, reindex, queue OCR, or change source files. This
command implements PDF/status integrity only; do not imply a full vault health
check.
