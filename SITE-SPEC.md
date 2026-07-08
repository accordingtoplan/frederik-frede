# SITE-SPEC.md — frederikfrede.com
**Canonical reference for every session. Read this first, every time.**

Last updated: 2026-07-08 (branch rename: production branch is now `live`)

---

## Stack

Plain HTML/CSS/JS. No frameworks, no build step. GitHub Pages (`accordingtoplan/frederik-frede`).
87 HTML pages at root level. Live at frederikfrede.com (Cloudflare DNS, all records DNS-only for GitHub cert compatibility).
Python `http.server` for local preview. Push via `git -c http.version=HTTP/1.1 -c http.postBuffer=524288000 push` with sandbox disabled (HTTP/2 pack-upload hangs otherwise).

---

## Branch model + previews (branch renamed 2026-07-08; model from 2026-07-05)

**One line per destination:**

- **`live` branch = THE SITE.** GitHub Pages serves it. Every commit here is public on frederikfrede.com within minutes. All HTML edits, all infra, all new pages go here. Never switch the Pages source branch.
- **`/staging/` FOLDER (inside `live`) = Frederik's review workspace.** Cloned case studies reworked before publishing. `frederikfrede.com/staging/[case].html` = preview, root URL = published page. Do NOT merge, publish, or delete anything in `/staging/` without explicit sign-off from Frederik.
- **`main` branch = asset storage only.** New assets push to `main/assets/[client]/`, referenced from live HTML with absolute `https://frederikfrede.com/assets/` URLs. Never HTML.

History note: the production branch was named `staging` until 2026-07-08, which caused constant confusion with the `/staging/` preview folder. Renamed to `live` via GitHub UI (Pages source moved automatically). Any older notes saying "push to staging" mean the branch now called `live`.

- Publishing a reviewed case is a per-page merge: take content changes from the preview folder, keep root-side infra changes (contrast values, YouTube facades, srcset wrapping, lazy-load). Never a blind copy in either direction. Content truth lives in preview, infrastructure truth lives in root.
- Known consequence: `debug-check.py` run repo-wide fails on the preview folder's hotlinks and dead cross-links. Scope the run to the files you changed (`python3 debug-check.py file.html`) or verify against a clean HEAD.

---

## Architecture rules (non-negotiable)

- `style.css` = single source of truth for type, nav, footer, @font-face, colour vars, reset, figure/grid system. NEVER add these to a page `<style>` block.
- `footer.js` = single source of truth for footer, scroll reveal, video lazy-load, cookie consent, GA. Nav injection added in Session E (see Nav section below).
- Page `<style>` blocks = ONLY genuinely page-specific layout.
- NEVER add `aspect-ratio` or `object-fit:cover/fill` to `.cs-grid`/`.cs-grid-3`/`.cs-media-full` img/video.
- NEVER push while another session is writing. `git fetch` + check status before every push.
- Every session prompt must open with: **"Fetch SITE-SPEC.md and _goldstandard.md from repo root and read them fully before doing anything else."**

---

## Nav (✅ componentized — Session E)

Nav injects from `footer.js` into `<div id="nav-mount"></div>`. Active state set via `window.location.pathname`. Link text: **Home, Work, About, Contact** — "About" href `/about.html`, "Contact" href `/about.html#contact`. NEVER "Information".

Injection is synchronous (top of footer.js IIFE body, before DOMContentLoaded) to minimise FOUC. `setTheme()` is defined per-page before `</body>` — onclick handlers on swatches reference it at click time, not at injection time, so it is always defined when needed.

