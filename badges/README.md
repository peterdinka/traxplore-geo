# Badge artwork

One PNG per badge per state. The app finds them by filename — there is no
manifest and no index to keep in sync, so adding a badge illustration is a
commit here and nothing else. No app release, no code change.

## Naming

    <badge_id>.png           earned   — full colour
    <badge_id>-locked.png    unearned — greyed

`<badge_id>` is the `id` in `BadgeEngine.swift`, not the display name. For
example the 50-station badge is `station_50`, so:

    station_50.png
    station_50-locked.png

A badge with no file here keeps drawing the hexagon-and-SF-Symbol it always
has, so partial coverage is fine and a typo in a filename is invisible rather
than fatal.

## Export settings

- **Transparent background.** The app draws a shadow around the earned badge;
  against a white rectangle that shadow is a rectangle.
- **~300 px wide.** The largest the artwork is ever drawn is 190 pt tall on the
  detail page, so 300 px covers 2× on every current device with room to spare.
  Exporting at 2000 px does not look better — it decodes to a bitmap two orders
  of magnitude larger for the same picture on screen.
- **Same outline and proportions for every badge.** The grid assumes a width
  to height ratio of 0.72 (see `TxBadgeArt.aspect`); badges drawn to other
  shapes will sit unevenly in a row.
- Keep each file well under 100 KB.

## Where the app reads this from

`TxBadgeArt.swift`:

    https://raw.githubusercontent.com/peterdinka/traxplore-geo/main/badges/

The `main` branch, deliberately — this is unrelated to the `collections`
migration, so the URL does not have to change when that merges.

Downloads are cached to disk on the device, and the app revalidates each one
once per launch with a conditional request. Replacing an image in place does
reach phones that already have the old one — they pick it up on the next launch,
with no reinstall. When nothing has changed the server answers 304 with no body.

**Export with a transparent background.** Five of the first badges were exported
opaque, which drew a grey box behind them in the app; their backgrounds were
stripped after the fact, which works but softens the rim slightly compared to
exporting it right.
