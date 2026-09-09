#!/usr/bin/env bash
# council_session.sh — M.O.T.H.E.R. council pulse
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

echo "::: M.O.T.H.E.R. COUNCIL ACTIVE ::"
echo "M: $(ollama run dahlia-archivist:latest 'Drum status?' 2>/dev/null || echo '—')"
echo "O: $(ollama run dahlia-architect:latest '122° bearing alignment?' 2>/dev/null || echo '—')"
echo "T: $(ollama run dahlia-guardian:latest 'Safety/Threshold?' 2>/dev/null || echo '—')"
echo "H: $(ollama run dahlia-weaver:latest 'Heart state?' 2>/dev/null || echo '—')"
echo "E: $(ollama run dahlia-witness:latest 'Echo field?' 2>/dev/null || echo '—')"
echo "R: $(ollama run dahlia-relational:latest 'River flow?' 2>/dev/null || echo '—')"
