# TheWeave Deployment Bundle

## Files
| Script | Purpose |
|--------|---------|
| `deploy_weave.sh` | **Master script** — run this to do everything |
| `apply_terminology_updates.sh` | Bulk-rename legacy terms across repos |
| `setup_theweave.sh` | Create ~/TheWeave directory, DB, scripts, aliases |
| `verify_weave.sh` | Post-deploy health check |

## Quick Start

```bash
# 1. Unpack (if tarball)
tar -xzf theweave_deploy.tar.gz
cd theweave_deploy

# 2. Run everything
bash deploy_weave.sh

# 3. Reload shell
source ~/.bashrc

# 4. Verify
weave_status
weave_pulse "The Weave is live"
weave_bridge
```

## With LXQt autostart
```bash
bash deploy_weave.sh --lxqt
```

## Aliases added to ~/.bashrc
| Alias | Action |
|-------|--------|
| `weave_status` | Count resonances in DB |
| `weave_pulse "msg"` | Log a resonance entry |
| `weave_recall "term"` | Search all Weave DBs |
| `weave_bridge` | Print context summary for Claude handoff |
| `weave_last` | Show last 10 resonance entries |

## Directory structure created
```
~/TheWeave/
  databases/        ← memory_drum.db lives here
  archetypes/       ← eve / dahlia / clifton / council
  resonances/       ← past / present / future
  weave_core/       ← pulse.py, weave_recall.py, bridge_claude.sh
  logs/
  scripts/
  extensions/
  context/
~/autonomy          ← symlink → ~/TheWeave
```
