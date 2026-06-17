# Pre-Session-D Audit — 2026-06-17

Scanned 82 case-study pages (all .html except index, work, about, 404, imprint).
Replaces the missing _format-audit.md from B6. Committed before any CSS changes.

---

## 0a — Remaining external hotlinks

**Media src= hotlinks (src, data-src, srcset, poster pointing at external domains): NONE**

All external URLs found in HTML are `href=` on anchor tags — intentional "Live site" credits links or in-page article references. No external image/video/font src= hotlinks remain after Session C.

Notable `href=` external links that are not issues but worth noting:
- `facebook-privacy-interactive.html`: href to `yourhome.moresleep.net` (old interactive demo — site may be down; not a media asset, just a linked URL in text)
- `siemens-home-appliances.html`: 12× `href` links to `freundevonfreunden.com` stories (intentional — FvF editorial links embedded in the figcaption of the Siemens case study content)
- `classpass-bethebalance-campaign.html`: 3× `href` to FvF film stories (same pattern — intentional editorial links)
- `vitra-brand-strategy.html`: hrefs to coolhunting.com, dwell.com, designmadeingermany.de (press coverage links, intentional)
- `iconist-ipad-app.html`: hrefs to horizont.net, kress.de, garciamedia.com (press/award links, intentional)

**Session C resolved:** all `andtradition.com` image src= hotlinks (1 file). `moresleep.net` media refs previously resolved.

**Verdict: No new hotlinks to fix.**

---

## 0b — Large images (>300KB) without srcset/picture wrapper

These are bare `<img src="...">` pointing at files >300KB with no `<picture>/<source>` srcset wrapper.

**Most critical — architonic-brand-strategy-platform-design.html (21 images):**
All in bare `<img>` without responsive srcset. This page was flagged in Session C but not addressed.

| File | Size |
|------|------|
| architonic-ultimate.jpg | 4245KB |
| architonic-img-7577.jpeg | 3406KB |
| architonic-at-logo-on-coral-display-03.jpg | 2811KB |
| architonic-at-co-mockup.jpg | 3185KB |
| architonic-new-at-interface-product-page-02.jpg | 2271KB |
| architonic-new-at-interface-brand-page-products-03.jpg | 2303KB |
| architonic-new-at-interface-brand-presentation-03.jpg | 1994KB |
| architonic-at-logo-on-coral-display-01.jpg | 1624KB |
| architonic-at-logo-on-coral-mockup-01.jpg | 1567KB |
| architonic-new-at-interface-product-page-3d-configurator-01.jpg | 1545KB |
| architonic-new-at-interface-text-search-results.jpg | 2017KB |
| architonic-new-at-interface-smart-search.jpg | 911KB |
| architonic-new-at-interface-visual-search-results-06.jpg | 651KB |
| architonic-at-logo-on-coral-mockup-04.jpg | 980KB |
| architonic-at-logo-on-coral-mockup-12.jpg | 751KB |
| architonic-poster-mockup-milan-06.jpg | 1000KB |
| architonic-poster-mockup-milan-05.jpg | 721KB |
| architonic-poster-mockup-milan-02.jpg | 707KB |
| architonic-poster-mockup-milan-01.jpg | 587KB |
| architonic-poster-mockup-milan-03.jpg | 525KB |
| architonic-poster-mockup-milan-04.jpg | 519KB |
| architonic-at-poster-01.jpg | 635KB (compressed in C; already has picture wrapper) |
| architonic-at-poster-02.jpg | 675KB (compressed in C; already has picture wrapper) |
| architonic-at-poster-03.jpg | 593KB (compressed in C; already has picture wrapper) |

**Other pages with large bare images (representative, not exhaustive):**

