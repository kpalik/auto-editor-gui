from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class VideoFile:
    id: int
    filepath: str
    filename: str
    project_id: Optional[int] = None
    status: str = 'new'
    comment: str = ''
    file_size: Optional[int] = None
    duration: Optional[float] = None
    detected_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            filepath=data['filepath'],
            filename=data['filename'],
            project_id=data.get('project_id'),
            status=data.get('status', 'new'),
            comment=data.get('comment', ''),
            file_size=data.get('file_size'),
            duration=data.get('duration'),
            detected_at=data.get('detected_at')
        )
    
    def get_status_emoji(self) -> str:
        status_emojis = {
            'new': '🆕',
            'queued': '⏳',
            'processing': '⚡',
            'completed': '✓',
            'failed': '❌',
            'archived': '📦'
        }
        return status_emojis.get(self.status, '❓')
