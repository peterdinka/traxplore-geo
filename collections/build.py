#!/usr/bin/env python3
"""Validate the collections source files and build what the app downloads.

Run by CI on every push, and runnable by hand:

    python3 collections/build.py

Two outputs, both generated — never edit them:

  index.json   every list and guide, metadata only. Small enough to stay one
               request however far the catalogue grows.
  all.json     everything, including places and stops. What the app fetches
               today, while the catalogue is small enough for that to be the
               cheapest option.

The validation matters more than the building. A malformed list used to reach
the app and fail silently; here it fails the push with a message naming the file
and the field, so a bad edit is caught while you still remember making it.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
PLACE_REQUIRED = ("latitude", "longitude")


class Problem(Exception):
    pass


def load(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        # The single most likely mistake when editing by hand, so it gets the
        # clearest message: file, line, column, and what the parser expected.
        raise Problem(f"{path.relative_to(ROOT.parent)} is not valid JSON — "
                      f"{e.msg} at line {e.lineno}, column {e.colno}")


def check_entries(path: pathlib.Path, doc: dict, key: str, name_field: str) -> None:
    for i, entry in enumerate(doc.get(key, [])):
        where = f"{path.relative_to(ROOT.parent)} → {key}[{i}]"
        if not entry.get(name_field):
            raise Problem(f"{where} has no '{name_field}'")
        for field in PLACE_REQUIRED:
            value = entry.get(field)
            if value is None:
                raise Problem(f"{where} ({entry[name_field]}) has no '{field}' — "
                              f"a place without coordinates can never be detected "
                              f"as visited, so it is rejected rather than shipped")
            if not isinstance(value, (int, float)):
                raise Problem(f"{where} ({entry[name_field]}) has a non-numeric "
                              f"'{field}': {value!r}")
        lat, lon = entry["latitude"], entry["longitude"]
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise Problem(f"{where} ({entry[name_field]}) is at {lat}, {lon}, "
                          f"which is not on Earth")


def collect(folder: str, kind: str, child_key: str, name_field: str) -> list:
    out, seen = [], {}
    for path in sorted((ROOT / folder).glob("*.json")):
        doc = load(path)
        for field in ("id", "name"):
            if not doc.get(field):
                raise Problem(f"{path.relative_to(ROOT.parent)} has no '{field}'")
        if doc["id"] in seen:
            raise Problem(f"two files share the id '{doc['id']}': "
                          f"{seen[doc['id']]} and {path.name}")
        seen[doc["id"]] = path.name
        check_entries(path, doc, child_key, name_field)
        doc["kind"] = kind
        out.append(doc)
    return out


def main() -> int:
    try:
        lists = collect("lists", "list", "places", "name")
        guides = collect("guides", "guide", "stops", "title")
        bundles = collect("bundles", "bundle", "__none__", "name")

        known = {d["id"] for d in lists}
        for bundle in bundles:
            for ref in bundle.get("lists", []):
                if ref not in known:
                    raise Problem(f"bundle '{bundle['id']}' points at list "
                                  f"'{ref}', which does not exist")
    except Problem as e:
        print(f"::error::{e}", file=sys.stderr)
        print(f"\n✗ {e}\n", file=sys.stderr)
        return 1

    published = [d for d in lists + guides if d.get("published")]

    index = [{k: v for k, v in {
        "id": d["id"], "kind": d["kind"], "name": d.get("name"),
        "country": d.get("country"), "city": d.get("city"),
        "cover": d.get("coverImageURL"), "order": d.get("order"),
        "count": len(d.get("places") or d.get("stops") or []),
    }.items() if v not in (None, "")} for d in published]

    write(ROOT / "index.json", {"version": 1, "entries": index})
    write(ROOT / "all.json", {
        "version": 1,
        "lists": [d for d in lists if d.get("published")],
        "guides": [d for d in guides if d.get("published")],
        "bundles": [d for d in bundles if d.get("published")],
    })

    places = sum(len(d.get("places", [])) for d in lists)
    stops = sum(len(d.get("stops", [])) for d in guides)
    print(f"✓ {len(lists)} lists ({places} places) · {len(guides)} guides "
          f"({stops} stops) · {len(bundles)} bundles")
    print(f"  index.json {(ROOT / 'index.json').stat().st_size / 1024:.0f} KB · "
          f"all.json {(ROOT / 'all.json').stat().st_size / 1024:.0f} KB")
    return 0


def write(path: pathlib.Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    sys.exit(main())
