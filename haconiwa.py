#!/usr/bin/env python3
"""
Haconiwa - AI-powered collaborative development support tool
"""

import argparse
import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml


class HaconiwaConfig:
    """Configuration manager for Haconiwa"""
    
    def __init__(self, config_path: str = "haconiwa.yaml"):
        self.config_path = Path(config_path)
        self.config = {}
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            print(f"Configuration file {self.config_path} not found")
            return {}
            
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
                return self.config
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to YAML file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False


class HaconiwaWorkspace:
    """Workspace management for Haconiwa"""
    
    def __init__(self, config: HaconiwaConfig):
        self.config = config
        
    def _run_tmux_command(self, command: List[str]) -> bool:
        """Run tmux command and return success status"""
        try:
            result = subprocess.run(['tmux'] + command, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"tmux command failed: {e}")
            return False
        except FileNotFoundError:
            print("tmux not found. Please install tmux first.")
            return False
    
    def _session_exists(self, session_name: str) -> bool:
        """Check if tmux session exists"""
        try:
            result = subprocess.run(['tmux', 'has-session', '-t', session_name], 
                                  capture_output=True, 
                                  text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
        
    def create_workspace(self, name: str) -> bool:
        """Create a new workspace with tmux session"""
        session_name = f"haconiwa-{name}"
        
        if self._session_exists(session_name):
            print(f"Workspace '{name}' already exists")
            return False
        
        print(f"Creating workspace: {name}")
        
        # Create tmux session
        if not self._run_tmux_command(['new-session', '-d', '-s', session_name]):
            return False
        
        # Create default windows
        self._run_tmux_command(['rename-window', '-t', f'{session_name}:0', 'main'])
        self._run_tmux_command(['new-window', '-t', session_name, '-n', 'editor'])
        self._run_tmux_command(['new-window', '-t', session_name, '-n', 'terminal'])
        
        # Split main window into panes
        self._run_tmux_command(['split-window', '-t', f'{session_name}:main', '-h'])
        self._run_tmux_command(['split-window', '-t', f'{session_name}:main.1', '-v'])
        
        print(f"Workspace '{name}' created successfully")
        print(f"Attach with: tmux attach-session -t {session_name}")
        return True
        
    def list_workspaces(self) -> List[str]:
        """List all Haconiwa workspaces"""
        try:
            result = subprocess.run(['tmux', 'list-sessions'], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            
            workspaces = []
            for line in result.stdout.strip().split('\n'):
                if line and 'haconiwa-' in line:
                    session_name = line.split(':')[0]
                    workspace_name = session_name.replace('haconiwa-', '')
                    workspaces.append(workspace_name)
            
            return workspaces
        except subprocess.CalledProcessError:
            return []
        except FileNotFoundError:
            print("tmux not found. Please install tmux first.")
            return []
        
    def delete_workspace(self, name: str) -> bool:
        """Delete a workspace and its tmux session"""
        session_name = f"haconiwa-{name}"
        
        if not self._session_exists(session_name):
            print(f"Workspace '{name}' does not exist")
            return False
        
        print(f"Deleting workspace: {name}")
        
        if self._run_tmux_command(['kill-session', '-t', session_name]):
            print(f"Workspace '{name}' deleted successfully")
            return True
        else:
            return False
    
    def attach_workspace(self, name: str) -> bool:
        """Attach to a workspace"""
        session_name = f"haconiwa-{name}"
        
        if not self._session_exists(session_name):
            print(f"Workspace '{name}' does not exist")
            return False
        
        print(f"Attaching to workspace: {name}")
        try:
            os.execvp('tmux', ['tmux', 'attach-session', '-t', session_name])
        except FileNotFoundError:
            print("tmux not found. Please install tmux first.")
            return False


class HaconiwaGit:
    """Git worktree management for Haconiwa"""
    
    def __init__(self, config: HaconiwaConfig):
        self.config = config
        
    def _run_git_command(self, command: List[str], cwd: str = None) -> tuple[bool, str]:
        """Run git command and return success status and output"""
        try:
            result = subprocess.run(['git'] + command, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True,
                                  cwd=cwd)
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {e}")
            return False, e.stderr.strip() if e.stderr else ""
        except FileNotFoundError:
            print("Git not found. Please install git first.")
            return False, ""
    
    def _is_git_repo(self, path: str = ".") -> bool:
        """Check if current directory is a git repository"""
        success, _ = self._run_git_command(['rev-parse', '--git-dir'], cwd=path)
        return success
    
    def create_worktree(self, path: str, branch: str) -> bool:
        """Create git worktree"""
        if not self._is_git_repo():
            print("Not in a git repository. Please run this command from a git repository.")
            return False
        
        worktree_path = Path(path).resolve()
        
        if worktree_path.exists():
            print(f"Path '{path}' already exists")
            return False
        
        print(f"Creating worktree: {path} on branch {branch}")
        
        # Check if branch exists
        success, output = self._run_git_command(['branch', '--list', branch])
        if not success:
            return False
        
        # Create new branch if it doesn't exist
        if branch not in output:
            print(f"Creating new branch: {branch}")
            success, _ = self._run_git_command(['branch', branch])
            if not success:
                return False
        
        # Create worktree
        success, _ = self._run_git_command(['worktree', 'add', str(worktree_path), branch])
        if success:
            print(f"Worktree created successfully at {worktree_path}")
            return True
        else:
            return False
        
    def list_worktrees(self) -> List[Dict[str, str]]:
        """List all worktrees"""
        if not self._is_git_repo():
            print("Not in a git repository.")
            return []
        
        success, output = self._run_git_command(['worktree', 'list', '--porcelain'])
        if not success:
            return []
        
        worktrees = []
        current_worktree = {}
        
        for line in output.split('\n'):
            if line.startswith('worktree '):
                if current_worktree:
                    worktrees.append(current_worktree)
                    current_worktree = {}
                current_worktree['path'] = line.split(' ', 1)[1]
            elif line.startswith('HEAD '):
                current_worktree['commit'] = line.split(' ', 1)[1]
            elif line.startswith('branch '):
                current_worktree['branch'] = line.split(' ', 1)[1]
            elif line.startswith('bare'):
                current_worktree['bare'] = True
        
        if current_worktree:
            worktrees.append(current_worktree)
        
        return worktrees
        
    def remove_worktree(self, path: str) -> bool:
        """Remove git worktree"""
        if not self._is_git_repo():
            print("Not in a git repository.")
            return False
        
        worktree_path = Path(path).resolve()
        
        # Check if worktree exists
        worktrees = self.list_worktrees()
        worktree_exists = any(wt['path'] == str(worktree_path) for wt in worktrees)
        
        if not worktree_exists:
            print(f"Worktree '{path}' does not exist")
            return False
        
        print(f"Removing worktree: {path}")
        
        # Remove worktree
        success, _ = self._run_git_command(['worktree', 'remove', str(worktree_path)])
        if success:
            print(f"Worktree removed successfully: {path}")
            return True
        else:
            return False
    
    def prune_worktrees(self) -> bool:
        """Prune stale worktree references"""
        if not self._is_git_repo():
            print("Not in a git repository.")
            return False
        
        print("Pruning stale worktrees...")
        success, _ = self._run_git_command(['worktree', 'prune'])
        if success:
            print("Worktrees pruned successfully")
            return True
        else:
            return False


class HaconiwaAI:
    """AI integration for Haconiwa"""
    
    def __init__(self, config: HaconiwaConfig):
        self.config = config
        
    def setup_ai_agent(self, name: str, permissions: List[str]) -> bool:
        """Setup AI agent with permissions"""
        print(f"Setting up AI agent: {name} with permissions: {permissions}")
        # TODO: Implement AI agent setup
        return True
        
    def list_ai_agents(self) -> List[str]:
        """List all AI agents"""
        # TODO: Implement AI agent listing
        return []


class HaconiwaCLI:
    """Main CLI interface for Haconiwa"""
    
    def __init__(self):
        self.config = HaconiwaConfig()
        self.workspace = HaconiwaWorkspace(self.config)
        self.git = HaconiwaGit(self.config)
        self.ai = HaconiwaAI(self.config)
        
    def create_default_config(self) -> None:
        """Create default configuration file"""
        default_config = {
            'nation': 'MyNation',
            'city': 'MyCity',
            'company': 'MyCompany',
            'rooms': {
                'main': {
                    'type': 'development',
                    'tmux_session': 'haconiwa-main',
                    'git_worktree': True
                }
            },
            'ai_agents': {
                'claude': {
                    'permissions': ['read', 'write', 'execute'],
                    'workspace_access': ['main']
                }
            }
        }
        
        if self.config.save_config(default_config):
            print("Default configuration created: haconiwa.yaml")
        else:
            print("Failed to create default configuration")
    
    def init_command(self, args) -> None:
        """Initialize Haconiwa workspace"""
        print("Initializing Haconiwa workspace...")
        
        if not Path("haconiwa.yaml").exists():
            self.create_default_config()
        
        config = self.config.load_config()
        print(f"Nation: {config.get('nation', 'Unknown')}")
        print(f"City: {config.get('city', 'Unknown')}")
        print(f"Company: {config.get('company', 'Unknown')}")
        print("Initialization complete!")
    
    def workspace_command(self, args) -> None:
        """Workspace management commands"""
        if args.action == 'create':
            self.workspace.create_workspace(args.name)
        elif args.action == 'list':
            workspaces = self.workspace.list_workspaces()
            print("Workspaces:")
            for ws in workspaces:
                print(f"  - {ws}")
        elif args.action == 'delete':
            self.workspace.delete_workspace(args.name)
        elif args.action == 'attach':
            self.workspace.attach_workspace(args.name)
    
    def git_command(self, args) -> None:
        """Git worktree management commands"""
        if args.action == 'create':
            self.git.create_worktree(args.path, args.branch)
        elif args.action == 'list':
            worktrees = self.git.list_worktrees()
            print("Worktrees:")
            for wt in worktrees:
                branch = wt.get('branch', 'detached')
                path = wt.get('path', 'unknown')
                print(f"  - {path} ({branch})")
        elif args.action == 'remove':
            self.git.remove_worktree(args.path)
        elif args.action == 'prune':
            self.git.prune_worktrees()
    
    def ai_command(self, args) -> None:
        """AI agent management commands"""
        if args.action == 'setup':
            permissions = args.permissions.split(',') if args.permissions else []
            self.ai.setup_ai_agent(args.name, permissions)
        elif args.action == 'list':
            agents = self.ai.list_ai_agents()
            print("AI Agents:")
            for agent in agents:
                print(f"  - {agent}")
    
    def status_command(self, args) -> None:
        """Show Haconiwa status"""
        config = self.config.load_config()
        
        print("=== Haconiwa Status ===")
        print(f"Nation: {config.get('nation', 'Not set')}")
        print(f"City: {config.get('city', 'Not set')}")
        print(f"Company: {config.get('company', 'Not set')}")
        
        rooms = config.get('rooms', {})
        print(f"Rooms: {len(rooms)}")
        for room_name, room_config in rooms.items():
            print(f"  - {room_name}: {room_config.get('type', 'unknown')}")
        
        ai_agents = config.get('ai_agents', {})
        print(f"AI Agents: {len(ai_agents)}")
        for agent_name in ai_agents:
            print(f"  - {agent_name}")
    
    def run(self) -> None:
        """Run the CLI application"""
        parser = argparse.ArgumentParser(
            description="Haconiwa - AI-powered collaborative development support tool"
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Init command
        init_parser = subparsers.add_parser('init', help='Initialize Haconiwa workspace')
        init_parser.set_defaults(func=self.init_command)
        
        # Status command
        status_parser = subparsers.add_parser('status', help='Show Haconiwa status')
        status_parser.set_defaults(func=self.status_command)
        
        # Workspace commands
        workspace_parser = subparsers.add_parser('workspace', help='Workspace management')
        workspace_subparsers = workspace_parser.add_subparsers(dest='action')
        
        workspace_create = workspace_subparsers.add_parser('create', help='Create workspace')
        workspace_create.add_argument('name', help='Workspace name')
        
        workspace_list = workspace_subparsers.add_parser('list', help='List workspaces')
        
        workspace_delete = workspace_subparsers.add_parser('delete', help='Delete workspace')
        workspace_delete.add_argument('name', help='Workspace name')
        
        workspace_attach = workspace_subparsers.add_parser('attach', help='Attach to workspace')
        workspace_attach.add_argument('name', help='Workspace name')
        
        workspace_parser.set_defaults(func=self.workspace_command)
        
        # Git commands
        git_parser = subparsers.add_parser('git', help='Git worktree management')
        git_subparsers = git_parser.add_subparsers(dest='action')
        
        git_create = git_subparsers.add_parser('create', help='Create worktree')
        git_create.add_argument('path', help='Worktree path')
        git_create.add_argument('branch', help='Branch name')
        
        git_list = git_subparsers.add_parser('list', help='List worktrees')
        
        git_remove = git_subparsers.add_parser('remove', help='Remove worktree')
        git_remove.add_argument('path', help='Worktree path')
        
        git_prune = git_subparsers.add_parser('prune', help='Prune stale worktrees')
        
        git_parser.set_defaults(func=self.git_command)
        
        # AI commands
        ai_parser = subparsers.add_parser('ai', help='AI agent management')
        ai_subparsers = ai_parser.add_subparsers(dest='action')
        
        ai_setup = ai_subparsers.add_parser('setup', help='Setup AI agent')
        ai_setup.add_argument('name', help='Agent name')
        ai_setup.add_argument('--permissions', help='Comma-separated permissions')
        
        ai_list = ai_subparsers.add_parser('list', help='List AI agents')
        
        ai_parser.set_defaults(func=self.ai_command)
        
        # Parse and execute
        args = parser.parse_args()
        
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()


def main():
    """Main entry point"""
    cli = HaconiwaCLI()
    cli.run()


if __name__ == '__main__':
    main()