import customtkinter as ctk
from tkinter import messagebox

class ProjectDialog:
    def __init__(self, parent, db_manager, settings_manager, project=None):
        self.db = db_manager
        self.settings_manager = settings_manager
        self.project = project
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("New Project" if not project else "Edit Project")
        self.dialog.geometry("500x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(main_frame, 
                            text="New Project" if not project else "Edit Project",
                            font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(0, 20))
        
        ctk.CTkLabel(main_frame, text="Project Name:").pack(anchor="w", pady=(5, 0))
        self.name_entry = ctk.CTkEntry(main_frame, width=400)
        self.name_entry.pack(fill="x", pady=5)
        
        ctk.CTkLabel(main_frame, text="Description:").pack(anchor="w", pady=(10, 0))
        self.desc_entry = ctk.CTkEntry(main_frame, width=400)
        self.desc_entry.pack(fill="x", pady=5)
        
        ctk.CTkLabel(main_frame, text="Output Folder:").pack(anchor="w", pady=(10, 0))
        self.output_entry = ctk.CTkEntry(main_frame, width=400)
        self.output_entry.insert(0, "processed")
        self.output_entry.pack(fill="x", pady=5)
        
        ctk.CTkLabel(main_frame, text="Project-Specific Settings (leave empty to use global)", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(15, 5))
        
        margin_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        margin_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(margin_frame, text="Margin (seconds):", width=150).pack(side="left")
        self.margin_entry = ctk.CTkEntry(margin_frame, width=100, placeholder_text="Global")
        self.margin_entry.pack(side="left", padx=5)
        
        threshold_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        threshold_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(threshold_frame, text="Threshold (dB):", width=150).pack(side="left")
        self.threshold_entry = ctk.CTkEntry(threshold_frame, width=100, placeholder_text="Global")
        self.threshold_entry.pack(side="left", padx=5)
        
        silent_speed_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        silent_speed_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(silent_speed_frame, text="Silent Speed:", width=150).pack(side="left")
        self.silent_speed_entry = ctk.CTkEntry(silent_speed_frame, width=100, placeholder_text="Global")
        self.silent_speed_entry.pack(side="left", padx=5)
        
        video_speed_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        video_speed_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(video_speed_frame, text="Video Speed:", width=150).pack(side="left")
        self.video_speed_entry = ctk.CTkEntry(video_speed_frame, width=100, placeholder_text="Global")
        self.video_speed_entry.pack(side="left", padx=5)
        
        if project:
            self.name_entry.insert(0, project['name'])
            self.desc_entry.insert(0, project.get('description', ''))
            self.output_entry.delete(0, 'end')
            self.output_entry.insert(0, project.get('output_folder', 'processed'))
            
            if project.get('margin_seconds'):
                self.margin_entry.insert(0, str(project['margin_seconds']))
            if project.get('silent_threshold_db'):
                self.threshold_entry.insert(0, str(project['silent_threshold_db']))
            if project.get('silent_speed'):
                self.silent_speed_entry.insert(0, str(int(project['silent_speed'])))
            if project.get('video_speed'):
                self.video_speed_entry.insert(0, str(project['video_speed']))
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(side="bottom", pady=(20, 0))
        
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", 
                                   command=self.dialog.destroy, width=100)
        cancel_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(button_frame, text="Save", 
                                command=self.on_save, width=100)
        save_btn.pack(side="left", padx=5)
    
    def on_save(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Project name is required")
            return
        
        settings = {}
        
        try:
            if self.margin_entry.get():
                settings['margin_seconds'] = float(self.margin_entry.get())
            if self.threshold_entry.get():
                settings['silent_threshold_db'] = float(self.threshold_entry.get())
            if self.silent_speed_entry.get():
                settings['silent_speed'] = float(self.silent_speed_entry.get())
            if self.video_speed_entry.get():
                settings['video_speed'] = float(self.video_speed_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
            return
        
        if self.project:
            self.db.update_project(
                self.project['id'],
                name=name,
                description=self.desc_entry.get(),
                output_folder=self.output_entry.get(),
                **settings
            )
        else:
            self.db.create_project(
                name=name,
                description=self.desc_entry.get(),
                output_folder=self.output_entry.get(),
                **settings
            )
        
        self.dialog.destroy()
