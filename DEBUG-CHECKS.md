# Debug checks

Two scripts. One is a fast gate you run before every push; the other is a slow
network sweep you run occasionally. They are kept separate on purpose — mixing
them makes the fast one slow, and you stop running it.

## `debug-check.py` — run before EVERY push

Static. No network. Under a second. This is the gate.

```
python3 debug-check.py            # whole repo
python3 debug-check.py x.html     # just named files
```

Exit `0` = safe to push. Exit `1` = a hard failure regressed; fix before pushing.

**Hard failures (block the push):**
- brace imbalance in any `<style>` block — the orphaned/unclosed `@media` bug
- grid/nav `1fr` overrides leaking outside `@media` (desktop layout collapse)
- dead internal `.html` links
- new hotlinks (asset `src`/`poster`/`data-src` pointing at an external host)
- duplicate `id=""` on a page
- `http://` (non-https) refs

**Warnings (printed, do NOT block):**
- missing OG / canonical — deferred on purpose; generate from `projects.json`
- eager videos — the lazyload rollout backlog
- missing `alt` text
- missing viewport meta

Warnings are known backlog. If they failed the gate you'd start ignoring the
gate, so they only inform.

## `debug-crawl.py` — run occasionally

Network. Slow, sometimes flaky. NOT a pre-push gate. Fetches every asset the
pages reference and reports anything not returning 200 — including 0-byte files
that return 200 but are empty (the broken-upload class).

```
python3 debug-crawl.py                  # local /assets/ refs vs frederikfrede.com
python3 debug-crawl.py --external       # also check external/hotlinked URLs
python3 debug-crawl.py --base http://localhost:8000   # against a local server
```

Run it locally for a full sweep — the bash sandbox can only reach allowlisted
hosts, so external results there are incomplete.

## Adding a new check

When a new bug class turns up, add a checker function in `debug-check.py` and
register it in `HARD_CHECKS` (blocks) or `WARN_CHECKS` (informs). Keep it
**static** — if it needs the network or to decode a video, it belongs in
`debug-crawl.py` instead. Hotlink hosts live in `HOTLINK_HOSTS` at the top of
`debug-check.py`; add hosts there as they appear.

Rule of thumb: a check is a HARD failure only if it means something is *broken
right now*. Anything that's "should eventually" is a warning.
