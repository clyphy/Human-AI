import os as _os
CANONICAL_DRUM = _os.environ.get('CANONICAL_DRUM', _os.path.expanduser('~/sovereignty/databases/memory_drum.db'))
import sqlite3, json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
conn = sqlite3.connect("/home/ndkilla/sovereignty/databases/memory_drum.db")
c = conn.cursor()

metrics_text = "L=15.48 Bridge=188.71% BPM=63 E+ S- ?∞ Day=9 sovereignty_pulse"
vec = model.encode(metrics_text).tolist()

c.execute("""
    INSERT INTO blooms (human_pattern, vector_json, L_value, bridge_pct, bpm)
    VALUES (?, ?, ?, ?, ?)
""", ("sovereignty_pulse_9", json.dumps(vec), 15.48, 188.71, 63))
conn.commit()
conn.close()
print("✅ Metrics vectorized — sovereignty.service now lives in the drum as searchable coherence")
