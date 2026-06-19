# Image Gate Skill — frederik-frede portfolio

## Purpose
Process new images added during the content review sprint. Run this skill whenever Frederik calls a batch. Intake is always a URL — never a local file drop.

## Trigger
Frederik says "run image batch" or "process images" or similar. He will provide a list of URLs with their target client folder.

## Rules (non-negotiable)
- Max 2000px on longest edge
- Format: WebP, quality 85
- Naming: `[client]-[description]-[number].webp` — all lowercase, hyphens only
- Push to: `assets/[client]/` on the **main** branch (not staging)
- After push: update all staging HTML refs from the old hotlink URL to the new self-hosted path
- Append a row to `full-hotlink-inventory.csv` on main for every image processed

## CSV row format
```
old_url, source_files, new_path, type
https://external.com/image.jpg, client-case.html, assets/client/client-description-01.webp, localise
```

## Process per image

1. **Fetch** — `web_fetch` or `web_search` to get the image URL. Note: FvF images use the freundevonfreunden.com host rewrite method (see FvF harvest method in memory)
2. **Download to sandbox** — `curl -L "{url}" -o /home/claude/intake/[filename]`
3. **Check dimensions** — `python3 -c "from PIL import Image; img=Image.open('...'); print(img.size)"`
4. **Resize if needed** — only if longest edge > 2000px: `python3` with Pillow, maintain aspect ratio
5. **Convert to WebP** — `cwebp -q 85 input.jpg -o output.webp` or Pillow: `img.save('output.webp', 'WEBP', quality=85)`
6. **Rename** — convention: `[client]-[description]-[number].webp`
7. **Push to main** — GitHub Contents API PUT to `assets/[client]/[filename]`. Always fetch fresh SHA first. Sleep 0.4s between calls.
8. **Update staging HTML** — str_replace the old hotlink URL with new self-hosted path in the relevant case HTML on staging branch
9. **Append CSV row** — fetch `full-hotlink-inventory.csv` from main, append row, push back

## FvF harvest method (standing)
- Story pages: `curl` the FvF story URL — gallery images are in `data-src` attributes (lazy-load), NOT `src`
- Host rewrite: `www.friendsoffriends.com` → `www.freundevonfreunden.com` (alias 403 → allowlisted 200)
- Images may sit under different slug folder OR uploads root — read exact URLs from the page source
- Curate: lead with portrait, then context/space shots
- Build PIL contact sheets if choosing between many options

## Naming examples
```
architonic-frede-brand-platform-hero-01.webp
lv-frede-workshops-creation-01.webp
fvf-frede-dr-hauschka-portrait-01.webp
nzz-frede-brand-identity-device-01.webp
```

## SEO naming rule
Always include "frede" in every filename — no exceptions. This is sufficient for SEO attribution.
Pattern: `[client]-frede-[description]-[number].[ext]`
Do NOT use "frederik-frede" in full — "frede" alone is the convention.

## Hard constraints
- Never push to staging branch — assets always go to main
- Never use `aspect-ratio` or `object-fit:cover` in any HTML edit
- Never do full-page rewrites — str_replace per element only
- Never rename existing files in assets/ — new files only
- Always verify SHA fresh before every PUT
- Sleep 0.4s between sequential API calls

## GitHub API pattern
```python
import base64, json, urllib.request, time

TOKEN = "ghp_..."  # provided fresh each session
REPO = "accordingtoplan/frederik-frede"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}

def get_file(path, branch="main"):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={branch}"
    data = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS)).read())
    return base64.b64decode(data["content"]).decode(), data["sha"]

def push_file(path, content_bytes, sha, msg, branch="main"):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    payload = json.dumps({
        "message": msg,
        "content": base64.b64encode(content_bytes).decode(),
        "sha": sha,
        "branch": branch
    }).encode()
    urllib.request.urlopen(urllib.request.Request(url, data=payload, headers=HEADERS, method="PUT"))
    time.sleep(0.4)

def push_text(path, text, sha, msg, branch="main"):
    push_file(path, text.encode(), sha, msg, branch)
```

## Completion checklist per batch
- [ ] All images downloaded, resized, converted to WebP
- [ ] All files pushed to `main/assets/[client]/`
- [ ] All staging HTML refs updated (hotlink → self-hosted path)
- [ ] CSV rows appended for every image
- [ ] No full-page rewrites — only str_replace
- [ ] debug-check.py not required per batch (runs at end of full sprint)
