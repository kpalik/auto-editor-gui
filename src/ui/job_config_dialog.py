import customtkinter as ctk
from tkinter import messagebox

class JobConfigDialog:
    def __init__(self, parent, db_manager, settings_manager, video_file):
        self.db = db_manager
        self.settings_manager = settings_manager
        self.video_file = video_file
        self.result = None
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Configure Processing Job")
        self.dialog.geometry("500x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        settings = self.settings_manager.resolve_settings(video_file_id=video_file['id'])
        sources = self.settings_manager.get_settings_source(video_file_id=video_file['id'])
        
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(main_frame, text=f"Configure: {video_file['filename'][:40]}...",
                            font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(0, 20))
        
        ctk.CTkLabel(main_frame, text="Silence Detection", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
        
        margin_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        margin_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(margin_frame, text="Margin (seconds):", width=150).pack(side="left")
        self.margin_entry = ctk.CTkEntry(margin_frame, width=100)
        self.margin_entry.insert(0, str(settings.margin_seconds))
        self.margin_entry.pack(side="left", padx=5)
        ctk.CTkLabel(margin_frame, text=f"(from: {sources['margin_seconds']})", 
                    font=ctk.CTkFont(size=10)).pack(side="left")
        
        threshold_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        threshold_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(threshold_frame, text="Threshold (dB):", width=150).pack(side="left")
        self.threshold_entry = ctk.CTkEntry(threshold_frame, width=100)
        self.threshold_entry.insert(0, str(settings.silent_threshold_db))
        self.threshold_entry.pack(side="left", padx=5)
        ctk.CTkLabel(threshold_frame, text=f"(from: {sources['silent_threshold_db']})", 
                    font=ctk.CTkFont(size=10)).pack(side="left")
        
        ctk.CTkLabel(main_frame, text="Speed Settings", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15, 5))
        
        silent_speed_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        silent_speed_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(silent_speed_frame, text="Silent Speed:", width=150).pack(side="left")
        self.silent_speed_entry = ctk.CTkEntry(silent_speed_frame, width=100)
        self.silent_speed_entry.insert(0, str(int(settings.silent_speed)))
        self.silent_speed_entry.pack(side="left", padx=5)
        ctk.CTkLabel(silent_speed_frame, text="(99999 = cut)", 
                    font=ctk.CTkFont(size=10)).pack(side="left")
        
        video_speed_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        video_speed_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(video_speed_frame, text="Video Speed:", width=150).pack(side="left")
        self.video_speed_entry = ctk.CTkEntry(video_speed_frame, width=100)
        self.video_speed_entry.insert(0, str(settings.video_speed))
        self.video_speed_entry.pack(side="left", padx=5)
        ctk.CTkLabel(video_speed_frame, text=f"(from: {sources['video_speed']})", 
                    font=ctk.CTkFont(size=10)).pack(side="left")
        
        ctk.CTkLabel(main_frame, text="Output Preview", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15, 5))
        
        self.preview_label = ctk.CTkLabel(main_frame, text="", 
                                         font=ctk.CTkFont(size=11),
                                         wraplength=450)
        self.preview_label.pack(fill="x", pady=5)
        
        self.update_preview()
        
        for entry in [self.margin_entry, self.threshold_entry, self.video_speed_entry]:
            entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(side="bottom", pady=(20, 0))
        
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", 
                                   command=self.dialog.destroy, width=100)
        cancel_btn.pack(side="left", padx=5)
        
        add_btn = ctk.CTkButton(button_frame, text="Add to Queue", 
                               command=self.on_add, width=120)
        add_btn.pack(side="left", padx=5)
    
    def update_preview(self):
        try:
            margin = float(self.margin_entry.get())
            db = float(self.threshold_entry.get())
            speed = float(self.video_speed_entry.get())
            
            from core.output_manager import OutputManager
            filename = OutputManager.generate_output_filename(
                self.video_file['filepath'], margin, db, speed
            )
            
            self.preview_label.configure(text=f"Output: {filename}")
        except ValueError:
            self.preview_label.configure(text="Invalid values")
    
    def on_add(self):
        try:
            self.result = {
                'margin_seconds': float(self.margin_entry.get()),
                'silent_threshold_db': float(self.threshold_entry.get()),
                'silent_speed': float(self.silent_speed_entry.get()),
                'video_speed': float(self.video_speed_entry.get())
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
