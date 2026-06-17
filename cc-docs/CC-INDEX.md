# Frederik Frede portfolio — Claude Code work index

One place for all the outstanding CC passes, in the order they should run, plus the
forward-looking pieces that keep FUTURE case studies correct automatically.

---

## STATUS — each session updates this before wrapping up

Mark your pass `[x]` when done, add the date + commit hash, and note anything left.
The next session reads this first to know where things stand.

- [x] **1. CSS migration to style.css** — `CC-PROMPT-css-migration.md`
      _done + MERGED TO main 2026-06-16: commits 3dd8c18 (style.css canonical) + 003dd6a (strip 81 pages), pushed to origin/main (4482f2a..003dd6a). Live. (Superseded the earlier buggy `pass1-css-migration` branch, now deleted.)_
      _Canonical cs-* ruleset (+ footer-logo) now lives once in style.css, built empirically from the dominant body of each selector across 81 pages (see cc-docs/_inventory.py, _canonical.css, _strip.py). 55 pages have zero inline CSS; 26 keep only page-specific rules. Verified pre/post via computed-style diffing at desktop+mobile (architonic, meama, bmw, concierge, spot, signal-la)._
      _Caveats: (1) The orphaned-media bug was already gone on origin (top-level grids were all 2-col), so this pass is purely structural — no grid "fix" was needed. (2) ONE intended visual change: 19 pages carried a duplicate 2nd mobile @media block (24px h-padding + tighter section spacing) that was overriding the 1st; collapsing it means those 19 now use the site-wide mobile spacing the other 62 already had (header `80px 20px 36px` not `48px 24px 40px`, h-padding 24px→20px). Worth an eyeball on mobile if that tighter spacing was intentional. (3) Two cascade traps found+fixed mid-pass (both in _strip.py): (a) cascade-ORDER — when a page keeps a top-level selector override, its mobile rule for that selector must stay inline too (else canonical-in-style.css wins at mobile); (b) property-LEAK — a page's PARTIAL override (e.g. LV/spot `.cs-grid img{width;display;height:auto}` for natural-ratio images, pferdt/ritz credits without `position`) previously relied on there being NO global cs-* rule; once canonical exists, its other props (object-fit/aspect-ratio/position/border-top/margin-top…) leak in. Fix: `neutralize()` appends explicit resets (marked `/*keep*/`) for omitted canonical props on kept TOP-LEVEL rules — initial for non-inherited (the `*{margin:0;padding:0}` reset makes initial==pre), `inherit` for inherited. Verified by re-running the leak analyzer → zero residual leaks. **Lesson for passes 2-3: globalizing a rule that any page partially overrides leaks properties; always diff computed styles pre/post.**_
      _Page-specific overrides retained: spot (--fg design generation), ritz-carlton + rooms-hotels + classpass + siemens (alt cs-2col/3col/fig/figrid/slideshow templates), concierge/umane/frederik-pferdt/signal-la (credits-column variants), neubau (cs-covers/slides 24px-gap variant), bianca (dead cs-slides/grid-wide rules — no elements), plus a 10-page `.cs-slides padding:0 24px!important` group._
- [x] **2. Credits-structure fix** — `CC-PROMPT-credits-fix.md`
      _done + pushed to main 2026-06-17: commits 04866e0 (bucket A), 53d2565 (B), 9962e57 (C); live (rebased onto origin 64e4b4a, homepage/about had advanced again). Audit script: cc-docs/_credits_audit.py / _add_credits.py._
      _Bucket A (13 pages, was missing body credits): added full .cs-bottom block before nav; Year from each page's own cs-tags; Live site only where verified live+genuine (rooms-hotels→roomshotels.com; thesoonernow.com REJECTED — now a gambling squatter, always re-verify old URLs). mini-the-sooner-now was TRUNCATED by an earlier rebuild (no credits/nav/footer/closing tags) — restored full tail (credits, prev/next Ørgreen↔Thonet, footer.js + theme script, </body></html>); confirmed footer mounts live._
      _Bucket B (2 pages): las-art folded Design+Development→Collaborators (kept Typefaces); ritz added Year 2019; also fixed meama's broken empty `Live site — ↗` row (removed)._
      _Bucket C (5 of 45 backfilled): only credited collaborators a page NAMES in its own copy — Friends of Friends (25hours/adidas/engel-völkers/wefox), ENGN (markilux). The other 40 keep honest `—` (no fabrication on a real portfolio). Final audit: missing 0, nonstandard 0, standard 41, empty-collab 40. No Frederik in any Collaborators._
