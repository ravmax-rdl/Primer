import assert from "node:assert/strict";
import test from "node:test";

import { hitsSensitivePath } from "../vault/.pi/extensions/guard/patterns.ts";

const blocked = [
  "notes/recovery-codes.txt",
  "notes/recovery_phrase.md",
  ".env",
  "credentials.json",
  "id_ed25519",
  "account-private-key.asc",
  "tokens/auth-token.txt",
];

for (const path of blocked) {
  test(`blocks ${path}`, () => {
    assert.ok(hitsSensitivePath(path));
  });
}

const allowed = [
  "Study Notes/Review/Foundations of Logic/Implication.md",
  "Dev/CMD Snippets.md",
  "docs/security.md",
  "assets/key-concepts.svg",
];

for (const path of allowed) {
  test(`allows ${path}`, () => {
    assert.equal(hitsSensitivePath(path), null);
  });
}
