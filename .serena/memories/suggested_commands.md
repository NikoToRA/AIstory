# Suggested Commands for AIstory Project

## Development Commands

### Python Environment
```bash
# Run main CLI tool
python3 haconiwa.py --help

# Initialize workspace
python3 haconiwa.py init

# Check status
python3 haconiwa.py status

# Workspace management
python3 haconiwa.py workspace create my-workspace
python3 haconiwa.py workspace list
python3 haconiwa.py workspace delete my-workspace
```

### Git Operations
```bash
# Standard git commands
git status
git add .
git commit -m "message"
git push

# Git worktree management (via Haconiwa)
python3 haconiwa.py git create ./feature-branch feature-branch
python3 haconiwa.py git list
python3 haconiwa.py git remove ./feature-branch
```

### Story System Testing
```bash
# Manual story generation testing
python3 manual_test.py

# Character growth demonstration
python3 character_growth_demo.py

# Story evaluation
python3 evaluate_story.py

# Complex relationship development
python3 complex_relationship_development.py
```

### File Operations (Darwin/macOS)
```bash
# Directory listing
ls -la
ls story-world/characters/

# File searching
find . -name "*.py"
find story-world -name "*.json"

# Content searching
grep -r "チャッピー" story-world/
grep -r "class " *.py
```

### GitHub Integration
```bash
# Trigger GitHub Actions manually (if needed)
# Actions run automatically on Issue creation with 'scenario' or 'story' labels
```

## No Build/Test/Lint Commands Identified
⚠️ **Important**: No specific linting, testing, or formatting commands were found in the codebase. The project appears to be in development phase without formal testing infrastructure.

## System Commands (Darwin)
```bash
# Python version check
python3 -c "import sys; print(sys.version)"

# Dependency installation
pip3 install -r requirements.txt

# Check available commands
which python3 git ls find grep
```

## Configuration Files
- `haconiwa.yaml` - Main configuration
- `story-world/claude.md` - AI system configuration
- `requirements.txt` - Python dependencies
- `.github/workflows/aistory.yml` - GitHub Actions automation