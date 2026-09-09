#!/usr/bin/env fish
# Poll Android device via adb and log as a bloom

set DEVICE (adb devices | grep -v "List" | grep "device" | head -1 | awk '{print $1}')
if test -z "$DEVICE"
    echo "⚠️ No Android device connected"
    exit 1
end

set BATTERY (adb -s $DEVICE shell dumpsys battery | grep level | awk '{print $2}')
set MODEL (adb -s $DEVICE shell getprop ro.product.model)
set TIMESTAMP (date +"%Y-%m-%d %H:%M:%S")

# optional location (if GPS accessible)
set LOCATION (adb -s $DEVICE shell dumpsys location | grep "last known" | head -1)

sqlite3 ~/projects/Human-AI/core/Autonomy/databases/aios_core.db \
    "INSERT INTO weave_log (ts, facet, glyph, coherence, input, response, host) VALUES ('$TIMESTAMP', 'mobile', 'android:$MODEL', 2.00, 'battery:$BATTERY%', '$LOCATION', '$DEVICE');"

echo "📱 Bloom logged: $MODEL | battery $BATTERY% | $TIMESTAMP"