Nav HTML (canonical — change here, nowhere else):
```html
<nav class="nav">
  <div class="nav-left">
    <a class="nav-logo" href="/">Frederik</a>
    <a class="nav-studio" href="/">&nbsp;Frede</a>
  </div>
  <div class="nav-center">
    <div class="swatches">
      <div class="swatch" style="background:#fff" onclick="setTheme('white',this)"></div>
      <div class="swatch" style="background:#111" onclick="setTheme('black',this)"></div>
      <div class="swatch" style="background:#e63222" onclick="setTheme('signal',this)"></div>
    </div>
  </div>
  <div class="nav-right" id="navLinks">
    <ul>
      <button class="nav-close" aria-label="Close menu" onclick="document.getElementById('navLinks').classList.remove('open')">×</button>
      <li><a href="/" onclick="document.getElementById('navLinks').classList.remove('open')">Home</a></li>
      <li><a href="/work.html" onclick="document.getElementById('navLinks').classList.remove('open')">Work</a></li>
      <li><a href="/about.html" onclick="document.getElementById('navLinks').classList.remove('open')">About</a></li>
      <li><a href="/about.html#contact" onclick="document.getElementById('navLinks').classList.remove('open')">Contact</a></li>
    </ul>
  </div>
  <button class="hamburger" aria-label="Menu" onclick="document.getElementById('navLinks').classList.toggle('open')"><span></span><span></span></button>
</nav>
```

Active state logic (injected after nav HTML):
- `/` or `/index.html` → `.active` on Home `<a>`
- pathname includes `/work` → Work
- pathname includes `/about` → About
- anything else → no active link

---

## Grid + media system (LOCKED — natural ratio, 2026-06-17)

All case-study images and videos display at **original/natural ratio**. Never crop, never stretch.

CSS (authoritative — trust `style.css`; `_goldstandard.md` CSS snippets were stale pre-Session-E, now updated):

```css
.cs-grid img, .cs-grid video,
.cs-grid-3 img, .cs-grid-3 video,
.cs-grid-wide img, .cs-grid-wide video { width: 100%; height: auto; display: block; object-fit: contain; }
.cs-fig img, .cs-fig video { width: 100%; height: auto; display: block; object-fit: contain; border: 0; }
.cs-grid, .cs-grid-3 { align-items: start; }
/* iframes: always aspect-ratio: 16/9 — unchanged */
```

CLS: every grid `<img>` must have `width="W" height="H"` attrs from real file dimensions.
Gold standard page: `architonic-brand-strategy-platform-design.html`
Homepage `index.html`: deliberate video-ratio system (`ratio-wide`/`lvwide`/`ratio-2`/`video-contain`, ffprobe-verified per file) — **NEVER touch it**.

---

## Lazy-load system (107 videos)

```html
<video muted loop playsinline preload="metadata" data-lazy poster="/assets/[client]/[name]-poster.jpg">
  <source data-src="/assets/[client]/[name].mp4" type="video/mp4">
</video>
```

IntersectionObserver in `footer.js` swaps `data-src` → `src` when near viewport (600px rootMargin).
A `<video>` with `data-src` child and **NO `src`** is CORRECT (lazy). Do not add `src`.
Hero video (first in doc order): `preload="auto" fetchpriority="high"`, plain `<source src>` (not lazy).
Poster: ~50–80KB JPEG, same orientation as video.

---

## Font system (✅ consolidated — Session D)

`@font-face` in `style.css` with `font-display:swap`. NOT in any page `<style>` block.
Pages keep only `<link rel="preload">` hints for fonts they use.
Fonts: Helvetica Neue (system), UnifrakturMaguntia (footer logotype), Permanent Marker (footer SVG).

---

## Credits system (✅ complete — Sessions B7 + D4)

```html
<div class="cs-bottom">
  <div class="cs-description"><p>…closing copy…</p></div>
  <dl class="cs-credits-cols">
    <div class="cs-credit-group"><dt>Live site</dt><dd><a href="https://…" target="_blank" rel="noopener">domain ↗</a></dd></div>
    <div class="cs-credit-group"><dt>Collaborators</dt><dd>Name A</dd><dd>Name B</dd></div>
    <div class="cs-credit-group"><dt>Year</dt><dd>YYYY</dd></div>
  </dl>
</div>
```

**One `<dd>` per collaborator name. Never middot/comma-separated in one `<dd>`. Never `<br>` between names.**
Standard fields: Live site (omit if no URL), Collaborators (`—` if none), Year. Credits block before `cs-nav`.

