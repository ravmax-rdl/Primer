#!/usr/bin/env python3
"""Layered canvas layout. The model supplies the graph; this script
supplies x/y. Never let the LLM invent coordinates.

Usage:
  python3 layout.py graph.json > placed.json
  python3 layout.py graph.json --write "Study Notes/BSc/S01_2026/Discrete Mathematics/Overview.canvas"
  python3 layout.py graph.json --merge existing.canvas --write out.canvas

graph.json:
{
  "nodes": [
    {"id": "sets", "label": "Sets", "group": "Foundations",
     "file": "Study Notes/BSc/S01_2026/W04/D02/Discrete Mathematics.md",
     "deps": [], "color": "#ee9b00", "kind": "file"}
  ],
  "edges": [{"from": "sets", "to": "relations", "label": "needed for"}]
}
kind: file | text | gap  (gap becomes a text node flagged as missing)
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib.vault import find_vault  # noqa: E402

VAULT = find_vault()
NODE_W = 320
NODE_H = 140
HGAP = 100
VGAP = 48
GROUP_PAD_X = 40
GROUP_PAD_Y = 56
LEVEL_X0 = 0
LEVEL_Y0 = 0


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def topo_levels(nodes: list[dict]) -> dict[str, int]:
    ids = {n["id"] for n in nodes}
    indeg = {n["id"]: 0 for n in nodes}
    adj = defaultdict(list)
    for n in nodes:
        for dep in n.get("deps") or []:
            if dep in ids:
                adj[dep].append(n["id"])
                indeg[n["id"]] += 1
    q = deque([i for i, d in indeg.items() if d == 0])
    level = {i: 0 for i in indeg}
    seen = 0
    while q:
        u = q.popleft()
        seen += 1
        for v in adj[u]:
            level[v] = max(level[v], level[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if seen != len(ids):
        # cycle — pin leftovers to max+1
        mx = max(level.values()) if level else 0
        for i, d in indeg.items():
            if d > 0:
                level[i] = mx + 1
    return level


def layout(graph: dict) -> dict:
    nodes = graph["nodes"]
    levels = topo_levels(nodes)
    by_level = defaultdict(list)
    for n in nodes:
        by_level[levels[n["id"]]].append(n)

    placed = []
    id_to_xy = {}
    for lv in sorted(by_level):
        col = by_level[lv]
        x = LEVEL_X0 + lv * (NODE_W + HGAP)
        y = LEVEL_Y0
        for n in col:
            px, py = x, y
            id_to_xy[n["id"]] = (px, py)
            kind = n.get("kind") or ("file" if n.get("file") else "text")
            node = {
                "id": n["id"],
                "type": "file" if kind == "file" and n.get("file") else "text",
                "x": px,
                "y": py,
                "width": n.get("width", NODE_W),
                "height": n.get("height", NODE_H),
            }
            if node["type"] == "file":
                node["file"] = n["file"]
            else:
                label = n.get("label") or n["id"]
                if kind == "gap":
                    node["text"] = "**Gap** — %s\nNo lecture note yet." % label
                else:
                    node["text"] = n.get("text") or label
            if n.get("color"):
                node["color"] = n["color"]
            if n.get("group"):
                node["_group"] = n["group"]
            placed.append(node)
            y += NODE_H + VGAP

    groups = defaultdict(list)
    for node in placed:
        g = node.pop("_group", None)
        if g:
            groups[g].append(node)

    group_nodes = []
    gid = 0
    for label, members in groups.items():
        xs = [m["x"] for m in members]
        ys = [m["y"] for m in members]
        x = min(xs) - GROUP_PAD_X
        y = min(ys) - GROUP_PAD_Y
        w = max(xs) + NODE_W - x + GROUP_PAD_X
        h = max(ys) + NODE_H - y + GROUP_PAD_X
        group_nodes.append({
            "id": "g%d" % gid,
            "type": "group",
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "label": label,
        })
        gid += 1

    edges_out = []
    for i, e in enumerate(graph.get("edges") or []):
        frm, to = e.get("from"), e.get("to")
        if frm not in id_to_xy or to not in id_to_xy:
            continue
        edges_out.append({
            "id": "e%d" % i,
            "fromNode": frm,
            "toNode": to,
            "fromSide": e.get("fromSide", "right"),
            "toSide": e.get("toSide", "left"),
            **({"label": e["label"]} if e.get("label") else {}),
        })
    # also honour deps as unlabelled edges if no explicit edge list
    if not graph.get("edges"):
        i = 0
        for n in nodes:
            for dep in n.get("deps") or []:
                if dep in id_to_xy and n["id"] in id_to_xy:
                    edges_out.append({
                        "id": "e%d" % i,
                        "fromNode": dep,
                        "toNode": n["id"],
                        "fromSide": "right",
                        "toSide": "left",
                    })
                    i += 1

    return {
        "metadata": {"version": "1.0-1.0", "frontmatter": {}},
        "nodes": group_nodes + placed,
        "edges": edges_out,
    }


def merge(existing: dict, incoming: dict) -> dict:
    """Keep x/y of existing nodes matched by file path or id; place only new ones."""
    by_file = {}
    by_id = {}
    for n in existing.get("nodes") or []:
        by_id[n["id"]] = n
        if n.get("file"):
            by_file[n["file"].replace("\\", "/")] = n
    out_nodes = []
    seen_ids = set()
    for n in incoming.get("nodes") or []:
        old = None
        if n.get("file"):
            old = by_file.get(n["file"].replace("\\", "/"))
        if old is None:
            old = by_id.get(n["id"])
        if old and old.get("type") == n.get("type"):
            n = dict(n)
            n["x"] = old["x"]
            n["y"] = old["y"]
            n["width"] = old.get("width", n["width"])
            n["height"] = old.get("height", n["height"])
            n["id"] = old["id"]
        out_nodes.append(n)
        seen_ids.add(n["id"])
    # preserve leftover user nodes (hand-placed extras)
    for n in existing.get("nodes") or []:
        if n["id"] not in seen_ids:
            out_nodes.append(n)
    incoming = dict(incoming)
    incoming["nodes"] = out_nodes
    if existing.get("metadata"):
        incoming["metadata"] = existing["metadata"]
    return incoming


def write_canvas(doc: dict, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(doc, indent="\t") + "\n", encoding="utf-8")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    graph = load(Path(args[0]))
    placed = layout(graph)
    merge_path = None
    write_path = None
    if "--merge" in args:
        merge_path = Path(args[args.index("--merge") + 1])
    if "--write" in args:
        write_path = Path(args[args.index("--write") + 1])
        if not write_path.is_absolute():
            write_path = VAULT / write_path
    if merge_path:
        existing = load(merge_path if merge_path.is_absolute() else VAULT / merge_path)
        placed = merge(existing, placed)
    if write_path:
        write_canvas(placed, write_path)
        print("wrote %s (%d nodes, %d edges)" % (
            write_path, len(placed["nodes"]), len(placed["edges"])
        ), file=sys.stderr)
    else:
        json.dump(placed, sys.stdout, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
