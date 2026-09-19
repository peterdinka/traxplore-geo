# Seasonal banners

The promoted strip on Home. Several can be in rotation at once — the app fades
from one to the next every 6 seconds, and does nothing at all when there is
only one.

## Why this folder has a manifest and the others do not

Badges and place icons are found *by name*: the app knows it wants `station_50`
or `cafe` and asks for that exact file. Banners are the opposite — the app has
no idea what banners exist, and `raw.githubusercontent.com` cannot list a
directory. So `banners.json` is the list, and a PNG that is not in it is never
shown.

## Adding one

1. Drop the PNG in this folder.
2. Add an entry to `banners.json`.
3. Push. It appears on the next launch — no app release.

```json
{
  "banners": [
    { "id": "autumn-london", "image": "autumn-london.png",
      "from": "2026-09-01", "to": "2026-11-30" },
    { "id": "winter-lights", "image": "winter-lights.png",
      "from": "2026-12-01", "to": "2027-01-15" },
    { "id": "always-on",     "image": "always-on.png" }
  ]
}
```

- `id` — anything unique and stable. Used to tell one banner from another.
- `image` — the filename in this folder.
- `from` / `to` — **optional**, `yyyy-MM-dd`, both inclusive. Outside that
  window the banner is not shown. Omit both for a banner that is always
  eligible.

Order in the file is the order of the rotation.

## Export settings

- **3:1, landscape** — 1800 x 600 is a good size. Banners are cropped to fill
  that ratio rather than letterboxed, so a few pixels out is invisible, but
  something markedly squarer will lose its top and bottom.
- **The lettering is part of the artwork.** The app draws no text over it, so
  everything the banner says — the eyebrow, the title, the description, the
  button — has to be in the image.
- The whole banner is one tap target and opens Seasonal Challenges. A drawn
  button is decoration, so keep it clear of the very edge.
- Corners are rounded by the app at 20pt; do not round them in the file.
- Opaque is fine here, unlike badges and icons — the banner fills its own
  rectangle.

## Where the app reads this from

`TxSeasonalBanner.swift`:

    https://raw.githubusercontent.com/peterdinka/traxplore-geo/main/seasonal-banners/

The manifest is fetched fresh each launch and cached, so a banner that has been
seen once keeps appearing offline. Images cache and revalidate like the badges.
