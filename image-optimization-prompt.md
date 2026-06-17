# Image Optimization Sprint — Poster & Static Image WebP Conversion
# frederikfrede.com / accordingtoplan/frederik-frede
# Add this to a Claude Code session. Run locally — no sandbox timeout risk.

---

## TO RE-RUN ON NEW IMAGES (quick-start)
```
python3 optimize_images.py --dry-run   # preview what changes
python3 optimize_images.py             # run for real
```
Then push changed files + updated index.html/work.html/footer.js as needed.

---

## CONTEXT

PageSpeed Insights (mobile, Jun 2026) flagged ~2,340 KiB saveable from oversized poster
images and static assets. All poster JPEGs are displayed at ~372px wide on mobile but
stored at 1280–3840px. frede-logo.png is 109 KiB displayed at 26×40px.

Target: convert all poster JPEGs + frede-logo.png → WebP, resize to 800px max dimension
(2× retina cap for mobile grid). Update all src references in HTML/JS.

---

## SPEC

### Poster images (video poster= attributes, homepage cases grid)
- Input: `/assets/**/*-poster.jpg` + `/assets/showreel-poster.jpg` + `/assets/las-poster.jpg`
  + `/assets/umane-poster.jpg`
- Output: same path, `.jpg` → `.webp`
- Resize: max 800px on long edge (never upscale)
- Quality: WebP q82
- Keep original only if new file ≥ 90% of original size (rare for JPEGs → WebP)
- Delete original `.jpg` after conversion

### Homepage NZZ image (biggest single win: 1,349 KiB)
- File: `/assets/home/home-index-nzzde-front-gerollt-21.png`
- Output: `/assets/home/home-index-nzzde-front-gerollt-21.webp`
- Resize: max 900px wide (displayed at 683px desktop / 419px mobile, 900 = safe 1.3× buffer)
- Quality: WebP q85
- Delete original `.png` after conversion

### Signal background image (572 KiB)
- File: `/assets/signal/signal-bg-web-01.jpg`
- Output: `/assets/signal/signal-bg-web-01.webp`
- Resize: max 1200px wide (used as full-bleed tile bg, needs more headroom)
- Quality: WebP q82
- Delete original `.jpg`

### Siemens bg image (409 KiB)
- File: `/assets/siemens/siemens-home-stories-arno-brandlhuber-krampnitz-interior.jpg`
- Output: same path, `.jpg` → `.webp`
- Resize: max 1200px wide
- Quality: WebP q82
- Delete original

### frede-logo.png (109 KiB, displayed 26×40px — absurd ratio)
- DECISION NEEDED: SVG preferred (ask Frederik). If PNG stays:
  - Output: `/frede-logo.webp`
  - Resize: 90px tall (3× retina cap for 30px display height)
  - Quality: WebP q90 (logo needs crispness)
  - Update `footer.js` src reference

---

## HTML/JS UPDATES AFTER CONVERSION

Files to update (do a global find+replace per renamed file):
- `index.html` — poster= attributes in cases JS array, NZZ img src, Signal bg
- `footer.js` — frede-logo src
- `work.html` — any poster or img src references matching converted files

Pattern: `filename.jpg` → `filename.webp` (and `.png` → `.webp` for NZZ + logo)

---

## PYTHON SCRIPT

```python
#!/usr/bin/env python3
"""
optimize_images.py
Converts poster JPEGs and oversized static images to WebP for frederikfrede.com
Run from repo root. Requires: Pillow (pip install Pillow)
"""

import os, sys, glob, shutil
from pathlib import Path
from PIL import Image

DRY_RUN = '--dry-run' in sys.argv
REPO_ROOT = Path(__file__).parent

# (glob_pattern, max_px, webp_quality, keep_threshold_ratio)
TARGETS = [
    # Poster images — all *-poster.jpg anywhere in assets/
    ('assets/**/*-poster.jpg',        800,  82, 0.90),
    ('assets/showreel-poster.jpg',    800,  82, 0.90),
    ('assets/las-poster.jpg',         800,  82, 0.90),
    ('assets/umane-poster.jpg',       800,  82, 0.90),
    # Big static images
    ('assets/home/home-index-nzzde-front-gerollt-21.png',    900,  85, 0.90),
    ('assets/signal/signal-bg-web-01.jpg',                   1200, 82, 0.90),
    ('assets/siemens/siemens-home-stories-arno-brandlhuber-krampnitz-interior.jpg', 1200, 82, 0.90),
]

def convert(src_path, max_px, quality, keep_ratio):
    src = REPO_ROOT / src_path
    if not src.exists():
        print(f'  SKIP (not found): {src_path}')
        return None, None

    dst = src.with_suffix('.webp')
    orig_size = src.stat().st_size

    if DRY_RUN:
        img = Image.open(src)
        w, h = img.size
        scale = min(1.0, max_px / max(w, h))
        new_w, new_h = int(w*scale), int(h*scale)
        print(f'  DRY: {src.name} {w}×{h} → {new_w}×{new_h} .webp q{quality}')
        return None, None

    img = Image.open(src).convert('RGB')
    w, h = img.size
    scale = min(1.0, max_px / max(w, h))
    if scale < 1.0:
        img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)

    img.save(dst, 'WEBP', quality=quality, method=6)
    new_size = dst.stat().st_size

    if new_size >= orig_size * keep_ratio:
        print(f'  SKIP (no gain): {src.name} {orig_size//1024}KB → {new_size//1024}KB')
        dst.unlink()
        return None, None

    saved = orig_size - new_size
    print(f'  OK: {src.name} {orig_size//1024}KB → {new_size//1024}KB (saved {saved//1024}KB)')
    src.unlink()
    return str(src.relative_to(REPO_ROOT)), str(dst.relative_to(REPO_ROOT))

print(f'{"DRY RUN — " if DRY_RUN else ""}Image optimization sprint\n')
renames = []  # [(old_relative, new_relative), ...]

for pattern, max_px, quality, keep_ratio in TARGETS:
    matches = list(REPO_ROOT.glob(pattern))
    if not matches:
        print(f'No match: {pattern}')
        continue
    for match in matches:
        old, new = convert(match.relative_to(REPO_ROOT), max_px, quality, keep_ratio)
        if old and new:
            renames.append((old, new))

if not DRY_RUN and renames:
    print(f'\n{len(renames)} files converted. Now update HTML/JS references:')
    for old, new in renames:
        old_name = Path(old).name
        new_name = Path(new).name
        print(f'  s/{old_name}/{new_name}/g  →  index.html, work.html, footer.js')
    print('\nRun find+replace in those files, then commit everything together.')
```

---

## COMMIT MESSAGE
```
perf: convert poster JPEGs + static images to WebP, resize to mobile-appropriate dimensions

~2,300 KiB saved on initial page load (mobile). Affects: showreel, architonic,
pferdt, lv, umane, las, usm, bianca-chen, mini posters + NZZ PNG + Signal bg.
References updated in index.html.
```

---

## AFTER THE SPRINT — RE-RUN PAGESPEED
Expected mobile score improvement: 89 → 93–95
Remaining flag after this sprint: Google Fonts render-block (needs HTTP/2 push or
self-hosting fonts — lower priority, already async-loaded for Permanent Marker).
