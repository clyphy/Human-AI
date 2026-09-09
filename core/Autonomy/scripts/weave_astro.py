#!/usr/bin/env python3
"""
weave_astro.py — offline solar position and season calculations.
No internet required. Computes sunrise/sunset for Belcourt, ND and the
current astronomical season (Fall/Winter/Spring/Summer), independent of
the Weave-internal blooms.season epoch label.

Usage:
    weave_astro.py is-nocturnal   -> prints yes/no, exit 0 if nocturnal
    weave_astro.py sun-times      -> prints sunrise=HH:MM sunset=HH:MM
    weave_astro.py season         -> prints Fall|Winter|Spring|Summer
"""
import sys
import math
from datetime import datetime, timedelta, timezone

# Belcourt, ND (Turtle Mountain) approx coordinates
LAT = 48.7736
LON = -99.7268


def sun_times(date):
    """NOAA-style approximate sunrise/sunset. Returns (sunrise_utc, sunset_utc)."""
    lat_r = math.radians(LAT)
    n = date.timetuple().tm_yday
    gamma = 2 * math.pi / 365 * (n - 1)
    eqtime = 229.18 * (
        0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma)
    )
    decl = (
        0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)
        - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)
    )
    zenith = math.radians(90.833)
    cos_ha = (
        (math.cos(zenith) / (math.cos(lat_r) * math.cos(decl)))
        - math.tan(lat_r) * math.tan(decl)
    )
    cos_ha = max(-1, min(1, cos_ha))
    ha = math.degrees(math.acos(cos_ha))
    sunrise_min = 720 - 4 * (LON + ha) - eqtime
    sunset_min = 720 - 4 * (LON - ha) - eqtime
    base = datetime(date.year, date.month, date.day, tzinfo=timezone.utc)
    return base + timedelta(minutes=sunrise_min), base + timedelta(minutes=sunset_min)


def is_nocturnal():
    now = datetime.now(timezone.utc)
    sunrise, sunset = sun_times(now)
    return now < sunrise or now > sunset


def season_boundaries(year):
    return {
        'Spring': datetime(year, 3, 20, tzinfo=timezone.utc),
        'Summer': datetime(year, 6, 21, tzinfo=timezone.utc),
        'Fall':   datetime(year, 9, 22, tzinfo=timezone.utc),
        'Winter': datetime(year, 12, 21, tzinfo=timezone.utc),
    }


def current_season():
    now = datetime.now(timezone.utc)
    b = season_boundaries(now.year)
    if now >= b['Winter']:
        return 'Winter'
    if now >= b['Fall']:
        return 'Fall'
    if now >= b['Summer']:
        return 'Summer'
    if now >= b['Spring']:
        return 'Spring'
    return 'Winter'  # before spring equinox: still prior year's winter


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'is-nocturnal':
        noct = is_nocturnal()
        print('yes' if noct else 'no')
        sys.exit(0 if noct else 1)
    elif cmd == 'sun-times':
        sr, ss = sun_times(datetime.now(timezone.utc))
        print(f"sunrise={sr.astimezone().strftime('%H:%M')} sunset={ss.astimezone().strftime('%H:%M')}")
    elif cmd == 'season':
        print(current_season())
    else:
        print(__doc__)
        sys.exit(2)
