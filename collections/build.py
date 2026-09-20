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

# What a badge rule may say. The app implements one evaluator per entry here and
# nothing else, so a typo in a rule type is caught at build time rather than
# becoming a badge that can never be earned.
RULE_FIELDS = {
    "visitedCount":        {"count"},
    "autoVisitCount":      {"count"},
    "countryCount":        {"count"},
    "guideCount":          {"count"},
    "xpAtLeast":           {"xp"},
    "placeCategoryCount":  {"category", "count"},
    "poiTypeCount":        {"poiType", "count"},
    "listComplete":        {"list"},
    "listCount":           {"list", "count"},
    "guideComplete":       {"guide"},
    "listsTouchedWithTag": {"tag"},          # count optional — omit for "all"
}
BADGE_REQUIRED = ("id", "name", "family")


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


def check_badge(where: str, badge: dict, families: set, rule: dict) -> None:
    for field in BADGE_REQUIRED:
        if not badge.get(field):
            raise Problem(f"{where} badge has no '{field}'")
    if badge["family"] not in families:
        raise Problem(f"{where} badge '{badge['id']}' is in family "
                      f"'{badge['family']}', which is not in badge-families.json")
    kind = rule.get("type")
    if kind not in RULE_FIELDS:
        raise Problem(f"{where} badge '{badge['id']}' has rule type {kind!r}. "
                      f"Known types: {', '.join(sorted(RULE_FIELDS))}")
    for field in RULE_FIELDS[kind]:
        if rule.get(field) in (None, ""):
            raise Problem(f"{where} badge '{badge['id']}' is a {kind} rule and "
                          f"needs '{field}'")


def collect_badges(lists: list, guides: list) -> tuple:
    """Standalone badges, plus the ones authored inside a list or guide.

    A badge that is earned by finishing one collection lives in that
    collection's file, so authoring a guide and the badge it awards is one edit
    in one place — and the guide page can show the badge without a lookup.
    """
    families_doc = load(ROOT / "badge-families.json")
    families = families_doc.get("families", [])
    ids = {f["id"] for f in families}
    if len(ids) != len(families):
        raise Problem("badge-families.json has two families with the same id")

    badges, seen = [], {}

    def add(badge: dict, where: str) -> None:
        check_badge(where, badge, ids, badge.get("rule", {}))
        if badge["id"] in seen:
            raise Problem(f"two badges share the id '{badge['id']}': "
                          f"{seen[badge['id']]} and {where}")
        seen[badge["id"]] = where
        badges.append(badge)

    for path in sorted((ROOT / "badges").glob("*.json")):
        doc = load(path)
        add(doc, str(path.relative_to(ROOT.parent)))

    # Synthesised: the collection supplies the label, the builder supplies the
    # rule, so an author never writes the same slug twice.
    for doc in guides:
        if badge := doc.get("badge"):
            add({**badge, "rule": {"type": "guideComplete", "guide": doc["id"]}},
                f"guides/{doc['id']}.json")
    for doc in lists:
        if badge := doc.get("badge"):
            add({**badge, "rule": {"type": "listComplete", "list": doc["id"]}},
                f"lists/{doc['id']}.json")

    badges.sort(key=lambda b: (b.get("family", ""), b.get("order", 0), b["id"]))
    return families, badges


def main() -> int:
    try:
        lists = collect("lists", "list", "places", "name")
        guides = collect("guides", "guide", "stops", "title")
        bundles = collect("bundles", "bundle", "__none__", "name")
        families, badges = collect_badges(lists, guides)

        known = {d["id"] for d in lists}
        for bundle in bundles:
            for ref in bundle.get("lists", []):
                if ref not in known:
                    raise Problem(f"bundle '{bundle['id']}' points at list "
                                  f"'{ref}', which does not exist")

        # A rule pointing at a collection that does not exist is a badge nobody
        # can ever earn, and silently so.
        known_guides = {d["id"] for d in guides}
        tags = {t for d in lists for t in (d.get("tags") or [])}
        for badge in badges:
            rule = badge["rule"]
            if rule["type"] in ("listComplete", "listCount") and rule["list"] not in known:
                raise Problem(f"badge '{badge['id']}' needs list '{rule['list']}', "
                              f"which does not exist")
            if rule["type"] == "guideComplete" and rule["guide"] not in known_guides:
                raise Problem(f"badge '{badge['id']}' needs guide '{rule['guide']}', "
                              f"which does not exist")
            if rule["type"] == "listsTouchedWithTag" and rule["tag"] not in tags:
                raise Problem(f"badge '{badge['id']}' counts lists tagged "
                              f"'{rule['tag']}', and no list carries that tag")
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
        "badgeFamilies": families,
        "badges": badges,
    })

    places = sum(len(d.get("places", [])) for d in lists)
    stops = sum(len(d.get("stops", [])) for d in guides)
    print(f"✓ {len(lists)} lists ({places} places) · {len(guides)} guides "
          f"({stops} stops) · {len(bundles)} bundles · {len(badges)} badges "
          f"in {len(families)} families")
    print(f"  index.json {(ROOT / 'index.json').stat().st_size / 1024:.0f} KB · "
          f"all.json {(ROOT / 'all.json').stat().st_size / 1024:.0f} KB")
    return 0


def write(path: pathlib.Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    sys.exit(main())
