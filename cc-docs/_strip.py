#!/usr/bin/env python3
"""Strip migrated canonical cs-* rules from each case page's inline <style>.

Rule kept iff it is NOT covered by the canonical block in cc-docs/_canonical.css:
  - top-level rule: dropped only on EXACT (selector, body) match to canonical
    (so genuine per-page variants stay inline and override via source order).
  - mobile rule: dropped on exact canonical match OR if it is one of the known
    24px-second-block drift bodies (the residue we are collapsing). Genuine
    page-specific mobile overrides (concierge 2-col grid, bianca cs-grid-wide
    4/3, spot cs-media-full 24px, the cs-slides !important group, classpass
    cs-figrid*) do not match either set and are preserved.

Pass --write to apply; default is dry-run (prints per-page kept/dropped counts).
"""
import re, glob, sys

EX = {"index.html","work.html","about.html","imprint.html","404.html",
      "republish.html","case-template.html"}

# ---- shared normalization (must match cc-docs/_inventory.py) ----
def norm_body(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    out = []
    for d in (x.strip() for x in s.split(";") if x.strip()):
        if ":" in d:
            p, v = d.split(":", 1)
            v = re.sub(r"\s*,\s*", ",", v.strip()); v = re.sub(r"\s+", " ", v)
            out.append(f"{p.strip().lower()}:{v}")
        else:
            out.append(d.strip())
    return ";".join(sorted(out))

def norm_sel(sel):
    parts = [re.sub(r"\s+", " ", x.strip()) for x in sel.split(",") if x.strip()]
    return ",".join(sorted(parts)), parts

# ---- generic CSS splitter preserving raw text ----
def split_rules(css):
    """Yield dicts: {'kind':'rule', sel, body, raw} or
       {'kind':'media', prelude, inner:[rule...], raw}."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)  # drop comments first
    items, i, n = [], 0, len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1:
            tail = css[i:].strip()
            break
        prelude = css[i:brace]
        pstrip = prelude.strip()
        depth, j = 1, brace + 1
        while j < n and depth > 0:
            if css[j] == "{": depth += 1
            elif css[j] == "}": depth -= 1
            j += 1
        raw = css[i:j]
        if pstrip.startswith("@media"):
            inner_css = css[brace+1:j-1]
            inner = []
            k, m = 0, len(inner_css)
            while k < m:
                b2 = inner_css.find("{", k)
                if b2 == -1: break
                sel2 = inner_css[k:b2]
                d2, l = 1, b2+1
                while l < m and d2 > 0:
                    if inner_css[l] == "{": d2 += 1
                    elif inner_css[l] == "}": d2 -= 1
                    l += 1
                inner.append({"sel": sel2.strip(), "body": inner_css[b2+1:l-1],
                              "raw": inner_css[k:l].strip()})
                k = l
            items.append({"kind":"media","prelude":pstrip,"inner":inner})
        else:
            items.append({"kind":"rule","sel":pstrip,
                          "body":css[brace+1:j-1],"raw":raw.strip()})
        i = j
    return items

# ---- build canonical covered sets ----
canon = open("cc-docs/_canonical.css").read()
COV_TOP, COV_MOB = {}, {}   # sel -> set(norm_body)
for it in split_rules(canon):
    if it["kind"] == "rule":
        nb = norm_body(it["body"]); _, parts = norm_sel(it["sel"])
        full,_ = norm_sel(it["sel"])
        for key in [full] + parts:
            COV_TOP.setdefault(key, set()).add(nb)
    else:
        for r in it["inner"]:
            nb = norm_body(r["body"]); full, parts = norm_sel(r["sel"])
            for key in [full] + parts:
                COV_MOB.setdefault(key, set()).add(nb)

# explicit 24px second-block drift bodies to also drop (collapse to canonical)
DRIFT_MOB = {
    ".cs-header":   {"padding:48px 24px 40px"},
    ".cs-intro":    {"padding:0 24px 48px"},
    ".cs-strategy": {"padding:48px 24px"},
    ".cs-pullquote":{"padding:48px 24px"},
    ".cs-bottom":   {"padding:48px 24px"},
    ".cs-caption":  {"flex-direction:column;gap:6px;padding:16px 24px 48px"},
    ".cs-grid":     {"grid-template-columns:1fr;padding:0 24px", "grid-template-columns:1fr"},
    ".cs-grid-3":   {"grid-template-columns:1fr 1fr;padding:0 24px", "grid-template-columns:1fr 1fr"},
    ".cs-nav-item": {"padding:32px 24px"},
    ".cs-nav-item.next": {"text-align:left"},
}

def covered_top(sel, body):
    full, parts = norm_sel(sel); nb = norm_body(body)
    keys = [full] + parts
    return any(nb in COV_TOP.get(k, set()) for k in keys)

def covered_mob(sel, body):
    full, parts = norm_sel(sel); nb = norm_body(body)
    keys = [full] + parts
    if any(nb in COV_MOB.get(k, set()) for k in keys): return True
    if any(nb in DRIFT_MOB.get(k, set()) for k in keys): return True
    return False

# ---- leak neutralization ----------------------------------------------------
# A page rule kept inline now coexists with canonical's rule for the same
# selector (canonical loads first, in style.css). If the kept rule is PARTIAL
# (omits a property canonical sets), canonical's value LEAKS in — which never
# happened pre-migration (there was no global cs-* rule). To replicate the old
# behaviour exactly, append explicit resets for every canonical property the
# kept rule omits. Pre-migration value with the global `*{margin:0;padding:0}`
# reset in place == CSS initial for non-inherited props, == inherited for
# inherited props.
def _cprops(body):
    d = {}
    for x in body.split(";"):
        x = x.strip()
        if ":" in x:
            k, v = x.split(":", 1)
            d[k.strip().lower()] = re.sub(r"\s+", " ", v.strip())
    return d
CPROP_TOP, CPROP_MOB = {}, {}
for _it in split_rules(open("cc-docs/_canonical.css").read()):
    if _it["kind"] == "rule":
        _f, _p = norm_sel(_it["sel"])
        for _k in [_f] + _p: CPROP_TOP.setdefault(_k, {}).update(_cprops(_it["body"]))
    else:
        for _r in _it["inner"]:
            _f, _p = norm_sel(_r["sel"])
            for _k in [_f] + _p: CPROP_MOB.setdefault(_k, {}).update(_cprops(_r["body"]))

INHERITED = {"color","letter-spacing","font-weight","line-height","font-size",
             "text-align","text-transform","font-family","font-style","white-space"}
RESET = {  # explicit pre-migration (post global reset) values for non-inherited props
    "object-fit":"fill","aspect-ratio":"auto","position":"static","right":"auto",
    "top":"auto","left":"auto","bottom":"auto","margin":"0","margin-top":"0",
    "margin-bottom":"0","margin-left":"0","margin-right":"0","padding":"0",
    "padding-top":"0","padding-bottom":"0","padding-left":"0","padding-right":"0",
    "border-top":"0","border":"0","gap":"normal","row-gap":"normal",
    "column-gap":"normal","align-items":"normal","align-content":"normal",
    "justify-content":"normal","transition":"none","transform":"none",
    "overflow":"visible","background":"transparent","grid-column":"auto",
    "max-width":"none","opacity":"1",
}
# props where blindly resetting could itself break layout — skip + warn instead
SKIP = {"display","flex-direction","grid-template-columns","grid-template-rows"}
WARN = []

def neutralize(raw, ctx, page):
    mm = re.match(r"\s*([^{]+)\{(.*)\}\s*$", raw, re.S)
    if not mm: return raw
    sel, body = mm.group(1).strip(), mm.group(2)
    have = set(_cprops(body))
    full, parts = norm_sel(sel)
    table = CPROP_TOP if ctx == "top" else CPROP_MOB
    canon = {}
    for k in [full] + parts:
        if k in table: canon.update(table[k])
    add = []
    for prop in sorted(set(canon) - have):
        if prop in SKIP:
            WARN.append(f"{page} [{ctx}] {sel} omits SKIP-prop '{prop}' (verify)")
            continue
        if prop in INHERITED:
            add.append(f"{prop}:inherit")
        elif prop in RESET:
            add.append(f"{prop}:{RESET[prop]}")
        else:
            add.append(f"{prop}:initial")
    if not add: return raw
    body2 = body.rstrip()
    if not body2.rstrip().endswith(";") and body2.strip(): body2 += ";"
    body2 += "/*keep*/" + ";".join(add)
    return f"{sel}{{{body2}}}"

write = "--write" in sys.argv
pages = [f for f in sorted(glob.glob("*.html")) if f not in EX]
report = []
for p in pages:
    html = open(p, encoding="utf-8").read()
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    if not m:
        continue
    css = m.group(1)
    items = split_rules(css)
    # Pass 1: which base selectors does this page KEEP at top level?
    # If a page keeps a top-level override of S, its mobile rule for S must
    # also stay inline — otherwise the canonical mobile rule (now earlier in
    # source order, in style.css) loses to the page's inline top-level rule
    # at mobile widths (cascade-order regression).
    kept_top_sels = set()
    for it in items:
        if it["kind"] == "rule" and not covered_top(it["sel"], it["body"]):
            _, parts = norm_sel(it["sel"])
            kept_top_sels.update(parts)
    kept_top, kept_mob, dropped = [], [], 0
    for it in items:
        if it["kind"] == "rule":
            if covered_top(it["sel"], it["body"]):
                dropped += 1
            else:
                kept_top.append(neutralize(it["raw"], "top", p))
        else:  # media (only max-width:640px exists)
            for r in it["inner"]:
                _, mparts = norm_sel(r["sel"])
                if any(pp in kept_top_sels for pp in mparts):
                    kept_mob.append(r["raw"])      # preserve intra-page order
                elif covered_mob(r["sel"], r["body"]):
                    dropped += 1
                else:
                    kept_mob.append(r["raw"])
    # rebuild
    blocks = []
    if kept_top:
        blocks.append("\n".join("  " + x for x in kept_top))
    if kept_mob:
        inner = "\n".join("    " + x for x in kept_mob)
        blocks.append("  @media (max-width: 640px) {\n" + inner + "\n  }")
    if blocks:
        new_style = "<style>\n" + "\n\n".join(blocks) + "\n</style>"
    else:
        new_style = ""   # nothing page-specific left
    report.append((p, len(kept_top), len(kept_mob), dropped))
    if write:
        new_html = html[:m.start()] + new_style + html[m.end():]
        # if we removed the whole style block, also drop a now-blank line
        open(p, "w", encoding="utf-8").write(new_html)

print(f"{'page':52} keptTop keptMob dropped")
tot=[0,0,0]
for p,kt,km,d in report:
    tot[0]+=kt; tot[1]+=km; tot[2]+=d
    flag = "" if (kt or km) else "  <empty>"
    print(f"{p:52} {kt:6d} {km:6d} {d:6d}{flag}")
print(f"{'TOTAL':52} {tot[0]:6d} {tot[1]:6d} {tot[2]:6d}")
print(f"\npages fully emptied: {sum(1 for _,kt,km,_ in report if not kt and not km)}")
if WARN:
    print("\n=== SKIP-prop warnings (verify these omissions are inert) ===")
    for w in WARN: print("  " + w)
print("MODE:", "WRITE" if write else "dry-run")
