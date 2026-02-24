# Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install auto-editor

```bash
pip install auto-editor
```

### Step 3: Verify Installation

```bash
python test_installation.py
```

All checks should pass with ✓ marks.

## First Run (2 minutes)

### Launch the Application

```bash
cd src
python main.py
```

The application will:
- Create a database at `%USERPROFILE%\.auto-editor-gui\app.db`
- Load with default settings
- Show an empty file list

## Basic Workflow

### 1. Add a Watch Folder (30 seconds)

1. Click **"+ Add Folder"** in the sidebar
2. Select a folder containing video files
3. Existing videos will be automatically detected and listed

### 2. Quick Process a Video (1 click)

1. Find your video in the list (status: 🆕 NEW)
2. Click **"Remove Silence"** button
3. Video is added to queue and processing starts automatically
4. Output saved to `[source_folder]/processed/` with parametric filename

### 3. Custom Processing (Advanced)

1. Click **"Add to Queue"** on a video
2. Adjust parameters:
   - **Margin**: Time to keep around loud sections (default: 0.2s)
   - **Threshold**: Audio level for silence detection (default: -28dB)
   - **Video Speed**: Playback speed multiplier (default: 1.0x)
3. Preview the output filename
4. Click **"Add to Queue"**

### 4. Create a Project (Organization)

1. Click **"+ New Project"** in sidebar
2. Enter project name (e.g., "Course Module 1")
3. Optionally set project-specific defaults:
   - Leave empty to use global settings
   - Set values to override for all videos in this project
4. Click **"Save"**

### 5. Assign Videos to Projects

1. Select a video in the list
2. Right-click → "Assign to Project" (coming soon)
3. Or manually edit in database for now

## Settings Hierarchy Example

**Scenario**: You want aggressive silence removal for tutorial videos, but conservative for interviews.

### Global Settings (⚙ Settings)
```
Margin: 0.2s
Threshold: -28dB
Speed: 1.0x
```

### Project: "Tutorials" 
```
Margin: 0.1s (override)
Threshold: -25dB (override)
Speed: 1.2x (override)
```

### Project: "Interviews"
```
Margin: 0.3s (override)
Threshold: -30dB (override)
Speed: (inherit global: 1.0x)
```

### Job-Specific (per video)
```
Process tutorial_intro.mp4 with:
  Margin: 0.15s (override project)
  Threshold: (inherit project: -25dB)
  Speed: 1.0x (override project)
```

**Result**: `tutorial_intro_processed_100speed_25dB_150msmargin.mp4`

## Output Filename Format

```
[original_name]_processed_[speed]speed_[dB]dB_[margin]msmargin.[ext]
```

### Examples

| Settings | Output Filename |
|----------|----------------|
| 1.0x speed, -28dB, 0.2s | `video_processed_100speed_28dB_200msmargin.mp4` |
| 1.2x speed, -30dB, 0.15s | `video_processed_120speed_30dB_150msmargin.mp4` |
| 0.8x speed, -25dB, 0.3s | `video_processed_80speed_25dB_300msmargin.mp4` |

## Multiple Versions Workflow

Create different versions of the same video:

1. Select video
2. Click "Add to Queue" → Set parameters (e.g., 1.0x speed, -28dB)
3. Click "Add to Queue" again → Set different parameters (e.g., 1.2x speed, -25dB)
4. Both jobs process independently
5. Two output files created with different filenames

## Queue Management

### Status Bar
```
Queue: 2 pending | 1 processing | 5 completed
```

- **Pending**: Jobs waiting to start
- **Processing**: Currently running (max: concurrent_jobs setting)
- **Completed**: Successfully finished

### Controls
- **⏸ Pause**: Pause queue processing
- **▶ Resume**: Resume queue processing
- **🔄 Refresh**: Update file list

## Tips & Tricks

### Optimal Settings for Screencasts
```
Margin: 0.2s
Threshold: -28dB
Silent Speed: 99999 (cut)
Video Speed: 1.0x
```

### Faster Processing (Less Quality)
```
Margin: 0.1s
Threshold: -25dB
Video Speed: 1.3x
```

### Conservative (Keep More Audio)
```
Margin: 0.3s
Threshold: -30dB
Video Speed: 1.0x
```

## Troubleshooting

### "auto-editor not found"
```bash
pip install auto-editor
auto-editor --version
```

### "No video files found"
- Check watch folder contains video files (.mp4, .mov, .avi, etc.)
- Click 🔄 Refresh button
- Check file permissions

### Processing stuck
- Click ⏸ Pause then ▶ Resume
- Check auto-editor output in database
- Verify source file is not corrupted

### Output file not created
- Check disk space
- Verify write permissions on output folder
- Check error message in file status

## Next Steps

1. ✓ Process your first video
2. ✓ Create projects for organization
3. ✓ Experiment with different settings
4. ✓ Create multiple versions
5. ⚙ Adjust global settings to your preference
6. 📦 Build standalone executable: `python build.py`

## Keyboard Shortcuts (Coming Soon)

- `Ctrl+R`: Refresh
- `Ctrl+S`: Settings
- `Ctrl+N`: New Project
- `Ctrl+Q`: Quit

## Support

For issues or questions:
1. Check README.md for detailed documentation
2. Review auto-editor docs: https://auto-editor.com/docs/
3. Check database at `~/.auto-editor-gui/app.db`
