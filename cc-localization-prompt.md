# Claude Code Session Prompt — Full Hotlink Localization Sprint

## Context
Repo: `github.com/accordingtoplan/frederik-frede`, live at frederikfrede.com (GitHub Pages).
~70 HTML files, 47 case studies threaded in one prev/next loop via work.html order.
moresleep.net hotlinks are already fully eliminated. This sprint targets the REMAINING
external hotlinks: freundevonfreunden.com, cdn.prod.website-files.com (Webflow), plus
smaller ones (framerusercontent, vitra, shopify, squarespace, thonet, hay, cargo.site).

## Step 1 — Inventory (already done — use it directly)
A full crawl of all 70 HTML files was already run this session. Result:
**`full-hotlink-inventory.csv`** (141 rows: `old_url, source_files, new_path`), covering
every remaining external asset across freundevonfreunden.com, cdn.prod.website-files.com,
static.vitra.com, framerusercontent.com, cdn.shopify.com, images.squarespace-cdn.com,
thonet.de, hay.com, assets01.sdd1.ch — AND a previously-missed block of 16
moresleep.net assets on `mini-the-sooner-now-brand-campaign.html` (moresleep.net was
NOT fully eliminated as memory assumed; this page needs the same localization treatment).

Load this CSV as the authoritative source/target mapping. Two things to double check at
the start since they were auto-generated:
- A few `new_path` values for plain numbered Webflow assets (e.g. LAS-Work_13.2.webp →
  `...las-work-13-2.webp`) are mechanical; feel free to improve the `[description]` segment
  with something more meaningful if the surrounding alt text/context suggests a better name,
  but the client/project-type/extension are correct — don't need to re-derive those.
- Two `index.html` rows map to `assets/home/` (the homepage LAS preview clip + the NZZ
  frontpage image) — these duplicate assets already used on the LAS and NZZ case study
  pages respectively. Where a homepage asset is identical to a case-study asset, point
  BOTH references at the SAME single file (the case-study one) rather than creating a
  duplicate in `assets/home/`.

Cross-check `rename-map.md` (provided alongside this prompt) for the original
work.html-level mappings — those are consistent with this CSV's conventions.

## Step 2 — Download
For each unique URL:
- Fetch the asset.
- Note original dimensions/filesize before processing.

## Step 3 — Optimize
- **Images** (jpg/png/webp): resize so longest edge ≤ 2400px, re-encode at quality 82.
- **GIFs**: convert to muted looping H.264 mp4 (and webm if easy) — GIFs are large and
  these are used as autoplay/loop media anyway. Update the corresponding `type:"img"` or
  `type:"gif"` entries to `type:"video"` with `autoplay muted loop playsinline`.
- **Videos** (.mp4 already, or .mov): re-encode to H.264 mp4, target reasonable web bitrate
  (CRF ~23, 1080p max unless source is smaller). Generate a poster frame (first or a
  representative frame) as jpg if one doesn't exist, named `[same-base-name]-poster.jpg`.
- Skip re-processing if a file is already reasonably small/optimized — don't blow up a
  small svg/logo.

## Step 4 — Place & rename
Save everything under `assets/[client]/` using the SEO names from Step 1/rename-map.md.
Verify no filename collisions.

## Step 5 — Rewrite references
Do a careful find-and-replace across all affected HTML files: every old absolute URL →
new local path (`/assets/[client]/...`). Double-check:
- `src` AND `poster` attributes
- any inline data-arrays/JS objects with the same URLs repeated
- og:image / meta tags if any reference these URLs

## Step 6 — Specific known fixes
- `assets/pferdt/230807-FGP-Screen_Rec-SM.mp4` is currently 0 bytes in the repo — re-fetch
  this from its original source (check the Pferdt case study page for the original hotlink
  if still present, or moresleep.net backup if cached) and replace properly.
- LV (Louis Vuitton) case study: source looks complete on GitHub but Frederik only sees
  2 videos live. After localizing LV's assets in this sprint, do a live render check —
  view the deployed page (after push + GitHub Pages rebuild) and confirm ALL video
  elements load and play. If something's still missing, check for a referrer/hotlink-block
  issue on a remaining un-localized FvF URL on that page specifically.

## Step 7 — Validate & push
- Spot-check a handful of pages locally (open in browser / screenshot) to confirm media
  loads.
- Confirm total repo size growth is reasonable (videos are the bulk — keep an eye on
  GitHub's soft repo size limits; flag if any single asset >100MB or repo total getting
  large, and propose Git LFS or further compression if so).
- Commit in logical batches (e.g. per client or per asset type), with clear messages.
- Push to `main`. GitHub Pages will rebuild — no separate deploy step needed.

## Step 8 — Report back
Produce a final summary: total assets localized, total size before/after optimization,
any URLs that couldn't be fetched (404s, auth-walled, etc. — list these explicitly so
Frederik can supply alternates), and confirmation that frederikfrede.com pages no longer
reference any external CDN except Vimeo (USM) and the Cargo.site showreel (hero video,
intentionally external per current setup — confirm with Frederik whether this one should
also be localized).

## Notes
- Use the GitHub Contents API or local git + push, whichever is faster for batch commits.
- `imprint.html` is being edited in a parallel thread — GET fresh SHA before touching it,
  and ideally don't touch it in this sprint at all.
- Maintain the "Frederik Frede excluded from Collaborators" rule if any credits blocks
  are incidentally touched while editing a page (don't re-add it).
