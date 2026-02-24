import os
from pathlib import Path
from typing import Tuple

class OutputManager:
    @staticmethod
    def generate_output_filename(source_path: str, margin_sec: float, 
                                 db: float, speed: float) -> str:
        name, ext = os.path.splitext(os.path.basename(source_path))
        margin_ms = int(margin_sec * 1000)
        speed_int = int(speed * 100)
        db_int = abs(int(db))
        
        return f"{name}_processed_{speed_int}speed_{db_int}dB_{margin_ms}msmargin{ext}"
    
    @staticmethod
    def generate_output_path(source_path: str, project_output_folder: str,
                           margin_sec: float, db: float, speed: float) -> Tuple[str, str]:
        source_dir = os.path.dirname(source_path)
        output_dir = os.path.join(source_dir, project_output_folder)
        
        os.makedirs(output_dir, exist_ok=True)
        
        output_filename = OutputManager.generate_output_filename(
            source_path, margin_sec, db, speed
        )
        output_path = os.path.join(output_dir, output_filename)
        
        return output_path, output_filename
    
    @staticmethod
    def get_project_output_folder(project_id: int, db_manager) -> str:
        if project_id:
            project = db_manager.get_project(project_id)
            if project and project.get('output_folder'):
                return project['output_folder']
        
        return db_manager.get_setting('output_subfolder', 'processed')
