# New case study — authoring checklist

Build every new case by cloning `case-template.html`. Before it goes live, it must
pass all of this. (These are the exact things the cleanup passes fixed retroactively —
the checklist stops them recurring.)

## Setup
- [ ] Cloned from `case-template.html`, not from an old page (old pages carry the
      inline-CSS / orphaned-media-query risk).
- [ ] Filename = SEO slug: `[client]-[project-type]-[description].html`, lowercase,
      hyphens. Assets in `/assets/[slug]/` named `[client]-[type]-[desc]-[n].[ext]`.

## Head
- [ ] `<title>` = `{Client} — Frederik Frede`.
- [ ] `<meta name="description">` filled (~150 chars, real sentence).
- [ ] Open Graph tags filled (og:title / description / image / url) — image points to
      a real, non-black poster.
- [ ] Links `style.css`. NO inline `cs-*` `<style>` block. A `<style>` tag only if
      this page has genuinely unique rules (and even then, never `:root`, nav, footer,
      or type vars — those live in style.css).
- [ ] JSON-LD filled (name, description, year).

## Voice (all prose)
- [ ] Subjectless implied voice — no first-person pronouns, no "he", no name refs.
- [ ] NO em-dashes anywhere in prose.
- [ ] No AI-speak / LinkedIn clichés / rule-of-three / parallel negation
      ("not X, it's Y") / significance-claims ("the quiet argument").
- [ ] Short, direct sentences.
- [ ] A framing/intro block ONLY if the case has a real strategic stake; visual-only
      cases stay visual (forced framing is worse than none).

## Media
- [ ] First video (hero) is EAGER: `preload="auto"` + `fetchpriority="high"`, plain
      `src`, real poster.
- [ ] Every OTHER video uses the lazy pattern: `data-lazy` + `preload="metadata"` +
      `<source data-src="…">` + a real poster (footer.js loads it on scroll).
- [ ] Every poster is a real frame, NOT black/blank. (Quick check: a poster with
      mean brightness near 0 is broken — pull a brighter frame.)
- [ ] All assets self-hosted under `/assets/[slug]/`. No hotlinks from moresleep.net
      or other CDNs that block server-side fetches.
- [ ] Images have `loading="lazy"` and meaningful `alt`.
- [ ] Two-col via `cs-grid`, three-col via `cs-grid-3`. A lone landscape image may sit
      full-width (`cs-media-full`) rather than be forced into a half-empty grid cell.

## Credits (required)
- [ ] A `<dl class="cs-credits-cols">` block is present in `.cs-bottom`.
- [ ] Field order: Live site · [Press/Typeface/Scope if used] · Collaborators · Year.
      Year ALWAYS last.
- [ ] "Live site" omitted entirely if there's no public URL (no empty dash row).
- [ ] Frederik Frede NOT listed in Collaborators.
- [ ] Any film/photo/production people added to Collaborators.

## Wiring
- [ ] Prev/next spliced into the continuous work.html-order loop (and the
      neighbouring pages' next/prev updated to point here).
- [ ] Added to `work.html` archive grid with discipline[] + sector[] tags from the
      canonical vocabulary (8 disciplines, 9 sectors).
- [ ] `<script src="/footer.js"></script>` present (global JS, lazy-load, footer,
      theme).
- [ ] `setTheme()` works (logo filter switches across themes).

## Verify before publish
- [ ] Renders correctly at desktop AND mobile (grids side-by-side on desktop,
      single-col on mobile; credits column positions right; nav aligns).
- [ ] Brace-balanced if any inline `<style>` exists; no layout rule outside its
      `@media`.
- [ ] Live render check: posters show instantly, videos load on scroll, no layout
      shift, no 403/404 assets.

## After publish
- [ ] Update memory + Notion portfolio context page.
- [ ] If new external/hotlinked media was referenced, append to
      `full-hotlink-inventory.csv` with a dated note.
