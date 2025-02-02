CREATE TABLE IF NOT EXISTS todo (
    id INTEGER PRIMARY KEY,
    uuid TEXT UNIQUE NOT NULL,
    contents TEXT NOT NULL,
    tags TEXT,
    state TEXT NOT NULL,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    state_updated_at REAL NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_todo_uuid ON todo (uuid);
CREATE INDEX IF NOT EXISTS idx_todo_state ON todo (state);
CREATE INDEX IF NOT EXISTS idx_todo_created_at ON todo (created_at);

CREATE VIRTUAL TABLE IF NOT EXISTS fts_todo USING fts5(
    contents,
    content=todo,
    content_rowid=id
);

CREATE VIRTUAL TABLE IF NOT EXISTS fts_tag USING fts5(
    tags,
    content=todo,
    content_rowid=id
);

CREATE TRIGGER IF NOT EXISTS todo_ai AFTER INSERT ON todo BEGIN
    INSERT INTO fts_todo(rowid, contents) VALUES (new.id, new.contents);
    INSERT INTO fts_tag(rowid, tags) VALUES (new.id, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS todo_ad AFTER DELETE ON todo BEGIN
    INSERT INTO fts_todo(fts_todo, rowid, contents) VALUES ('delete', old.id, old.contents);
    INSERT INTO fts_tag(fts_tag, rowid, tags) VALUES ('delete', old.id, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS todo_au_todo AFTER UPDATE OF contents ON todo BEGIN
    INSERT INTO fts_todo(fts_todo, rowid, contents) VALUES ('delete', old.id, old.contents);
    INSERT INTO fts_todo(rowid, contents) VALUES (new.id, new.contents);
END;

CREATE TRIGGER IF NOT EXISTS todo_au_tag AFTER UPDATE OF tags ON todo BEGIN
    INSERT INTO fts_tag(fts_tag, rowid, tags) VALUES ('delete', old.id, old.tags);
    INSERT INTO fts_tag(rowid, tags) VALUES (new.id, new.tags);
END;

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    uuid TEXT UNIQUE NOT NULL,
    tag TEXT UNIQUE NOT NULL,
    created_at REAL NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_tags_tag ON tags (tag);
