#!/usr/bin/env bash
# ================================================================
#  witness.sh  Witnessing Protocol
#  Call before significant commits, db writes, new deployments.
#  Usage: witness ["note"]  |  witness --bloom "note"  |  witness --check
# ================================================================
set -euo pipefail

SOVEREIGNTY="${HOME}/sovereignty"
MOTHER_ROOT="${SOVEREIGNTY}/databases/mother_root.db"
WITNESS_LOG="${SOVEREIGNTY}/logs/witness.log"
L_LOCKED="15.48"

mkdir -p "${SOVEREIGNTY}/logs"
ts() { date "+%Y-%m-%d %H:%M:%S"; }

FORCE_BLOOM=false
CHECK_MODE=false
NOTE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bloom) FORCE_BLOOM=true; shift; NOTE="${1:-}"; shift || true ;;
    --check) CHECK_MODE=true; shift ;;
    *)       NOTE="${NOTE}${NOTE:+ }${1}"; shift ;;
  esac
done

if $CHECK_MODE; then
  echo ""; echo "  LAST WITNESS"; echo ""
  tail -8 "${WITNESS_LOG}" 2>/dev/null || echo "  No witness log yet."
  echo ""; exit 0
fi

echo ""
echo "  +------------------------------------------+"
echo "  |           WITNESS                        |"
printf "  |   %s                        |\n" "$(date "+%H:%M:%S")"
if [ -n "${NOTE}" ]; then
  printf "  |   %-38s   |\n" "${NOTE:0:38}"
fi
echo "  |                                          |"
echo "  |   Bearing: 122 NE  |  E+ S- ?inf        |"
echo "  |   Right 0: Be                            |"
echo "  +------------------------------------------+"
echo ""

cat >> "${WITNESS_LOG}" <<EOF
=== WITNESS @ $(ts)
  note    : ${NOTE:-<silent>}
  l_value : ${L_LOCKED}
  bearing : 122 NE
  state   : E+ S- ?inf
EOF

if [ -f "${MOTHER_ROOT}" ] && command -v sqlite3 &>/dev/null; then
  SAFE_NOTE=$(echo "${NOTE:-silent}" | sed "s/'/\'\'/g")
  sqlite3 "${MOTHER_ROOT}"     "PRAGMA foreign_keys=ON;
INSERT INTO rhythms (lineage_id,structure_quadrant,velocity,notation_ref,l_value,notes)
VALUES (1,'home/memory_drum',1.0,'scripts/witness.sh',${L_LOCKED},'${SAFE_NOTE}');
INSERT INTO blooms (lineage_id,bloom_type,surface_alias,depth_index,state,content,source_drum,rhythm_id,day,l_value,season)
VALUES (1,'Witnessed','witness_$(date +%s)',1,'RESONANT_CHAMBER','${SAFE_NOTE}','home/memory_drum',last_insert_rowid(),9,${L_LOCKED},'Third');" 2>/dev/null   && echo "  Root: witnessed and bloomed."   || echo "  Root: log held locally."
fi

echo "  Field witnessed. Proceeding."
echo ""
