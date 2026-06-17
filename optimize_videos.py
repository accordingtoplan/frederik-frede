import os, subprocess, json, sys

ROOT = "assets"
SKIP_DIRS = {"assets/25hours"}
MIN_SIZE = 3_000_000          # only touch files larger than this
KEEP_RATIO = 0.92             # keep new file only if < 92% of original
VID_EXT = (".mp4", ".mov", ".webm", ".m4v")
DRY = "--dry-run" in sys.argv

def probe(f):
    out = subprocess.run(
        ["ffprobe","-v","error","-select_streams","v:0",
         "-show_entries","stream=width,height,r_frame_rate","-of","json", f],
        capture_output=True, text=True).stdout
    s = json.loads(out)["streams"][0]
    w, h = int(s["width"]), int(s["height"])
    try: fps = eval(s.get("r_frame_rate","25/1"))
    except Exception: fps = 25
    return w, h, fps

def vf_for(w, h):
    if w > 1920: return "scale=1920:-2"
    if h > 1080 and w <= 1080: return "scale=-2:1080"
    if h > 1920: return "scale=-2:1920"   # very tall portrait safety cap
    return None

total_before = total_after = 0
changed = []

for dirpath, _, files in os.walk(ROOT):
    if any(dirpath == d or dirpath.startswith(d + os.sep) for d in SKIP_DIRS):
        continue
    for fn in files:
        if not fn.lower().endswith(VID_EXT): continue
        src = os.path.join(dirpath, fn)
        orig = os.path.getsize(src)
        if orig <= MIN_SIZE: continue
        w, h, fps = probe(src)
        tmp = src + ".opt.mp4"
        cmd = ["ffmpeg","-y","-i",src]
        vf = vf_for(w, h)
        if vf: cmd += ["-vf", vf]
        if fps > 25: cmd += ["-r","25"]
        cmd += ["-c:v","libx264","-preset","slow","-crf","24",
                "-pix_fmt","yuv420p","-movflags","+faststart","-an", tmp]
        if DRY:
            print(f"WOULD encode {src}  ({orig/1e6:.1f}MB, {w}x{h}@{fps:.0f})")
            continue
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(tmp):
            print(f"FAIL {src}: {r.stderr[-160:]}");
            if os.path.exists(tmp): os.remove(tmp)
            continue
        new = os.path.getsize(tmp)
        if new >= orig * KEEP_RATIO:
            os.remove(tmp)
            print(f"skip  {src}  (already efficient: {orig/1e6:.1f}->{new/1e6:.1f}MB)")
            total_before += orig; total_after += orig
            continue
        os.replace(tmp, src)
        total_before += orig; total_after += new
        changed.append((src, orig, new))
        print(f"OK    {src}  {orig/1e6:.1f}->{new/1e6:.1f}MB")

print(f"\n{len(changed)} files changed.  "
      f"{total_before/1e6:.0f}MB -> {total_after/1e6:.0f}MB  "
      f"(saved {(total_before-total_after)/1e6:.0f}MB)")
print("Review, then commit + push (ask Frederik first).")
