from dataclasses import dataclass
from typing import Optional

@dataclass
class Settings:
    margin_seconds: float = 0.2
    silent_threshold_db: float = -28.0
    silent_speed: float = 99999.0
    video_speed: float = 1.0
    output_subfolder: str = 'processed'
    concurrent_jobs: int = 2
