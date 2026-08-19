# Contributing

Primer accepts focused fixes to the public vault, Pi runtime, documentation, tests, and fictional examples.

## Before opening a change

- Use fictional, public-domain, or contributor-owned demo content.
- Do not include student records, private notes, credentials, recovery material, provider tokens, copyrighted lecture slides, textbook pages, or examination papers.
- Do not commit `.pi/cache`, Obsidian workspace or sync state, plugin binaries, theme files, or custom CSS.
- Keep the core provider neutral. Document a new provider, plugin, binary, or network call before making it required.
- Preserve exact course filenames used by Bases filters.

## Work locally

```bash
python -m unittest discover -s tests -v
node --test tests/guard.test.mjs
python scripts/verify.py .
```

Use `python3` where needed. A behavioral change to a script or guard rule needs a test that fails without the change. Human-facing prose does not need a source-text test.

## Pull requests

Keep one concern per pull request. Explain:

1. the student or maintainer problem;
2. the observable change;
3. privacy, licensing, provider, plugin, and OS effects;
4. the exact checks you ran.

For vault changes, include the affected Obsidian and Pi workflow. For visual changes, attach a rendered preview. Do not use a real student's vault as the fixture.

## Licenses

By contributing code, scripts, Pi extensions, or executable helpers, you agree to license the contribution under [MIT](LICENSE-CODE).

By contributing documentation, vault templates, fictional examples, or original visual assets, you agree to license the contribution under [CC BY 4.0](LICENSE-CONTENT).

You must have the right to submit the material. Linking a public source does not grant permission to copy it.
