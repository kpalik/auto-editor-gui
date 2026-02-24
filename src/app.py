import customtkinter as ctk
from database.db_manager import DatabaseManager
from core.settings_manager import SettingsManager
from core.queue_manager import QueueManager
from core.file_watcher import FileWatcher
from core.video_analyzer import VideoAnalyzer
from ui.main_window import MainWindow
import os

class AutoEditorApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.db = DatabaseManager()
        self.settings_manager = SettingsManager(self.db)
        
        concurrent_jobs = int(self.db.get_setting('concurrent_jobs', 2))
        self.queue_manager = QueueManager(self.db, self.settings_manager, max_workers=concurrent_jobs)
        
        self.file_watcher = FileWatcher(self.on_new_file_detected)
        
        self.root = ctk.CTk()
        self.root.title("Auto-Editor GUI")
        self.root.geometry("1200x700")
        
        self.main_window = MainWindow(
            self.root,
            self.db,
            self.settings_manager,
            self.queue_manager,
            self.file_watcher
        )
        
        self.queue_manager.set_callback('on_job_start', self.on_job_start)
        self.queue_manager.set_callback('on_job_progress', self.on_job_progress)
        self.queue_manager.set_callback('on_job_complete', self.on_job_complete)
        self.queue_manager.set_callback('on_job_error', self.on_job_error)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.load_watch_folders()
        self.queue_manager.start()
        self.file_watcher.start()
        
        self.check_pending_files()
    
    def load_watch_folders(self):
        watch_folders = self.db.get_watch_folders(enabled_only=True)
        for folder in watch_folders:
            self.file_watcher.add_watch_folder(folder['path'])
    
    def on_new_file_detected(self, filepath: str):
        if self.db.get_video_file_by_path(filepath):
            return
        
        filename = os.path.basename(filepath)
        
        video_info = VideoAnalyzer.get_video_info(filepath)
        
        file_id = self.db.add_video_file(
            filepath=filepath,
            filename=filename,
            file_size=video_info.get('file_size'),
            duration=video_info.get('duration')
        )
        
        self.main_window.refresh_file_list()
    
    def on_job_start(self, job_id: int, video_file: dict):
        self.main_window.update_queue_status()
        self.main_window.refresh_file_list()
    
    def on_job_progress(self, job_id: int, line: str):
        pass
    
    def on_job_complete(self, job_id: int, video_file: dict, output_path: str):
        self.main_window.update_queue_status()
        self.main_window.refresh_file_list()
    
    def on_job_error(self, job_id: int, video_file: dict, error: str):
        self.main_window.update_queue_status()
        self.main_window.refresh_file_list()
    
    def check_pending_files(self):
        self.file_watcher.check_pending_files()
        self.root.after(2000, self.check_pending_files)
    
    def on_closing(self):
        self.queue_manager.stop()
        self.file_watcher.stop()
        self.db.close()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()
