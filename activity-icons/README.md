# Activity icons

Hand-drawn glyphs for activity types, used on the Move page: the activity rows,
the week's activity mix, the month's mix beside the calendar, and the breakdown
under a tapped day.

The filename is the `TxActivityKind` case name, so adding a file is all that is
needed for it to appear — no app change.

| File | Shown for |
|---|---|
| `box.png` | Boxing, kickboxing, martial arts, wrestling |
| `coretraining.png` | Core training |
| `cycle.png` | Cycling (outdoor) |
| `dance.png` | Cardio dance, social dance, barre |
| `elliptical.png` | Elliptical, stair climbing, step training |
| `gym.png` | Traditional and functional strength training |
| `hiit.png` | High-intensity interval training |
| `hike.png` | Hiking |
| `indoorcycle.png` | Cycling marked indoor |
| `indoorrowing.png` | Rowing marked indoor |
| `multisport.png` | Swim-bike-run and transitions |
| `outdoorrowing.png` | Rowing (outdoor) |
| `pilates.png` | Pilates |
| `run.png` | Running (outdoor) |
| `skating.png` | Skating sports |
| `ski.png` | Downhill and cross-country skiing, snowboarding, snow sports |
| `stretching.png` | Flexibility, cooldown, preparation and recovery |
| `swim.png` | Swimming, water fitness and water sports |
| `tennis.png` | Tennis, badminton, squash, table tennis, racquetball, pickleball |
| `treadmill.png` | Running marked indoor |
| `walk.png` | Walking |
| `yoga.png` | Yoga, mind and body |

**Format:** PNG with transparency (RGBA), longest side 240 px, trimmed to the
drawing. They are shown at 17–26 points, so keep the linework heavy enough to
read small.

A missing file is not an error: the app falls back to the SF Symbol for that
type. `other` has no drawing and always uses its symbol.
