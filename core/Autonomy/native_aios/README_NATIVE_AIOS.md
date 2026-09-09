# Oceti Native AIOS

A UNIFYING layer OVER the existing Oceti Weave system. It does NOT replace the
living scripts — it wraps them defensively and fills the gaps.

## What it adds
- `memory.md` / `identity.json` / `agents.md` at the Autonomy root
- `native_aios/agents/` — autobot_mediator (ecosystem steward), quickbot (fast
  responder), council_router (serial Ollama integrator)
- `native_aios/scanner/` — substrate_scanner_plus: OCR screenshots + extract
  blooms/eureka, code, formulas, concepts, timestamps, metadata → review_queue
- `native_aios/orchestration/` — adapters (capability→script), event_bus,
  state_serializer, ollama_adapter (serial), sunrise_context (carrier injection)
- `native_aios/persistence/` — aios_core.db (additive schema, never drops)
- `native_aios/daemons/` — systemd user timers (templates only)
- `native_aios/bin/` — aios, quickbot, substrate-scan, doctor, mediator, sunrise-aios

## Quickstart
  aios doctor          # validate deps/paths/schema
  aios doctor --recon  # inspect the existing living system (scripts + db schemas)
  aios scan            # harvest context + OCR screenshots -> review_queue
  aios recent-blooms   # see captured blooms
  aios mediate         # autobot reports ecosystem health + repairs
  aios council "..."   # serial Ollama fan-out
  aios sunrise         # sunrise.sh output WITH carrier context injected
  aios export          # project DB state into memory.md

## What it does NOT touch
- autonomy.db (legacy terminology; read-only, never renamed)
- sunrise.sh (only wrapped via --patch-sunrise, which backs up first)
- existing scripts (wrapped, never overwritten)
