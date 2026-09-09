#!/usr/bin/env python3
"""
Oceti Weave v3.0 - Zero-Dependency One-Shot Corpus Pipeline
Path: src/rag/corpus_pipeline.py
"""

import os
import sqlite3
import json
import urllib.request
import urllib.error
from pathlib import Path

# Configuration & Paths (defaults to your CachyOS environment)
DB_PATH = os.environ.get("DB_PATH", os.path.expanduser("~/memory_drum.db"))
CORPUS_DIR = os.environ.get("CORPUS_DIR", os.path.expanduser("~/projects/Human-AI/core/Autonomy/corpus"))
OLLAMA_EMBED_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434") + "/api/embeddings"
EMBED_MODEL = os.environ.get("EMBED_MODEL", "llama3.2:3b")

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64

def init_substrate():
    """Ensure parent directories and SQLite WAL tables exist."""
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(CORPUS_DIR).mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS corpus_chunks (
            chunk_id TEXT PRIMARY KEY,
            source_file TEXT,
            chunk_index INTEGER,
            content TEXT,
            embedding BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def get_embedding(text: str) -> list:
    """Fetch vector embedding from local Ollama service using standard library."""
    payload = json.dumps({"model": EMBED_MODEL, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_EMBED_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                return data.get("embedding", [])
    except Exception as e:
        print(f"Embedding error: {e}")
    return []

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Generator yielding text chunks."""
    start = 0
    while start < len(text):
        end = start + size
        yield text[start:end]
        start += size - overlap

def run_pipeline():
    init_substrate()
    corpus_path = Path(CORPUS_DIR)
    
    files = list(corpus_path.glob("**/*.md")) + list(corpus_path.glob("**/*.txt"))
    if not files:
        print(f"No markdown or text files found in {CORPUS_DIR}.")
        print("Drop some documents into the corpus directory and re-run.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for file_path in files:
        print(f"Processing: {file_path.name}")
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"Skipping {file_path.name}: {e}")
            continue
            
        for idx, chunk in enumerate(chunk_text(text)):
            chunk_id = f"{file_path.stem}_{idx}"
            
            cursor.execute("SELECT 1 FROM corpus_chunks WHERE chunk_id = ?", (chunk_id,))
            if cursor.fetchone():
                continue
                
            embedding = get_embedding(chunk)
            if not embedding:
                continue
                
            embedding_blob = json.dumps(embedding).encode("utf-8")
            cursor.execute("""
                INSERT OR REPLACE INTO corpus_chunks (chunk_id, source_file, chunk_index, content, embedding)
                VALUES (?, ?, ?, ?, ?)
            """, (chunk_id, str(file_path), idx, chunk, embedding_blob))
            
        conn.commit()
        
    conn.close()
    print("Corpus processing stream completed successfully.")

if __name__ == "__main__":
    run_pipeline()