| Page | File | Size |
|------|------|------|
| ziegert-real-estate-event.html | ziegert-header-1024x682.png | 4716KB |
| ziegert-real-estate-event.html | ziegert-layout-01-1024x696.png | 2147KB |
| ziegert-real-estate-event.html | ziegert-layout-02-1024x762.png | 1915KB |
| selfnation-campaign.html | selfnation-banners-1024x832.png | 3718KB |
| qwstion-company-portrait.html | qwstion-qwstion-stripping-2-laussicht.jpg | 2346KB |
| louis-vuitton-employer-branding-campaign.html | louis-vuitton-employer-branding-lv-5-1800x1152.png | 3359KB |
| egon-zehnder-leadership-interviews.html | egon-zehnder-xvideo-images-3000x1800.jpg | 1092KB |
| roots-management-brand-digital.html | roots-management-post-9.png | 1179KB |
| roots-management-brand-digital.html | roots-management-post-7.png | 1103KB |
| fvf-friends-space-apartment.html | fvf-friends-space-apartment-...-oksdah2o.jpeg | 1050KB |
| lewis-group-brand-identity-web-design.html | lewis-group-lewis-bus-top.png | 1160KB |
| mezcla-brand-digital.html | mezcla-download.png | 1292KB |
| mini-the-sooner-now.html | mini-brand-campaign-...-podcast-cover.jpeg | 1334KB |
| weiler-brand-identity.html | weiler-founders-1024x683.jpg | 1102KB |
| weiler-brand-identity.html | weiler-portrait-683x1024.jpg | 918KB |

Note: Many pages with large images also lack srcset — this is a broader optimization backlog for a future pass (Session E or dedicated image pass). Session D does not compress images.

---

## 0c — Missing width/height attrs on grid imgs

CLS risks: imgs in grid/media containers with no explicit `width=` and `height=` attributes.

### architonic-brand-strategy-platform-design.html (21 images)

All bare `<img>` in `.cs-grid`, `.cs-grid-3`, and `.cs-media-full` containers lack w/h.
Pixel dimensions measured via sips:

| File | Dimensions |
|------|-----------|
| architonic-poster-mockup-milan-03.jpg | 2588×982 |
| architonic-at-logo-on-coral-mockup-01.jpg | 1984×1323 |
| architonic-at-logo-on-coral-mockup-04.jpg | 1846×1232 |
| architonic-at-logo-on-coral-display-01.jpg | 1843×1382 |
| architonic-at-logo-on-coral-display-03.jpg | 1843×1382 |
| architonic-at-co-mockup.jpg | 2551×1754 |
| architonic-at-logo-on-coral-mockup-12.jpg | 1984×1364 |
| architonic-new-at-interface-visual-search-results-06.jpg | 1984×1364 |
| architonic-new-at-interface-text-search-results.jpg | 1984×1364 |
| architonic-new-at-interface-product-page-02.jpg | 1984×1323 |
| architonic-new-at-interface-product-page-3d-configurator-01.jpg | 1984×1364 |
| architonic-new-at-interface-brand-page-products-03.jpg | 1984×1323 |
| architonic-new-at-interface-brand-presentation-03.jpg | 1984×1322 |
| architonic-at-poster-01.jpg (in picture wrapper) | 1920×1439 |
| architonic-at-poster-02.jpg (in picture wrapper) | 1920×1280 |
| architonic-ultimate.jpg | 3800×2833 |
| architonic-poster-mockup-milan-01.jpg | 2582×1000 |
| architonic-poster-mockup-milan-02.jpg | 2582×994 |
| architonic-poster-mockup-milan-04.jpg | 2588×979 |
| architonic-poster-mockup-milan-05.jpg | 1054×1566 |
| architonic-poster-mockup-milan-06.jpg | 1804×1262 |

### canyon-digital-experience-web-design.html (3 images)

| File | Dimensions |
|------|-----------|
| canyon-f-utl-evo-el-148294-sitzknoten-3.jpg | 1024×683 |
| canyon-mockup-2n.jpg | 1024×513 |
| canyon-mockup-4n.jpg | 1024×513 |

