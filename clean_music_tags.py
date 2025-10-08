#!/usr/bin/env python3
"""
Music Tag Cleaner - Strips unnecessary ID3 tags from music files.

This script processes music files (MP3, FLAC, M4A, etc.) and removes all metadata
except for essential tags: Artist, Album Artist, Title, Track Number, Genre,
Cover Art (front), Publishing Year, and Total Tracks.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple
import mutagen
from mutagen.id3 import ID3, APIC, TPE1, TPE2, TIT2, TALB, TDRC, TCON, TRCK, TPOS
from mutagen.flac import FLAC, Picture
from mutagen.mp4 import MP4, MP4Cover


# Supported file extensions
SUPPORTED_EXTENSIONS = {'.mp3', '.flac', '.m4a', '.mp4', '.m4b', '.m4p', '.ogg', '.opus', '.wma'}


class TagData:
    """Container for essential music metadata."""

    def __init__(self):
        self.artist: Optional[str] = None
        self.album_artist: Optional[str] = None
        self.title: Optional[str] = None
        self.album: Optional[str] = None
        self.track_number: Optional[int] = None
        self.total_tracks: Optional[int] = None
        self.genre: Optional[str] = None
        self.year: Optional[str] = None
        self.cover_art: Optional[bytes] = None
        self.cover_mime: Optional[str] = None

    def __repr__(self):
        return (f"TagData(artist={self.artist}, album_artist={self.album_artist}, "
                f"title={self.title}, track={self.track_number}/{self.total_tracks})")


def extract_tags_mp3(filepath: Path) -> TagData:
    """Extract essential tags from MP3 files."""
    tags = TagData()

    try:
        audio = ID3(filepath)

        # Artist
        if 'TPE1' in audio:
            tags.artist = str(audio['TPE1'].text[0])

        # Album Artist
        if 'TPE2' in audio:
            tags.album_artist = str(audio['TPE2'].text[0])

        # Title
        if 'TIT2' in audio:
            tags.title = str(audio['TIT2'].text[0])

        # Album
        if 'TALB' in audio:
            tags.album = str(audio['TALB'].text[0])

        # Genre
        if 'TCON' in audio:
            tags.genre = str(audio['TCON'].text[0])

        # Year
        if 'TDRC' in audio:
            tags.year = str(audio['TDRC'].text[0])
        elif 'TYER' in audio:
            tags.year = str(audio['TYER'].text[0])

        # Track number
        if 'TRCK' in audio:
            track_str = str(audio['TRCK'].text[0])
            if '/' in track_str:
                parts = track_str.split('/')
                tags.track_number = int(parts[0])
                tags.total_tracks = int(parts[1])
            else:
                tags.track_number = int(track_str)

        # Cover art (front cover only)
        for key in audio.keys():
            if key.startswith('APIC'):
                apic = audio[key]
                if apic.type == 3:  # Front cover
                    tags.cover_art = apic.data
                    tags.cover_mime = apic.mime
                    break
        # If no front cover found, use first available
        if not tags.cover_art:
            for key in audio.keys():
                if key.startswith('APIC'):
                    apic = audio[key]
                    tags.cover_art = apic.data
                    tags.cover_mime = apic.mime
                    break

    except Exception as e:
        print(f"Error extracting MP3 tags from {filepath}: {e}")

    return tags


def extract_tags_flac(filepath: Path) -> TagData:
    """Extract essential tags from FLAC files."""
    tags = TagData()

    try:
        audio = FLAC(filepath)

        # Artist
        if 'artist' in audio:
            tags.artist = audio['artist'][0]

        # Album Artist
        if 'albumartist' in audio:
            tags.album_artist = audio['albumartist'][0]

        # Title
        if 'title' in audio:
            tags.title = audio['title'][0]

        # Album
        if 'album' in audio:
            tags.album = audio['album'][0]

        # Genre
        if 'genre' in audio:
            tags.genre = audio['genre'][0]

        # Year
        if 'date' in audio:
            tags.year = audio['date'][0]
        elif 'year' in audio:
            tags.year = audio['year'][0]

        # Track number
        if 'tracknumber' in audio:
            track_str = audio['tracknumber'][0]
            if '/' in track_str:
                parts = track_str.split('/')
                tags.track_number = int(parts[0])
                tags.total_tracks = int(parts[1])
            else:
                tags.track_number = int(track_str)

        if 'totaltracks' in audio and not tags.total_tracks:
            tags.total_tracks = int(audio['totaltracks'][0])
        elif 'tracktotal' in audio and not tags.total_tracks:
            tags.total_tracks = int(audio['tracktotal'][0])

        # Cover art (front cover)
        if audio.pictures:
            for pic in audio.pictures:
                if pic.type == 3:  # Front cover
                    tags.cover_art = pic.data
                    tags.cover_mime = pic.mime
                    break
            # If no front cover, use first available
            if not tags.cover_art and audio.pictures:
                tags.cover_art = audio.pictures[0].data
                tags.cover_mime = audio.pictures[0].mime

    except Exception as e:
        print(f"Error extracting FLAC tags from {filepath}: {e}")

    return tags


def extract_tags_m4a(filepath: Path) -> TagData:
    """Extract essential tags from M4A/MP4 files."""
    tags = TagData()

    try:
        audio = MP4(filepath)

        # Artist
        if '\xa9ART' in audio:
            tags.artist = audio['\xa9ART'][0]

        # Album Artist
        if 'aART' in audio:
            tags.album_artist = audio['aART'][0]

        # Title
        if '\xa9nam' in audio:
            tags.title = audio['\xa9nam'][0]

        # Album
        if '\xa9alb' in audio:
            tags.album = audio['\xa9alb'][0]

        # Genre
        if '\xa9gen' in audio:
            tags.genre = audio['\xa9gen'][0]

        # Year
        if '\xa9day' in audio:
            tags.year = audio['\xa9day'][0]

        # Track number
        if 'trkn' in audio:
            track_info = audio['trkn'][0]
            tags.track_number = track_info[0]
            if len(track_info) > 1:
                tags.total_tracks = track_info[1]

        # Cover art
        if 'covr' in audio:
            cover = audio['covr'][0]
            tags.cover_art = bytes(cover)
            # Determine MIME type from imageformat
            if cover.imageformat == MP4Cover.FORMAT_JPEG:
                tags.cover_mime = 'image/jpeg'
            elif cover.imageformat == MP4Cover.FORMAT_PNG:
                tags.cover_mime = 'image/png'

    except Exception as e:
        print(f"Error extracting M4A tags from {filepath}: {e}")

    return tags


def apply_tags_mp3(filepath: Path, tags: TagData):
    """Apply cleaned tags to MP3 file."""
    try:
        # Delete all existing tags
        audio = ID3(filepath)
        audio.delete()

        # Create new ID3 tag
        audio = ID3()

        if tags.artist:
            audio.add(TPE1(encoding=3, text=tags.artist))

        if tags.album_artist:
            audio.add(TPE2(encoding=3, text=tags.album_artist))

        if tags.title:
            audio.add(TIT2(encoding=3, text=tags.title))

        if tags.album:
            audio.add(TALB(encoding=3, text=tags.album))

        if tags.genre:
            audio.add(TCON(encoding=3, text=tags.genre))

        if tags.year:
            audio.add(TDRC(encoding=3, text=tags.year))

        if tags.track_number:
            track_str = str(tags.track_number)
            if tags.total_tracks:
                track_str += f"/{tags.total_tracks}"
            audio.add(TRCK(encoding=3, text=track_str))

        if tags.cover_art:
            audio.add(APIC(
                encoding=3,
                mime=tags.cover_mime or 'image/jpeg',
                type=3,  # Front cover
                desc='Front Cover',
                data=tags.cover_art
            ))

        audio.save(filepath, v2_version=3)

    except Exception as e:
        print(f"Error applying MP3 tags to {filepath}: {e}")


def apply_tags_flac(filepath: Path, tags: TagData):
    """Apply cleaned tags to FLAC file."""
    try:
        audio = FLAC(filepath)

        # Clear all existing tags
        audio.clear()
        audio.clear_pictures()

        if tags.artist:
            audio['artist'] = tags.artist

        if tags.album_artist:
            audio['albumartist'] = tags.album_artist

        if tags.title:
            audio['title'] = tags.title

        if tags.album:
            audio['album'] = tags.album

        if tags.genre:
            audio['genre'] = tags.genre

        if tags.year:
            audio['date'] = tags.year

        if tags.track_number:
            track_str = str(tags.track_number)
            if tags.total_tracks:
                track_str += f"/{tags.total_tracks}"
            audio['tracknumber'] = track_str

        if tags.total_tracks:
            audio['totaltracks'] = str(tags.total_tracks)

        if tags.cover_art:
            picture = Picture()
            picture.type = 3  # Front cover
            picture.mime = tags.cover_mime or 'image/jpeg'
            picture.desc = 'Front Cover'
            picture.data = tags.cover_art
            audio.add_picture(picture)

        audio.save()

    except Exception as e:
        print(f"Error applying FLAC tags to {filepath}: {e}")


def apply_tags_m4a(filepath: Path, tags: TagData):
    """Apply cleaned tags to M4A/MP4 file."""
    try:
        audio = MP4(filepath)

        # Clear all existing tags
        audio.clear()

        if tags.artist:
            audio['\xa9ART'] = tags.artist

        if tags.album_artist:
            audio['aART'] = tags.album_artist

        if tags.title:
            audio['\xa9nam'] = tags.title

        if tags.album:
            audio['\xa9alb'] = tags.album

        if tags.genre:
            audio['\xa9gen'] = tags.genre

        if tags.year:
            audio['\xa9day'] = tags.year

        if tags.track_number:
            if tags.total_tracks:
                audio['trkn'] = [(tags.track_number, tags.total_tracks)]
            else:
                audio['trkn'] = [(tags.track_number, 0)]

        if tags.cover_art:
            # Determine format
            if tags.cover_mime == 'image/png':
                imageformat = MP4Cover.FORMAT_PNG
            else:
                imageformat = MP4Cover.FORMAT_JPEG

            audio['covr'] = [MP4Cover(tags.cover_art, imageformat=imageformat)]

        audio.save()

    except Exception as e:
        print(f"Error applying M4A tags to {filepath}: {e}")


def process_file(filepath: Path) -> bool:
    """Process a single music file."""
    ext = filepath.suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        return False

    print(f"Processing: {filepath.name}")

    # Extract tags based on file type
    if ext == '.mp3':
        tags = extract_tags_mp3(filepath)
        apply_tags_mp3(filepath, tags)
    elif ext == '.flac':
        tags = extract_tags_flac(filepath)
        apply_tags_flac(filepath, tags)
    elif ext in {'.m4a', '.mp4', '.m4b', '.m4p'}:
        tags = extract_tags_m4a(filepath)
        apply_tags_m4a(filepath, tags)
    else:
        print(f"  Skipping unsupported format: {ext}")
        return False

    print(f"  ✓ Cleaned tags: {tags}")
    return True


def process_directory(directory: str):
    """Process all music files in a directory."""
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        sys.exit(1)

    # Find all music files
    music_files = []
    for ext in SUPPORTED_EXTENSIONS:
        music_files.extend(dir_path.glob(f"*{ext}"))

    if not music_files:
        print(f"No music files found in '{directory}'")
        return

    print(f"Found {len(music_files)} music file(s)\n")

    processed = 0
    for filepath in sorted(music_files):
        if process_file(filepath):
            processed += 1
        print()

    print(f"Processed {processed}/{len(music_files)} files successfully.")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python clean_music_tags.py <directory>")
        print("\nThis script will:")
        print("  1. Read all music files in the specified directory")
        print("  2. Extract essential ID3 tags (Artist, Album Artist, Title, etc.)")
        print("  3. Strip all other metadata")
        print("  4. Re-apply only the essential tags")
        print(f"\nSupported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
        sys.exit(1)

    directory = sys.argv[1]

    try:
        process_directory(directory)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
