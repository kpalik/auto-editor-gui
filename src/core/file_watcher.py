import os
import time
from pathlib import Path
from typing import Callable, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from .video_analyzer import VideoAnalyzer

class VideoFileHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.pending_files = {}
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        filepath = event.src_path
        
        if VideoAnalyzer.is_video_file(filepath):
            self.pending_files[filepath] = time.time()
    
    def check_pending_files(self):
        current_time = time.time()
        completed_files = []
        
        for filepath, added_time in list(self.pending_files.items()):
            if current_time - added_time > 2:
                if os.path.exists(filepath):
                    try:
                        initial_size = os.path.getsize(filepath)
                        time.sleep(0.5)
                        final_size = os.path.getsize(filepath)
                        
                        if initial_size == final_size and final_size > 0:
                            completed_files.append(filepath)
                            del self.pending_files[filepath]
                    except (OSError, FileNotFoundError):
                        del self.pending_files[filepath]
                else:
                    del self.pending_files[filepath]
        
        for filepath in completed_files:
            self.callback(filepath)

class FileWatcher:
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.observer = Observer()
        self.handlers = {}
        self.is_running = False
    
    def add_watch_folder(self, folder_path: str):
        if not os.path.exists(folder_path):
            return False
        
        if folder_path in self.handlers:
            return True
        
        handler = VideoFileHandler(self.callback)
        self.handlers[folder_path] = handler
        self.observer.schedule(handler, folder_path, recursive=False)
        
        return True
    
    def remove_watch_folder(self, folder_path: str):
        if folder_path in self.handlers:
            del self.handlers[folder_path]
    
    def start(self):
        if not self.is_running:
            self.observer.start()
            self.is_running = True
    
    def stop(self):
        if self.is_running:
            self.observer.stop()
            self.observer.join()
            self.is_running = False
    
    def check_pending_files(self):
        for handler in self.handlers.values():
            handler.check_pending_files()
    
    def scan_existing_files(self, folder_path: str) -> List[str]:
        video_files = []
        
        if not os.path.exists(folder_path):
            return video_files
        
        try:
            for item in os.listdir(folder_path):
                filepath = os.path.join(folder_path, item)
                if os.path.isfile(filepath) and VideoAnalyzer.is_video_file(filepath):
                    video_files.append(filepath)
        except (OSError, PermissionError):
            pass
        
        return video_files
