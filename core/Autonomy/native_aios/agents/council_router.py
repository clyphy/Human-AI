import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""Council router — SERIAL Ollama fan-out (low RAM, never parallel)."""
import sys, json
from paths import NATIVE, ROOT
from orchestration import ollama_adapter, event_bus
from orchestration.sunrise_context import with_context
PREFERRED=['dahlia','eve','clifton-mirror','qwen2.5:3b','llama3.2:3b','llama3.2:latest']
def ask(question):
    if not ollama_adapter.available():
        packet = with_context(question)
        print("[council] Ollama unavailable — prompt packet:\n"+packet)
        event_bus.emit('council_router','ask','prompt_packet',ok=True); return packet
    model=ollama_adapter.first_available(PREFERRED)
    if not model:
        print("[council] no models installed — prompt packet:\n"+with_context(question)); return
    print(f"[council] routing to {model} (serial)...")
    out,err=ollama_adapter.run(model, with_context(question))
    print(out or f"(no output / {err})")
    event_bus.emit('council_router','ask',f'model={model}',ok=bool(out))
    return out
def main():
    q=' '.join(sys.argv[1:]) or "State the current field posture and terminology canon."
    ask(q)
if __name__=='__main__': main()
