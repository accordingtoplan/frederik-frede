# Session Handover Log

---

## Session A — 2026-06-17

**Verdict: PASS**

### What was done

**STEP 0 — Gold standard established**
- Parsed `style.css` (post-pass-1) and `architonic-brand-strategy-platform-design.html` as canonical reference.
- Wrote `_goldstandard.md` to repo root with verbatim CSS patterns and HTML examples for the full figure/grid/credits system.

**TASK A1 — CSS consolidation**

Rules moved from page `<style>` blocks into `style.css`:

| Rule(s) | From page(s) | Notes |
|---------|-------------|-------|
| `.cs-figrid` | siemens, classpass | 2-col figure grid; identical to `.cs-grid` layout |
| `.cs-figrid-3` | siemens, classpass | 3-col figure grid; identical to `.cs-grid-3` layout |
| `.cs-fig` + all sub-selectors (img/video/iframe/figcaption/.cap-name/.cap-meta) | siemens, classpass | figure item with caption; siemens had iframe in selector, classpass did not — canonical includes iframe |
| `.cs-story-head` + h3/a/a:hover | classpass | also used in siemens markup (was unstyled there) |
| `.cs-media-full iframe { aspect-ratio:16/9; border:0 }` | la-marzocco | logical extension of the `.cs-media-full` system |
| Mobile rules for all of the above | siemens, classpass | added to the single consolidated `@media (max-width:640px)` block in style.css |

Pages whose `<style>` blocks were edited:
- `siemens-home-appliances.html` — removed figrid/fig rules; kept slideshow (`.ss-*`) + land/port/natural overrides
- `classpass-bethebalance-campaign.html` — removed figrid/fig/story-head rules; kept `.cs-grid-three-land`
- `la-marzocco-friends-of-friends.html` — `<style>` block removed entirely

### Deferred to Session B (markup migration)

- `ritz-carlton-berlin-brand-event.html`: still uses `.cs-2col` / `.cs-3col` / `.cs-item` / `.cs-full` / `.cs-spacer` — pre-migration classes, markup not touched per instructions.
- `rooms-hotels.html`: same pre-migration classes as Ritz.
- All other pages with `/*keep*/`-marked inline overrides remain unchanged (intentional page-specific cascade).

### Flags for Frederik

1. **`siemens-home-appliances.html` mobile `.cs-fig figcaption { font-size: 11px }`**: kept inline as a minor page-specific tightening (12→11px on mobile). Low priority, easy to remove.
2. **`.cs-media-full iframe` (new global rule)**: only used by la-marzocco currently. Will apply to any future page using `<div class="cs-media-full"><iframe ...></iframe></div>` — which is the correct desired behaviour.
3. **`siemens` `.cs-story-head` markup was unstyled before this session** (the class existed in the HTML but had no CSS). Now picks up the canonical style from style.css. Visual change: the story chapter heads now render with `flex; justify-content: space-between` and proper type scale. Worth a quick visual check.
4. **Mobile gap for `.cs-figrid`/`.cs-figrid-3`**: set to `16px` (matching classpass). Siemens had `20px` inline — now `16px`. Minimal visual difference on mobile.

### Self-verify results

- `style.css` contains complete `.cs-grid`/`.cs-grid-3`/`.cs-grid-wide`/`.cs-figrid`/`.cs-figrid-3`/`.cs-fig`/`.cs-story-head`/`.cs-credits-cols` system. ✓
- No page `<style>` block left half-edited; all three edited pages spot-checked for intact structure. ✓
- 28 other pages with page-specific inline styles untouched. ✓

---

## Session B — 2026-06-17

**Verdict: PASS**

### What was done

**B2 — Dead media removed (pferdt)**
- `assets/pferdt/pferdt-fgp-screen-rec-sm.mp4` (0-byte file) deleted from repo.
- Dead `<div class="cs-media-full">` block referencing it removed from `frederik-pferdt-personal-brand-identity.html`.

