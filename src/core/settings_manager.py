from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ProcessingSettings:
    margin_seconds: float
    silent_threshold_db: float
    silent_speed: float
    video_speed: float
    output_subfolder: str = 'processed'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'margin_seconds': self.margin_seconds,
            'silent_threshold_db': self.silent_threshold_db,
            'silent_speed': self.silent_speed,
            'video_speed': self.video_speed,
            'output_subfolder': self.output_subfolder
        }

class SettingsManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get_global_settings(self) -> ProcessingSettings:
        settings = self.db.get_all_settings()
        return ProcessingSettings(
            margin_seconds=float(settings.get('margin_seconds', 0.2)),
            silent_threshold_db=float(settings.get('silent_threshold_db', -28)),
            silent_speed=float(settings.get('silent_speed', 99999)),
            video_speed=float(settings.get('video_speed', 1.0)),
            output_subfolder=settings.get('output_subfolder', 'processed')
        )
    
    def set_global_settings(self, **kwargs):
        for key, value in kwargs.items():
            if key in ['margin_seconds', 'silent_threshold_db', 'silent_speed', 
                      'video_speed', 'output_subfolder']:
                self.db.set_setting(key, value)
    
    def get_project_settings(self, project_id: int) -> Optional[Dict[str, Any]]:
        project = self.db.get_project(project_id)
        if not project:
            return None
        
        return {
            'margin_seconds': project.get('margin_seconds'),
            'silent_threshold_db': project.get('silent_threshold_db'),
            'silent_speed': project.get('silent_speed'),
            'video_speed': project.get('video_speed'),
            'output_subfolder': project.get('output_folder')
        }
    
    def resolve_settings(self, video_file_id: int = None, project_id: int = None,
                        job_overrides: Dict[str, Any] = None) -> ProcessingSettings:
        global_settings = self.get_global_settings()
        result = global_settings.to_dict()
        
        if video_file_id:
            video_file = self.db.get_video_file(video_file_id)
            if video_file and video_file.get('project_id'):
                project_id = video_file['project_id']
        
        if project_id:
            project_settings = self.get_project_settings(project_id)
            if project_settings:
                for key, value in project_settings.items():
                    if value is not None:
                        result[key] = value
        
        if job_overrides:
            for key, value in job_overrides.items():
                if value is not None and key in result:
                    result[key] = value
        
        return ProcessingSettings(**result)
    
    def get_settings_source(self, video_file_id: int = None, project_id: int = None,
                           job_overrides: Dict[str, Any] = None) -> Dict[str, str]:
        sources = {
            'margin_seconds': 'Global',
            'silent_threshold_db': 'Global',
            'silent_speed': 'Global',
            'video_speed': 'Global',
            'output_subfolder': 'Global'
        }
        
        if video_file_id:
            video_file = self.db.get_video_file(video_file_id)
            if video_file and video_file.get('project_id'):
                project_id = video_file['project_id']
        
        if project_id:
            project_settings = self.get_project_settings(project_id)
            if project_settings:
                for key, value in project_settings.items():
                    if value is not None:
                        sources[key] = 'Project'
        
        if job_overrides:
            for key, value in job_overrides.items():
                if value is not None and key in sources:
                    sources[key] = 'Job'
        
        return sources
