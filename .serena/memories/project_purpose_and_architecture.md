# AIstory Project - Purpose and Architecture

## Project Purpose
AIstory is a dual-purpose project combining two systems:
1. **Haconiwa** - An AI-powered collaborative development support tool for managing complex development environments
2. **AIstory System** - An AI-driven story/manga generation system with GitHub integration

## Architecture Overview

### Core Components
1. **Haconiwa CLI Tool** (`haconiwa.py`)
   - Python-based CLI for workspace management
   - YAML configuration system
   - Git worktree support
   - tmux-based multi-pane workspace creation
   - AI agent coordination

2. **AIstory Character System** (`story-world/`)
   - AI character interaction system (Chappie & Gemmy)
   - GitHub Issues-based story generation
   - Automated character responses via GitHub Actions
   - Character memory and relationship tracking

### Key Features
- **Declarative YAML configurations** - Environment setup through `haconiwa.yaml`
- **Hierarchical organization** - Nations → Cities → Companies → Rooms structure
- **AI Character Simulation** - Realistic character interactions with memory persistence
- **Automated Story Generation** - GitHub Issues trigger AI-generated character dialogues
- **Character Growth System** - Characters learn and evolve through interactions

## Current Status
- Project is 90% complete according to CLAUDE.md
- 13 episodes of character stories already generated
- Complex relationship development system implemented
- GitHub Actions automation working
- Next phase: Moving from 4-panel manga to chat-style format with facial expressions

## File Structure
```
/
├── haconiwa.py              # Main CLI tool
├── haconiwa.yaml            # Configuration file
├── requirements.txt         # Python dependencies
├── story-world/             # AIstory system
│   ├── characters/          # Character profiles & memory
│   ├── stories/             # Generated stories
│   ├── engine/              # Story generation engine
│   └── .github/workflows/   # Automation
└── *.py                     # Various utility scripts
```