- [x] **3. Video loading optimization** — `CC-PROMPT-video-loading-optimization.md`
      _done + pushed to main 2026-06-17: commit 99b870a. Script: lazyload-videos.py (committed to repo root). 30 pages converted (117 video elements across 31 pages; Architonic was already done). Hero = first <video> in document order: preload="auto" + fetchpriority="high", src kept plain. All others: data-lazy + preload="metadata" + <source data-src>. 74 first-frame poster JPEGs generated via ffmpeg (max 1600px). Black-poster check run (PIL mean brightness): 2 FvF videos (logo-grid-animation, showreel) are intentionally dark — white marks on black throughout, left as best available frame. pferdt-fgp-screen-rec-sm.mp4 is 0 bytes (pre-existing broken asset, noted in poster-manifest.txt, no poster possible). Videos with inline <video src> (25hours, hospitality-projects) restructured to <source data-src> so footer.js observer fires. Origin advanced 3× during session (perf fixes + docs); rebased cleanly._
- [ ] **4. Template + checklist verified live** — `case-template.html` + `NEW-CASE-CHECKLIST.md`
      _status: files drafted; verify against final structure after pass 1_

> When you finish a pass, replace its `_status:_` line with e.g.
> `_done 2026-06-20, commit a1b2c3d. Note: 2 pages needed page-specific overrides (X, Y)._`

---

**Run all of this in Claude Code (local clone of `accordingtoplan/frederik-frede`),
NOT GitHub Copilot in VS Code.** Copilot has a separate monthly credit pool that's
exhausted until July 1; CC bills through the Anthropic plan. Open CC inside the repo
folder and `git pull` first — a lot shipped recently (Architonic page, footer.js,
posters, homepage, the new architonic poster).

Every session: paste a fresh GitHub token when asked, follow the house voice + repo
rules, GET a fresh SHA before any PUT (or just use git from the clean clone), and
update memory + the Notion context page at the end.

---

## Why the order matters

The cleanup prompts (1–3) fix the **82 pages that exist today**. The template +
checklist (4) is what makes everything **stay fixed for new cases you add later** —
without it, the next case study you build can reintroduce every bug we just removed.

Run them in this sequence because each depends on the previous being done:

### 1. CSS migration to style.css  →  `CC-PROMPT-css-migration.md`  **(do first — foundation)**
Moves the shared `cs-*` rules (currently duplicated as an ~8.5KB inline `<style>`
block on all 82 pages) into `style.css` once. This is the structural fix for the
orphaned-media-query bug class — that bug only spreads because the CSS is copy-pasted
per page. After this, there's ONE source of truth and the bug becomes impossible to
repeat. Do this first because the template (step 4) should be built against the
post-migration minimal-head structure, not the old inline-heavy one.

### 2. Credits-structure fix  →  `CC-PROMPT-credits-fix.md`
Adds missing credits blocks (14 pages), normalizes field vocabulary (12 pages),
backfills Collaborators (34 pages). Decisions already baked in: bucket A fully
filled incl. Collaborators from case sources; Press/Typeface/Scope are sanctioned
optional fields. Run after CSS migration so credits edits happen on the clean
structure.

### 3. Video loading optimization  →  `CC-PROMPT-video-loading-optimization.md`
Lazy-loads case-study videos + generates first-frame posters across the 88 pages,
matching what's already live on Architonic and the homepage. `footer.js` already has
the observer; this converts the page markup + makes posters. Includes the
black-poster check (scan for any poster under ~5 mean brightness — the architonic
homepage poster was pure black; catch broken exports automatically).

### 4. Clean template + authoring checklist  →  `case-template.html` + `NEW-CASE-CHECKLIST.md`  **(the future-proofing)**
A clean, canonical case-study page to clone for every NEW case, plus a checklist the
new page must satisfy. Built against the post-migration structure (minimal head,
inherits from style.css, correct credits block, lazy video pattern). This is what
makes "works globally for future cases" true rather than just "82 pages fixed once."

---

## Separate (not a build pass)

- `BUGS-FOUND-architonic-session.md` — the running bug log from this session
  (orphaned media-query, eager video loading, stale GA/cookie notes, black poster).
  Reference doc; its fixes are folded into prompts 1–3.

---

## Definition of done for the whole programme
- All 82 case studies share one `cs-*` ruleset in style.css; inline `<style>` blocks
  reduced to page-specific rules only (or empty).
- Every case has a canonical credits block; no Frederik in Collaborators.
- Every case video lazy-loads with a real (non-black) poster.
- `case-template.html` exists and passes the checklist; building a new case = clone
  it, fill content, run the checklist.
- Memory + Notion updated.

## Suggested working rhythm
Do 1 fully (it's the biggest and everything builds on it), verify live, commit.
Then 2, then 3 — each is independent once 1 is done. Build 4 last so the template
reflects the final structure. Don't run all four in one mega-session; one prompt per
session keeps each reviewable and avoids token exhaustion.

**Every session, before wrapping up:** tick your pass in the STATUS block at the top
of this file (date + commit + any caveats), then update memory + the Notion context
page. That STATUS block is the handoff — the next session trusts it to know what's
done.
