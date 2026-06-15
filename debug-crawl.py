#!/usr/bin/env python3
"""
debug-crawl.py — on-demand network checks for frederik-frede.

SEPARATE from debug-check.py on purpose. This one hits the network: it fetches
every asset the pages reference and reports anything that doesn't return 200.
Slow and occasionally flaky (a CDN hiccup looks like a failure), so run it
occasionally — NOT as a pre-push gate.

  python3 debug-crawl.py                     # check all local /assets/ refs
  python3 debug-crawl.py --base URL          # resolve root-relative paths against URL
                                             # (default: https://frederikfrede.com)
  python3 debug-crawl.py --external          # ALSO check external/hotlinked URLs

Catches the class of bug that static checks can't see: a reference that looks
fine in markup but fails on load — e.g. the 0-byte pferdt screen-rec, a renamed
asset whose old path is still referenced, a 404 image.

NOTE: the sandbox can only reach allowlisted hosts. Run locally (full network)
for a complete external sweep.
"""
import re, sys, glob, os, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

BASE = "https://frederikfrede.com"
CHECK_EXTERNAL = "--external" in sys.argv
if "--base" in sys.argv:
    BASE = sys.argv[sys.argv.index("--base") + 1]
BASE = BASE.rstrip('/')

ASSET_ATTR = re.compile(r'(?:src|poster|data-src|href)\s*=\s*["\']([^"\']+)["\']')
ASSET_EXT = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg',
             '.mp4', '.mov', '.webm', '.woff', '.woff2', '.css', '.js')


def collect_refs():
    refs = {}  # url -> set(source pages)
    for p in glob.glob('**/*.html', recursive=True):
        html = open(p, encoding='utf-8', errors='replace').read()
        for m in ASSET_ATTR.finditer(html):
            u = m.group(1)
            if u.startswith('#') or u.startswith('mailto:') or u.startswith('tel:'):
                continue
            is_ext = u.startswith('http')
            if is_ext and not CHECK_EXTERNAL:
                continue
            # only check things that look like assets, plus external if asked
            low = u.split('?')[0].lower()
            if not is_ext and not low.endswith(ASSET_EXT):
                continue
            full = u if is_ext else BASE + ('/' + u.lstrip('./').lstrip('/'))
            refs.setdefault(full, set()).add(p)
    return refs


def check(url):
    try:
        req = urllib.request.Request(url, method='HEAD',
                                     headers={'User-Agent': 'debug-crawl/1.0'})
        r = urllib.request.urlopen(req, timeout=15)
        code = r.getcode()
        clen = r.headers.get('Content-Length')
        # 0-byte files (the pferdt class) are functional failures even at 200
        if clen is not None and int(clen) == 0:
            return url, 'ZERO-BYTE (200 but empty)'
        return url, code
    except urllib.error.HTTPError as e:
        return url, e.code
    except Exception as e:
        # some hosts reject HEAD; retry GET once
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'debug-crawl/1.0'})
            r = urllib.request.urlopen(req, timeout=15)
            return url, r.getcode()
        except Exception as e2:
            return url, f'ERR {type(e2).__name__}'


def main():
    refs = collect_refs()
    print(f"debug-crawl: {len(refs)} unique asset URLs "
          f"({'incl. external' if CHECK_EXTERNAL else 'local only'}), base={BASE}\n")
    bad = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for url, status in ex.map(check, refs):
            if status != 200:
                bad.append((url, status))
    if not bad:
        print(f"All {len(refs)} assets OK.")
        sys.exit(0)
    print(f"{len(bad)} problem assets:\n")
    for url, status in sorted(bad, key=lambda x: str(x[1])):
        srcs = ', '.join(sorted(refs[url]))[:90]
        print(f"  [{status}] {url}")
        print(f"          referenced by: {srcs}")
    sys.exit(1)


if __name__ == '__main__':
    main()
