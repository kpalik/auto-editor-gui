from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ProcessedOutput:
    id: int
    video_file_id: int
    output_filepath: str
    output_filename: str
    margin_seconds: float
    silent_threshold_db: float
    silent_speed: float
    video_speed: float
    output_file_size: Optional[int] = None
    output_duration: Optional[float] = None
    processing_time_seconds: Optional[float] = None
    processed_at: Optional[datetime] = None
    success: bool = True
    error_message: Optional[str] = None
    auto_editor_output: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            video_file_id=data['video_file_id'],
            output_filepath=data['output_filepath'],
            output_filename=data['output_filename'],
            margin_seconds=data['margin_seconds'],
            silent_threshold_db=data['silent_threshold_db'],
            silent_speed=data['silent_speed'],
            video_speed=data['video_speed'],
            output_file_size=data.get('output_file_size'),
            output_duration=data.get('output_duration'),
            processing_time_seconds=data.get('processing_time_seconds'),
            processed_at=data.get('processed_at'),
            success=data.get('success', True),
            error_message=data.get('error_message'),
            auto_editor_output=data.get('auto_editor_output')
        )
