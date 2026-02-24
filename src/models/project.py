from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Project:
    id: int
    name: str
    description: str = ''
    color: str = '#3b82f6'
    output_folder: str = 'processed'
    margin_seconds: Optional[float] = None
    silent_threshold_db: Optional[float] = None
    silent_speed: Optional[float] = None
    video_speed: Optional[float] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            color=data.get('color', '#3b82f6'),
            output_folder=data.get('output_folder', 'processed'),
            margin_seconds=data.get('margin_seconds'),
            silent_threshold_db=data.get('silent_threshold_db'),
            silent_speed=data.get('silent_speed'),
            video_speed=data.get('video_speed'),
            created_at=data.get('created_at')
        )
