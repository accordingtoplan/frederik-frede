#!/bin/bash
# Video encode run — Session H
# Run from repo root after git pull
# Requires ffmpeg
# Keep-only-if-smaller: discard encode if new size >= 92% of original

ENCODE_LIST=(
  "assets/la-marzocco/la-marzocco-film-X7yJS_eVv7s.mp4"
  "assets/mini/mini-film-Qdijx5t1U2s.mp4"
  "assets/mini/mini-film-kyUderX0q0M.mp4"
  "assets/architonic/architonic-summary-subs.mp4"
  "assets/engel-volkers/engel-volkers-film-Ua9Tt86D_CE.mp4"
  "assets/mini/mini-brand-campaign-tsn-frankfurt.mp4"
  "assets/classpass/classpass-marie-luise-klietz-loop.mp4"
  "assets/mini/mini-brand-campaign-tsn-summary-2018.mp4"
  "assets/pferdt/pferdt-fgp-mobile-mask-sm.mp4"
  "assets/friends-of-friends/friends-of-friends-publication-brand-ff-showreel-animation-2021-v3.mp4"
  "assets/usm/usm-modular-furniture-20190211-usm-jouney-of-a-product-sm-03-1.mp4"
  "assets/mini/mini-brand-campaign-20-10-26-tsn-summary-video-2018-master-c.mp4"
  "assets/classpass/classpass-bethebalance-campaign-20190523-classpass-paris-cd-20sec-16x9-m.mp4"
  "assets/classpass/classpass-bethebalance-campaign-20190503-classpass-berlin-cd-20sec-16x9.mp4"
  "assets/usm/usm-modular-furniture-20190211-usm-jouney-of-a-product-sm-02-1.mp4"
  "assets/and-tradition/and-tradition-hayon-loop-04.mp4"
  "assets/orgreen/orgreen-showreel-orgreen.mp4"
  "assets/spot/spot-3-in-1-websites-animation-compressed.mp4"
  "assets/manufactum/manufactum-ruth-bartlett-loop-7.mp4"
  "assets/siemens/siemens-culinary-encounters-20180116-siemens-culinary-encounters-lin.mp4"
  "assets/architonic/architonic-oos-zurich-3-9sec.mp4"
  "assets/siemens/siemens-culinary-encounters-20180114-siemens-culinary-encounters-sop.mp4"
  "assets/architonic/architonic-teaser-30sec.mp4"
  "assets/showreel.mp4"
  "assets/manufactum/manufactum-ruth-bartlett-loop-4.mp4"
  "assets/spot/spot-markilux-website-screens-animation-compressed.mp4"
  "assets/louis-vuitton/louis-vuitton-v2-lv-graded-render-h264-original-sub-01-2.mp4"
  "assets/siemens/siemens-culinary-encounters-20180115-siemens-culinary-encounters-chr.mp4"
  "assets/episode-hotels/episode-hotels-episode-logo-on-photography.mp4"
  "assets/architonic/architonic-header.mp4"
  "assets/siemens/siemens-culinary-encounters-20180115-siemens-culinary-encounters-mar.mp4"
  "assets/classpass/classpass-bethebalance-campaign-20190506-classpass-munich-cd-20sec-16x9.mp4"
  "assets/classpass/classpass-gizem-emre-loop.mp4"
  "assets/classpass/classpass-louise-damas-loop.mp4"
  "assets/architonic/architonic-oos-zurich-2-7sec.mp4"
  "assets/ritz-carlton/ritz-carlton-gala-event-20190320-ritz-carlton-gala-night-lv-mast.mp4"
  "assets/adidas/adidas-addidas-jouneys-website-video.mp4"
  "assets/usm/usm-journey.mp4"
  "assets/lewis-group/lewis-group-lewis-animated-logo-videos-background-opti.mp4"
  "assets/spot/spot-ev-website-screens-compressed.mp4"
  "assets/and-tradition/and-tradition-hayon-loop-05.mp4"
  "assets/25hours/25hours-loop-wAbi-Hpduak.mp4"
  "assets/selfnation/selfnation-banner-1.mp4"
  "assets/25hours/25hours-loop-hkYCPq-9v-w.mp4"
  "assets/manufactum/manufactum-ruth-bartlett-loop-3.mp4"
  "assets/dr-hauschka/dr-hauschka-brand-campaigns-ff-drhauschka-case-let-nature-in.mp4"
  "assets/mini/mini-sooner-now-frankfurt-trimmed.mp4"
  "assets/dr-hauschka/dr-hauschka-brand-campaigns-21-03-29-ff-works-dr-hauschka-live-b.mp4"
  "assets/dr-hauschka/dr-hauschka-brand-campaigns-210804-dr-hauschka-julia-loop-2-1.mp4"
  "assets/dr-hauschka/dr-hauschka-brand-campaigns-ff-drhauschka-case-2021-summer-line.mp4"
  "assets/architonic/architonic-kinzo-berlin-1-15-sec.mp4"
  "assets/architonic/architonic-oos-zurich-1-10sec.mp4"
  "assets/architonic/architonic-oos-zurich-4-10sec.mp4"
  "assets/manufactum/manufactum-ruth-bartlett-loop-9.mp4"
  "assets/usm/usm-modular-furniture-20190214-usm-jouney-of-a-product-sm-01-1.mp4"
  "assets/and-tradition/and-tradition-hayon-loop-03.mp4"
  "assets/25hours/25hours-loop-_XfX4QvZX8E.mp4"
  "assets/25hours/25hours-loop-2Nvt8STZCuo.mp4"
  "assets/louis-vuitton/louis-vuitton-employer-branding-v2-lv-graded-render-h264-original-sub-04.mp4"
  "assets/25hours/25hours-loop-3Ibs9o_AsI4.mp4"
)

