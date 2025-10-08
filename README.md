# Music Tag Cleaner

A Python script that cleans music file metadata by preserving only essential ID3 tags and removing all other information.

## Features

- Supports multiple audio formats: MP3, FLAC, M4A, MP4, M4B, M4P, OGG, OPUS, WMA
- Preserves essential tags:
  - Artist
  - Album Artist
  - Title
  - Album
  - Track Number
  - Total Tracks
  - Genre
  - Publishing Year
  - Cover Art (front cover only)
- Strips all other metadata and tags
- Processes entire directories at once

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python clean_music_tags.py <directory>
```

Example:
```bash
python clean_music_tags.py /path/to/music/folder
```

The script will:
1. Scan the directory for supported music files
2. Extract essential tags from each file
3. Remove all existing metadata
4. Re-apply only the essential tags
5. Save the cleaned files

## Requirements

- Python 3.6+
- mutagen library

## Notes

- The script modifies files in-place. Consider backing up your files before processing.
- Cover art is limited to front cover only (type 3).
- If no front cover is found, the first available cover art will be used.
