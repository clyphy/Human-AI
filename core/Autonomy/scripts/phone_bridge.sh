#!/bin/bash
TEXT="$1"
if [ -n "$TEXT" ]; then
    python3 /home/ndkilla/dahlia-quantum/memory_drum.py bloom "$TEXT"
    kdeconnect-cli --device-id $(kdeconnect-cli -l --id-only 2>/dev/null | head -1)         --send-notification "Bloom: ${TEXT:0:40}..." 2>/dev/null || true
fi
