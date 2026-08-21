#!/usr/bin/env python3
"""Read-only Zotero lookup. Copies zotero.sqlite to temp first — never query
the live DB (Zotero holds a lock).

Usage:
  python3 query.py search <text>
  python3 query.py get <itemID|citekey>
  python3 query.py collections
"""

from __future__ import annotations

import os
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib.vault import zotero_db  # noqa: E402

DB = zotero_db()


def connect_copy():
    if not DB.exists():
        raise SystemExit("Zotero DB not found at %s" % DB)
    tmp = Path(tempfile.gettempdir()) / "primer-zotero-copy.sqlite"
    shutil.copy2(DB, tmp)
    con = sqlite3.connect("file:%s?mode=ro" % tmp.as_posix(), uri=True)
    con.row_factory = sqlite3.Row
    return con, tmp


def field_map(con) -> dict[str, int]:
    return {row["fieldName"]: row["fieldID"] for row in con.execute(
        "SELECT fieldID, fieldName FROM fieldsCombined"
    )}


def item_fields(con, item_id: int, fmap: dict[str, int]) -> dict[str, str]:
    out = {}
    rows = con.execute(
        """
        SELECT f.fieldName, v.value
        FROM itemData d
        JOIN fieldsCombined f ON f.fieldID = d.fieldID
        JOIN itemDataValues v ON v.valueID = d.valueID
        WHERE d.itemID = ?
        """,
        (item_id,),
    )
    for row in rows:
        out[row["fieldName"]] = row["value"]
    return out


def creators(con, item_id: int) -> str:
    rows = list(con.execute(
        """
        SELECT c.lastName, c.firstName
        FROM itemCreators ic
        JOIN creators c ON c.creatorID = ic.creatorID
        WHERE ic.itemID = ?
        ORDER BY ic.orderIndex
        """,
        (item_id,),
    ))
    parts = []
    for r in rows:
        name = ", ".join(p for p in [r["lastName"], r["firstName"]] if p)
        if name:
            parts.append(name)
    return "; ".join(parts)


def list_items(con):
    fmap = field_map(con)
    items = []
    for row in con.execute(
        """
        SELECT i.itemID, t.typeName, i.key
        FROM items i
        JOIN itemTypesCombined t ON t.itemTypeID = i.itemTypeID
        WHERE t.typeName NOT IN ('attachment', 'note', 'annotation')
        """
    ):
        fields = item_fields(con, row["itemID"], fmap)
        items.append({
            "id": row["itemID"],
            "key": row["key"],
            "type": row["typeName"],
            "title": fields.get("title", ""),
            "date": fields.get("date", ""),
            "DOI": fields.get("DOI", ""),
            "citekey": fields.get("citationKey", ""),
            "creators": creators(con, row["itemID"]),
        })
    return items


def cmd_search(q: str) -> None:
    con, tmp = connect_copy()
    try:
        qlow = q.lower()
        hits = []
        for it in list_items(con):
            blob = " ".join(str(v) for v in it.values()).lower()
            if qlow in blob:
                hits.append(it)
        if not hits:
            print("# 0 hits — Zotero library currently has very few parent items")
            return
        for it in hits:
            cite = it["citekey"] or it["key"]
            print("%s\t%s\t%s\t%s\t%s" % (
                cite, it["type"], it["creators"], it["date"], it["title"]
            ))
    finally:
        con.close()
        try:
            os.remove(tmp)
        except OSError:
            pass


def cmd_collections() -> None:
    con, tmp = connect_copy()
    try:
        rows = list(con.execute("SELECT collectionName FROM collections ORDER BY 1"))
        if not rows:
            print("# no collections")
            return
        for r in rows:
            print(r[0])
    finally:
        con.close()
        try:
            os.remove(tmp)
        except OSError:
            pass


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == "search" and len(args) >= 2:
        cmd_search(" ".join(args[1:]))
    elif args[0] == "collections":
        cmd_collections()
    elif args[0] == "get" and len(args) == 2:
        cmd_search(args[1])
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
