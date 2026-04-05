# AGENTS.md

This file contains guidelines and commands for agentic coding agents working in this repository.

## Project Overview

This is a simple Python utility for cleaning music file metadata tags. The project consists of:
- `clean_music_tags.py` - Main Python script with comprehensive tag cleaning functionality
- `clean_tags` - Bash wrapper script that activates a virtual environment
- `requirements.txt` - Python dependencies (mutagen>=1.47.0)

## Development Commands

### Running the Application
```bash
# Direct execution
python3 clean_music_tags.py <directory>

# Via wrapper script (recommended)
./clean_tags <directory>
```

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv ~/Development/virtualenvs/tag_cleaner
source ~/Development/virtualenvs/tag_cleaner/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Testing
**No testing framework is currently configured.** To add testing:
1. Install pytest: `pip install pytest`
2. Create `tests/` directory
3. Add test files with `test_*.py` naming convention
4. Run tests: `pytest tests/`
5. Run single test: `pytest tests/test_specific.py::test_function`

### Code Quality Tools
**No linting or formatting tools are currently configured.** Recommended additions:
```bash
# Install code quality tools
pip install black flake8 mypy

# Format code
black clean_music_tags.py

# Lint code
flake8 clean_music_tags.py

# Type checking
mypy clean_music_tags.py
```

## Code Style Guidelines

### Python Conventions
- **Python Version**: 3.6+ (tested with 3.14.2)
- **Shebang**: Use `#!/usr/bin/env python3` at top of main script
- **Type Hints**: Required for all function parameters and return values
- **Docstrings**: Use triple-quoted strings for all functions and classes
- **Error Handling**: Use try-except blocks with informative error messages

### Import Organization
```python
# Standard library imports first
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Third-party imports second
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
```

### Naming Conventions
- **Functions**: `snake_case` with descriptive names (e.g., `extract_flac_tags`)
- **Variables**: `snake_case` (e.g., `tag_data`, `file_path`)
- **Constants**: `UPPER_SNAKE_CASE` (if added)
- **Classes**: `PascalCase` (e.g., `TagData`)

### Code Structure
- **Single Responsibility**: Each function should handle one specific task
- **Function Organization**: Group related functions (extract/apply per format)
- **Class Design**: Simple data containers with `__repr__` methods
- **Main Execution**: Use `if __name__ == "__main__":` guard

### Error Handling Patterns
```python
try:
    # Operation that might fail
    result = some_operation()
except SpecificException as e:
    print(f"Error description: {e}")
    return None  # or appropriate fallback
except Exception as e:
    print(f"Unexpected error: {e}")
    raise
```

### Type Hinting Guidelines
```python
from typing import Dict, List, Optional, Tuple, Union

# Function signatures
def extract_flac_tags(file_path: str) -> Optional[TagData]:
    pass

# Variable annotations
tag_mapping: Dict[int, int] = {0: 0, 1: 1}
```

## File Organization

### Current Structure
- Root directory contains all files (flat structure)
- Main script: `clean_music_tags.py` (634 lines)
- Wrapper script: `clean_tags`
- Dependencies: `requirements.txt`

### Adding New Files
- Keep flat structure for simplicity
- Name files descriptively (e.g., `utils.py`, `config.py`)
- Update `requirements.txt` if adding new dependencies

## Development Workflow

### Making Changes
1. Read existing code to understand patterns
2. Follow established naming conventions and style
3. Add type hints and docstrings to new functions
4. Test changes manually with sample files
5. Update README.md if user-facing changes

### Git Workflow
- Use descriptive commit messages
- Current author: Wolfgang Kulhanek <wolfgang@famkulhanek.com>
- No CI/CD configured (all changes are manual)

## Dependencies

### Current Dependencies
- `mutagen>=1.47.0` - Audio metadata library

### Adding Dependencies
1. Update `requirements.txt` with new package and version
2. Install in virtual environment: `pip install -r requirements.txt`
3. Test functionality before committing

## User Interface Guidelines

### Command Line Interface
- Single positional argument: directory path
- Use print statements for user feedback
- Provide clear error messages for invalid input
- Show progress for operations on multiple files

### Output Format
- Use f-strings for formatted output
- Include file paths in error messages
- Show summary statistics when appropriate

## Security Considerations

- Validate file paths and directory access
- Handle file permissions gracefully
- Don't expose system information unnecessarily
- Use relative paths where possible

## Performance Guidelines

- Process files sequentially (no current need for parallelization)
- Use efficient file operations
- Minimize memory usage for large file collections
- Consider adding progress indicators for long operations

## Testing Strategy

### Manual Testing
- Test with various audio formats (MP3, FLAC, OGG)
- Verify tag extraction and application
- Test error conditions (missing files, permissions)

### Future Automated Testing
When adding pytest:
- Test each extraction function with sample files
- Test error handling paths
- Use fixtures for test audio files
- Mock file system operations for unit tests