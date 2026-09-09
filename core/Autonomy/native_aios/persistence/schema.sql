-- Native AIOS core schema. CREATE TABLE IF NOT EXISTS only — never drops.
CREATE TABLE IF NOT EXISTS scan_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  started_at TEXT NOT NULL,
  finished_at TEXT,
  root TEXT,
  files_scanned INTEGER DEFAULT 0,
  images_ocrd INTEGER DEFAULT 0,
  findings INTEGER DEFAULT 0,
  ocr_engine TEXT,
  status TEXT
);
CREATE TABLE IF NOT EXISTS sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id INTEGER REFERENCES scan_runs(id),
  path TEXT NOT NULL,
  sha256 TEXT,
  size INTEGER,
  mtime TEXT,
  ext TEXT,
  source_type TEXT,            -- text | image | ocr
  ocr_engine TEXT,
  image_w INTEGER, image_h INTEGER,
  git_repo TEXT, git_branch TEXT, git_commit TEXT,
  scanned_at TEXT NOT NULL,
  UNIQUE(sha256)
);
CREATE TABLE IF NOT EXISTS extracted_text (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER REFERENCES sources(id),
  line_start INTEGER, line_end INTEGER,
  content TEXT,
  content_hash TEXT,
  UNIQUE(source_id, content_hash)
);
CREATE TABLE IF NOT EXISTS review_queue (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER REFERENCES sources(id),
  kind TEXT NOT NULL,            -- bloom | code | formula | concept | timestamp | metadata
  content TEXT,
  score REAL DEFAULT 0,
  context TEXT,                  -- surrounding lines
  line_start INTEGER, line_end INTEGER,
  terminology_flags TEXT,        -- json array of legacy terms found
  redacted INTEGER DEFAULT 0,
  status TEXT DEFAULT 'pending', -- pending | promoted | dismissed
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS blooms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER REFERENCES sources(id),
  content TEXT, trigger TEXT, score REAL, dL REAL,
  promoted_at TEXT
);
CREATE TABLE IF NOT EXISTS code_snippets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER REFERENCES sources(id),
  language TEXT, content TEXT, content_hash TEXT, line_start INTEGER, line_end INTEGER,
  UNIQUE(content_hash)
);
CREATE TABLE IF NOT EXISTS formulas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER REFERENCES sources(id),
  content TEXT, content_hash TEXT, line_start INTEGER
);
CREATE TABLE IF NOT EXISTS concepts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER REFERENCES sources(id),
  term TEXT, definition TEXT, occurrence_count INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS timestamps (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER REFERENCES sources(id),
  raw TEXT, iso TEXT, line INTEGER
);
CREATE TABLE IF NOT EXISTS metadata_kv (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER REFERENCES sources(id),
  key TEXT, value TEXT
);
CREATE TABLE IF NOT EXISTS agent_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  at TEXT NOT NULL, agent TEXT, event TEXT, detail TEXT, ok INTEGER
);
CREATE TABLE IF NOT EXISTS heartbeats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  at TEXT NOT NULL, db_ok INTEGER, ollama_ok INTEGER, disk_pct REAL, note TEXT
);
CREATE TABLE IF NOT EXISTS resonances (
  id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT, name TEXT, direction TEXT, note TEXT
);
CREATE TABLE IF NOT EXISTS affordances (
  id INTEGER PRIMARY KEY AUTOINCREMENT, point INTEGER, holder TEXT, text TEXT, at TEXT
);
CREATE TABLE IF NOT EXISTS legacy_sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, kind TEXT, note TEXT, inspected_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_rq_status ON review_queue(status);
CREATE INDEX IF NOT EXISTS idx_sources_sha ON sources(sha256);
CREATE INDEX IF NOT EXISTS idx_et_search ON extracted_text(content);
