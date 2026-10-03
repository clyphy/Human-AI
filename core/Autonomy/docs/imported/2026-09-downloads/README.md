# Imported September 2026 Reference Material

These files were curated from `~/projects/Human-AI/Downloads` on 2026-09-16.

They are preserved as historical/design reference material. They are not, by
themselves, authoritative runtime configuration.

Use current audited configuration and executable tests as operational authority:

- Canonical Memory Drum: `databases/memory_drum.db`
- Drum status checker: `scripts/daily_drum_check.py`
- Ollama model store: `~/projects/Human-AI/.ollama`
- Ollama API binding: `127.0.0.1:11434`
- Verified runtime checks: `python3 -m pytest -q tests/`,
  `./scripts/check_e8.sh`, and `./scripts/check_cap.sh`

Before acting on any path, command, database schema, model roster, service,
or deployment instruction in the imported files, validate it against the
current repository and system audit.