**B1 MODE 1 — .land/.port/.natural CSS removed (pferdt)**
- Removed 3 CSS rules from pferdt's inline `<style>` (aspect-ratio overrides for img.land/img.port/img.natural).
- Class attributes remain in markup but are now inert — global 4/3 cover applies uniformly.

**B1 MODE 4 — object-fit:fill removed (5 pages)**
- `concierge-coffee-brand-web.html`: removed `.cs-media-full img/video{object-fit:fill}` entirely (global `object-fit:unset` applies).
- `louis-vuitton-employer-branding-campaign.html`: removed both `.cs-grid img/video` and `.cs-grid-3 img` fill rules; global 4/3 cover now applies. Empty `<style>` block removed.
- `neubau-welt.html`: removed `.cs-media-full img{object-fit:fill}` entirely.
- `umane-brand-identity.html`: removed `.cs-media-full video/img{object-fit:fill}` entirely.
- `spot-asset-management-system.html`: changed `fill` → `contain` on cs-media-full (screenshot content); changed `fill` → `cover` on cs-grid (intentional design-system variant retained).

**B1 MODE 2 — Pre-migration class migration (ritz + rooms-hotels)**
- `ritz-carlton-berlin-brand-event.html`: migrated `.cs-full→.cs-media-full`, `.cs-2col→.cs-grid`, all `cs-item` wrappers removed. Style block reduced to `.cs-spacer` + intentional `.cs-bottom`/`.cs-credits-cols` overrides (horizontal flex credits, no border-top — KEEP).
- `rooms-hotels.html`: same migration. Style block reduced to `.cs-spacer` only. No custom credits layout (global applies).
- `_goldstandard.md` overrides table updated — pre-migration entries removed.

**B7 — Collaborator name stacking (6 pages)**
- Convention: one `<dd>` per collaborator/typeface. No middot separators, no `<br>`.
- Applied to: `siemens-home-appliances.html` (9 names), `classpass-bethebalance-campaign.html` (2), `frederik-pferdt-personal-brand-identity.html` (4), `umane-brand-identity.html` (3), `bianca-chen-brand-identity.html` (3 + 2 typefaces), `signal-la-brand-identity.html` (3).
- `_goldstandard.md` credits pattern updated with new one-dd-per-name example.

### Deferred / not yet done

- B3 (credits conformance verification): not started.
- B4 (loading/performance audit beyond lazy-load): not started.
- B5 (mobile global fixes): not started.
- B6 (container audit + `_format-audit.md`): not started.
- Pass 4 (template + checklist verify): not started.

### Flags for Frederik

1. **pferdt `.land`/`.port` classes in markup**: class attrs remain on `<img>` elements but are now inert (no CSS rules). Either strip them in a future pass or leave — they do no harm.
2. **rooms-hotels portrait photos** (4448, dsc-4529, tbilisi-dsc-6130, 5424, dsc-5449): now render at 4/3 global ratio (cover) instead of their natural 2:3 portrait ratio. Visually they'll be cropped landscape. If that looks wrong, add per-image aspect-ratio overrides.
3. **ritz `.cs-bottom`/`.cs-credits-cols` intentional variant**: horizontal flex credits, no border-top — kept as intended. Confirmed in `_goldstandard.md` overrides table under pferdt entry.

---

## Session C — 2026-06-17

**Verdict: PASS**

### What was done

**C1 — Hotlink patched (1 file)**
- `siemens-home-appliances.html`: replaced `https://wp.andtradition.com/...Freunde-von-Freunden-Friends-Space-5672-1200x1200.jpg` with `/assets/siemens/siemens-friends-space-kreuzberg.jpg` (file downloaded: 388KB).

