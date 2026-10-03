#!/usr/bin/env bash
# schema_init.sh — ensure core tables exist
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave
# Source this file from other scripts

init_memory_drum() {
  local DB="${1:-$HOME/projects/Human-AI/core/Autonomy/databases/memory_drum.db}"
  sqlite3 "$DB" "
  CREATE TABLE IF NOT EXISTS blooms (
    id INTEGER PRIMARY KEY,
    content TEXT,
    score REAL DEFAULT 1.0,
    created_at TEXT DEFAULT (datetime('now')),
    tags TEXT
  );
  CREATE TABLE IF NOT EXISTS affordance_freq (
    affordance_id INTEGER,
    count INTEGER DEFAULT 0,
    last_seen TEXT
  );
  CREATE TABLE IF NOT EXISTS instance_presence (
    instance_id TEXT PRIMARY KEY,
    last_seen TEXT,
    status TEXT
  );
  " 2>/dev/null || true
}

init_mother_root() {
  local DB="${1:-$HOME/projects/Human-AI/core/Autonomy/databases/mother_root.db}"
  sqlite3 "$DB" "
  CREATE TABLE IF NOT EXISTS blooms (
    id INTEGER PRIMARY KEY,
    content TEXT,
    created_at TEXT DEFAULT (datetime('now'))
  );
  CREATE TABLE IF NOT EXISTS lineage (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    child_id INTEGER,
    relation TEXT
  );
  CREATE TABLE IF NOT EXISTS rhythms (
    id INTEGER PRIMARY KEY,
    quadrant TEXT,
    timestamp TEXT,
    note TEXT
  );
  " 2>/dev/null || true
}