### siemens-home-appliances.html (1 image)

| File | Dimensions |
|------|-----------|
| siemens-friends-space-kreuzberg.jpg | 1200×1200 |

**Total: 25 images across 3 pages. Session D Task 4 adds these attrs.**

Note: orgreen-optics-brand-digital.html has an `<img>` element whose `src=` points to an `.mp4` file (the orgreen showreel). This is not an img dimension issue — the element should be a `<video>` not `<img>`. Flagged for a future fix; not addressed in Session D.

---

## 0d — Pages with no credits block

**None.** All 82 case-study pages have `.cs-bottom > dl.cs-credits-cols`. Session B Pass 2 credits work is complete.

---

## 0e — Poster ratio mismatches

Checked 62 `<video poster="...">` elements inside `.cs-media-full` containers across all case pages. Compared video orientation (landscape/portrait) to poster orientation.

**Mismatches found: 0**

All poster images match their video's orientation (both landscape or both portrait).

One skip: `dr-hauschka-brand-campaigns.html` — `dr-hauschka-doerte-loop.mp4` — ffprobe returned no stream dimensions (file may have unusual encoding). Poster not verified for this file.

**Verdict: No poster regeneration required. CSS height:auto fix self-corrects pre-load CLS for all verified pairs.**

---

## 0f — Multi-collaborator credits not yet stacked

B7 converted 6 pages in Session B. These 12 pages still need one-`<dd>`-per-name conversion:

| Page | Current value | Separator |
|------|--------------|-----------|
| and-tradition-jaime-hayon.html | "Friends of Friends · Paula Prats · Emily May" | middot |
| berlin-green-brand-identity.html | "Elias Tinchon, Tim Howard, Torsten Bergler, Valeria BK" | comma |
| concierge-coffee-brand-web.html | "Klein Agency<br>(space design)" | br |
| dr-hauschka-brand-campaigns.html | "Friends of Friends · Sima Dehgani" | middot |
| egon-zehnder-leadership-interviews.html | "Marino Coates-Chitty · Jackson Eagan · Aidan Rolls" | middot |
| friends-of-friends-brand-identity-web.html | "Thomas Provost<br>Sam Taylor<br>Elias Tinchon<br>Isabelle Junge<br>Torsten Bergler" | br |
| iconist-ipad-app.html | "Axel Springer · Welt am Sonntag" | middot |
| las-art-foundation-brand-identity-motion.html | "Thomas Provost, Tim Howard, Sveta Koliada, Cecilia Martin" | comma |
| manufactum-alltagsfreude-ruth-bartlett.html | "Friends of Friends · Dan Zoubek · Serita Braxton" | middot |
| mezcla-brand-digital.html | "Lupe García · Juan Carlos García" | middot |
| qwstion-company-portrait.html | "Marino Coates-Chitty · Samuel Templeton · Megan Courtis" | middot |
| usm-modular-furniture-brand-digital.html | "Friends of Friends<br>ENGN" | br |

Note: `concierge-coffee-brand-web.html` has a note in the collaborator content ("Klein Agency<br>(space design)") — this may be intentional parenthetical, not a second person name. Verify before splitting.

**Action: Defer to Session E or handle in a follow-up B7 sweep.**

---

## Summary for Session D

- **CSS change needed:** Fix 4 forced-ratio rules in style.css (Task 1) — the core reason for this session.
- **Per-page overrides to remove:** Scan all 89 pages for residual `object-fit` / `aspect-ratio` overrides on grid/media selectors (Task 2).
- **width/height to add:** 25 images across 3 pages — architonic (21), canyon (3), siemens (1) (Task 4).
- **Poster mismatches:** None to fix.
- **Unstacked collaborators:** 12 pages — defer to follow-up.
- **Large images without srcset:** ~50+ images across ~30 pages — major backlog, defer to dedicated image-optimization session (Session E).
- **No media hotlinks remaining.**