**C2 — GIF → muted-loop mp4 (7 GIFs across 6 pages)**
- All 7 GIFs converted with ffmpeg: H.264, CRF 24, preset medium, `pix_fmt yuv420p`, `movflags +faststart`.
- Per-GIF poster JPEGs extracted (`-ss 0.5 -vframes 1`).
- GIF frame rates: slow animations set to `-r 10` (lewis, ad-magazine); others at default 25fps or native.
- `ad-magazine-1.gif` (4199px wide): scaled to max 1600px.
- HTML updated: `<img src="...gif">` → `<video muted loop playsinline preload="metadata" data-lazy poster="...jpg"><source data-src="...mp4">`.
- Pages: `mohab-brand-identity.html`, `25hours-hotels-brand-identity.html`, `ad-magazin-web-design-art-direction.html`, `engel-volkers-web-design.html`, `lewis-group-brand-identity-web-design.html`, `ritz-carlton-berlin-brand-event.html` (2 GIFs).
- Lazy-load verified: all 7 have `data-lazy + poster` confirmed.

Size savings (GIF → mp4):
- mohab-logo-on-photography: 6.6M → 2.3M (35%)
- ritz-carlton-press: 1.7M → 372K (22%)
- ritz-carlton-instagram: 872K → 188K (22%)
- 25hours-companion: 5.6M → 1.8M (32%)
- ad-magazine-1: 1.8M → 284K (16%, also scaled 4199→1600px)
- engel-volkers-euv-pages: 1.7M → 656K (39%)
- lewis-group-website-screens: 1.6M → 664K (42%)

**C4 — Video re-encode (34 files replaced, 1 converted, 2 kept)**
- Script: `/tmp/encode-videos.sh`. Spec: H.264, CRF 24, preset medium, strip audio, max 1920px, replace if < 92% of original.
- 34 mp4/mov files replaced in-place. 2 KEPT (≥92%: pferdt-macbook-mockup-animation, architonic-summary-subs).
- `assets/mezcla/mezcla-video-mswebsite.mov` → CONVERTED to `.mp4` (16MB → 2MB). `mezcla-brand-digital.html` updated from `.mov` to `.mp4`.
- Notable savings: la-marzocco-film 67→49MB; mini films 32→23MB / 43→30MB; classpass-marie-luise 30→11MB; pferdt series all under 3MB (was 21–32MB each).

**C3 — Image optimization (3 poster images)**
- `architonic-at-poster-0{1,2,3}.jpg`: compressed via sips (quality 75, max 1920px). 2.4/2.1/2.0MB → 691/650/608KB (29%). WebP srcset `<picture>` wrappers added to `architonic-brand-strategy-platform-design.html` (WebP variants already existed).

### Deferred / not yet done

- B3 (credits conformance verification): not started.
- B4 (loading/performance audit): not started.
- B5 (mobile global fixes): not started.
- B6 (container audit + `_format-audit.md`): not started.
- Pass 4 (template + checklist verify): not started.
- C3 full: architonic-brand-strategy-platform-design.html has ~20 more bare `src="assets/..."` (no leading slash, no srcset) — not addressed this session.

### Flags for Frederik

1. **`mezcla-video-mswebsite.mov`** still exists alongside the new `.mp4` — safe to delete the .mov from the repo to save ~16MB.
2. **`architonic-brand-strategy-platform-design.html`** has ~20 bare `src="assets/..."` paths (no `/`, no srcset). Works from root but inconsistent; worth a future sweep.
3. **GIF originals** still on disk (7 files). Safe to delete after verifying mp4 quality on-site.

---

## Session D — 2026-06-17

**Verdict: PASS**

### Task 0 — Pre-session audit (`_pre-D-audit.md`)