---

## Copy + voice rules

- Subjectless prose — no first-person, no third-person name references
- No em-dashes in body copy (only in section labels `"01 — Identity"`, CSS comments, credits placeholders `<dd>—</dd>`)
- No AI-speak: no "redefining", "iconic", "from the inside out", no rule-of-three, no parallel-negation
- Register: Rick Rubin / Way of Code. Wikipedia "Signs of AI writing" is the reference
- Thinking layer: only cases with genuine strategic stake earn a framing block

---

## Asset conventions

- Location: `/assets/[client-slug]/`. Self-hosted. Never hotlinked externally.
- Naming: lowercase, hyphens, `[client]-[project-type]-[description]-[optional-number].[ext]`
- Images: cap ~2400px @ q82 JPEG or WebP. FvF assets: ~2000px @ q85.
- Videos: H.264, CRF 24, preset slow, max 1080p, 25fps, no audio (`-an`), `-pix_fmt yuv420p -movflags +faststart`. Keep only if smaller (≥92% of orig = discard).
- GIFs as media: always convert to muted-loop mp4. GIF format only for `assets/img/archive/*`.
- Exceptions — do NOT rename: `25hours-loop-<YouTubeID>.mp4`, `assets/img/archive/*`, font files in `/assets/fonts/`.

---

## Adding a new case study — checklist

**MARKUP:**
- `<div id="nav-mount"></div>` (NOT hardcoded nav — componentized in Session E)
- `<script src="/footer.js"></script>` near bottom of `<body>`
- `<link rel="preload">` for fonts used (NOT @font-face in `<style>`)
- One `<h1>` with client/project name
- All images in global grid classes — no local `aspect-ratio`/`object-fit`
- All `<img>`: `loading="lazy"` (except hero) + `width="W" height="H"` from real dimensions
- All videos: `muted loop playsinline preload="metadata"` + `poster` + `data-lazy` + `<source data-src="...">`
- All iframes in 16/9 ratio container
- Credits: `.cs-bottom > dl.cs-credits-cols` — Live site, Collaborators (one `<dd>` per name), Year
- `cs-nav` prev/next updated on this page AND adjacent pages

**SEO:**
- Unique `<title>` ending with `— Frederik Frede`
- `<meta name="description">` (unique, ≤160 chars)
- `lang="en"` on `<html>`
- Canonical and OG tags (note in `_og-canonical-gaps.md` — generated from projects.json build pass)
- JSON-LD CreativeWork structured data
- Descriptive `alt` on every image
- `sitemap.xml` updated after adding the page

**ASSETS:**
- All media in `/assets/[client-slug]/`
- Files named per convention
- Images optimized (2400px, q82, WebP + srcset)
- Videos encoded to spec
- No external hotlinks (except intentional Vimeo/YouTube embeds)

---

## Open backlog (as of 2026-06-17 post-Session-E)

**Technical:**
- Large image optimization: ~50 images without srcset across ~30 pages — partial progress in Session E (worst offenders remain)
- OG + canonical tags: all 84 pages — blocked on projects.json (Frederik's xlsx)
- projects.json build pass (Frederik locks discipline/sector tags in xlsx first)
- Nav active state: set `data-theme` persistence across pages (currently theme resets on nav)

**Content (Frederik):**
- Per-case content review: layout positions, 2/3 col decisions, missing media
- Image gaps: Dr. Hauschka, Manufactum, &Tradition, selfnation, egon-zehnder, la-marzocco, closed-editorial
- Thinking layer: next 1–2 cases with genuine strategic stake
- NZZ: Figma device mockup to replace homepage card when ready
- FF monogram: Frederik designing himself

**Forward:**
- Credentials-deck generator (projects.json → filter by sector → HTML+PDF)
- Essay: three-sites-one-method.md (title TBD; publish gate: ~75–80% across 3 PoCs)
- Video content layer: Higgsfield shorts + YT explainers
- Domain: call UD (frederikfrede.de NS) + Netbeat (frede.net) — secondary domains, not blocking
