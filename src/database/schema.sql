-- Global settings table
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects/Groups table
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    color TEXT,
    output_folder TEXT DEFAULT 'processed',
    margin_seconds REAL,
    silent_threshold_db REAL,
    silent_speed REAL,
    video_speed REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Watch folders table
CREATE TABLE IF NOT EXISTS watch_folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE NOT NULL,
    enabled BOOLEAN DEFAULT 1,
    default_project_id INTEGER,
    FOREIGN KEY (default_project_id) REFERENCES projects(id)
);

-- Video files table (source files)
CREATE TABLE IF NOT EXISTS video_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filepath TEXT UNIQUE NOT NULL,
    filename TEXT NOT NULL,
    project_id INTEGER,
    status TEXT DEFAULT 'new',
    comment TEXT,
    file_size INTEGER,
    duration REAL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Processed outputs table (one source can have multiple processed versions)
CREATE TABLE IF NOT EXISTS processed_outputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_file_id INTEGER NOT NULL,
    output_filepath TEXT NOT NULL,
    output_filename TEXT NOT NULL,
    margin_seconds REAL NOT NULL,
    silent_threshold_db REAL,
    silent_speed REAL,
    video_speed REAL NOT NULL,
    output_file_size INTEGER,
    output_duration REAL,
    processing_time_seconds REAL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT 1,
    error_message TEXT,
    auto_editor_output TEXT,
    FOREIGN KEY (video_file_id) REFERENCES video_files(id) ON DELETE CASCADE
);

-- Processing presets table
CREATE TABLE IF NOT EXISTS presets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    margin_seconds REAL,
    silent_threshold_db REAL,
    silent_speed REAL,
    video_speed REAL,
    additional_args TEXT,
    is_default BOOLEAN DEFAULT 0
);

-- Processing queue table
CREATE TABLE IF NOT EXISTS processing_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_file_id INTEGER NOT NULL,
    preset_id INTEGER,
    margin_seconds REAL,
    silent_threshold_db REAL,
    silent_speed REAL,
    video_speed REAL,
    output_filepath TEXT,
    status TEXT DEFAULT 'pending',
    priority INTEGER DEFAULT 0,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    FOREIGN KEY (video_file_id) REFERENCES video_files(id) ON DELETE CASCADE,
    FOREIGN KEY (preset_id) REFERENCES presets(id) ON DELETE SET NULL
);

-- Insert default global settings
INSERT OR IGNORE INTO settings (key, value) VALUES ('margin_seconds', '0.2');
INSERT OR IGNORE INTO settings (key, value) VALUES ('silent_threshold_db', '-28');
INSERT OR IGNORE INTO settings (key, value) VALUES ('silent_speed', '99999');
INSERT OR IGNORE INTO settings (key, value) VALUES ('video_speed', '1.0');
INSERT OR IGNORE INTO settings (key, value) VALUES ('output_subfolder', 'processed');
INSERT OR IGNORE INTO settings (key, value) VALUES ('concurrent_jobs', '2');

-- Insert default presets
INSERT OR IGNORE INTO presets (name, description, margin_seconds, silent_threshold_db, silent_speed, video_speed, is_default) 
VALUES ('Quick Silence Removal', 'Standard silence removal with balanced settings', 0.2, -28, 99999, 1.0, 1);

INSERT OR IGNORE INTO presets (name, description, margin_seconds, silent_threshold_db, silent_speed, video_speed, is_default) 
VALUES ('Aggressive', 'More aggressive silence detection', 0.1, -25, 99999, 1.0, 0);

INSERT OR IGNORE INTO presets (name, description, margin_seconds, silent_threshold_db, silent_speed, video_speed, is_default) 
VALUES ('Conservative', 'Preserve more audio, less aggressive', 0.3, -30, 99999, 1.0, 0);

INSERT OR IGNORE INTO presets (name, description, margin_seconds, silent_threshold_db, silent_speed, video_speed, is_default) 
VALUES ('Speed Up', 'Remove silence and speed up video', 0.2, -28, 99999, 1.2, 0);
