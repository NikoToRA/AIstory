# Haconiwa

AI-powered collaborative development support tool

## Overview

Haconiwa is a Python CLI tool that manages complex development environments using:
- Declarative YAML configurations
- Hierarchical organization modeling (nations → cities → companies → rooms)
- Git worktree support for parallel task development
- tmux-based multi-room, multi-pane workspace creation
- AI agent coordination and permission management

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Initialize a new workspace

```bash
python haconiwa.py init
```

### Check status

```bash
python haconiwa.py status
```

### Workspace management

```bash
# Create a new workspace
python haconiwa.py workspace create my-workspace

# List workspaces
python haconiwa.py workspace list

# Delete a workspace
python haconiwa.py workspace delete my-workspace
```

### Git worktree management

```bash
# Create a worktree
python haconiwa.py git create ./feature-branch feature-branch

# List worktrees
python haconiwa.py git list

# Remove a worktree
python haconiwa.py git remove ./feature-branch
```

### AI agent management

```bash
# Setup AI agent
python haconiwa.py ai setup claude --permissions read,write,execute

# List AI agents
python haconiwa.py ai list
```

## Configuration

The configuration is stored in `haconiwa.yaml`:

```yaml
nation: MyNation
city: MyCity
company: MyCompany
rooms:
  main:
    type: development
    tmux_session: haconiwa-main
    git_worktree: true
ai_agents:
  claude:
    permissions: [read, write, execute]
    workspace_access: [main]
```

## Development Status

This is an alpha version. Core features are implemented as placeholders and will be expanded in future versions.