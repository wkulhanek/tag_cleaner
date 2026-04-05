# Development Notes and Directives

This file contains important lessons learned, directives, and best practices for working on this project.

## Python Environment Directives

### ✅ ALWAYS use virtual environments
- **Never** install Python packages system-wide
- **Always** create and activate a virtual environment before installing dependencies
- Use the existing venv if it exists: `source venv/bin/activate`
- If no venv exists: `python3 -m venv venv && source venv/bin/activate`

### ✅ Dependency management
- Install dependencies with: `pip install -r requirements.txt`
- Add new dependencies to `requirements.txt`
- Never commit `venv/` directory

## Testing Directives

### ✅ Test with real files
- Create test files in `/tmp/` or similar temporary directories
- Use `ffmpeg` to generate test audio files with specific metadata:
  ```bash
  ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 10 \
    -c:a libmp3lame -b:a 128k \
    -metadata title="Test Song" \
    -metadata track="1/10" \
    -metadata artist="Test Artist" \
    -metadata album="Test Album" \
    "test_song.mp3" -y
  ```

### ✅ Test edge cases
- Case-sensitive filename conflicts
- Multiple files with same track numbers
- Different bitrates for conflict resolution
- Various audio formats (MP3, FLAC, M4A, OGG)

## Code Quality Directives

### ✅ Follow existing code style
- Match existing indentation (4 spaces)
- Use type hints for all functions
- Add docstrings for new functions
- Follow existing naming conventions

### ✅ Error handling
- Use try-except blocks for file operations
- Provide informative error messages
- Don't crash on individual file failures

## Git Workflow

### ✅ Branch strategy
- Create feature branches: `git checkout -b feature/description`
- Use descriptive branch names
- Keep main branch stable

### ✅ Commit messages
- Use imperative mood ("Add feature" not "Added feature")
- First line: short summary (<50 chars)
- Blank line
- Detailed explanation if needed
- Reference issues if applicable

## Lessons Learned

### 🔧 Conflict Resolution Implementation
- **Problem**: Case-sensitive files with same track numbers caused random behavior
- **Solution**: Compare bitrates and keep highest quality version
- **Key Insight**: Must recalculate track counts AFTER deleting duplicates

### 🔢 Track Numbering Fix
- **Problem**: Track counts were wrong after conflict resolution (e.g., 1/3 instead of 1/2)
- **Solution**: Recalculate `tracks_per_disc` after deleting duplicate files
- **Key Insight**: Initial count included files that would be deleted

### 🗃️ File Management
- **Problem**: Files were being deleted incorrectly during renaming
- **Solution**: Delete lower-quality files BEFORE processing/renaming higher-quality ones
- **Key Insight**: Preserve original file paths until conflict resolution is complete

### 🔍 Bitrate Extraction
- **Challenge**: Different audio formats store bitrate differently
- **Solution**: Create `get_bitrate()` function with format-specific logic
- **Key Insight**: Use mutagen's format-specific classes (MP3, FLAC, etc.)

## Debugging Tips

### 🐛 Common Issues
- **ModuleNotFoundError**: Forgot to activate virtual environment
- **FileNotFoundError**: Test files not created properly
- **Metadata errors**: FFmpeg metadata format issues

### 🔍 Debugging Tools
- Check file metadata: `mutagen-inspect filename.mp3`
- List files with bitrates: `mediainfo *.mp3`
- Test individual functions in Python REPL

## Future Improvements

### 🚀 Potential Enhancements
- Add unit tests with pytest
- Support more audio formats
- Add dry-run mode
- Implement logging instead of print statements
- Add progress indicators for large collections

### 📊 Metrics to Track
- Files processed vs files with conflicts
- Space saved by deleting duplicates
- Quality improvements (average bitrate changes)

---

*Last updated: 2024-04-05*
*Maintainer: Wolfgang Kulhanek <wolfgang@famkulhanek.com>*