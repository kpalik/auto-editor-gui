# Auto-Editor GUI

A modern desktop application for managing and processing screencast videos with [auto-editor](https://auto-editor.com/). Built with Python and CustomTkinter.

## Features

- **Automatic File Detection**: Watch folders for new video files
- **Silence Removal**: One-click silence removal with customizable settings
- **Hierarchical Settings**: Global → Project → Job-level configuration cascade
- **Project Management**: Organize videos into projects with custom settings
- **Processing Queue**: Batch processing with concurrent workers
- **Multiple Versions**: Create multiple processed versions with different parameters
- **Parametric Filenames**: Output files named with processing parameters
- **Modern UI**: Clean, dark-themed interface with CustomTkinter

## Installation

### Prerequisites

- Python 3.11 or higher
- auto-editor installed and available in PATH
- ffmpeg/ffprobe (required by auto-editor)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd auto-editor-gui
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install auto-editor:
```bash
pip install auto-editor
```

## Usage

### Running the Application

```bash
python src/main.py
```

### Quick Start

1. **Add a Watch Folder**: Click "+ Add Folder" in the sidebar to monitor a directory
2. **Create a Project**: Click "+ New Project" to organize your videos
3. **Process Videos**: 
   - Click "Remove Silence" for quick processing with default settings
   - Click "Add to Queue" to customize parameters before processing
4. **Monitor Progress**: Check the status bar for queue information

### Settings Hierarchy

The app uses a three-level settings system:

1. **Global Settings** (⚙ Settings button)
   - Default values for all processing
   - Margin: 0.2s, Threshold: -28dB, Speed: 1.0x

2. **Project Settings** (Edit Project)
   - Override global settings for specific projects
   - NULL values inherit from global

3. **Job Settings** (Add to Queue dialog)
   - Per-file processing parameters
   - Create multiple versions with different settings

### Output Filenames

Processed files are named with their parameters:

```
original_name_processed_[speed]speed_[dB]dB_[margin]msmargin.mp4
```

Examples:
- `tutorial_processed_100speed_28dB_200msmargin.mp4`
- `screencast_processed_120speed_30dB_150msmargin.mp4`

### Project Structure

```
auto-editor-gui/
├── src/
│   ├── main.py              # Application entry point
│   ├── app.py               # Main application class
│   ├── database/            # Database management
│   ├── core/                # Core functionality
│   │   ├── auto_editor_wrapper.py
│   │   ├── file_watcher.py
│   │   ├── queue_manager.py
│   │   ├── settings_manager.py
│   │   └── output_manager.py
│   ├── models/              # Data models
│   ├── ui/                  # User interface
│   └── utils/               # Utility functions
├── assets/                  # Icons and themes
├── database/                # Database templates
└── requirements.txt
```

## Configuration

### Database Location

The SQLite database is stored at:
- Windows: `%USERPROFILE%\.auto-editor-gui\app.db`
- Linux/Mac: `~/.auto-editor-gui/app.db`

### Default Settings

- Margin: 0.2 seconds
- Silent Threshold: -28 dB
- Silent Speed: 99999 (cut)
- Video Speed: 1.0x
- Output Folder: "processed"
- Concurrent Jobs: 2

## Building Executable

To create a standalone executable:

```bash
python build.py
```

The executable will be created in the `dist/` directory.

## Keyboard Shortcuts

- `Ctrl+R`: Refresh file list
- `Ctrl+S`: Open settings
- `Ctrl+N`: New project
- `Ctrl+Q`: Quit application

## Troubleshooting

### auto-editor not found

Ensure auto-editor is installed and in your PATH:
```bash
auto-editor --version
```

### FFmpeg not found

Install FFmpeg and ensure it's in your PATH:
- Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Linux: `sudo apt install ffmpeg`
- Mac: `brew install ffmpeg`

### Database errors

Delete the database to reset:
```bash
rm ~/.auto-editor-gui/app.db
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
black src/
flake8 src/
```

## License

MIT License

## Credits

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Powered by [auto-editor](https://auto-editor.com/)
- Uses [watchdog](https://github.com/gorakhargosh/watchdog) for file monitoring

## Roadmap

- [ ] Preset templates for common scenarios
- [ ] Batch export to different formats
- [ ] Video preview with timeline
- [ ] Advanced auto-editor options UI
- [ ] Cloud sync for settings
- [ ] Plugin system for custom processors
