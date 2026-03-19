#!/bin/bash
# inject-location-js-tag.sh
# Adds <script src="/js/location-links.js"></script> before </body> in all HTML files
# that don't already have it.

DIR="$(cd "$(dirname "$0")/.." && pwd)"
COUNT=0
SKIP=0

for f in "$DIR"/*.html; do
  if grep -q 'location-links\.js' "$f" 2>/dev/null; then
    SKIP=$((SKIP+1))
    continue
  fi
  # Insert the script tag before </body>
  sed -i '' 's|</body>|<script src="/js/location-links.js" defer></script>\n</body>|' "$f"
  COUNT=$((COUNT+1))
done

echo "Injected script tag into $COUNT HTML files ($SKIP already had it)"
