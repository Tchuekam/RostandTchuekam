#!/usr/bin/env bash
# Convenience wrapper for fetch_innertube.js
# Usage: fetch_innertube.sh <VIDEO_ID> [--text]
#   --text: print just the caption track summary (plain text)
#   default: print JSON

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIDEO_ID="$1"
MODE="${2:-}"

if [ -z "$VIDEO_ID" ]; then
  echo "Usage: $0 <VIDEO_ID> [--text]"
  exit 1
fi

OUTPUT=$(node "$SCRIPT_DIR/fetch_innertube.js" "$VIDEO_ID" 2>&1)
EXIT_CODE=$?

if [ "$MODE" = "--text" ]; then
  if [ $EXIT_CODE -eq 1 ]; then
    echo "NO CAPTIONS: Video '$VIDEO_ID' has no captions."
  elif [ $EXIT_CODE -eq 0 ]; then
    echo "$OUTPUT" | node -e "
      const d = require('fs').readFileSync('/dev/stdin','utf8');
      const j = JSON.parse(d);
      console.log('Title:', j.title);
      console.log('Length:', j.length_seconds + 's');
      console.log('Captions:', j.has_captions ? 'YES' : 'NO');
      if (j.tracks) j.tracks.forEach(t => console.log('  [' + t.languageCode + '] ' + t.kind + ' - ' + t.name));
    "
  else
    echo "ERROR getting captions for '$VIDEO_ID'"
    echo "$OUTPUT"
  fi
else
  echo "$OUTPUT"
fi

exit $EXIT_CODE
