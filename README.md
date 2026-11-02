# Free Open-Source Games Directory

> Great games that cost $0 — because the code says so. No ads, no tracking, no paywalls.

A hand-curated, fully static directory of **free, open-source (FLOSS) games**, plus a
plain-English guide, *Play Free Forever*, covering categories, install tips, controller
support, gift-able picks, FLOSS licenses explained, and verified links.

Curated and maintained by **Asdale Dynamics, LLC**.

## What's inside

| Path | What it is |
| --- | --- |
| `site/index.html` | The main directory: 22 license-verified games across 8 categories, with platform, controller, and license badges |
| `site/style.css` | The shared stylesheet (no external assets, works offline) |
| `docs/index.html` | Docs landing page |
| `docs/play-free-forever.html` | The *Play Free Forever* guide: categories, install tips, controller support, gift-able picks, FLOSS licenses explained, verified-link methodology |
| `LICENSE` | MIT license — Copyright (c) 2026 Asdale Dynamics, LLC |
| `STATUS.md` | Build/run/verification status and known gaps |

## How links are verified

Every external link points only to an **official project website** or the project's
**public source repository** — never third-party mirrors, download portals, or affiliate
links. At publication, all external links were checked programmatically with a local
Python script that issues HTTP HEAD/GET requests and reports the status of each URL
(`tools/linkcheck.py`, run as described below). Licenses for each game were verified
against the project's own `LICENSE`/docs — including the less obvious cases
(Veloren: GPLv3+; Mindustry: GPLv3; Shattered Pixel Dungeon: GPLv3; Warzone 2100: GPLv2+;
NetHack: its own OSI-approved NetHack GPL). Re-verify after your own edits:

```bash
python3 tools/linkcheck.py site docs
```

## Run it

No build step. It's plain HTML and CSS — just open a file in a browser, or serve it
locally (recommended, so relative links resolve cleanly):

```bash
python3 -m http.server 8000
# then open:
#   http://localhost:8000/site/index.html
#   http://localhost:8000/docs/play-free-forever.html
```

## Principles

- **No ads. No tracking. No analytics. No affiliate links.** The site ships zero
  scripts and zero external assets, so it even works fully offline.
- **Local-first.** One folder, plain files, no build system, no dependencies.
- **Beginner-friendly.** Explanations written "like a friend would": plain English,
  step by step, never condescending.
- **Fix links fast.** These files are small on purpose, so updating a link is a
  one-line edit.

## License

Code and site content: MIT — `LICENSE`. Brand names and trademarks of the listed games
belong to their respective projects; the directory merely links to them.

Copyright (c) 2026 Asdale Dynamics, LLC
