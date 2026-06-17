#!/usr/bin/env python3
"""
Pass 3 — site-wide video lazy-loading rollout.

Converts non-hero <video> elements to the data-lazy + <source data-src> pattern
that footer.js's initVideoLazy() observer handles. Hero = first <video> in
document order; kept eager (preload="auto" + fetchpriority="high").

Poster detection: looks for {stem}-poster.jpg or {stem}.jpg in the same folder.
Writes poster-manifest.txt with ffmpeg commands for videos still missing a poster.

Usage:
    python3 lazyload-videos.py          # dry-run (prints, no writes)
    python3 lazyload-videos.py --write  # writes HTML + poster-manifest.txt
"""
import re, glob, os, sys

WRITE = "--write" in sys.argv
EX = {"index.html", "work.html", "about.html", "imprint.html",
      "404.html", "republish.html"}
EXT_TYPE = {".mp4": "video/mp4", ".webm": "video/webm",
            ".mov": "video/quicktime", ".ogg": "video/ogg"}


def poster_candidates(src):
    """Return (attr_value, local_path) pairs to check for an existing poster."""
    s = src.lstrip("/")
    stem = os.path.splitext(s)[0]
    results = []
    for suffix in ("-poster.jpg", ".jpg"):
        local = stem + suffix
        attr = ("/" + local) if src.startswith("/") else local
        results.append((attr, local))
    return results


def find_existing_poster(src):
    """Return (attr_value, local_path) if a poster file exists, else None."""
    for attr_val, local in poster_candidates(src):
        if os.path.isfile(local):
            return attr_val, local
    return None


def manifest_cmd(src):
    """Return an ffmpeg command line (or a comment) for generating a poster."""
    s = src.lstrip("/")
    stem = os.path.splitext(s)[0]
    out = stem + "-poster.jpg"
    if not os.path.isfile(s):
        return f"# FILE MISSING (skip): {s}"
    size = os.path.getsize(s)
    if size == 0:
        return f"# FILE EMPTY (skip): {s}"
    return (f'ffmpeg -ss 1 -i "{s}" -vframes 1 '
            f'-vf "scale=\'min(1600,iw):-2\'" -q:v 3 "{out}"')


def get_video_src(block):
    """Extract the primary src from a video block (video src= or first source src=)."""
    m = re.search(r'\bsrc="([^"]+)"', block.split(">", 1)[0])  # on <video tag
    if m:
        return m.group(1)
    m = re.search(r'<source\b[^>]*\bsrc="([^"]+)"', block)
    if m:
        return m.group(1)
    m = re.search(r'<source\b[^>]*\bdata-src="([^"]+)"', block)
    if m:
        return m.group(1)
    return None


