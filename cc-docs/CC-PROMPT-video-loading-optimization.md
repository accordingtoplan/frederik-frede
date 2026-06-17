# CC PROMPT — Global video loading optimization (roll out the Architonic pattern site-wide)

Paste everything below into a Claude Code session opened at the repo root
(`accordingtoplan/frederik-frede`, local clone, full network access).

---

## Context

We fixed slow page loads + missing poster images on the Architonic case study
(`architonic-brand-strategy-platform-design.html`) and want the same fix on every
other case study. The root cause on AT: all videos used plain `<source src>` with
default `preload="auto"`, so the browser pulled every MP4 on page open (one was
88MB), and most videos had no `poster`, so you got long blank holds instead of a
still while loading.

The fix has three parts, two of which are ALREADY DONE and live:

1. **DONE & live — `footer.js`** has a global `initVideoLazy()` IntersectionObserver.
   It finds any `<video data-lazy>`, and when it comes within 600px of the viewport,
   swaps each child `<source data-src="…">` to `src` and calls `.load()` (then
   `.play()` for autoplay videos, ignoring the promise rejection). Videos using a
   plain `src` keep working untouched, so half-converted state never breaks a page.
   **Do not modify footer.js** — just rely on it.

2. **DONE — Architonic page** is fully converted and is the reference for the pattern.
   Read it first to see the target shape:
   `architonic-brand-strategy-platform-design.html`

3. **YOUR JOB — convert the other 88 HTML pages** to the same pattern and generate
   the posters they need.

## The exact pattern (per content `<video>`)

- **First video on the page = the case hero.** Keep it EAGER: `preload="auto"` +
  `fetchpriority="high"`, keep its plain `src`, do NOT add `data-lazy`. It's above
  the fold and should load immediately. (If it already has `fetchpriority="high"`
  or `class="hero-video"`, leave it as-is.)
- **Every other `<video>`:**
  - add `data-lazy` to the `<video>` tag
  - set `preload="metadata"` (replace an existing `preload`, or add it)
  - change `<source src="X">` to `<source data-src="X">`
  - add `poster="<video-basename>-poster.jpg"` IF a matching poster exists in the
    video's asset folder and the video has no poster yet. Poster naming convention:
    `assets/foo/bar.mp4` → `assets/foo/bar-poster.jpg` (same folder, `-poster.jpg`).
- Idempotent: re-running must not double-convert. Already-converted videos and
  eager/hero videos are skipped.

## Use the prepared script

A transform script is already written and proven on AT. It walks every `.html`,
applies the pattern above, and writes `poster-manifest.txt` listing every lazy
video still missing a poster — each line is a ready-to-run ffmpeg command that grabs
a frame ~1s in (avoids black intro frames) and caps width at 1600px.

If `lazyload-videos.py` is in the repo, use it. If not, recreate it from the spec
above (it's a regex pass over `<video>…</video>` blocks; ask me and I'll paste it).

## Rollout steps

```bash
# 1. First pass — lazify everything, emit the poster manifest
python3 lazyload-videos.py
#    Sanity-check the printed counts: files / converted / skipped_eager / posters_added

# 2. Generate the missing posters (commands pre-written in the manifest)
bash poster-manifest.txt

# 3. Second pass — wire the freshly generated posters into the HTML
python3 lazyload-videos.py

# 4. Spot-check 3–4 pages in a browser (or headless): hero loads immediately,
#    other videos show a poster and only fetch when scrolled near.

# 5. Commit + push
git add -A && git commit -m "Site-wide: lazy-load case-study videos + first-frame posters"
git push
```

## Important rules / gotchas

- **Hotlinked/external (`http…`) video sources:** the transform should still lazify
  them, but DON'T try to ffmpeg-generate a poster from a remote file. Localize those
  videos first (standing CC asset-localization method), then re-run.
- **Per-page first-video check:** the eager-hero logic assumes the first `<video>` in
  document order is the intended hero. After the pass, eyeball a few pages where the
  first video might NOT be the hero (e.g. a page that opens with a logo loop) and
  fix any mis-tagged eager video by hand.
- **Big files worth a re-encode while you're in here:** e.g. Architonic's
  `architonic-summary-subs.mp4` is 88MB. Lazy-load means it no longer blocks page
  open, but a re-encode (H.264, reasonable bitrate, cap ~1080p) helps anyone who
  scrolls to it. Do an `ls -laS assets/**/*.mp4` and flag anything over ~20MB.
- **Don't touch `footer.js`** — the observer is already correct and live.
- **Leave `index.html` (homepage) alone.** It already has its own page-local lazy
  system: a separate `IntersectionObserver` (`lazyMediaObserver`) that swaps
  `data-src`→`src` for `video.lazy-video` / `iframe.lazy-vimeo` per `.case`, all
  case videos already use `preload="none"` + `data-src`, the hero is already eager
  (`fetchpriority="high"`), and every video case already has a poster. The transform
  keys on plain `<source src>`, of which the homepage has none, so it won't be
  modified anyway — but don't try to "unify" the two lazy mechanisms or migrate the
  homepage to `data-lazy`. Two independent observers is intentional and fine.
- **Get a fresh SHA immediately before any write** if you push via the GitHub API
  rather than git (multi-thread sessions can cause silent SHA overwrites). With a
  plain `git push` from a clean clone this isn't a concern.

## Definition of done

- Every case-study page: first video eager with a poster; all other videos
  `data-lazy` + `preload="metadata"` + a working `poster`.
- `poster-manifest.txt` empty (or only external/hotlinked videos remain, noted).
- A few pages verified live: posters show instantly, videos load on scroll, no
  layout shift.
- Committed and pushed.
- Update memory + the Notion portfolio context page with what shipped.
