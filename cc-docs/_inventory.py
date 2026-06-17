#!/usr/bin/env python3
"""Inventory inline <style> cs-* rules across case-study pages.
Builds selector -> {normalized declaration body -> [pages]} so we can see
which rules are universal, which are variants, which are page-unique.
"""
import os, re, glob, json, collections

EXCLUDE = {"index.html","work.html","about.html","imprint.html","404.html",
           "republish.html","case-template.html"}

def extract_style(html):
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    return m.group(1) if m else None

def norm(s):
    # collapse whitespace, normalize for comparison
    s = re.sub(r"\s+", " ", s).strip()
    return s

def norm_body(s):
    """Canonicalize a declaration body so formatting (minified vs spaced)
    does not register as a real variant. Sorts declarations so order noise
    is ignored too."""
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    decls = [d.strip() for d in s.split(";") if d.strip()]
    out = []
    for d in decls:
        if ":" in d:
            prop, val = d.split(":", 1)
            prop = prop.strip().lower()
            val = re.sub(r"\s*,\s*", ",", val.strip())
            val = re.sub(r"\s+", " ", val)
            out.append(f"{prop}:{val}")
        else:
            out.append(d.strip())
    return ";".join(sorted(out))

def parse_rules(css):
    """Yield (context, selector, body) where context is '' or a @media prelude.
    Handles one level of @media nesting (sufficient for these files)."""
    rules = []
    i, n = 0, len(css)
    # strip comments
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    n = len(css)
    i = 0
    while i < n:
        # find next '{' or '@'
        # capture prelude up to '{'
        brace = css.find("{", i)
        if brace == -1:
            break
        prelude = css[i:brace].strip()
        if prelude.startswith("@media") or prelude.startswith("@supports"):
            # find matching close for this at-rule block
            depth = 1
            j = brace + 1
            while j < n and depth > 0:
                if css[j] == "{": depth += 1
                elif css[j] == "}": depth -= 1
                j += 1
            inner = css[brace+1:j-1]
            # parse inner rules with this context
            for sel, body in parse_flat(inner):
                rules.append((norm(prelude), sel, body))
            i = j
        else:
            # flat rule: find its closing brace
            depth = 1
            j = brace + 1
            while j < n and depth > 0:
                if css[j] == "{": depth += 1
                elif css[j] == "}": depth -= 1
                j += 1
            body = css[brace+1:j-1]
            rules.append(("", norm(prelude), norm(body)))
            i = j
    return rules

def parse_flat(css):
    out = []
    i, n = 0, len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1: break
        sel = css[i:brace].strip()
        depth = 1; j = brace+1
        while j < n and depth > 0:
            if css[j] == "{": depth += 1
            elif css[j] == "}": depth -= 1
            j += 1
        body = css[brace+1:j-1]
        out.append((norm(sel), norm(body)))
        i = j
    return out

pages = sorted(f for f in glob.glob("*.html") if f not in EXCLUDE)
no_style = []
brace_imbalance = []
media_counts = {}
# key = (context, selector) -> {body: [pages]}
table = collections.defaultdict(lambda: collections.defaultdict(list))

for p in pages:
    html = open(p, encoding="utf-8").read()
    css = extract_style(html)
    if css is None:
        no_style.append(p)
        continue
    if css.count("{") != css.count("}"):
        brace_imbalance.append((p, css.count("{"), css.count("}")))
    media_counts[p] = len(re.findall(r"@media\s*\(\s*max-width:\s*640px\s*\)", css))
    for ctx, sel, body in parse_rules(css):
        parts = [re.sub(r"\s+", " ", x.strip()) for x in sel.split(",") if x.strip()]
        nsel = ",".join(sorted(parts))
        nctx = re.sub(r"\s+", "", ctx)
        table[(nctx, nsel)][norm_body(body)].append(p)

print("CASE PAGES:", len(pages))
print("NO <style> BLOCK:", no_style)
print("BRACE IMBALANCE:", brace_imbalance)
dup_media = {p:c for p,c in media_counts.items() if c > 1}
print("PAGES WITH >1 @media(max-width:640px):", len(dup_media))
print(json.dumps(dup_media, indent=0))

# classify
universal, variant, unique = [], [], []
N = len(pages)
for (ctx, sel), bodies in table.items():
    total_pages = len(set(pg for pgs in bodies.values() for pg in pgs))
    if len(bodies) == 1:
        if total_pages == 1:
            unique.append((ctx, sel, total_pages))
        else:
            universal.append((ctx, sel, total_pages, list(bodies)[0]))
    else:
        variant.append((ctx, sel, {norm(b): sorted(set(pgs)) for b,pgs in bodies.items()}))

print("\n=== SELECTOR SUMMARY ===")
print("universal (1 body, >1 page):", len(universal))
print("variant   (>1 distinct body):", len(variant))
print("page-unique (1 body, 1 page):", len(unique))

# dump full data
out = {
  "pages": pages,
  "no_style": no_style,
  "brace_imbalance": brace_imbalance,
  "dup_media_640": dup_media,
  "variant": [{"ctx":c,"sel":s,"bodies":{k:v for k,v in b.items()}} for c,s,b in variant],
  "unique": [{"ctx":c,"sel":s} for c,s,_ in unique],
  "universal": [{"ctx":c,"sel":s,"pages":n,"body":bd} for c,s,n,bd in universal],
}
json.dump(out, open("cc-docs/_inventory.json","w"), indent=2)
print("\nwrote cc-docs/_inventory.json")