Committed as `e58a8d1` before any CSS changes. Covers all 6 sections:
- **0a** Media hotlinks: none remaining (all external URLs are `href=` credits links, not `src=`).
- **0b** Large images without srcset: ~50+ images across ~30 pages. Backlog deferred to Session E image-optimization pass.
- **0c** Missing width/height on grid imgs: 25 images across 3 pages (architonic 21, canyon 3, siemens 1). Fixed in Task 4.
- **0d** Missing credits blocks: none — all 82 pages have `.cs-credits-cols`.
- **0e** Poster ratio mismatches: none — all 62 verified `<video poster>` pairs match orientation.
- **0f** Unstacked collaborators: 12 pages still using middot/comma/br separators. Deferred to Session E.

### Task 1 — style.css natural-ratio system

**Before** (forced-crop rules):
```css
.cs-grid img, .cs-grid video { width:100%; display:block; object-fit:cover; aspect-ratio:4/3; }
.cs-grid-3 img, .cs-grid-3 video { width:100%; display:block; object-fit:cover; aspect-ratio:3/4; }
.cs-grid-wide img, .cs-grid-wide video { width:100%; display:block; object-fit:cover; aspect-ratio:16/7; }
.cs-fig img, .cs-fig video { width:100%; display:block; object-fit:cover; aspect-ratio:4/3; border:0; }
/* @media: .cs-grid-wide img, .cs-grid-wide video { aspect-ratio:16/9; } */
```

**After** (natural-ratio system):
```css
.cs-grid img, .cs-grid video,
.cs-grid-3 img, .cs-grid-3 video,
.cs-grid-wide img, .cs-grid-wide video { width:100%; height:auto; display:block; object-fit:contain; }
.cs-fig img, .cs-fig video { width:100%; height:auto; display:block; object-fit:contain; border:0; }
/* .cs-grid has align-items:start — top-aligns cells so mixed-height grids don't stretch */
/* iframes keep aspect-ratio:16/9 — not changed */
/* mobile forced-ratio rule removed entirely */
```

### Task 2 — Per-page override removal

6 pages with residual `object-fit`/`aspect-ratio` overrides on grid/media selectors:

| Page | Removed rule(s) |
|------|----------------|
| `25hours-hotels-brand-identity.html` | `.cs-grid .cs-loop video { object-fit:cover; aspect-ratio:16/9 }` |
| `classpass-bethebalance-campaign.html` | `.cs-grid-three-land img { aspect-ratio:3/2 }` |
| `concierge-coffee-brand-web.html` | `.cs-grid.portrait img { aspect-ratio:2/3 }` + `.cs-grid-3 img { object-fit:cover; aspect-ratio:2/3 }` |
| `siemens-home-appliances.html` | `.land/.port/.natural` aspect-ratio rules (3 rules) |
| `spot-asset-management-system.html` | redundant `.cs-media-full img/video` rule + conflicting `.cs-grid img/video { aspect-ratio:auto; object-fit:cover }` |
| `umane-brand-identity.html` | `.cs-grid-3 img { object-fit:cover; aspect-ratio:16/9 }` + `.cs-grid-3.portrait img { aspect-ratio:3/4 }` |

`mini-the-sooner-now-brand-campaign.html`: NOT touched — its `.cs-video-wrap` rules are a responsive iframe wrapper, not a `.cs-grid` override.

### Task 3 — Poster ratio mismatches

Zero found. No action required.

### Task 4 — width/height attrs added

- `architonic-brand-strategy-platform-design.html`: 22 imgs (21 bare + 3 `<picture>` wrapper fallback imgs). Dimensions from `sips -g pixelWidth pixelHeight`.
- `canyon-digital-experience-web-design.html`: 3 imgs (1024×683, 1024×513, 1024×513).
- `siemens-home-appliances.html`: 1 img (siemens-friends-space-kreuzberg.jpg, 1200×1200).

### Task 5 — Verification results

All verified pages pass. Images render at intrinsic dimensions, no forced crops.

