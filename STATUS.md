# STATUS

**Project:** Free Open-Source Games Directory
**Maintained by:** Asdale Dynamics, LLC
**Date:** November 2, 2026

## What was built

- **`site/index.html`** — a fully static, no-JS, no-tracking directory of 22 free,
  open-source (FLOSS) games in 8 categories (Strategy & Tactics, Action & FPS,
  RPG & Adventure, Roguelike, Racing & Simulation, Puzzle & Casual, Kids & Family,
  Sandbox & Building). Each entry carries a license badge, platform list, controller
  badge where applicable, and links to the official website and public source repository.
- **`site/style.css`** — shared stylesheet; zero external assets, works offline.
- **`docs/index.html`** — docs landing page.
- **`docs/play-free-forever.html`** — the *Play Free Forever* guide covering:
  category picks, install tips per platform, controller support levels explained,
  gift-able picks, FLOSS licenses explained in plain English, and the
  verified-links methodology.
- **`tools/linkcheck.py`** — stdlib-only verification script: internal-link
  resolution, HTML structure parsing, and live HTTP status checks of all external links.
- **`README.md`** — project overview, run instructions, link-verification methodology.
- **`LICENSE`** — MIT, `Copyright (c) 2026 Asdale Dynamics, LLC`.

## How to run it

No build step. Either open `site/index.html` directly in a browser, or serve locally:

```bash
python3 -m http.server 8000
# open http://localhost:8000/site/index.html
# guide: http://localhost:8000/docs/play-free-forever.html
```

Re-verify links after edits:

```bash
python3 tools/linkcheck.py site docs
```

## Verification results (all passing)

1. **HTTP smoke test** — `python3 -m http.server` + curl: all 6 tracked files
   (`site/index.html`, `site/style.css`, `docs/index.html`,
   `docs/play-free-forever.html`, `README.md`, `LICENSE`) return **HTTP 200**.
2. **Link check** — `tools/linkcheck.py`: **44/44 unique external links return a
   live 2xx/3xx status** (with retry logic for transient 5xx/timeouts); all internal
   links resolve; all 3 HTML files parse without structural errors.
3. **License accuracy** — non-obvious licenses web-verified against each project's
   own LICENSE/docs: Veloren GPLv3+, Mindustry GPLv3, Shattered Pixel Dungeon GPLv3,
   Warzone 2100 GPLv2+, NetHack's OSI-approved NGPL.
4. **No secrets/personal data** — scanned all files: no API keys, tokens, passwords,
   or personal data. The only "secret" string is the word in SuperTux's "secret
   tunnels" game description.
5. **No tracking** — no `<script>` tags, no analytics, no external assets anywhere.

## Known gaps

- **Stunt Rally's legacy site** (`stuntrally.tuxfamily.org`) is offline at
  publication (HTTP 503); its entry links to the official GitHub repository instead,
  with a note. If the tuxfamily site returns, it can be restored as the primary link.
- **Veloren update cadence** — stable builds can lag the public game servers; the
  recommended path is the official *Airshipper* launcher (noted in the guide's
  install section).
- **OpenMW** plays Morrowind's content only via your own copy of the original game's
  data files; this caveat is stated in its directory entry.
- **Counts and status badges** (e.g., exact gamepad support per game) are as
  documented by each project at publication; games update, so occasional re-checks
  are worthwhile.
- The directory is intentionally small and opinionated (22 games) rather than
  exhaustive; expansion is a matter of adding `<article class="game">` blocks.
