from dataclasses import dataclass
from typing import Optional

@dataclass
class Preset:
    id: int
    name: str
    description: str = ''
    margin_seconds: Optional[float] = None
    silent_threshold_db: Optional[float] = None
    silent_speed: Optional[float] = None
    video_speed: Optional[float] = None
    additional_args: Optional[str] = None
    is_default: bool = False
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            margin_seconds=data.get('margin_seconds'),
            silent_threshold_db=data.get('silent_threshold_db'),
            silent_speed=data.get('silent_speed'),
            video_speed=data.get('video_speed'),
            additional_args=data.get('additional_args'),
            is_default=data.get('is_default', False)
        )
