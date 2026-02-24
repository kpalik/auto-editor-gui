import subprocess
import os
from typing import Callable, Optional, List
import threading
import time

class AutoEditorWrapper:
    def __init__(self):
        self.current_process: Optional[subprocess.Popen] = None
        self.is_running = False
    
    def build_command(self, source_path: str, output_path: str,
                     margin_seconds: float, silent_threshold_db: float,
                     silent_speed: float, video_speed: float,
                     additional_args: List[str] = None) -> List[str]:
        cmd = [
            'auto-editor',
            source_path,
            '--margin', f'{margin_seconds}s',
            '--edit', f'audio:threshold={silent_threshold_db}dB',
            '--silent-speed', str(silent_speed),
            '--video-speed', str(video_speed),
            '--output', output_path
        ]
        
        if additional_args:
            cmd.extend(additional_args)
        
        return cmd
    
    def process_video(self, source_path: str, output_path: str,
                     margin_seconds: float, silent_threshold_db: float,
                     silent_speed: float, video_speed: float,
                     progress_callback: Callable[[str], None] = None,
                     additional_args: List[str] = None) -> tuple[bool, str]:
        cmd = self.build_command(
            source_path, output_path, margin_seconds, silent_threshold_db,
            silent_speed, video_speed, additional_args
        )
        
        try:
            self.is_running = True
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            output_lines = []
            
            for line in self.current_process.stdout:
                line = line.strip()
                if line:
                    output_lines.append(line)
                    if progress_callback:
                        progress_callback(line)
            
            self.current_process.wait()
            return_code = self.current_process.returncode
            
            self.is_running = False
            self.current_process = None
            
            full_output = '\n'.join(output_lines)
            
            if return_code == 0:
                return True, full_output
            else:
                return False, f"Process failed with code {return_code}\n{full_output}"
        
        except Exception as e:
            self.is_running = False
            self.current_process = None
            return False, f"Error: {str(e)}"
    
    def cancel_processing(self):
        if self.current_process and self.is_running:
            self.current_process.terminate()
            try:
                self.current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.current_process.kill()
            
            self.is_running = False
            self.current_process = None
    
    def is_auto_editor_available(self) -> bool:
        try:
            result = subprocess.run(
                ['auto-editor', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
