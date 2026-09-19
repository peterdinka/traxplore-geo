# Place icons

One hand-drawn PNG per kind of place, shown beside the nearest attractions on
Home. The app picks the file by what the place is, so adding a drawing is a
commit here and nothing else — no app release, no code change.

Anything not yet drawn falls back to the SF Symbol the app has always used for
that place, so partial coverage is fine and a misnamed file is invisible rather
than fatal.

## Export settings

- **Transparent background.** Learn from the badges: five were exported opaque
  and drew a grey box in the app.
- **Square canvas, 240 px.** These are drawn at 44 pt on Home, so 240 px covers
  every current device at well over 2x.
- **Keep the drawing centred and filling most of the canvas**, with a consistent
  margin across the set — an icon drawn smaller inside its square appears
  smaller in the row, which is exactly the problem the badges had.
- Keep each file well under 100 KB.

## Where the app reads this from

`TxPlaceIcon.swift`:

    https://raw.githubusercontent.com/peterdinka/traxplore-geo/main/poi-icons/

Downloads are cached on the device and revalidated once per launch, so
replacing an icon in place does reach phones that already have the old one.

## The 31 filenames

Exactly these names, lowercase, `.png`. A file by any other name is never
requested.

### Areas

- `country.png`
- `region.png`
- `city.png`
- `borough.png`
- `county.png`

### Nature

- `park.png`
- `garden.png`
- `beach.png`
- `mountain.png`
- `viewpoint.png`

### Culture and sights

- `museum.png`
- `gallery.png`
- `monument.png`
- `church.png`
- `castle.png`
- `library.png`
- `landmark.png`
- `stadium.png`
- `university.png`

### Food and drink

- `cafe.png`
- `restaurant.png`
- `bar.png`
- `bakery.png`
- `market.png`

### Transport

- `train-station.png`
- `bus-station.png`
- `airport.png`
- `bridge.png`

### Everything else

- `hotel.png`
- `shop.png`
- `place.png`

