#!/usr/bin/env python3
"""
debug-check.py — static pre-push gate for frederik-frede.

Reads the HTML/CSS/JS files in the repo and reports problems WITHOUT touching
the network. Fast (<1s), deterministic. Run before any batch push.

  python3 debug-check.py            # check whole repo (cwd)
  python3 debug-check.py file1.html # check only the named files

EXIT CODES
  0  = no hard failures (safe to push; warnings may still print)
  1  = at least one HARD failure (brace imbalance, dead internal link,
       new hotlink, duplicate id) — fix before pushing

HARD failures block. WARNINGS are known-deferred backlog items (missing OG,
eager videos, missing alt) — printed for visibility, do NOT fail the gate.

When you find a new bug class, add a checker function below and register it in
HARD_CHECKS or WARN_CHECKS. Keep checks STATIC (no network) — anything needing
to fetch a URL or decode a video belongs in debug-crawl.py instead.
"""
import re, sys, glob, os
from collections import defaultdict

# ── hotlink hosts: any asset src/href pointing at these is an unlocalized hotlink.
# These mirror the localization backlog. Add hosts as new ones appear.
HOTLINK_HOSTS = [
    "moresleep.net", "freundevonfreunden.com", "friendsoffriends.com",
    "website-files.com", "webflow", "squarespace", "vitra.com", "hay.com",
    "thonet.de", "sonos.com", "architonic.com", "egonzehnder.com",
    "lewisgroupofcompanies.com", "aleo-solar.com",
]
# hosts that are legitimately external (links out, embeds) and NOT hotlinked assets
ALLOW_EXTERNAL = ["youtube.com", "youtu.be", "vimeo.com", "player.vimeo.com",
                  "instagram.com", "linkedin.com", "fonts.googleapis.com",
                  "fonts.gstatic.com", "w3.org", "schema.org"]


def get_styles(html):
    return re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)


def strip_comments(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)


def media_ranges(s):
    ranges = []
    for m in re.finditer(r'@media[^{]*\{', s):
        start = m.end() - 1; depth = 0; i = start
        while i < len(s):
            if s[i] == '{': depth += 1
            elif s[i] == '}':
                depth -= 1
                if depth == 0:
                    ranges.append((m.start(), i)); break
            i += 1
    return ranges


# ───────────────────────── HARD CHECKS ─────────────────────────

def check_brace_balance(files):
    """Unbalanced { } inside any <style> block — the orphaned/unclosed @media bug."""
    out = []
    for path, html in files.items():
        for i, s in enumerate(get_styles(html)):
            sc = strip_comments(s)
            ob, cb = sc.count('{'), sc.count('}')
            if ob != cb:
                out.append(f"{path}: <style#{i}> brace imbalance open={ob} close={cb} (diff {ob-cb})")
    return out


def check_leaked_grid(files):
    """Layout-critical grid/nav collapse to 1fr sitting OUTSIDE any @media."""
    out = []
    crit = re.compile(r'\.(cs-grid|cs-grid-3|cs-nav|cs-slides|cs-covers|cs-testimonials)\b'
                      r'[^{}]*\{[^}]*grid-template-columns\s*:\s*1fr\b(?!\s+1fr)')
    for path, html in files.items():
        for s in get_styles(html):
            sc = strip_comments(s)
            ranges = media_ranges(sc)
            for m in crit.finditer(sc):
                if not any(a <= m.start() <= b for a, b in ranges):
                    out.append(f"{path}: '{m.group(0)[:50]}...' leaks to desktop (outside @media)")
    return out


def check_dead_internal_links(files):
    """href to a local .html page that does not exist in the repo.

    The set of valid targets is ALWAYS the full repo, not just the files being
    checked — otherwise single-file mode reports every cross-page link as dead.
    """
    existing = set()
    for path in glob.glob('**/*.html', recursive=True):
        rel = path.lstrip('./')
        existing.add('/' + rel); existing.add(rel)
    out = []
    for path, html in files.items():
        for m in re.finditer(r'href=["\']([^"\'#?]+\.html)(?:[#?][^"\']*)?["\']', html):
            link = m.group(1)
            if link.startswith('http'):
                continue
            norm = link.lstrip('./')
            if not ({'/' + norm, norm} & existing):
                out.append(f"{path}: dead internal link -> {link}")
    return out


def check_new_hotlinks(files):
    """Asset src/poster pointing at a known external host = unlocalized hotlink."""
    out = []
    pat = re.compile(r'(?:src|poster|data-src)\s*=\s*["\'](https?://[^"\']+)["\']')
    for path, html in files.items():
        for m in pat.finditer(html):
            url = m.group(1)
            if any(a in url for a in ALLOW_EXTERNAL):
                continue
            if any(h in url for h in HOTLINK_HOSTS):
                out.append(f"{path}: hotlinked asset -> {url[:80]}")
    return out


