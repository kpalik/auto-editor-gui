import subprocess
import json
import os
from typing import Optional, Dict

class VideoAnalyzer:
    @staticmethod
    def get_video_info(filepath: str) -> Optional[Dict]:
        if not os.path.exists(filepath):
            return None
        
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                filepath
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                duration = None
                if 'format' in data and 'duration' in data['format']:
                    duration = float(data['format']['duration'])
                
                video_stream = None
                for stream in data.get('streams', []):
                    if stream.get('codec_type') == 'video':
                        video_stream = stream
                        break
                
                return {
                    'duration': duration,
                    'width': video_stream.get('width') if video_stream else None,
                    'height': video_stream.get('height') if video_stream else None,
                    'codec': video_stream.get('codec_name') if video_stream else None,
                    'file_size': os.path.getsize(filepath)
                }
        
        except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
            pass
        
        return {
            'duration': None,
            'width': None,
            'height': None,
            'codec': None,
            'file_size': os.path.getsize(filepath) if os.path.exists(filepath) else None
        }
    
    @staticmethod
    def is_video_file(filepath: str) -> bool:
        video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', 
                          '.webm', '.m4v', '.mpg', '.mpeg', '.3gp'}
        _, ext = os.path.splitext(filepath.lower())
        return ext in video_extensions