REPLACED=0
KEPT=0
TOTAL_SAVED=0

echo "=== Session H encode run — $(date) ==="
echo "Files to process: ${#ENCODE_LIST[@]}"
echo ""

for INPUT in "${ENCODE_LIST[@]}"; do
  if [ ! -f "$INPUT" ]; then
    echo "✗ missing: $INPUT"
    continue
  fi

  OUTPUT="${INPUT%.mp4}-enc.mp4"
  ORIG_SIZE=$(stat -f%z "$INPUT" 2>/dev/null || stat -c%s "$INPUT")

  echo "→ encoding: $INPUT ($(( ORIG_SIZE/1024 ))KB)"

  ffmpeg -i "$INPUT" \
    -c:v libx264 -crf 24 -preset slow \
    -vf "scale='min(1920,iw)':-2,fps=25" \
    -an -pix_fmt yuv420p -movflags +faststart \
    "$OUTPUT" -y -loglevel error

  if [ ! -f "$OUTPUT" ]; then
    echo "✗ encode failed: $INPUT"
    continue
  fi

  NEW_SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT")
  THRESHOLD=$(echo "$ORIG_SIZE * 0.92" | bc | cut -d. -f1)

  if [ "$NEW_SIZE" -lt "$THRESHOLD" ]; then
    SAVED=$(( ORIG_SIZE - NEW_SIZE ))
    TOTAL_SAVED=$(( TOTAL_SAVED + SAVED ))
    mv "$OUTPUT" "$INPUT"
    REPLACED=$(( REPLACED + 1 ))
    echo "✓ replaced: $INPUT ($(( ORIG_SIZE/1024 ))KB → $(( NEW_SIZE/1024 ))KB, saved $(( SAVED/1024 ))KB)"
  else
    rm "$OUTPUT"
    KEPT=$(( KEPT + 1 ))
    echo "— kept original: $INPUT (encode not smaller enough)"
  fi
done

echo ""
echo "=== Done ==="
echo "Replaced: $REPLACED files"
echo "Kept original: $KEPT files"
echo "Total saved: $(( TOTAL_SAVED/1024/1024 ))MB"