def check_duplicate_ids(files):
    """Duplicate id="" within a single page — breaks anchors / JS lookups."""
    out = []
    for path, html in files.items():
        ids = re.findall(r'\bid=["\']([^"\']+)["\']', html)
        seen = defaultdict(int)
        for i in ids:
            seen[i] += 1
        for i, c in seen.items():
            if c > 1:
                out.append(f"{path}: duplicate id='{i}' x{c}")
    return out


def check_http_refs(files):
    """http:// (non-https) src/href — mixed-content risk or hygiene."""
    out = []
    for path, html in files.items():
        for m in re.finditer(r'(?:src|href)\s*=\s*["\'](http://[^"\']+)["\']', html):
            if any(x in m.group(1) for x in ['w3.org', 'schema.org']):
                continue
            out.append(f"{path}: http:// ref -> {m.group(1)[:70]}")
    return out


# ───────────────────────── WARN CHECKS ─────────────────────────

def warn_missing_og(files):
    """Pages without Open Graph tags (deferred to projects.json refactor)."""
    out = []
    for path, html in files.items():
        head = re.search(r'<head\b.*?</head>', html, re.DOTALL)
        head = head.group(0) if head else html
        if not re.search(r'property=["\']og:', head):
            out.append(path)
    return [f"{len(out)} pages missing OG tags (deferred → generate from projects.json)"] if out else []


def warn_missing_canonical(files):
    out = []
    for path, html in files.items():
        head = re.search(r'<head\b.*?</head>', html, re.DOTALL)
        head = head.group(0) if head else html
        if not re.search(r'rel=["\']canonical["\']', head):
            out.append(path)
    return [f"{len(out)} pages missing canonical (deferred → generate from projects.json)"] if out else []


def warn_eager_videos(files):
    """Videos loading eagerly with no lazy/metadata — perf, biggest on mobile."""
    pages = {}
    for path, html in files.items():
        eager = 0
        for v in re.findall(r'<video\b[^>]*>.*?</video>', html, re.DOTALL):
            if 'data-lazy' in v or 'data-src' in v or 'preload="metadata"' in v:
                continue
            eager += 1
        if eager:
            pages[path] = eager
    if not pages:
        return []
    total = sum(pages.values())
    top = sorted(pages.items(), key=lambda x: -x[1])[:5]
    detail = ', '.join(f"{os.path.basename(p)}({c})" for p, c in top)
    return [f"{total} eager videos across {len(pages)} pages (run lazyload rollout). Top: {detail}"]


def warn_missing_alt(files):
    """<img> without alt — SEO + a11y on a visual portfolio."""
    n = 0
    for path, html in files.items():
        for m in re.finditer(r'<img\b[^>]*>', html):
            if not re.search(r'\balt=', m.group(0)):
                n += 1
    return [f"{n} <img> without alt text (SEO + accessibility)"] if n else []


def warn_missing_viewport(files):
    out = [p for p, h in files.items()
           if not re.search(r'name=["\']viewport["\']', h)]
    return [f"missing viewport meta: {', '.join(out)}"] if out else []


HARD_CHECKS = [
    ("brace balance (style blocks)", check_brace_balance),
    ("leaked grid/nav overrides",     check_leaked_grid),
    ("dead internal links",           check_dead_internal_links),
    ("new hotlinks",                  check_new_hotlinks),
    ("duplicate ids",                 check_duplicate_ids),
    ("http:// refs",                  check_http_refs),
]
WARN_CHECKS = [
    ("missing OG tags",        warn_missing_og),
    ("missing canonical",      warn_missing_canonical),
    ("eager videos",           warn_eager_videos),
    ("missing alt text",       warn_missing_alt),
    ("missing viewport",       warn_missing_viewport),
]


def load(paths):
    files = {}
    for p in paths:
        rel = p[len(os.getcwd()) + 1:] if p.startswith(os.getcwd()) else p
        rel = rel.lstrip('./')
        files[rel] = open(p, encoding='utf-8', errors='replace').read()
    return files


def main():
    args = sys.argv[1:]
    if args:
        paths = [a for a in args if a.endswith('.html')]
    else:
        paths = glob.glob('**/*.html', recursive=True)
    files = load(paths)
    print(f"debug-check: scanning {len(files)} HTML files\n")

    hard_fail = 0
    for name, fn in HARD_CHECKS:
        res = fn(files)
        if res:
            hard_fail += len(res)
            print(f"FAIL  {name}  ({len(res)})")
            for r in res:
                print(f"        {r}")
        else:
            print(f"ok    {name}")

    print()
    for name, fn in WARN_CHECKS:
        res = fn(files)
        for r in res:
            print(f"warn  {name}: {r}")

    print()
    if hard_fail:
        print(f"RESULT: {hard_fail} hard failure(s) — DO NOT push until fixed. (exit 1)")
        sys.exit(1)
    print("RESULT: no hard failures — safe to push. (exit 0)")
    sys.exit(0)


if __name__ == '__main__':
    main()
