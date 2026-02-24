from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class QueueJob:
    id: int
    video_file_id: int
    preset_id: Optional[int] = None
    margin_seconds: Optional[float] = None
    silent_threshold_db: Optional[float] = None
    silent_speed: Optional[float] = None
    video_speed: Optional[float] = None
    output_filepath: str = ''
    status: str = 'pending'
    priority: int = 0
    added_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            video_file_id=data['video_file_id'],
            preset_id=data.get('preset_id'),
            margin_seconds=data.get('margin_seconds'),
            silent_threshold_db=data.get('silent_threshold_db'),
            silent_speed=data.get('silent_speed'),
            video_speed=data.get('video_speed'),
            output_filepath=data.get('output_filepath', ''),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 0),
            added_at=data.get('added_at'),
            started_at=data.get('started_at'),
            completed_at=data.get('completed_at'),
            error_message=data.get('error_message')
        )
