# Collections

Curated content for Traxplore: the guides, lists and bundles shown in Explore.

## Editing

One file per thing. Open the file for the list or guide you want to change, edit
it in GitHub's web editor, and commit. A push runs a workflow that validates
every file and rebuilds the two files the app actually downloads — so a mistake
is reported as a failed check rather than shipping silently.

    collections/
      lists/<slug>.json      one curated list and its places
      guides/<slug>.json     one guide and its stops
      bundles/<slug>.json    a named group of lists

Never edit `index.json` or `all.json` — they are generated.

## Why one file each

The file you edit is also the unit the app fetches. Opening a guide in the app
downloads that one file and caches it, so a growing catalogue costs a bigger
index rather than a bigger download for everybody. A single merged file would be
unopenable in the browser long before it was unusable in the app, and one stray
comma would take every list down with it.

## Fields

Lists carry `id`, `name`, `description`, `country`, `order`, `published` and a
`places` array of `{ name, latitude, longitude, description, category, order,
photos, history }`. Guides carry the same shape with `stops` instead of
`places`, plus `city` and `durationEstimate`. Bundles carry `lists`, an array of
list ids.

`published: false` hides something from the app without deleting it.

Anything absent is simply omitted rather than written as null.
