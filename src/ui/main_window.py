import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

class MainWindow:
    def __init__(self, root, db_manager, settings_manager, queue_manager, file_watcher):
        self.root = root
        self.db = db_manager
        self.settings_manager = settings_manager
        self.queue_manager = queue_manager
        self.file_watcher = file_watcher
        
        self.selected_file_id = None
        self.current_project_filter = None
        self.current_status_filter = None
        
        self.setup_ui()
        self.refresh_file_list()
        self.refresh_project_list()
        self.update_queue_status()
    
    def setup_ui(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar()
        self.create_main_area()
        self.create_status_bar()
    
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        title_label = ctk.CTkLabel(self.sidebar, text="Auto-Editor GUI", 
                                   font=ctk.CTkFont(size=18, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        projects_label = ctk.CTkLabel(self.sidebar, text="Projects", 
                                      font=ctk.CTkFont(size=14, weight="bold"))
        projects_label.grid(row=1, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.project_list_frame = ctk.CTkScrollableFrame(self.sidebar, height=200)
        self.project_list_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        
        add_project_btn = ctk.CTkButton(self.sidebar, text="+ New Project", 
                                       command=self.add_project)
        add_project_btn.grid(row=3, column=0, padx=20, pady=5)
        
        watch_label = ctk.CTkLabel(self.sidebar, text="Watch Folders", 
                                   font=ctk.CTkFont(size=14, weight="bold"))
        watch_label.grid(row=5, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.watch_list_frame = ctk.CTkScrollableFrame(self.sidebar, height=150)
        self.watch_list_frame.grid(row=6, column=0, padx=10, pady=5, sticky="nsew")
        
        add_watch_btn = ctk.CTkButton(self.sidebar, text="+ Add Folder", 
                                      command=self.add_watch_folder)
        add_watch_btn.grid(row=7, column=0, padx=20, pady=(5, 20))
        
        self.refresh_watch_folders()
    
    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        toolbar = ctk.CTkFrame(self.main_frame)
        toolbar.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(toolbar, text="Status:").pack(side="left", padx=5)
        self.status_filter = ctk.CTkComboBox(toolbar, 
                                             values=["All", "New", "Queued", "Processing", "Completed", "Failed"],
                                             command=self.on_filter_change,
                                             width=120)
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=5)
        
        ctk.CTkLabel(toolbar, text="Project:").pack(side="left", padx=5)
        self.project_filter = ctk.CTkComboBox(toolbar, 
                                              values=["All"],
                                              command=self.on_filter_change,
                                              width=150)
        self.project_filter.set("All")
        self.project_filter.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(toolbar, text="🔄 Refresh", width=100,
                                    command=self.refresh_file_list)
        refresh_btn.pack(side="right", padx=5)
        
        settings_btn = ctk.CTkButton(toolbar, text="⚙ Settings", width=100,
                                     command=self.open_settings)
        settings_btn.pack(side="right", padx=5)
        
        header = ctk.CTkFrame(self.main_frame)
        header.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(header, text="Video Files", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=10)
        
        self.file_list = ctk.CTkScrollableFrame(self.main_frame)
        self.file_list.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
    
    def create_status_bar(self):
        self.status_bar = ctk.CTkFrame(self.root, height=40)
        self.status_bar.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")
        
        self.queue_status_label = ctk.CTkLabel(self.status_bar, text="Queue: 0 pending | 0 processing")
        self.queue_status_label.pack(side="left", padx=10)
        
        self.pause_btn = ctk.CTkButton(self.status_bar, text="⏸ Pause", width=100,
                                       command=self.toggle_queue_pause)
        self.pause_btn.pack(side="right", padx=10)
    
    def refresh_project_list(self):
        for widget in self.project_list_frame.winfo_children():
            widget.destroy()
        
        all_btn = ctk.CTkButton(self.project_list_frame, text="📁 All Files",
                               command=lambda: self.select_project(None),
                               fg_color="transparent", hover_color=("#3B8ED0", "#1F6AA5"))
        all_btn.pack(fill="x", padx=5, pady=2)
        
        projects = self.db.get_all_projects()
        for project in projects:
            btn = ctk.CTkButton(self.project_list_frame, 
                               text=f"▶ {project['name']}",
                               command=lambda p=project: self.select_project(p['id']),
                               fg_color="transparent", hover_color=("#3B8ED0", "#1F6AA5"))
            btn.pack(fill="x", padx=5, pady=2)
        
        project_names = ["All"] + [p['name'] for p in projects]
        self.project_filter.configure(values=project_names)
    
    def refresh_watch_folders(self):
        for widget in self.watch_list_frame.winfo_children():
            widget.destroy()
        
        watch_folders = self.db.get_watch_folders()
        for folder in watch_folders:
            frame = ctk.CTkFrame(self.watch_list_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            status = "✓" if folder['enabled'] else "✗"
            label = ctk.CTkLabel(frame, text=f"{status} {os.path.basename(folder['path'])}")
            label.pack(side="left", padx=5)
    
    def refresh_file_list(self):
        for widget in self.file_list.winfo_children():
            widget.destroy()
        
        status_filter = self.status_filter.get().lower() if self.status_filter.get() != "All" else None
        
        files = self.db.get_all_video_files(
            project_id=self.current_project_filter,
            status=status_filter
        )
        
        if not files:
            no_files_label = ctk.CTkLabel(self.file_list, 
                                         text="No video files found. Add a watch folder to get started.",
                                         font=ctk.CTkFont(size=14))
            no_files_label.pack(pady=50)
            return
        
        for file in files:
            self.create_file_card(file)
    
    def create_file_card(self, file):
        from models.video_file import VideoFile
        video_file = VideoFile.from_dict(file)
        
        card = ctk.CTkFrame(self.file_list, fg_color=("#E0E0E0", "#2B2B2B"))
        card.pack(fill="x", padx=5, pady=5)
        
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=5)
        
        status_label = ctk.CTkLabel(header_frame, 
                                    text=f"{video_file.get_status_emoji()} {video_file.filename}",
                                    font=ctk.CTkFont(size=14, weight="bold"))
        status_label.pack(side="left")
        
        status_badge = ctk.CTkLabel(header_frame, text=f"[{video_file.status.upper()}]",
                                   font=ctk.CTkFont(size=12))
        status_badge.pack(side="left", padx=10)
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=2)
        
        size_mb = file['file_size'] / (1024*1024) if file['file_size'] else 0
        duration_str = f"{int(file['duration']//60)}:{int(file['duration']%60):02d}" if file['duration'] else "N/A"
        
        info_text = f"Size: {size_mb:.1f} MB | Duration: {duration_str}"
        ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=11)).pack(side="left")
        
        if file['comment']:
            comment_frame = ctk.CTkFrame(card, fg_color="transparent")
            comment_frame.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(comment_frame, text=f'"{file["comment"]}"', 
                        font=ctk.CTkFont(size=11, slant="italic")).pack(side="left")
        
        processed_outputs = self.db.get_processed_outputs(file['id'])
        if processed_outputs:
            outputs_frame = ctk.CTkFrame(card, fg_color="transparent")
            outputs_frame.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(outputs_frame, text=f"Processed versions ({len(processed_outputs)}):",
                        font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w")
            
            for output in processed_outputs[:3]:
                output_label = ctk.CTkLabel(outputs_frame, 
                                           text=f"  ✓ {output['output_filename'][:50]}...",
                                           font=ctk.CTkFont(size=10))
                output_label.pack(anchor="w")
        
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=5)
        
        if video_file.status in ['new', 'failed']:
            remove_silence_btn = ctk.CTkButton(button_frame, text="Remove Silence",
                                              command=lambda f=file: self.quick_process(f),
                                              width=120)
            remove_silence_btn.pack(side="left", padx=5)
            
            add_queue_btn = ctk.CTkButton(button_frame, text="Add to Queue",
                                         command=lambda f=file: self.add_to_queue_dialog(f),
                                         width=120)
            add_queue_btn.pack(side="left", padx=5)
        
        if file['project_id']:
            project = self.db.get_project(file['project_id'])
            if project:
                project_label = ctk.CTkLabel(button_frame, 
                                            text=f"Project: {project['name']}",
                                            font=ctk.CTkFont(size=10))
                project_label.pack(side="right", padx=5)
    
    def quick_process(self, file):
        job_id = self.queue_manager.add_job(file['id'])
        if job_id:
            messagebox.showinfo("Success", f"Added {file['filename']} to processing queue")
            self.refresh_file_list()
            self.update_queue_status()
    
    def add_to_queue_dialog(self, file):
        from ui.job_config_dialog import JobConfigDialog
        dialog = JobConfigDialog(self.root, self.db, self.settings_manager, file)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            job_id = self.queue_manager.add_job(file['id'], **dialog.result)
            if job_id:
                messagebox.showinfo("Success", f"Added {file['filename']} to queue with custom settings")
                self.refresh_file_list()
                self.update_queue_status()
    
    def select_project(self, project_id):
        self.current_project_filter = project_id
        self.refresh_file_list()
    
    def on_filter_change(self, value):
        self.refresh_file_list()
    
    def add_project(self):
        from ui.project_dialog import ProjectDialog
        dialog = ProjectDialog(self.root, self.db, self.settings_manager)
        self.root.wait_window(dialog.dialog)
        self.refresh_project_list()
    
    def add_watch_folder(self):
        folder = filedialog.askdirectory(title="Select folder to watch")
        if folder:
            try:
                self.db.add_watch_folder(folder)
                self.file_watcher.add_watch_folder(folder)
                self.refresh_watch_folders()
                
                existing_files = self.file_watcher.scan_existing_files(folder)
                for filepath in existing_files:
                    if not self.db.get_video_file_by_path(filepath):
                        from core.video_analyzer import VideoAnalyzer
                        filename = os.path.basename(filepath)
                        video_info = VideoAnalyzer.get_video_info(filepath)
                        self.db.add_video_file(
                            filepath=filepath,
                            filename=filename,
                            file_size=video_info.get('file_size'),
                            duration=video_info.get('duration')
                        )
                
                self.refresh_file_list()
                messagebox.showinfo("Success", f"Added watch folder: {folder}\nFound {len(existing_files)} existing video files")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add watch folder: {str(e)}")
    
    def open_settings(self):
        from ui.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self.root, self.db, self.settings_manager)
        self.root.wait_window(dialog.dialog)
    
    def toggle_queue_pause(self):
        if self.queue_manager.is_paused:
            self.queue_manager.resume()
            self.pause_btn.configure(text="⏸ Pause")
        else:
            self.queue_manager.pause()
            self.pause_btn.configure(text="▶ Resume")
        self.update_queue_status()
    
    def update_queue_status(self):
        status = self.queue_manager.get_queue_status()
        status_text = f"Queue: {status['pending']} pending | {status['processing']} processing | {status['completed']} completed"
        if status['is_paused']:
            status_text += " (PAUSED)"
        self.queue_status_label.configure(text=status_text)
