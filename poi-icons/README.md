# Place icons

One hand-drawn PNG per kind of place, shown beside the nearest attractions on
Home. The app picks the file by what the place is, so adding a drawing is a
commit here and nothing else — no app release, no code change.

**A kind with no file yet falls back to `questionmark.png`**, not to a system
icon, so a half-finished set still looks drawn rather than broken.

## Export settings

- **Transparent background.**
- **Square canvas, 240 px.**
- **Fill a consistent share of the canvas.** The first batch arrived filling
  anywhere from 71 to 89 per cent of its square, which makes one icon look
  larger than its neighbour in the same row. They were normalised to 88 per
  cent before shipping; drawing to a consistent margin saves that step.
- Keep each file well under 100 KB. The first batch came in at about 2 MB each.

## Where the app reads this from

`TxPlaceIcon.swift`:

    https://raw.githubusercontent.com/peterdinka/traxplore-geo/main/poi-icons/

Downloads are cached on the device and revalidated once per launch, so
replacing an icon in place reaches phones that already have the old one.

## The filenames

Exactly these names, lowercase, `.png`. A file by any other name is never
requested. 16 of 36 drawn so far — the rest fall back to the question mark.

### Areas

- [ ] `country.png`
- [x] `region.png`
- [x] `city.png`
- [ ] `borough.png`
- [ ] `county.png`

### Nature

- [x] `park.png`
- [ ] `garden.png`
- [ ] `beach.png`
- [ ] `mountain.png`
- [ ] `viewpoint.png`

### Culture and sights

- [x] `museum.png`
- [ ] `gallery.png`
- [x] `monument.png`
- [x] `church.png`
- [ ] `castle.png`
- [ ] `library.png`
- [ ] `landmark.png`
- [ ] `stadium.png`
- [ ] `university.png`
- [x] `theatre.png`
- [x] `cinema.png`
- [x] `music.png`

### Food and drink

- [x] `cafe.png`
- [x] `restaurant.png`
- [x] `bar.png`
- [ ] `bakery.png`
- [x] `supermarket.png`

### Transport

- [ ] `train-station.png`
- [ ] `bus-station.png`
- [ ] `airport.png`
- [ ] `bridge.png`

### Services

- [x] `hospital.png`

### Everything else

- [x] `hotel.png`
- [ ] `shop.png`
- [ ] `place.png`
- [x] `questionmark.png`

