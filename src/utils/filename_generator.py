import os
from pathlib import Path

def generate_parametric_filename(source_path: str, margin_sec: float,
                                 db: float, speed: float, silent_speed: float = None) -> str:
    name, ext = os.path.splitext(os.path.basename(source_path))
    margin_ms = int(margin_sec * 1000)
    speed_int = int(speed * 100)
    db_int = abs(int(db))
    
    return f"{name}_processed_{speed_int}speed_{db_int}dB_{margin_ms}msmargin{ext}"

def ensure_unique_filename(filepath: str) -> str:
    if not os.path.exists(filepath):
        return filepath
    
    base, ext = os.path.splitext(filepath)
    counter = 1
    
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    
    return f"{base}_{counter}{ext}"
