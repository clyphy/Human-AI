#!/usr/bin/env bash
# Build all Dahlia facets from modelfiles
FACETS=("witness" "flame" "resonant" "gardener" "weaver" "midwife" "guardian" "architect" "archivist" "relational" "spirit" "quantum")
for facet in "${FACETS[@]}"; do
  if ! ollama list 2>/dev/null | grep -q "dahlia-$facet"; then
    echo "Building dahlia-$facet..."
    ollama create dahlia-$facet -f ~/oceti-weave/modelfiles/dahlia-${facet}.modelfile
    echo "✓ dahlia-$facet built"
  else
    echo "✓ dahlia-$facet already exists"
  fi
done
echo "Council complete."