def transform_block(block, is_hero):
    """
    Transform one <video>...</video> block.
    Returns (new_block, missing_poster_src_or_None).
    missing_poster_src: src string if poster is needed but absent, else None.
    """
    # Split: <video ...attrs... > body </video>
    m = re.match(r'(<video\b)([ \t\n][^>]*?)(>)(.*?)(</video>)', block, re.S)
    if not m:
        return block, None

    open_kw = m.group(1)    # '<video'
    attrs    = m.group(2)   # ' autoplay muted ...'
    gt       = m.group(3)   # '>'
    body     = m.group(4)   # inner HTML
    close    = m.group(5)   # '</video>'

    has_poster      = 'poster=' in attrs
    already_lazy    = 'data-lazy' in attrs
    video_src_m     = re.search(r'\bsrc="([^"]+)"', attrs)
    video_src       = video_src_m.group(1) if video_src_m else None
    has_source_child = bool(re.search(r'<source\b', body))

    # Primary src (for poster lookup + manifest)
    if video_src:
        primary_src = video_src
    elif has_source_child:
        sm = re.search(r'<source\b[^>]*\bsrc="([^"]+)"', body)
        if not sm:
            sm = re.search(r'<source\b[^>]*\bdata-src="([^"]+)"', body)
        primary_src = sm.group(1) if sm else None
    else:
        primary_src = None

    # --- HERO: keep eager, add fetchpriority + preload=auto, no data-lazy ---
    if is_hero:
        attrs = re.sub(r'\s*\bdata-lazy\b', '', attrs)
        if 'preload=' in attrs:
            attrs = re.sub(r'\bpreload="[^"]*"', 'preload="auto"', attrs)
        else:
            attrs += ' preload="auto"'
        if 'fetchpriority=' not in attrs:
            attrs += ' fetchpriority="high"'
        # Wire poster if exists and missing
        miss = None
        if not has_poster and primary_src:
            found = find_existing_poster(primary_src)
            if found:
                attrs += f' poster="{found[0]}"'
            else:
                miss = primary_src
        return open_kw + attrs + gt + body + close, miss

    # --- NON-HERO already converted: check for missing poster only ---
    if already_lazy:
        miss = None
        if not has_poster and primary_src:
            found = find_existing_poster(primary_src)
            if found:
                attrs += f' poster="{found[0]}"'
            else:
                miss = primary_src
        if miss or ('poster=' in attrs and 'poster=' not in m.group(2)):
            return open_kw + attrs + gt + body + close, miss
        return block, miss

    # --- NON-HERO: lazify ---
    # 1. preload="metadata"
    if 'preload=' in attrs:
        attrs = re.sub(r'\bpreload="[^"]*"', 'preload="metadata"', attrs)
    else:
        attrs += ' preload="metadata"'

    # 2. data-lazy
    attrs += ' data-lazy'

    # 3. Handle src on <video> tag → move to <source data-src> child
    if video_src and not has_source_child:
        attrs = re.sub(r'\s*\bsrc="[^"]*"', '', attrs)
        ext = os.path.splitext(video_src)[1].lower()
        vtype = EXT_TYPE.get(ext, 'video/mp4')
        source_el = f'\n    <source data-src="{video_src}" type="{vtype}">\n  '
        body = source_el + body.strip()
    elif has_source_child and not already_lazy:
        body = re.sub(r'(<source\b[^>]*)\bsrc="([^"]*)"',
                      r'\1data-src="\2"', body)

    # 4. Poster
    miss = None
    if not has_poster and primary_src:
        found = find_existing_poster(primary_src)
        if found:
            attrs += f' poster="{found[0]}"'
        else:
            miss = primary_src

    return open_kw + attrs + gt + body + close, miss


def process_file(path):
    h = open(path, encoding="utf-8").read()
    vid_re = re.compile(r'<video\b[^>]*>.*?</video>', re.S)
    blocks = list(vid_re.finditer(h))
    if not blocks:
        return None, []

    missing_posters = []
    result = h
    offset = 0
    changed = False

    for i, m in enumerate(blocks):
        is_hero = (i == 0)
        original = m.group(0)
        new_block, miss = transform_block(original, is_hero)
        if miss:
            missing_posters.append(miss)
        if new_block != original:
            s = m.start() + offset
            e = m.end() + offset
            result = result[:s] + new_block + result[e:]
            offset += len(new_block) - len(original)
            changed = True

    return (result if changed else None), missing_posters


# ---------- Main ----------
manifest_lines = []
pages_changed = 0
pages_miss_poster = 0

for path in sorted(glob.glob("*.html")):
    if path in EX:
        continue
    new_h, missing = process_file(path)
    if missing:
        pages_miss_poster += 1
        for src in missing:
            manifest_lines.append(manifest_cmd(src))
    if new_h is not None:
        pages_changed += 1
        if WRITE:
            open(path, "w", encoding="utf-8").write(new_h)
            print(f"WROTE  {path}")
        else:
            print(f"WOULD  {path}")
    else:
        if missing:
            print(f"(no markup change, {len(missing)} poster(s) missing) {path}")

manifest_str = "\n".join(manifest_lines) + ("\n" if manifest_lines else "")
if WRITE:
    with open("poster-manifest.txt", "w") as f:
        f.write(manifest_str)

print(f"\n{'Wrote' if WRITE else 'Would write'} poster-manifest.txt — "
      f"{len(manifest_lines)} ffmpeg command(s) for {pages_miss_poster} page(s)")
print(f"Pages to change: {pages_changed}")
print(f"MODE: {'WRITE' if WRITE else 'dry-run'}")
