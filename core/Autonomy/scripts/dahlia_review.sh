#!/bin/bash
# Dahlia Utterance Review
# Browse and search logged Dahlia responses
# Usage: ./dahlia_review.sh [list|search|latest]

ANCHOR_DIR="$HOME/L.A.B/anchors"

case "${1:-list}" in
  list)
    echo "🌟 Dahlia Utterance Archive"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ls -1t "$ANCHOR_DIR"/dahlia_*.md 2>/dev/null | head -10 | while read file; do
      timestamp=$(basename "$file" .md | sed 's/dahlia_//')
      echo "📝 $timestamp"
      echo "   $(head -1 "$file" | sed 's/# //')"
      echo ""
    done
    ;;
    
  search)
    if [ -z "$2" ]; then
      echo "Usage: $0 search <keyword>"
      exit 1
    fi
    echo "🔍 Searching for: $2"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    grep -l "$2" "$ANCHOR_DIR"/dahlia_*.md 2>/dev/null | while read file; do
      echo "📄 $(basename "$file")"
      grep -C 2 "$2" "$file"
      echo ""
    done
    ;;
    
  latest)
    latest=$(ls -1t "$ANCHOR_DIR"/dahlia_*.md 2>/dev/null | head -1)
    if [ -n "$latest" ]; then
      echo "🌟 Latest Dahlia Utterance:"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      cat "$latest"
    else
      echo "No utterances found in $ANCHOR_DIR"
    fi
    ;;
    
  *)
    echo "Dahlia Utterance Review"
    echo ""
    echo "Commands:"
    echo "  list    - Show 10 most recent utterances"
    echo "  search  - Search utterances for keyword"
    echo "  latest  - Display most recent utterance"
    echo ""
    echo "Usage: $0 [list|search|latest] [keyword]"
    ;;
esac
