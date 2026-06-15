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

---

## Status log — 2026-06-12

49 new rows appended to `full-hotlink-inventory.csv` for the 9 new MoreSleep
case studies added this session (ORNO, Swayed, Brutø, Internetstores,
Weiler, PURO Hotels, Ziegert, Mezcla, Selfnation) — all moresleep.net assets.
Auto-generated `new_path` values follow the same convention but the
`[description]` segment is mechanical (derived from the original filename);
feel free to tidy these up during the sprint using page context, same as the
existing note above for Webflow assets.

Going forward: whenever a new case study is added in a hosted-Claude session
and it references external/hotlinked media, append rows to this CSV in the
same format (`old_url,source_files,new_path`) so this file stays the single
authoritative backlog for the next Claude Code sprint.


---

## Status log — 2026-06-15

Added new page `siemens-home-appliances.html` (renamed from
`siemens-culinary-encounters.html`, old slug deleted, all inbound links
updated: index.html, work.html, dr-hauschka, classpass). Page restructured
into three sections: 01 Culinary Encounters, 02 Home Stories, 03 Friends Space.

WIP STATE — Home Stories currently uses YouTube/Vimeo **embeds** (sandbox can't
reach freundevonfreunden.com). 8 self-hosted assets appended to the CSV for this
sprint: 2 Friends Space images (FvF + &Tradition CDN) used as live <img> hotlinks
that SHOULD be localized, plus 6 Home Stories/Culinary loop videos (.mov/.mp4/.webm)
available to download and optionally swap in to replace the YT embeds with quiet
background loops (matching the site's autoplay-muted-loop convention).

Note: .mov files need re-encoding to .mp4 (H.264) on download (see Pferdt note).
The two Friends Space <img> hotlinks are the only *live* external refs on the page
— prioritize those so the page is fully self-hosted for its visible assets.

Also flagged (not on CSV, needs Frederik's input): 6 unidentified YouTube IDs are
embedded in a WIP cs-grid-3 block on the page marked "to identify" — these are
placeholders to review/prune, not localization targets.


---

## Status log — 2026-06-15 (Siemens full rebuild)

Siemens page rebuilt into FOUR sections: 01 Culinary Encounters, 02 Home Stories,
03 Architect Dialogues (NEW series — Barkow Leibinger/Berlin, Antonin Ziegler/Paris,
Marc Koehler/Amsterdam, Joanna Laajisto/Helsinki, all 2019), 04 Friends Space.
Now spans 2015–2021, reframed as campaign + content partnership.

9 more rows appended to CSV: 4 Home Stories real FvF hero images (Astridge, John
Henry, Kevin Chu, De Grijze Silo), all 4 Architect Dialogues hero images, + John
Henry loop video. These are LIVE hotlinks rendering on the page now — localize in
this sprint. Some Home Stories cards (Judin, Kolja, Brandlhuber, Veerle Wenes) use
img.youtube.com thumbnails as heroes — those are YT-hosted, lower priority, but
could be upgraded to real FvF stills during the sprint (real hero images exist on
each FvF story page's og:image where the og:image points to app/uploads rather
than img.youtube.com).

Captions are wired via new .cs-fig / .cs-figrid figure styles (name + meta).
6 unidentified YT IDs still in the WIP cs-grid-3 — awaiting Frederik's review/prune.


## 2026-06-15 — Image-gap audit + editorial-still localization (video-only FvF cases)

AUDIT: Built a stills-vs-video detector (counting <img> minus logos/posters, not raw
media refs — the raw-ref count gave false "all fine" earlier). Found 4 recently-built
FvF Film & Content cases were VIDEO-ONLY (zero photographic stills), plus 2 thin:
  - classpass-bethebalance-campaign.html  (0 stills, 6 vids)  -> FIXED
  - dr-hauschka-brand-campaigns.html      (0 stills, 6 vids)  -> FIXED
  - manufactum-alltagsfreude-ruth-bartlett.html (0, 4)        -> FIXED
  - and-tradition-jaime-hayon.html        (0 stills, 3 vids)  -> FIXED
  - selfnation-campaign.html              (2 stills)          -> STILL THIN, revisit
  - egon-zehnder-leadership-interviews.html (1 still)         -> STILL THIN, revisit

KEY: FvF (www.freundevonfreunden.com) NOW RESOLVES from the bash sandbox (allowlist
updated) — so og:image heroes were DOWNLOADED + SELF-HOSTED, not hotlinked. 8 stills
pushed to /assets/{classpass,dr-hauschka,manufactum,and-tradition}/ (SEO-named).
Method that works without the Chrome extension: web_search to find each protagonist's
FvF story slug -> og:image gives the real hero -> curl into sandbox -> push. The CSV's
stored app/uploads paths were the fastest way to recover the real story slugs (don't
guess them).

LIMITATION UNCHANGED: only ONE og:image hero per source page is reachable; in-body
galleries are JS-lazy-loaded and never appear in static HTML. Full galleries (multiple
stills per story) still need the Chrome extension's real browser OR Eagle. The 4 fixed
cases each got 1 strong still per protagonist, not the whole shoot.

CONTENT FIXES alongside images:
  - ClassPass: section 01 copy corrected to name all FOUR cities/protagonists incl.
    the previously-omitted Lizzy van der Ligt (Amsterdam). Her story lived on ClassPass's
    own blog (The Warm Up, by Disha Khatwani), NOT FvF — no FvF video portrait, no clean
    FvF still (only paparazzi/Alamy, not used). Amsterdam is text-only for now; needs an
    Eagle asset if a portrait is wanted.
  - Credits added per standing rule: Dr. Hauschka photography -> Sima Dehgani. (Frederik
    stays excluded though credited as ECD on the FvF source.)

TODO next sprint: selfnation + egon-zehnder still-thin; full-gallery harvest for all 4
fixed cases (Chrome ext / Eagle); re-check whether OTHER older Film & Content cases
(la-marzocco, closed editorial, etc.) have the same video-only gap.


## 2026-06-15 — CORRECTION: full FvF galleries ARE sandbox-reachable

Earlier claim ("only the og:image hero is reachable; in-body galleries are JS-lazy and
absent from static HTML") was WRONG. The galleries ARE in the static HTML — in
**data-src** attributes (lazy-load), not src. Method: curl the story page, grep
data-src/src for the protagonist's /app/uploads/ images. CATCH: the data-src host is
often **www.friendsoffriends.com** (alias) which is NOT allowlisted (403 host_not_allowed)
— rewrite the host to **www.freundevonfreunden.com** and the SAME file returns 200 (full
original, e.g. 3748x2500). So NO Chrome extension needed for galleries after all; only
needed for sites that truly hard-block (USM/Squarespace/Webflow). Folder gotcha: some
protagonist images live under a DIFFERENT slug folder than the story slug (e.g. Klietz
images are under app/uploads/classpass-marie-luise-klietz/, not her story slug) — always
read the exact data-src URLs from the page, don't assume the folder.

ClassPass now upgraded: section 02 rebuilt into 3 named protagonist blocks (Gizem Emre/
Berlin, Louise Damas/Paris, Marie-Luise Klietz/Munich), each with an <h3> name (SEO),
a link to their FvF story, the video portrait + 2 extra stills (cs-fig captioned figures).
+ a 2-up Paris/Munich place-setting grid before the pull-quote. 8 new gallery stills
self-hosted in /assets/classpass/. Picked best 2-3 per person from full galleries
(Gizem 7, Louise 14, Klietz ~10 available).


## 2026-06-15 — Siemens page: killed redundant YT-thumbnail stills, self-hosted real FvF story imagery

PROBLEM (Frederik): Home Stories / Architect Dialogues cards were using img.youtube.com/vi/<ID>/maxresdefault.jpg
as the still — which IS the video's own preview frame (so the same image showed twice) and often has
burned-in titles/graphics. Also "hero" was ambiguous: the ARTICLE/STORY hero (the editorial photo FvF opens
the story with) is the right image, NOT the video poster.

FIX: harvested each protagonist's FvF STORY hero + context/space shots via the data-src method (entry 16),
self-hosted 36 stills (3 per protagonist) + 1 Friends Space image -> /assets/siemens/. Rebuilt sections 02
(Home Stories, 8 protagonists) + 03 (Architect Dialogues, 4) into named blocks: <h3> name + "Read the story
on Friends of Friends ↗" link + video (where it exists) + portrait + 2 context shots in cs-figrid-3 with
captions. 0 img.youtube thumbnails left; 0 FvF /app/uploads hotlinks left.

Story URL map (for future retrofits): judin=art/juerg-judin; stegemann=stories/kolja-stegemann;
brandlhuber=architecture/arno-brandlhuber-anti-villa; astridge=architecture/london-architect-simon-astridge-on-creating-homes-with-an-emphasis-on-everyday-experience;
john-henry=stories/john-henry; kevin-chu=architecture/architect-kevin-chu-giulia-dibonaventura-sustainable-lifestyle;
grijze-silo=architecture/a-testament-to-preserving-industrial-heritage-in-the-dutch-countryside-with-the-de-grijze-silo;
veerle=art/the-gallery-of-veerle-wenes-dissolves-the-boundaries-between-public-and-private-art;
barkow=architecture/room-for-inventions-with-the-tech-focused-architecture-firm-barkow-leibinger;
ziegler=architecture/architect-antonin-ziegler-transforms-humble-structures-into-industrial-yet-serene-residences;
koehler=architecture/marc-koehler-wants-to-build-cities-of-the-future-one-flexible-sustainable-community-at-a-time;
laajisto=architecture/exploring-the-changing-landscape-of-finnish-design-with-interior-architect-joanna-laajisto.

GALLERY-FOLDER NOTE: Brandlhuber + Astridge gallery images sit in the uploads ROOT (named by protagonist),
not a slug folder — filter root refs by name. Arch-dialogues folks use *-siemens-arch-dialogues/ folders.
ONE remaining hotlink: Friends Space Kreuzberg image is on wp.andtradition.com (403 from sandbox, hard-block)
— left as hotlink, renders in browser; needs Chrome ext / local session to self-host.

RULE LEARNED: never use a YouTube maxresdefault thumbnail as a "still" next to its own embed — it's redundant
and often has burned-in type. Pull the article/story hero + context shots instead.
