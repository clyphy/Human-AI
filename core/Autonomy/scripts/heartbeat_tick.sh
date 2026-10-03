#!/usr/bin/env bash
set -e
set -u
set -o pipefail

# Pure Bash tracking anchor mapping
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export AIOS_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "heartbeat_tick: AIOS_ROOT anchored cleanly at ${AIOS_ROOT}"
