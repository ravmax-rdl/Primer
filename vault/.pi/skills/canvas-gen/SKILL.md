---
name: canvas-gen
description: >
  Generate per-course Obsidian Canvas maps. The model chooses nodes and edges;
  layout.py assigns deterministic coordinates and preserves manual positions.
---

# Canvas generation

## Model chooses, script places

- The model writes a graph JSON file with nodes, dependencies, labels, and optional colors.
- `layout.py` assigns collision-free geometry and writes an Obsidian `.canvas`.
- Never ask the model to invent coordinates.

Run from the vault root:

```bash
python .pi/skills/canvas-gen/layout.py graph.json --write "Study Notes/Programme/Y01_S01/Foundations of Logic/Overview.canvas"
python .pi/skills/canvas-gen/layout.py graph.json --merge "Study Notes/Programme/Y01_S01/Foundations of Logic/Overview.canvas" --write "Study Notes/Programme/Y01_S01/Foundations of Logic/Overview.canvas"
```

`--merge` keeps coordinates for nodes matched by file path, then by ID. Add course colors to graph data or use the verified colors in `Papers & Reviews/Programme/crosswalk.json`. Do not add vault-wide CSS for course colors.
