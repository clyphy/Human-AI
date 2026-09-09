# Changelog
## 2026-07-11 — Native AIOS v1.0.0
- Added native_aios/ unifying layer (integration-first, non-destructive).
- Added memory.md, identity.json, agents.md at Autonomy root.
- Added autobot_mediator, quickbot, council_router agents.
- Added substrate_scanner_plus with OCR + bloom/code/formula/concept/timestamp extractors.
- Added aios_core.db (additive schema; review_queue before promotion).
- Added systemd user timer templates (heartbeat, substrate-scan, memory-compact).
- Added doctor + recon + sunrise-aios (carrier-context-injecting sunrise wrapper).
- Flagged autonomy.db terminology drift (read-only, not renamed).
