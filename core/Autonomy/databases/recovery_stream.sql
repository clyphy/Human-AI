.dbconfig defensive off
BEGIN;
PRAGMA writable_schema = on;
PRAGMA foreign_keys = off;
PRAGMA encoding = 'UTF-8';
PRAGMA page_size = '4096';
PRAGMA auto_vacuum = '0';
PRAGMA user_version = '0';
PRAGMA application_id = '0';
CREATE TABLE tasks (                     id        INTEGER PRIMARY KEY,                     agent     TEXT,                     task      TEXT,                     model     TEXT,                     status    TEXT DEFAULT 'pending',                     result    TEXT,                     l_at_time REAL,                     created   TIMESTAMP DEFAULT CURRENT_TIMESTAMP                 );
PRAGMA writable_schema = off;
COMMIT;
