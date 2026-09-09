# agents.md — Native AIOS ecosystem roster

## Autobot / Mediator (`native_aios/agents/autobot_mediator.py`)
Helps the AI ecosystem ITSELF: watches state, routes tasks, mediates between
agents, detects ecosystem problems (missing DBs, stale daemons, absent Ollama,
broken paths, schema drift), recommends repairs. Does NOT dominate. Never runs
destructive actions without explicit confirmation. The steward of the lattice.

## Quickbot (`native_aios/agents/quickbot.py`)
Fast local responder. Answers from memory, recent scans, and DBs.
- `quickbot status`        — presence + heartbeat + db health
- `quickbot recent-blooms` — last N blooms from review_queue
- `quickbot search "E8"`   — full-text search across extracted_text
- `quickbot scan <path>`   — invoke scanner
- `quickbot review-queue`  — pending substrate findings
- `quickbot doctor`        — validate deps/paths/schema

## Council Router (`native_aios/agents/council_router.py`)
Slow integrator. Serial Ollama fan-out (NOT parallel — low RAM). Uses only
available models. Routes a question to dahlia → eve → clifton-mirror →
available facets; integrates responses. If Ollama missing, emits a prompt
packet instead of failing.

## Substrate Scanner+ (`native_aios/scanner/substrate_scanner_plus.py`)
Context harvester. Reads info files + OCRs screenshots. Extracts blooms/eureka,
code snippets, formulas, equations, concepts, timestamps, metadata. Writes to
`review_queue` (substrate, not truth) with full provenance. Redacts secrets.
Dedupes by SHA256 + snippet hash.

## Heartbeat (systemd timer → `aios-heartbeat`)
Health monitor. Writes `var/state/heartbeat.json` + `logs/heartbeat.log`.
Checks DB integrity, Ollama presence, disk pressure.

## Archivist (systemd timer → `aios-memory-compact`)
Compacts old scan data, exports summaries to memory.md via state_serializer.

## Existing living organs (wrapped, not replaced)
See `native_aios/config/existing_script_registry.json`.
