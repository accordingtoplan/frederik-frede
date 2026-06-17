#!/usr/bin/env python3
"""Audit the body credits block (<dl class="cs-credits-cols">) on each case page.
Classifies: missing-body-block / standard / non-standard / empty-collaborators.
"""
import re, glob, json
EX = {"index.html","work.html","about.html","imprint.html","404.html",
      "republish.html","case-template.html"}
CANON_CORE = {"live site","collaborators","year"}
CANON_OPT  = {"press","typeface","typefaces","scope"}

def fields(html):
    m = re.search(r'<dl class="cs-credits-cols">(.*?)</dl>', html, re.S)
    if not m: return None
    pairs = re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", m.group(1), re.S)
    out = []
    for dt, dd in pairs:
        label = re.sub(r"<[^>]+>", "", dt).strip()
        val = re.sub(r"<[^>]+>", " ", dd)
        val = re.sub(r"\s+", " ", val).strip()
        out.append((label, val))
    return out

rows = {"missing":[], "standard":[], "nonstandard":[], "empty_collab":[]}
detail = {}
for p in sorted(glob.glob("*.html")):
    if p in EX: continue
    h = open(p, encoding="utf-8").read()
    has_bottom = "cs-bottom" in h
    f = fields(h)
    if f is None:
        rows["missing"].append(p); detail[p] = {"has_bottom":has_bottom, "fields":None}
        continue
    labels = [l.lower() for l,_ in f]
    detail[p] = {"fields": f, "labels": labels}
    # order check: year last?
    year_last = (labels[-1] == "year") if labels else False
    noncanon = [l for l in labels if l not in CANON_CORE and l not in CANON_OPT]
    collab = next((v for l,v in f if l.lower()=="collaborators"), None)
    if noncanon or not year_last:
        rows["nonstandard"].append(p)
    elif collab is not None and collab.strip() in ("—","-","–",""):
        rows["empty_collab"].append(p)
    else:
        rows["standard"].append(p)

print("=== CREDITS AUDIT (current tree) ===")
for k in ["missing","nonstandard","empty_collab","standard"]:
    print(f"\n## {k}: {len(rows[k])}")
    for p in rows[k]:
        f = detail[p]["fields"]
        if f is None:
            print(f"  {p}  (has .cs-bottom: {detail[p]['has_bottom']})")
        else:
            print(f"  {p}  ::  " + " | ".join(f"{l}={v[:40]}" for l,v in f))
json.dump({k:rows[k] for k in rows}, open("cc-docs/_credits_audit.json","w"), indent=2)
print("\ntotals:", {k:len(v) for k,v in rows.items()})
