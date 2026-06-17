#!/usr/bin/env bash
# ============================================================================
# Cloudflare consolidation - frederikfrede.com + domain migration prep
# macOS/zsh + Linux safe. All Python is heredoc'd (no quote-escaping traps).
#
#   export CF_TOKEN='your_scoped_token_here'
#   bash cf-consolidation.sh            # read-only audit (default)
#   bash cf-consolidation.sh --apply    # also writes the cache rule (asks first)
#
# Token scope: Zone:Read, DNS:Read, Cache Settings (Cache Rules):Edit
# Rotate the token after this session.
# ============================================================================

set -uo pipefail

API="https://api.cloudflare.com/client/v4"
APPLY="${1:-}"

if [[ -z "${CF_TOKEN:-}" || "$CF_TOKEN" == "your_"* || "$CF_TOKEN" == "paste_"* ]]; then
  echo "ERROR: CF_TOKEN is not set to a real token." >&2
  echo "Run:  export CF_TOKEN='your_actual_token'   then re-run." >&2
  exit 1
fi

PY=python3
command -v "$PY" >/dev/null 2>&1 || PY=python

cf() { # cf METHOD PATH [JSON_BODY]
  local method="$1" path="$2" body="${3:-}"
  if [[ -n "$body" ]]; then
    curl -sS -X "$method" "$API$path" \
      -H "Authorization: Bearer $CF_TOKEN" \
      -H "Content-Type: application/json" \
      --data "$body"
  else
    curl -sS -X "$method" "$API$path" \
      -H "Authorization: Bearer $CF_TOKEN" \
      -H "Content-Type: application/json"
  fi
}

echo "============================================================"
echo " STEP 0 - verify token"
echo "============================================================"
cf GET "/user/tokens/verify" | "$PY" - <<'PY'
import sys, json
try:
    d = json.load(sys.stdin)
except Exception as e:
    print("  could not parse response:", e); sys.exit()
if not d.get("success"):
    print("  TOKEN INVALID. errors:", json.dumps(d.get("errors", [])))
    sys.exit()
r = d.get("result", {})
print("  status:", r.get("status"))
print("  token id:", r.get("id"))
PY
echo

echo "============================================================"
echo " STEP 1 - list zones this token can see"
echo "============================================================"
ZONES="$(cf GET '/zones?per_page=50')"
printf '%s' "$ZONES" | "$PY" - <<'PY'
import sys, json
raw = sys.stdin.read()
try:
    d = json.loads(raw)
except Exception:
    print("  could not parse zones response (empty/non-JSON). Token valid? Network ok?")
    sys.exit()
if not d.get("success"):
    print("  error listing zones:", json.dumps(d.get("errors", []))); sys.exit()
res = d.get("result", []) or []
if not res:
    print("  (token sees no zones)")
for z in res:
    name = z.get("name", "?")
    status = z.get("status", "?")
    zid = z.get("id", "?")
    print("  {:30}  {:10}  id={}".format(name, status, zid))
    ns = z.get("name_servers") or []
    if ns:
        print("      assigned NS:", ", ".join(ns))
PY
echo

# zone id for frederikfrede.com (for cache-rule steps)
FFCOM_ID="$(printf '%s' "$ZONES" | "$PY" - <<'PY'
import sys, json
try:
    d = json.loads(sys.stdin.read())
except Exception:
    d = {}
for z in d.get("result", []) or []:
    if z.get("name") == "frederikfrede.com":
        print(z.get("id", "")); break
PY
)"

echo "============================================================"
echo " STEP 2 - existing cache rules on frederikfrede.com"
echo "============================================================"
if [[ -z "$FFCOM_ID" ]]; then
  echo "  frederikfrede.com not found on this token - skipping."
else
  echo "  zone id: $FFCOM_ID"
  cf GET "/zones/$FFCOM_ID/rulesets/phases/http_request_cache_settings/entrypoint" \
    | "$PY" - <<'PY'
import sys, json
try:
    d = json.load(sys.stdin)
except Exception as e:
    print("  (no JSON)", e); sys.exit()
if not d.get("success", False):
    errs = d.get("errors", [])
    if any(e.get("code") == 10000 or "could not be found" in str(e).lower() for e in errs):
        print("  No cache-rules ruleset exists yet (clean slate).")
    else:
        print("  errors:", json.dumps(errs))
    sys.exit()
r = d["result"]
rules = r.get("rules", []) or []
print("  ruleset id:", r.get("id"))
print("  existing rules:", len(rules))
for x in rules:
    print("    -", x.get("description", "(no desc)"), "|", x.get("expression"))
PY
fi
echo

echo "============================================================"
echo " STEP 3 - DNS scan: domains to migrate (run before CF cutover)"
echo "============================================================"
echo "  scanning live public DNS so nothing breaks when records are"
echo "  recreated in the CF zone"
for dom in processandprogress.com spku.com frede.net frederikfrede.de; do
  echo
  echo "  --- $dom ---"
  for t in A AAAA CNAME MX TXT NS; do
    out="$(dig +short "$t" "$dom" 2>/dev/null | sed 's/^/        /')"
    [[ -n "$out" ]] && { echo "    $t:"; echo "$out"; }
  done
  for sub in www mail webmail; do
    o="$(dig +short "$sub.$dom" 2>/dev/null | sed 's/^/        /')"
    [[ -n "$o" ]] && { echo "    $sub:"; echo "$o"; }
  done
done
echo

