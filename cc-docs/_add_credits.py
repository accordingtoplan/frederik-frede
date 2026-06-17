#!/usr/bin/env python3
"""Bucket A: insert a complete .cs-bottom credits block before .cs-nav on the
13 case pages that have no body credits block. Year from each page's cs-tags
(verified), Live site only where a real URL was confirmed reachable+genuine,
Collaborators '—' (these are pre-MoreSleep solo archive works; honest
placeholder per the prompt). Description reuses the page's own cs-desc copy.
Idempotent: skips a page that already has .cs-bottom.
"""
import re, sys

# page -> (year, live_url_or_None, display_domain_or_None)
DATA = {
 "anja-wiroth": ("2005", None, None),
 "carhartt": ("2005", None, None),
 "grimetime-berlin": ("2004", None, None),
 "hardedged-recordings": ("2003", None, None),
 "ingo-robin": ("2006", None, None),
 # mini-the-sooner-now handled separately (page truncated: needs full tail restore)
 "neubau-welt": ("2006", None, None),
 "prg-ingenieure": ("2005", None, None),
 "rooms-hotels": ("2017", "https://roomshotels.com", "roomshotels.com"),
 "seppuku-industries": ("2004", None, None),
 "sisi-wasabi": ("2005", None, None),
 "smithgroup-shanghai": ("2006", None, None),
 "watergate-club": ("2004", None, None),
}

write = "--write" in sys.argv
for slug, (year, url, dom) in DATA.items():
    fn = slug + ".html"
    h = open(fn, encoding="utf-8").read()
    if 'class="cs-bottom"' in h:
        print(f"SKIP {fn} (already has cs-bottom)"); continue
    dm = re.search(r'<p class="cs-desc">(.*?)</p>', h, re.S)
    desc = dm.group(1).strip() if dm else ""
    rows = ""
    if url:
        rows += f'      <div class="cs-credit-group"><dt>Live site</dt><dd><a href="{url}" target="_blank" rel="noopener">{dom} ↗</a></dd></div>\n'
    rows += '      <div class="cs-credit-group"><dt>Collaborators</dt><dd>—</dd></div>\n'
    rows += f'      <div class="cs-credit-group"><dt>Year</dt><dd>{year}</dd></div>\n'
    block = (
        '  <div class="cs-bottom">\n'
        f'    <div class="cs-description"><p>{desc}</p></div>\n'
        '    <dl class="cs-credits-cols">\n'
        f'{rows}'
        '    </dl>\n'
        '  </div>\n\n'
    )
    # insert immediately before the cs-nav div (preserve its indentation)
    m = re.search(r'\n(\s*)<div class="cs-nav">', h)
    if not m:
        print(f"!! {fn}: no .cs-nav found — SKIP"); continue
    insert_at = m.start() + 1  # after the newline
    new = h[:insert_at] + block + h[insert_at:]
    print(f"--- {fn}: Year={year} Live={dom or '—'} ---")
    if not write:
        print(block.rstrip())
    else:
        open(fn, "w", encoding="utf-8").write(new)
print("MODE:", "WRITE" if write else "dry-run")
