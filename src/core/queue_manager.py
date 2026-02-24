import threading
import time
from datetime import datetime
from typing import Callable, Optional
from queue import Queue
from .auto_editor_wrapper import AutoEditorWrapper
from .output_manager import OutputManager

class QueueManager:
    def __init__(self, db_manager, settings_manager, max_workers: int = 2):
        self.db = db_manager
        self.settings_manager = settings_manager
        self.max_workers = max_workers
        self.workers = []
        self.is_running = False
        self.is_paused = False
        self.job_queue = Queue()
        self.active_jobs = {}
        self.callbacks = {
            'on_job_start': None,
            'on_job_progress': None,
            'on_job_complete': None,
            'on_job_error': None
        }
    
    def set_callback(self, event: str, callback: Callable):
        if event in self.callbacks:
            self.callbacks[event] = callback
    
    def start(self):
        if not self.is_running:
            self.is_running = True
            for i in range(self.max_workers):
                worker = threading.Thread(target=self._worker_loop, daemon=True)
                worker.start()
                self.workers.append(worker)
    
    def stop(self):
        self.is_running = False
        for worker in self.workers:
            if worker.is_alive():
                worker.join(timeout=1)
        self.workers.clear()
    
    def pause(self):
        self.is_paused = True
    
    def resume(self):
        self.is_paused = False
    
    def add_job(self, video_file_id: int, preset_id: int = None, **job_settings):
        video_file = self.db.get_video_file(video_file_id)
        if not video_file:
            return None
        
        settings = self.settings_manager.resolve_settings(
            video_file_id=video_file_id,
            job_overrides=job_settings
        )
        
        output_folder = OutputManager.get_project_output_folder(
            video_file['project_id'], self.db
        )
        
        output_path, output_filename = OutputManager.generate_output_path(
            video_file['filepath'],
            output_folder,
            settings.margin_seconds,
            settings.silent_threshold_db,
            settings.video_speed
        )
        
        job_id = self.db.add_to_queue(
            video_file_id=video_file_id,
            preset_id=preset_id,
            output_filepath=output_path,
            margin_seconds=settings.margin_seconds,
            silent_threshold_db=settings.silent_threshold_db,
            silent_speed=settings.silent_speed,
            video_speed=settings.video_speed,
            priority=job_settings.get('priority', 0)
        )
        
        self.db.update_video_file(video_file_id, status='queued')
        
        return job_id
    
    def cancel_job(self, job_id: int):
        if job_id in self.active_jobs:
            wrapper = self.active_jobs[job_id]
            wrapper.cancel_processing()
        
        self.db.update_queue_job(job_id, status='cancelled')
    
    def _worker_loop(self):
        while self.is_running:
            if self.is_paused:
                time.sleep(0.5)
                continue
            
            pending_jobs = self.db.get_queue_jobs(status='pending')
            
            if not pending_jobs:
                time.sleep(1)
                continue
            
            job = pending_jobs[0]
            job_id = job['id']
            
            self.db.update_queue_job(job_id, status='processing', started_at=datetime.now())
            
            video_file = self.db.get_video_file(job['video_file_id'])
            if not video_file:
                self.db.update_queue_job(job_id, status='failed', 
                                        error_message='Video file not found')
                continue
            
            self.db.update_video_file(video_file['id'], status='processing')
            
            if self.callbacks['on_job_start']:
                self.callbacks['on_job_start'](job_id, video_file)
            
            wrapper = AutoEditorWrapper()
            self.active_jobs[job_id] = wrapper
            
            start_time = time.time()
            
            def progress_callback(line: str):
                if self.callbacks['on_job_progress']:
                    self.callbacks['on_job_progress'](job_id, line)
            
            success, output = wrapper.process_video(
                source_path=video_file['filepath'],
                output_path=job['output_filepath'],
                margin_seconds=job['margin_seconds'],
                silent_threshold_db=job['silent_threshold_db'],
                silent_speed=job['silent_speed'],
                video_speed=job['video_speed'],
                progress_callback=progress_callback
            )
            
            processing_time = time.time() - start_time
            
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
            
            if success:
                import os
                output_file_size = os.path.getsize(job['output_filepath']) if os.path.exists(job['output_filepath']) else None
                
                self.db.add_processed_output(
                    video_file_id=video_file['id'],
                    output_filepath=job['output_filepath'],
                    output_filename=os.path.basename(job['output_filepath']),
                    margin_seconds=job['margin_seconds'],
                    silent_threshold_db=job['silent_threshold_db'],
                    silent_speed=job['silent_speed'],
                    video_speed=job['video_speed'],
                    output_file_size=output_file_size,
                    processing_time_seconds=processing_time,
                    success=True,
                    auto_editor_output=output
                )
                
                self.db.update_queue_job(job_id, status='completed', completed_at=datetime.now())
                self.db.update_video_file(video_file['id'], status='completed')
                
                if self.callbacks['on_job_complete']:
                    self.callbacks['on_job_complete'](job_id, video_file, job['output_filepath'])
            else:
                self.db.update_queue_job(job_id, status='failed', 
                                        completed_at=datetime.now(),
                                        error_message=output)
                self.db.update_video_file(video_file['id'], status='failed')
                
                if self.callbacks['on_job_error']:
                    self.callbacks['on_job_error'](job_id, video_file, output)
    
    def get_queue_status(self):
        pending = len(self.db.get_queue_jobs(status='pending'))
        processing = len(self.db.get_queue_jobs(status='processing'))
        completed = len(self.db.get_queue_jobs(status='completed'))
        failed = len(self.db.get_queue_jobs(status='failed'))
        
        return {
            'pending': pending,
            'processing': processing,
            'completed': completed,
            'failed': failed,
            'is_paused': self.is_paused
        }
