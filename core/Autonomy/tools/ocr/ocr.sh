#!/bin/bash
# OCR Tool for Wayland - Select area and copy text to clipboard

TMP=$(mktemp /tmp/ocr-XXXXXX.png)
grim -g "$(slurp)" "$TMP"
tesseract "$TMP" stdout -l eng | wl-copy
echo "OCR complete - text copied to clipboard"
rm -f "$TMP"