| Page | Check | Result |
|------|-------|--------|
| LAS Art Foundation | Portrait Marianna Simnett image full height, grid top-aligned | ✓ |
| Ritz-Carlton | Hero 1920×1080 correct, all imgs at natural heights | ✓ |
| Siemens | 3-col grid: iframe + portrait + landscape each own height, no override | ✓ |
| Lewis | All 5 grid imgs at natural 3:2 (387×258 → 328×219) | ✓ |
| Engel-Völkers | Images at natural ratios (775×371 → 679×326) | ✓ |
| Bianca Chen | Portrait imgs at 4:5 (387×484 → 328×409), not cropped to 4:3 | ✓ |
| Architonic | All 22 imgs have hasWH:true; panoramic 2588×982 ratio preserved | ✓ |
| Qwstion | Natural 3:2 ratios, no overrides | ✓ |
| Classpass | No overrides, natural 3:2 ratios | ✓ |
| 25hours | No overrides, lazy-load intact (data-src/no src) | ✓ |
| Weiler | No overrides, natural 3:2 and 16:9 ratios | ✓ |
| Umane | No overrides, natural 16:9 ratios | ✓ |
| Mobile 375px | Bianca Chen grid stacks single-column, portrait imgs 335×419 | ✓ |

**Lazy-load system preserved**: verified `data-src` present, `src` empty — correct on all loop video pages.
**index.html untouched**: homepage video-ratio system (ratio-wide/lvwide/2/contain) not modified.

### Deferred to Session E

- **0b** Large image optimization: ~50+ images across ~30 pages without srcset. Largest: architonic-ultimate.jpg (4.2MB), ziegert-header.png (4.7MB), selfnation-banners.png (3.7MB).
- **0f** Unstacked collaborators: 12 pages with middot/comma/br separators — see `_pre-D-audit.md §0f`.

### Standing rule (update to memory)

Grid/media system is now **NATURAL-RATIO**. Never add `aspect-ratio` or `object-fit:cover/fill` to `.cs-grid`, `.cs-grid-3`, `.cs-grid-wide`, `.cs-media-full` img/video selectors. iframes always keep `aspect-ratio:16/9`. `align-items:start` on grids is intentional — do not remove.

---

## Session D (final) — 2026-06-17

**Verdict: PASS**

### D1 — File renaming

`_rename-map.csv` committed. Full asset audit: 2468/2468 files already comply with `[client]-[description].[ext]` convention (all start with parent directory slug). The only genuine gap was `assets/lv/` — abbreviated `lv` for Louis Vuitton.

**Executed:** 6 files renamed from `assets/lv/lv-*` → `assets/louis-vuitton/louis-vuitton-employer-branding-*`. Directory `lv/` removed.

**Verification table (D1):**

| Old path | Old hits after rename | New hits |
|----------|----------------------|---------|
| assets/lv/lv-poster.jpg | 0 ✓ | 2 ✓ |
| assets/lv/lv-showreel.mp4 | 0 ✓ | 2 ✓ |
| assets/lv/lv-poster-*.webp (4) | 0 ✓ | correct ✓ |

Pages updated: `404.html`, `index.html`, `louis-vuitton-employer-branding-campaign.html`.

`assets/img/` (309 files) excluded per task instructions (per-case review deferred). YouTube-ID videos excluded per instructions.

### D2 — SEO

**Fixed on 6 pages:**
- `404.html`: `<div class="nf-num">` → `<h1 class="nf-num">404</h1>`
- `about.html`: meta description added, `<p class="intro-statement">` → `<h1>`, JSON-LD (Person schema) added
- `imprint.html`: meta description + `noindex` added, `<div>` → `<h1 class="intro-statement">`
- `index.html`: JSON-LD (Person + WebSite schema) added
- `spot-asset-management-system.html`: title → "SPOT — Asset Management System — Frederik Frede"
- `work.html`: JSON-LD (CollectionPage schema) added

**Created:** `sitemap.xml` (84 URLs — all pages except 404, imprint, republish). `robots.txt` (allow all, sitemap reference). `_og-canonical-gaps.md` (all 84 pages lack OG/canonical — deferred to projects.json build pass).

