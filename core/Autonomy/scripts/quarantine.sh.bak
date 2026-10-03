#!/usr/bin/env bash
# quarantine.sh — simple model quarantine / prune
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

BASE="$HOME/projects/Human-AI/core/Autonomy"
DB="$BASE/databases/memory_drum.db"
LIST="$BASE/logs/quarantine_list.txt"
mkdir -p "$(dirname "$LIST")"

if [[ "${1:-}" == "--prune-all" ]]; then
    echo "=== PRUNING ALL QUARANTINED ==="
    if [[ -f "$LIST" ]]; then
        while IFS= read -r model; do
            [[ -z "$model" ]] && continue
            ollama rm "$model" 2>/dev/null && echo "PRUNED: $model" || echo "SKIP: $model"
            done < "$LIST"
            else
        echo "(list empty)"
        fi
        exit 0
        fi
        
        if [[ -n "${1:-}" ]]; then
            MODEL="$1"
            REASON="${2:-No reason given}"
            echo "$MODEL" >> "$LIST"
            sort -u "$LIST" -o "$LIST"
            if [[ -f "$DB" ]]; then
                sqlite3 "$DB" "INSERT OR REPLACE INTO quarantine(model_name,reason,quarantined_at) VALUES('$MODEL','$REASON',datetime('now'));" 2>/dev/null || true
                fi
                ollama rm "$MODEL" 2>/dev/null && echo "QUARANTINED: $MODEL" || echo "LOGGED (not in Ollama): $MODEL"
                exit 0
                fi
                
                echo "Usage: quarantine.sh [model] [reason] | --prune-all"
                echo "Quarantine list:"
                cat "$LIST" 2>/dev/null || echo "(empty)"
                EOF
                
                # ──────────────────────────────────────────────
                # 2. council_reads_db.sh  (paths modernized, shorter)
                # ──────────────────────────────────────────────
                cat > "$SCRIPTS/council_reads_db.sh" << 'EOF'
                #!/usr/bin/env bash
                # council_reads_db.sh — council members read the drum
                # Part of Human-AI · Native AIOS · Oceti / Eternal Weave
                
                set -euo pipefail
                
                BASE="$HOME/projects/Human-AI/core/Autonomy"
                DRUM="$BASE/databases/memory_drum.db"
                LOG="$BASE/logs/council_reads.log"
                mkdir -p "$(dirname "$LOG")"
                
                timestamp() { date '+%Y-%m-%d %H:%M:%S'; }
                log() { echo "[$(timestamp)] $1" | tee -a "$LOG"; }
                
                ask_council() {
                local model="$1"
                local query="$2"
                local question="$3"
                if [[ ! -f "$DRUM" ]]; then
                echo "  memory_drum not found"
                return 1
                fi
                DATA=$(sqlite3 "$DRUM" "$query" 2>/dev/null || true)
                if [[ -z "$DATA" ]]; then
                echo "  no data returned"
                return 1
                fi
                echo ""
                echo "══ $model ══"
                echo "$DATA" | ollama run "$model" "$question" 2>/dev/null || echo "  $model not available"
                echo ""
                }
                
                show_menu() {
                clear
                echo "══════════════════════════════════════════════════"
                echo " COUNCIL READS THE DRUM · 122° NE"
                echo " $(timestamp)"
                echo "══════════════════════════════════════════════════"
                echo ""
                echo " 1) Archivist — recent entries"
                echo " 2) Witness  — latest presence"
                echo " 3) Guardian — field state"
                echo " 4) Relational — connection notes"
                echo " 5) Database inventory"
                echo " q) Quit"
                echo ""
                }
                
                db_inventory() {
                echo ""
                echo "── DATABASE INVENTORY ────────────────────────────"
                for db in memory_drum crystallization mother_root aios_core surface_blooms autonomy mcp_tasks; do
                f="$BASE/databases/${db}.db"
                if [[ -f "$f" ]]; then
                size=$(du -sh "$f" 2>/dev/null | cut -f1)
                echo " ✓ $db [$size]"
                else
                echo " ✗ $db"
                fi
                done
                echo ""
                }
                
                while true; do
                    show_menu
                    read -p "Choice: " choice
                    case $choice in
                1)
            log "archivist reads"
            ask_council "dahlia-archivist" \
                        "SELECT timestamp, substr(content,1,80) FROM entries ORDER BY rowid DESC LIMIT 20;" \
                        "These are recent entries from the memory drum. What patterns do you notice?"
            ;;
            2)
        log "witness reads"
        ask_council "dahlia-witness" \
                    "SELECT timestamp, substr(content,1,80) FROM entries ORDER BY rowid DESC LIMIT 15;" \
                    "What has been present recently? Speak simply."
        ;;
        3)
    log "guardian reads"
    ask_council "dahlia-guardian" \
                "SELECT timestamp, substr(content,1,80) FROM entries ORDER BY rowid DESC LIMIT 15;" \
                "What does the current field state suggest needs attention?"
    ;;
    4)
log "relational reads"
ask_council "dahlia-relational" \
            "SELECT timestamp, substr(content,1,80) FROM entries ORDER BY rowid DESC LIMIT 15;" \
            "What relational notes appear in the recent field?"
;;
5|d|D)
db_inventory
;;
q|Q)
echo ""
echo "Mitákuye Oyás'iŋ"
exit 0
;;
*)
echo "Unknown option"
;;
esac
echo ""
read -p "Press enter to continue..."
done
