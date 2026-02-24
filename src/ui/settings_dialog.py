import customtkinter as ctk
from tkinter import messagebox

class SettingsDialog:
    def __init__(self, parent, db_manager, settings_manager):
        self.db = db_manager
        self.settings_manager = settings_manager
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Global Settings")
        self.dialog.geometry("500x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(main_frame, text="Global Settings",
                            font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(0, 20))
        
        current_settings = self.settings_manager.get_global_settings()
        
        ctk.CTkLabel(main_frame, text="Silence Detection", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
        
        margin_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        margin_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(margin_frame, text="Margin (seconds):", width=150).pack(side="left")
        self.margin_entry = ctk.CTkEntry(margin_frame, width=100)
        self.margin_entry.insert(0, str(current_settings.margin_seconds))
        self.margin_entry.pack(side="left", padx=5)
        
        threshold_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        threshold_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(threshold_frame, text="Threshold (dB):", width=150).pack(side="left")
        self.threshold_entry = ctk.CTkEntry(threshold_frame, width=100)
        self.threshold_entry.insert(0, str(current_settings.silent_threshold_db))
        self.threshold_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(main_frame, text="Speed Settings", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15, 5))
        
        silent_speed_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        silent_speed_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(silent_speed_frame, text="Silent Speed:", width=150).pack(side="left")
        self.silent_speed_entry = ctk.CTkEntry(silent_speed_frame, width=100)
        self.silent_speed_entry.insert(0, str(int(current_settings.silent_speed)))
        self.silent_speed_entry.pack(side="left", padx=5)
        ctk.CTkLabel(silent_speed_frame, text="(99999 = cut)", 
                    font=ctk.CTkFont(size=10)).pack(side="left")
        
        video_speed_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        video_speed_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(video_speed_frame, text="Video Speed:", width=150).pack(side="left")
        self.video_speed_entry = ctk.CTkEntry(video_speed_frame, width=100)
        self.video_speed_entry.insert(0, str(current_settings.video_speed))
        self.video_speed_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(main_frame, text="Output Settings", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15, 5))
        
        output_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        output_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(output_frame, text="Output Subfolder:", width=150).pack(side="left")
        self.output_entry = ctk.CTkEntry(output_frame, width=150)
        self.output_entry.insert(0, current_settings.output_subfolder)
        self.output_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(main_frame, text="Processing Settings", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15, 5))
        
        concurrent_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        concurrent_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(concurrent_frame, text="Concurrent Jobs:", width=150).pack(side="left")
        self.concurrent_entry = ctk.CTkEntry(concurrent_frame, width=100)
        self.concurrent_entry.insert(0, self.db.get_setting('concurrent_jobs', '2'))
        self.concurrent_entry.pack(side="left", padx=5)
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(side="bottom", pady=(20, 0))
        
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", 
                                   command=self.dialog.destroy, width=100)
        cancel_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(button_frame, text="Save", 
                                command=self.on_save, width=100)
        save_btn.pack(side="left", padx=5)
    
    def on_save(self):
        try:
            self.settings_manager.set_global_settings(
                margin_seconds=float(self.margin_entry.get()),
                silent_threshold_db=float(self.threshold_entry.get()),
                silent_speed=float(self.silent_speed_entry.get()),
                video_speed=float(self.video_speed_entry.get()),
                output_subfolder=self.output_entry.get()
            )
            
            self.db.set_setting('concurrent_jobs', self.concurrent_entry.get())
            
            messagebox.showinfo("Success", "Settings saved successfully")
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
