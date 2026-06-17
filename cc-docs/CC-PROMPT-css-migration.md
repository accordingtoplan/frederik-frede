# CC PROMPT — Migrate shared cs-* CSS into style.css (Option 2, the structural fix)

Run in Claude Code, local clone of `accordingtoplan/frederik-frede`, `git pull` first.
This is the foundation pass — do it before the credits and template work.

I'll paste a fresh GitHub token. Use git from the clean clone for commits (avoids
SHA races). Update memory + Notion context page at the end.

---

## The problem this fixes

Every case-study page carries an ~8.5KB inline `<style>` block of `cs-*` rules
(layout for `.cs-header`, `.cs-grid`, `.cs-media-full`, `.cs-bottom`,
`.cs-credits-cols`, `.cs-nav`, `.cs-pullquote`, `.cs-strategy`, `.cs-testimonials`,
`.cs-studio*`, etc.). It's duplicated and has drifted page-to-page. That duplication
is HOW the orphaned-media-query bug spread (a stray `}` left `.cs-grid {1fr}` applying
at all widths, silently collapsing every two-col grid to one column on desktop).
Reference: that bug was fixed by hand on `architonic-brand-strategy-platform-design.html`.

Goal: extract the shared `cs-*` ruleset into `style.css` ONCE, remove it from the 82
pages, so there's a single source of truth and the bug class can't recur.

## Do this carefully — it's the highest-touch pass

This is NOT a blind copy of Architonic's inline block into style.css. Pages have
variants. Work empirically:

1. **Inventory.** For each of the 82 case studies (root-level .html, exclude
   index/work/about/imprint/404), extract the inline `<style>` block. Parse every
   rule. Build a map of selector → { set of distinct declaration-bodies seen, which
   pages use each }.

2. **Classify each rule:**
   - **Universal** — identical across (nearly) all pages → goes to style.css.
   - **Variant** — same selector, different declarations on different pages (e.g.
     `.cs-slides` with different `grid-template-columns`, page-specific `.cs-studio*`
     that only exist on Architonic). Decide per case: if it's a real per-page need,
     keep it inline on that page; if it's drift, reconcile to one canonical version
     in style.css.
   - **Page-unique** — only one page has it → leave inline on that page.

3. **Reconcile the media queries.** Several pages have TWO `@media (max-width:640px)`
   blocks (residue of the copy-paste that caused the AT bug). Collapse to one clean
   mobile block in style.css. Verify brace balance on every page after stripping.

4. **Write style.css additions.** Append a clearly-commented
   `/* ===== Case study layout (migrated from inline) ===== */` section with the
   universal/canonical `cs-*` rules. Keep the existing style.css contents intact
   (it's the source of truth for type/nav/footer/colour vars — don't duplicate those).

5. **Strip the inline blocks.** On each page, remove the migrated rules from its
   `<style>`. Leave only genuinely page-specific rules (or remove the `<style>` tag
   entirely if nothing remains). Keep each page's JSON-LD and any per-page `<script>`.

6. **Test thoroughly.** This pass can shift layouts if a variant was missed. After
   migration, spot-render a representative sample at desktop AND mobile widths:
   a media-heavy case (architonic), a slides case, a testimonials case, a plain
   text+image case. Confirm: two-col grids are side-by-side on desktop, single-col
   on mobile; credits column positions correctly; nav prev/next aligns; pullquotes
   and captions intact. Compare against the live (pre-migration) render of the same
   pages.

## Guardrails
- style.css stays the single source for `:root` vars, type, nav, footer, reset —
  do NOT move those or duplicate them.
- Don't change visual design — this is a refactor, not a redesign. If two pages
  legitimately differ, preserve both behaviours (canonical in style.css + a
  page-specific override only where truly needed).
- Brace-balance check every page's remaining inline `<style>` (count `{` == `}`)
  and confirm no `cs-*` layout rule sits outside an `@media` when it should be inside.
- Commit in logical chunks (style.css additions first, then strip pages in batches)
  so it's reviewable and revertible.

## Definition of done
- style.css contains the canonical `cs-*` case-study layout, well-commented.
- All 82 pages' inline `<style>` reduced to page-specific rules only (most empty).
- No page renders differently than before EXCEPT where it fixes the
  orphaned-media-query bug (grids that were wrongly stacked now sit side-by-side).
- Sample pages verified at desktop + mobile.
- The orphaned-media-query bug is now structurally impossible (shared rules live in
  one file).
- Memory + Notion updated; note any pages that needed page-specific overrides.

## Reproduce the inline-CSS audit
Parse `<style>…</style>` per case, map selector→declaration-bodies→pages, flag
selectors with >1 distinct body (variants) and any duplicated `@media` blocks.
