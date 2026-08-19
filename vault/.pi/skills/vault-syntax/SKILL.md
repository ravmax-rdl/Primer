---
name: vault-syntax
description: >
  The syntax contract for the UCSC learning vault product kit. The tutor loop
  must emit only syntax that is marked as live in this skill and in
  `Markdown Snippets.md`.
---

# Vault syntax (live subset)

This skill is the gatekeeper for what the tutor protocol is allowed to emit.

## Golden rules

- Dynamic views are **Bases** (`.base`) and must be written as YAML filters.
  Avoid Dataview; do not emit ` ```dataview ` blocks.
- Use checkbox markers for Understanding maps:
  `- [x]` known, `- [/]` edge, `- [?]` unknown, `- [!]` blocked.
- Use callouts exactly:
  `> [!note]`, `> [!question]`, `> [!Equation]`.

## Rendering-critical formatting

- `strictLineBreaks: true` means a single newline does not render. Use two trailing
  spaces or a blank line.

## pdf++ links (page evidence)

When you cite a PDF page/region, emit **pdf++**:

- Page-only:
  `[[<Name>.pdf#page=<N>|<Name>, p.<N>]]`
- Optional region (only when you copied real `rect=` from pdf++ output):
  `[[<Name>.pdf#page=<N>&rect=<x,y,w,h>|<Name>, p.<N>]]`

Never invent `rect=` coordinates.

## Math, Mermaid, TikZ

- Display derivations wrap with `> [!Equation]` and `align*` / `flalign*` inside `$$...$$`.
- Mermaid uses fenced ` ```mermaid ` blocks.
- TikZ uses fenced ` ```tikz ` blocks and only when the picture is the claim.

## Videos (cardlink)

For course/video cards, emit a fenced ` ```cardlink ` block (no bare URL dumping):

```cardlink
url: https://example.com/video
title: Video title
```