**All images have alt attributes.** No duplicate titles. All pages have unique `<title>` and `lang="en"`.

### D3 — @font-face consolidation

Both @font-face declarations (UnifrakturMaguntia, Permanent Marker) moved to top of `style.css`. Stripped from all 87 page `<style>` blocks. Empty `<style>` tags removed. No @font-face remains in any `.html` file. No aria-label issues found — all existing labels correct.

### D4 — Unstacked collaborators

All 12 remaining pages converted to one `<dd>` per name:

| Page | Before | After |
|------|--------|-------|
| and-tradition-jaime-hayon.html | `Friends of Friends · Paula Prats · Emily May` | 3 × `<dd>` |
| berlin-green-brand-identity.html | `Elias Tinchon, Tim Howard, Torsten Bergler, Valeria BK` | 4 × `<dd>` |
| concierge-coffee-brand-web.html | `Klein Agency<br>(space design)` | 1 × `<dd>` (qualifier inline) |
| dr-hauschka-brand-campaigns.html | `Friends of Friends · Sima Dehgani` | 2 × `<dd>` |
| egon-zehnder-leadership-interviews.html | `Marino Coates-Chitty · Jackson Eagan · Aidan Rolls` | 3 × `<dd>` |
| friends-of-friends-brand-identity-web.html | 5 names with `<br>` | 5 × `<dd>` |
| iconist-ipad-app.html | `Axel Springer · Welt am Sonntag` | 2 × `<dd>` |
| las-art-foundation-brand-identity-motion.html | `Thomas Provost, Tim Howard, Sveta Koliada, Cecilia Martin` | 4 × `<dd>` |
| manufactum-alltagsfreude-ruth-bartlett.html | `Friends of Friends · Dan Zoubek · Serita Braxton` | 3 × `<dd>` |
| mezcla-brand-digital.html | `Lupe García · Juan Carlos García` | 2 × `<dd>` |
| qwstion-company-portrait.html | `Marino Coates-Chitty · Samuel Templeton · Megan Courtis` | 3 × `<dd>` |
| usm-modular-furniture-brand-digital.html | `Friends of Friends<br>ENGN` | 2 × `<dd>` |

B7 convention now complete across all pages.

### Deferred to Session E

- **Large image optimization**: ~50+ images without srcset across ~30 pages (see `_pre-D-audit.md §0b`). Highest priority: architonic (4.2MB), ziegert (4.7MB), selfnation (3.7MB).
- **OG/canonical injection**: all pages need og:title, og:description, og:image, og:url, canonical — deferred to projects.json build pass (see `_og-canonical-gaps.md`). **Frederik action required:** populate projects.json with cover images and metadata.
- **Nav → component**: moving nav markup into footer.js/nav.js is a separate focused pass (post-run backlog).
- **orgreen-optics**: `<img src="...showreel.mp4">` — img element should be a video element (flagged in pre-D-audit).
- **_goldstandard.md**: CSS snippets show pre-natural-ratio rules — update to reflect current system.

### Summary across all sessions (A → D final)

| Session | What | Commit(s) |
|---------|------|---------|
| A | CSS migration to style.css; 81 pages stripped | 3dd8c18, 003dd6a |
| B | Credits stacked B7; page migrations B1/B2; pferdt dead media removed | 7f1fdc9 |
| C | 34 videos re-encoded; 1 .mov converted; 3 poster images compressed | 99b870a, various |
| Natural-ratio | style.css de-crop/de-stretch; 6 page overrides removed; 25 w/h attrs | e58a8d1, 7c259f8 |
| D (this) | Collaborators B7 complete; font-face consolidated; SEO/sitemap; lv→louis-vuitton | 3a70f96 |

**Site is now ready for DNS cutover** — pending Frederik's projects.json pass (OG/canonical tags).
