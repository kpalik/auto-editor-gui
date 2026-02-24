import sys
import subprocess

def check_module(module_name):
    try:
        __import__(module_name)
        print(f"✓ {module_name} is installed")
        return True
    except ImportError:
        print(f"✗ {module_name} is NOT installed")
        return False

def check_command(command):
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✓ {command} is available")
            return True
        else:
            print(f"✗ {command} is NOT available")
            return False
    except (subprocess.SubprocessError, FileNotFoundError):
        print(f"✗ {command} is NOT available")
        return False

print("Checking Python version...")
print(f"Python {sys.version}")
print()

print("Checking required Python packages...")
modules = ['customtkinter', 'PIL', 'watchdog', 'sqlite3']
all_modules_ok = all(check_module(m) for m in modules)
print()

print("Checking required commands...")
commands = ['auto-editor', 'ffmpeg', 'ffprobe']
all_commands_ok = all(check_command(c) for c in commands)
print()

if all_modules_ok and all_commands_ok:
    print("✓ All dependencies are installed! You can run the application.")
else:
    print("✗ Some dependencies are missing. Please install them:")
    if not all_modules_ok:
        print("  pip install -r requirements.txt")
    if not all_commands_ok:
        print("  Install auto-editor: pip install auto-editor")
        print("  Install ffmpeg from: https://ffmpeg.org/download.html")
