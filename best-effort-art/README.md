# Best-effort artwork

The wide illustrations on the four Best efforts cards at the foot of the Move
page — your furthest walk, run, hike and ride.

The filename is `best-` plus the `TxActivityKind` case name, alongside
`activity-icons/`, so adding a file is all that is needed for it to appear.

| File | Card |
|---|---|
| `best-walk.png`  | Longest walk |
| `best-run.png`   | Longest run |
| `best-hike.png`  | Longest hike |
| `best-cycle.png` | Longest cycle |

**Format:** PNG with transparency (RGBA), around 600 × 400 — wider than tall.
These are drawn across the top of a 150 pt card at about 44 pt high, so they take
more detail than the small glyphs in `activity-icons/`.

Only these four are used today: the cards cover walk, run, hike and cycle in
that order. A file for any other type is harmless but will not be shown.

A missing file is not an error — the card falls back to the SF Symbol for that
type.
