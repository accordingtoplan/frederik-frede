# Gold Standard — canonical patterns for frederikfrede.com

Established 2026-06-17 from `style.css` (post-pass-1-migration) and
`architonic-brand-strategy-platform-design.html` (reference page).

---

## Figure / Grid system

All classes live in `style.css`. Page `<style>` blocks may override
aspect-ratio or object-fit for specific images; the grid containers
themselves must not be redefined inline.

### 2-col image grid

```css
.cs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; padding: 0 48px; }
.cs-grid img, .cs-grid video { width: 100%; display: block; object-fit: cover; aspect-ratio: 4/3; }
.cs-grid iframe { width: 100%; display: block; border: 0; aspect-ratio: 16/9; }
```

### 3-col image grid

```css
.cs-grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 24px; margin-bottom: 24px; padding: 0 48px; }
.cs-grid-3 img, .cs-grid-3 video { width: 100%; display: block; object-fit: cover; aspect-ratio: 3/4; }
```

### Span-2 wide item (used inside .cs-grid)

```css
.cs-grid-wide { grid-column: span 2; }
.cs-grid-wide img, .cs-grid-wide video { width: 100%; display: block; object-fit: cover; aspect-ratio: 16/7; }
```

### 2-col figure grid (with captions)

```css
.cs-figrid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; padding: 0 48px; }
```

### 3-col figure grid (with captions)

```css
.cs-figrid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 24px; margin-bottom: 24px; padding: 0 48px; }
```

### Figure item (child of .cs-figrid or .cs-figrid-3)

```css
.cs-fig { display: flex; flex-direction: column; gap: 10px; margin: 0; }
.cs-fig img, .cs-fig video { width: 100%; display: block; object-fit: cover; aspect-ratio: 4/3; border: 0; }
.cs-fig iframe { width: 100%; display: block; border: 0; aspect-ratio: 16/9; }
.cs-fig figcaption { display: flex; justify-content: space-between; gap: 12px; font-size: 12px; line-height: 1.4; }
.cs-fig .cap-name { font-weight: 700; color: var(--grey-dark); }
.cs-fig .cap-meta { color: var(--grey-light); text-align: right; white-space: nowrap; }
```

HTML pattern:
```html
<div class="cs-figrid-3">
  <figure class="cs-fig">
    <img src="..." alt="...">
    <figcaption><span class="cap-name">Name</span><span class="cap-meta">Context</span></figcaption>
  </figure>
</div>
```

### Story chapter head (used above .cs-figrid-3 groups)

```css
.cs-story-head { padding: 0 48px 24px; display: flex; justify-content: space-between; align-items: baseline; gap: 24px; flex-wrap: wrap; }
.cs-story-head h3 { font-size: clamp(20px, 2.4vw, 30px); font-weight: 700; letter-spacing: -0.02em; color: var(--grey-dark); margin: 0; }
.cs-story-head a { font-size: 13px; color: var(--grey-mid); text-decoration: none; white-space: nowrap; }
.cs-story-head a:hover { color: var(--grey-dark); }
```

### Full-width media (including iframe)

```css
.cs-media-full { padding: 0 48px; margin-bottom: 24px; }
.cs-media-full img, .cs-media-full video { width: 100%; display: block; object-fit: unset; }
.cs-media-full iframe { width: 100%; display: block; border: 0; aspect-ratio: 16/9; }
```

---

## Credits block

Standard HTML (from `architonic-brand-strategy-platform-design.html`):

```html
<div class="cs-bottom">
  <div class="cs-description">
    <p>…closing copy…</p>
  </div>
  <dl class="cs-credits-cols">
    <div class="cs-credit-group"><dt>Live site</dt><dd><a href="https://…" target="_blank" rel="noopener">domain ↗</a></dd></div>
    <div class="cs-credit-group"><dt>Collaborators</dt><dd>Name A</dd><dd>Name B</dd></div>
    <div class="cs-credit-group"><dt>Year</dt><dd>YYYY</dd></div>
  </dl>
</div>
```

**B7 convention (Session B 2026-06-17):** one `<dd>` per collaborator name — no middots, no `<br>`. Same rule applies to any multi-value field (Typeface, Press, etc.).

Rules (in `style.css`):

```css
.cs-bottom { padding: 80px 48px 100px; position: relative; border-top: 1px solid var(--border); margin-top: 80px; }
.cs-description { max-width: 50%; }
.cs-credits-cols { position: absolute; right: 48px; top: 80px; text-align: right; align-content: start; }
.cs-credit-group { margin-bottom: 28px; }
.cs-credit-group dt { font-size: 11px; text-transform: uppercase; letter-spacing: 0.09em; color: var(--grey-light); margin-bottom: 4px; }
.cs-credit-group dd { font-size: 14px; font-weight: 700; color: var(--grey-dark); margin: 0; line-height: 1.5; }
.cs-credit-group dd a { color: var(--grey-dark); text-decoration: none; }
.cs-credit-group dd a:hover { opacity: 0.6; }
```

Standard fields: `Live site` (omit if no live URL), `Collaborators` (use `—` if none), `Year`.

---

## Known page-specific overrides (do NOT move to style.css)

| Page | Class(es) | Reason |
|------|-----------|--------|
| siemens-home-appliances.html | `.cs-grid img.land/port/natural` | per-image aspect ratio overrides |
| siemens-home-appliances.html | `.cs-slideshow` / `.ss-*` | bespoke JS slideshow component |
| classpass-bethebalance-campaign.html | `.cs-grid-three-land` | 3-col 3:2 landscape grid variant |
| frederik-pferdt-personal-brand-identity.html | `.cs-credits-cols` grid variant | right-aligned stacked credits |
| spot-asset-management-system.html | all `.cs-*` overrides | intentional design-system variant |