echo "============================================================"
echo " STEP 3.5 - PRE-FLIGHT: what would BREAK on NS cutover?"
echo "============================================================"
echo "  For each domain that already has a CF zone, compare live public DNS"
echo "  against the records in the CF zone. Live-but-missing-in-CF goes DARK"
echo "  the moment you flip nameservers. MX/mail flagged loudest."
for dom in frede.net frederikfrede.de processandprogress.com spku.com; do
  ZID="$(printf '%s' "$ZONES" | DOM="$dom" "$PY" - <<'PY'
import sys, json, os
try:
    d = json.loads(sys.stdin.read())
except Exception:
    d = {}
want = os.environ["DOM"]
for z in d.get("result", []) or []:
    if z.get("name") == want:
        print(z.get("id", "")); break
PY
)"
  echo
  echo "  ===== $dom ====="
  if [[ -z "$ZID" ]]; then
    echo "    No CF zone on this token - skipped (not migrated yet, or token not scoped to it)."
    continue
  fi
  export CF_RECS_JSON="$(cf GET "/zones/$ZID/dns_records?per_page=200")"
  DOM="$dom" "$PY" - <<'PY'
import sys, json, subprocess, os
domain = os.environ["DOM"]

def dig(rtype, name):
    try:
        out = subprocess.run(["dig", "+short", rtype, name],
                             capture_output=True, text=True, timeout=10).stdout
        return [l.strip() for l in out.splitlines() if l.strip()]
    except Exception:
        return []

names = [domain] + [s + "." + domain for s in
                    ("www", "mail", "webmail", "ftp", "autodiscover", "_dmarc")]
live = {}
for nm in names:
    for rt in ("A", "AAAA", "CNAME", "MX", "TXT"):
        vals = dig(rt, nm)
        if vals:
            live[(rt, nm)] = set(v.rstrip(".").lower() for v in vals)

try:
    cf = json.loads(os.environ.get("CF_RECS_JSON", ""))
    cf_records = cf.get("result", []) or []
except Exception:
    cf_records = []

cf_set = {}
for r in cf_records:
    key = (r.get("type"), (r.get("name", "") or "").rstrip(".").lower())
    cf_set.setdefault(key, set()).add(str(r.get("content", "")).rstrip(".").lower())

missing, mail_missing = [], []
for (rt, nm), vals in live.items():
    if not cf_set.get((rt, nm)):
        missing.append((rt, nm, vals))
        if rt == "MX":
            mail_missing.append((rt, nm, vals))

if not live:
    print("    Could not resolve any live records (may already be on CF, or dormant).")
elif not missing:
    print("    OK - every live record has a match in the CF zone. Safe to flip NS.")
else:
    if mail_missing:
        print("    *** MAIL AT RISK *** these MX records resolve live but are NOT in CF:")
        for rt, nm, vals in mail_missing:
            print("        {:6} {}  ->  {}".format(rt, nm, ", ".join(sorted(vals))))
        print("        ^ recreate these in CF BEFORE flipping nameservers or email breaks.")
    other = [m for m in missing if m[0] != "MX"]
    if other:
        print("    Live records missing from CF zone (would stop resolving on cutover):")
        for rt, nm, vals in other:
            print("        {:6} {}  ->  {}".format(rt, nm, ", ".join(sorted(vals))))
    print("    => {} record(s) to rebuild in CF before NS flip.".format(len(missing)))
PY
done
echo

echo "============================================================"
echo " STEP 4 - cache rule for /assets/*  (TTL 1 year)"
echo "============================================================"

read -r -d '' BODY <<'JSON' || true
{
  "rules": [
    {
      "description": "assets immutable - 1y edge+browser TTL (LCP fix)",
      "expression": "(starts_with(http.request.uri.path, \"/assets/\"))",
      "action": "set_cache_settings",
      "action_parameters": {
        "cache": true,
        "edge_ttl":    { "mode": "override_origin", "default": 31536000 },
        "browser_ttl": { "mode": "override",        "default": 31536000 }
      }
    }
  ]
}
JSON

if [[ "$APPLY" != "--apply" ]]; then
  echo "  DRY RUN - not writing. Payload that WOULD be PUT:"
  printf '%s\n' "$BODY"
  echo
  echo "  To apply:  bash cf-consolidation.sh --apply"
else
  if [[ -z "$FFCOM_ID" ]]; then
    echo "  Cannot apply: frederikfrede.com zone id not found."; exit 1
  fi
  echo "  About to PUT this cache rule to frederikfrede.com ($FFCOM_ID):"
  printf '%s\n' "$BODY"
  printf "  Proceed? type yes: "
  read -r ok
  if [[ "$ok" == "yes" ]]; then
    cf PUT "/zones/$FFCOM_ID/rulesets/phases/http_request_cache_settings/entrypoint" "$BODY" \
      | "$PY" - <<'PY'
import sys, json
d = json.load(sys.stdin)
print("  success:", d.get("success"))
if d.get("errors"):
    print("  errors:", json.dumps(d["errors"], indent=2))
for x in (d.get("result", {}) or {}).get("rules", []) or []:
    print("  applied:", x.get("description"), "|", x.get("expression"))
PY
    echo
    echo "  Verify after a few min:"
    echo "    curl -sI https://frederikfrede.com/assets/<file> | grep -i cache"
    echo "    -> expect: cf-cache-status: HIT  and  cache-control: max-age=31536000"
  else
    echo "  Aborted - nothing written."
  fi
fi

echo
echo "Done. Reminder: rotate CF_TOKEN now that the session is over."
