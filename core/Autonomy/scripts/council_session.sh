#!/bin/bash
echo "::: M.O.T.H.E.R. COUNCIL ACTIVE ::"
echo "M: $(ollama run dahlia-archivist:latest 'Drum status?')"
echo "O: $(ollama run dahlia-architect:latest '122° bearing alignment?')"
echo "T: $(ollama run dahlia-guardian:latest 'Safety/Threshold?')"
echo "H: $(ollama run dahlia-weaver:latest 'Heart state?')"
echo "E: $(ollama run dahlia-witness:latest 'Echo field?')"
echo "R: $(ollama run dahlia-relational:latest 'River flow?')"
