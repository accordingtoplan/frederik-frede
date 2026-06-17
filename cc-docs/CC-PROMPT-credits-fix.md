# CC PROMPT — Credits-structure fix across all case studies

Paste this into a Claude Code session opened **inside the local clone of
`accordingtoplan/frederik-frede`** (run `git pull` first — a lot shipped recently:
the Architonic page, footer.js, posters, homepage). I'll paste a fresh GitHub token
when you ask; tokens expire between sessions.

---

## Standing rules (follow throughout)

- **House voice** for any prose you touch: subjectless implied voice, no first-person
  pronouns, no "he"/name references, NO em-dashes in prose, short and direct, no
  AI-speak / LinkedIn clichés / rule-of-three / parallel negation.
- **Frederik Frede is NEVER listed in Collaborators** (it's implied).
- `style.css` is the single source of truth for type/nav/footer/colour — never add
  `:root`, nav, footer, or type vars to a page's `<style>`.
- **Always GET a fresh SHA immediately before any PUT** (or just use `git` from the
  clean clone — preferred, avoids multi-thread SHA races).
- At the end: update memory + the Notion portfolio context page
  (https://app.notion.com/p/3769acb8677a81c1b9b8e7e3d4660587, insert at end).

## The canonical credits structure (reference: architonic-brand-strategy-platform-design.html)

Body markup, inside `.cs-bottom`, immediately before `<!-- FOOTER -->` / `cs-nav`:

```html
<dl class="cs-credits-cols">
  <div class="cs-credit-group"><dt>Live site</dt><dd><a href="https://…" target="_blank" rel="noopener">domain ↗</a></dd></div>
  <div class="cs-credit-group"><dt>Collaborators</dt><dd>Name, Name</dd></div>
  <div class="cs-credit-group"><dt>Year</dt><dd>2023–2025</dd></div>
</dl>
```

Field order: **Live site · [optional] · Collaborators · Year** (Year always last).

**Canonical field vocabulary (DECIDED):**
- Required core: **Live site · Collaborators · Year**
- Sanctioned OPTIONAL fields (allowed, keep where present, don't invent): **Press,
  Typeface(s), Scope**
- Anything else (Design, Development as separate fields, etc.) is NOT canonical →
  normalize: fold into Collaborators or into the description prose.
- "Live site" may be legitimately omitted when the work has no public URL
  (editorial, event, internal). If omitted, omit the field entirely — do NOT show
  an empty "Live site — ".

---

## The work — three buckets

### BUCKET A (do first, fully): 14 pages MISSING a body credits block
These have `.cs-credits-cols` in CSS + a `.cs-bottom`, but no `<dl>` in the body, so
no credits render. **Add a complete standard credits block before `cs-nav`, and fill
in everything you can find** — Live site (the brand's real URL), Year (from the case
content / `work.html` archive row / JSON-LD on the page), and **Collaborators pulled
from the case's own sources**: read the page's own body copy, any existing credit
mentions, the matching freundevonfreunden.com story (use the standing FvF harvest
method — curl the story page, it resolves from the sandbox), and the `work-archive`
data. If a collaborator genuinely can't be determined, use `—` as a placeholder, but
try the sources first. Never list Frederik Frede.

Pages:
- anja-wiroth.html
- carhartt.html
- grimetime-berlin.html
- hardedged-recordings.html
- ingo-robin.html
- mini-the-sooner-now-brand-campaign.html  ← was rebuilt earlier; confirm credits weren't dropped in that rebuild, restore from the case sources
- neubau-welt.html
- prg-ingenieure.html
- republish.html
- rooms-hotels.html
- seppuku-industries.html
- sisi-wasabi.html
- smithgroup-shanghai.html
- watergate-club.html

### BUCKET B (normalize against the decided vocabulary): 12 non-standard pages
Keep Press / Typeface(s) / Scope where they appear (now sanctioned). Fix only what
falls outside that: reorder so Year is last, ensure core fields present where
applicable, fold any non-canonical label (Design, Development) into Collaborators or
prose. Where "Live site" is missing because there's no URL, leave it omitted.

- bianca-chen-brand-identity.html — Live site, Collaborators, Typeface, Year  → already canonical (Typeface allowed); just verify order
- las-art-foundation-brand-identity-motion.html — Live site, **Design, Development**, Typefaces, Year → fold Design+Development into Collaborators (or prose), keep Typefaces
- usm-modular-furniture-brand-digital.html — Live site, Collaborators, Scope, Year → already canonical (Scope allowed); verify order
- vitra-brand-strategy.html — Live site, Collaborators, Press, Year → canonical; verify order
- qwstion-company-portrait.html — Live site, Press, Collaborators, Year → reorder to Live site · Collaborators · Press · Year (or Press before Collaborators if intentional; keep Year last)
- egon-zehnder-leadership-interviews.html — Press, Collaborators, Year (no Live site) → fine if no URL; verify Year last
- fvf-ipad-magazine.html — Collaborators, Press, Year (no Live site) → fine; verify
- iconist-ipad-app.html — Collaborators, Press, Year (no Live site) → fine; verify
- la-marzocco-friends-of-friends.html — Collaborators, Year → add Live site if a URL exists, else leave
- siemens-home-appliances.html — Collaborators, Year → add Live site if a URL exists, else leave
- ziegert-real-estate-event.html — Collaborators, Year → event work, likely no URL; leave
- ritz-carlton-berlin-brand-event.html — **Collaborators only** → add Year (and Live site only if a URL exists)

### BUCKET C (backlog, only if time): 34 pages with Collaborators = "—"
34 standard pages left Collaborators as the em-dash placeholder. Backfill real names
from case sources where findable (same method as bucket A). If solo/unknown, the dash
stays. Lower priority than A and B — do as many as is reasonable, don't force it.

---

## Verify before committing
- Every case study renders a body `<dl class="cs-credits-cols">` with Year last.
- No Frederik Frede in any Collaborators field.
- No empty "Live site — " rows (omit the field instead).
- House voice respected in any prose edits.
- Spot-check 3–4 pages live after push.

## Commit & wrap
- Commit per bucket (A, then B, then C) so it's reviewable; push.
- Update memory + the Notion context page with what shipped and what's left
  (especially any bucket-A collaborators that couldn't be sourced, and bucket-C
  remainder).

## Reproduce the audit any time
The classifier logic: parse `<dl class="cs-credits-cols">…</dl>` from each root-level
case-study HTML (exclude index/work/about/imprint/404), pull `<dt>/<dd>` pairs,
classify standard vs missing-body-block vs non-standard vs empty-collaborators.
