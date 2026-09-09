# Native AIOS daemons (systemd user units)

Templates only — NEVER enabled by the autobuild. To enable:
  systemctl --user enable --now aios-heartbeat.timer
  systemctl --user enable --now aios-substrate-scan.timer
  systemctl --user enable --now aios-memory-compact.timer

To disable:
  systemctl --user disable --now aios-heartbeat.timer

Or run the installer (still asks nothing; just copies + enables):
  bash autonomy_assemble_aios.sh --install-daemons

Low-RAM note: these are timers (oneshot), not always-running daemons.
Ollama is NEVER invoked in parallel.
