import sqlite3
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path: str = None):
        if db_path is None:
            app_dir = Path.home() / '.auto-editor-gui'
            app_dir.mkdir(exist_ok=True)
            db_path = str(app_dir / 'app.db')
        
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._initialize_database()
    
    def _initialize_database(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        schema_path = Path(__file__).parent / 'schema.sql'
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        self.conn.executescript(schema_sql)
        self.conn.commit()
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        cursor = self.conn.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        return row['value'] if row else default
    
    def set_setting(self, key: str, value: Any):
        self.conn.execute(
            'INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, ?)',
            (key, str(value), datetime.now())
        )
        self.conn.commit()
    
    def get_all_settings(self) -> Dict[str, str]:
        cursor = self.conn.execute('SELECT key, value FROM settings')
        return {row['key']: row['value'] for row in cursor.fetchall()}
    
    def create_project(self, name: str, description: str = '', color: str = '#3b82f6',
                      output_folder: str = 'processed', **settings) -> int:
        cursor = self.conn.execute(
            '''INSERT INTO projects (name, description, color, output_folder,
               margin_seconds, silent_threshold_db, silent_speed, video_speed)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (name, description, color, output_folder,
             settings.get('margin_seconds'), settings.get('silent_threshold_db'),
             settings.get('silent_speed'), settings.get('video_speed'))
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_project(self, project_id: int) -> Optional[Dict]:
        cursor = self.conn.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_projects(self) -> List[Dict]:
        cursor = self.conn.execute('SELECT * FROM projects ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]
    
    def update_project(self, project_id: int, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['name', 'description', 'color', 'output_folder',
                      'margin_seconds', 'silent_threshold_db', 'silent_speed', 'video_speed']:
                fields.append(f'{key} = ?')
                values.append(value)
        
        if fields:
            values.append(project_id)
            query = f'UPDATE projects SET {", ".join(fields)} WHERE id = ?'
            self.conn.execute(query, values)
            self.conn.commit()
    
    def delete_project(self, project_id: int):
        self.conn.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        self.conn.commit()
    
    def add_watch_folder(self, path: str, enabled: bool = True, default_project_id: int = None) -> int:
        cursor = self.conn.execute(
            'INSERT INTO watch_folders (path, enabled, default_project_id) VALUES (?, ?, ?)',
            (path, enabled, default_project_id)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_watch_folders(self, enabled_only: bool = False) -> List[Dict]:
        query = 'SELECT * FROM watch_folders'
        if enabled_only:
            query += ' WHERE enabled = 1'
        cursor = self.conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]
    
    def update_watch_folder(self, folder_id: int, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['path', 'enabled', 'default_project_id']:
                fields.append(f'{key} = ?')
                values.append(value)
        
        if fields:
            values.append(folder_id)
            query = f'UPDATE watch_folders SET {", ".join(fields)} WHERE id = ?'
            self.conn.execute(query, values)
            self.conn.commit()
    
    def delete_watch_folder(self, folder_id: int):
        self.conn.execute('DELETE FROM watch_folders WHERE id = ?', (folder_id,))
        self.conn.commit()
    
    def add_video_file(self, filepath: str, filename: str, project_id: int = None,
                      file_size: int = None, duration: float = None) -> int:
        cursor = self.conn.execute(
            '''INSERT INTO video_files (filepath, filename, project_id, file_size, duration)
               VALUES (?, ?, ?, ?, ?)''',
            (filepath, filename, project_id, file_size, duration)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_video_file(self, file_id: int) -> Optional[Dict]:
        cursor = self.conn.execute('SELECT * FROM video_files WHERE id = ?', (file_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_video_file_by_path(self, filepath: str) -> Optional[Dict]:
        cursor = self.conn.execute('SELECT * FROM video_files WHERE filepath = ?', (filepath,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_video_files(self, project_id: int = None, status: str = None) -> List[Dict]:
        query = 'SELECT * FROM video_files WHERE 1=1'
        params = []
        
        if project_id is not None:
            query += ' AND project_id = ?'
            params.append(project_id)
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        query += ' ORDER BY detected_at DESC'
        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def update_video_file(self, file_id: int, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['project_id', 'status', 'comment', 'file_size', 'duration']:
                fields.append(f'{key} = ?')
                values.append(value)
        
        if fields:
            values.append(file_id)
            query = f'UPDATE video_files SET {", ".join(fields)} WHERE id = ?'
            self.conn.execute(query, values)
            self.conn.commit()
    
    def delete_video_file(self, file_id: int):
        self.conn.execute('DELETE FROM video_files WHERE id = ?', (file_id,))
        self.conn.commit()
    
    def add_processed_output(self, video_file_id: int, output_filepath: str, output_filename: str,
                           margin_seconds: float, silent_threshold_db: float, silent_speed: float,
                           video_speed: float, **kwargs) -> int:
        cursor = self.conn.execute(
            '''INSERT INTO processed_outputs 
               (video_file_id, output_filepath, output_filename, margin_seconds,
                silent_threshold_db, silent_speed, video_speed, output_file_size,
                output_duration, processing_time_seconds, success, error_message, auto_editor_output)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (video_file_id, output_filepath, output_filename, margin_seconds,
             silent_threshold_db, silent_speed, video_speed,
             kwargs.get('output_file_size'), kwargs.get('output_duration'),
             kwargs.get('processing_time_seconds'), kwargs.get('success', True),
             kwargs.get('error_message'), kwargs.get('auto_editor_output'))
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_processed_outputs(self, video_file_id: int) -> List[Dict]:
        cursor = self.conn.execute(
            'SELECT * FROM processed_outputs WHERE video_file_id = ? ORDER BY processed_at DESC',
            (video_file_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def create_preset(self, name: str, description: str = '', **settings) -> int:
        cursor = self.conn.execute(
            '''INSERT INTO presets (name, description, margin_seconds, silent_threshold_db,
               silent_speed, video_speed, additional_args, is_default)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (name, description, settings.get('margin_seconds'), settings.get('silent_threshold_db'),
             settings.get('silent_speed'), settings.get('video_speed'),
             settings.get('additional_args'), settings.get('is_default', False))
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_preset(self, preset_id: int) -> Optional[Dict]:
        cursor = self.conn.execute('SELECT * FROM presets WHERE id = ?', (preset_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_presets(self) -> List[Dict]:
        cursor = self.conn.execute('SELECT * FROM presets ORDER BY is_default DESC, name')
        return [dict(row) for row in cursor.fetchall()]
    
    def update_preset(self, preset_id: int, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['name', 'description', 'margin_seconds', 'silent_threshold_db',
                      'silent_speed', 'video_speed', 'additional_args', 'is_default']:
                fields.append(f'{key} = ?')
                values.append(value)
        
        if fields:
            values.append(preset_id)
            query = f'UPDATE presets SET {", ".join(fields)} WHERE id = ?'
            self.conn.execute(query, values)
            self.conn.commit()
    
    def delete_preset(self, preset_id: int):
        self.conn.execute('DELETE FROM presets WHERE id = ?', (preset_id,))
        self.conn.commit()
    
    def add_to_queue(self, video_file_id: int, preset_id: int = None, output_filepath: str = '',
                    **settings) -> int:
        cursor = self.conn.execute(
            '''INSERT INTO processing_queue 
               (video_file_id, preset_id, margin_seconds, silent_threshold_db,
                silent_speed, video_speed, output_filepath, priority)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (video_file_id, preset_id, settings.get('margin_seconds'),
             settings.get('silent_threshold_db'), settings.get('silent_speed'),
             settings.get('video_speed'), output_filepath, settings.get('priority', 0))
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_queue_jobs(self, status: str = None) -> List[Dict]:
        query = 'SELECT * FROM processing_queue WHERE 1=1'
        params = []
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        query += ' ORDER BY priority DESC, added_at ASC'
        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def update_queue_job(self, job_id: int, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['status', 'started_at', 'completed_at', 'error_message',
                      'margin_seconds', 'silent_threshold_db', 'silent_speed', 'video_speed']:
                fields.append(f'{key} = ?')
                values.append(value)
        
        if fields:
            values.append(job_id)
            query = f'UPDATE processing_queue SET {", ".join(fields)} WHERE id = ?'
            self.conn.execute(query, values)
            self.conn.commit()
    
    def delete_queue_job(self, job_id: int):
        self.conn.execute('DELETE FROM processing_queue WHERE id = ?', (job_id,))
        self.conn.commit()
