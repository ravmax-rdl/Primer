/**
 * Blocks tool calls that reference credential, recovery, or private-key files.
 * Prose rules remain useful context; this extension enforces the path boundary.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { isToolCallEventType } from "@earendil-works/pi-coding-agent";

import { hitsSensitivePath } from "./patterns.ts";

export default function activate(pi: ExtensionAPI): void {
  pi.on("tool_call", (event) => {
    for (const tool of ["read", "write", "edit"] as const) {
      if (!isToolCallEventType(tool, event)) continue;
      const path = (event.input as { path?: string }).path ?? "";
      const hit = hitsSensitivePath(path);
      if (!hit) continue;
      return {
        block: true,
        reason:
          `Blocked: '${path}' matches a protected credential or recovery pattern (${hit}). ` +
          "The user must explicitly remove the block for a confirmed false positive.",
        terminate: true,
      };
    }

    if (!isToolCallEventType("bash", event)) return;
    const command = (event.input as { command?: string }).command ?? "";
    const hit = hitsSensitivePath(command);
    if (!hit) return;
    return {
      block: true,
      reason:
        `Blocked: the command references protected credential or recovery material (${hit}). ` +
        "Do not read, print, copy, move, or transmit it.",
      terminate: true,
    };
  });
}
