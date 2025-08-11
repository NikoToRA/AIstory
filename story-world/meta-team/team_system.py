#!/usr/bin/env python3
"""
AIstory メタチーム連携システム
各担当者の協力・管理・品質管理を統合
"""

import json
import os
from datetime import datetime
from pathlib import Path

class MetaTeamSystem:
    """メタチーム全体の連携・管理システム"""
    
    def __init__(self):
        self.team_path = Path("story-world/meta-team")
        self.projects_path = self.team_path / "projects"
        self.projects_path.mkdir(exist_ok=True)
        
        # チームメンバー定義
        self.team_members = {
            "producer": "総合責任者（プロデューサー）",
            "writer": "テキスト記事担当者",
            "video-creator": "動画制作担当者", 
            "graphic-designer": "画像制作担当者"
        }
    
    def create_project(self, title: str, description: str, assigned_members: list, priority: str = "medium") -> dict:
        """
        新規プロジェクト作成
        
        Args:
            title: プロジェクトタイトル
            description: 概要・詳細
            assigned_members: 担当メンバーリスト
            priority: 優先度 (low/medium/high/urgent)
            
        Returns:
            プロジェクトデータ
        """
        project_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{title.replace(' ', '_')}"
        
        project_data = {
            "id": project_id,
            "title": title,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "status": "planning",
            "priority": priority,
            "assigned_members": assigned_members,
            "tasks": {},
            "deliverables": {},
            "timeline": {
                "created": datetime.now().isoformat(),
                "planned_start": None,
                "planned_completion": None,
                "actual_start": None,
                "actual_completion": None
            },
            "quality_checkpoints": [],
            "producer_notes": "",
            "final_approval": None
        }
        
        # プロジェクトディレクトリ作成
        project_dir = self.projects_path / project_id
        project_dir.mkdir(exist_ok=True)
        
        # 各担当者用サブディレクトリ作成
        for member in assigned_members:
            if member in self.team_members:
                (project_dir / member).mkdir(exist_ok=True)
                
        # プロジェクトデータ保存
        with open(project_dir / "project.json", 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
            
        print(f"🚀 新規プロジェクト作成: {title}")
        print(f"📁 プロジェクトID: {project_id}")
        print(f"👥 担当者: {', '.join([self.team_members.get(m, m) for m in assigned_members])}")
        
        return project_data
    
    def assign_task(self, project_id: str, member: str, task_title: str, task_details: str, deadline: str = None) -> bool:
        """特定メンバーにタスク割り当て"""
        project_path = self.projects_path / project_id / "project.json"
        
        if not project_path.exists():
            print(f"❌ プロジェクトが見つかりません: {project_id}")
            return False
            
        with open(project_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
            
        task_id = f"{member}_{len(project_data['tasks']) + 1}"
        project_data['tasks'][task_id] = {
            "title": task_title,
            "details": task_details,
            "assigned_to": member,
            "status": "assigned",
            "created_at": datetime.now().isoformat(),
            "deadline": deadline,
            "completed_at": None,
            "deliverable_path": None
        }
        
        with open(project_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ タスク割り当て完了: {task_title} → {self.team_members.get(member, member)}")
        return True
    
    def submit_deliverable(self, project_id: str, member: str, deliverable_type: str, file_path: str, notes: str = "") -> bool:
        """作業成果物の提出"""
        project_path = self.projects_path / project_id / "project.json"
        
        if not project_path.exists():
            return False
            
        with open(project_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
            
        deliverable_id = f"{member}_{deliverable_type}_{datetime.now().strftime('%H%M%S')}"
        project_data['deliverables'][deliverable_id] = {
            "type": deliverable_type,
            "submitted_by": member,
            "file_path": file_path,
            "submitted_at": datetime.now().isoformat(),
            "notes": notes,
            "status": "submitted",
            "quality_check": None,
            "feedback": ""
        }
        
        with open(project_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
            
        print(f"📤 成果物提出: {deliverable_type} by {self.team_members.get(member, member)}")
        return True
    
    def producer_review(self, project_id: str, deliverable_id: str, approved: bool, feedback: str) -> bool:
        """プロデューサーによる品質チェック・承認"""
        project_path = self.projects_path / project_id / "project.json"
        
        if not project_path.exists():
            return False
            
        with open(project_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
            
        if deliverable_id in project_data['deliverables']:
            project_data['deliverables'][deliverable_id].update({
                "quality_check": approved,
                "feedback": feedback,
                "reviewed_at": datetime.now().isoformat(),
                "status": "approved" if approved else "revision_needed"
            })
            
            with open(project_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)
                
            status = "承認" if approved else "要修正"
            print(f"🎬 プロデューサーレビュー完了: {status}")
            return True
        
        return False
    
    def get_project_status(self, project_id: str) -> dict:
        """プロジェクト状況確認"""
        project_path = self.projects_path / project_id / "project.json"
        
        if not project_path.exists():
            return {}
            
        with open(project_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_active_projects(self) -> list:
        """進行中プロジェクト一覧"""
        projects = []
        for project_dir in self.projects_path.iterdir():
            if project_dir.is_dir():
                project_file = project_dir / "project.json"
                if project_file.exists():
                    with open(project_file, 'r', encoding='utf-8') as f:
                        project_data = json.load(f)
                        if project_data.get('status') not in ['completed', 'cancelled']:
                            projects.append(project_data)
        
        return sorted(projects, key=lambda x: x['created_at'], reverse=True)
    
    def generate_team_report(self) -> dict:
        """チーム全体の活動レポート生成"""
        active_projects = self.list_active_projects()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_active_projects": len(active_projects),
            "projects_by_status": {},
            "tasks_by_member": {},
            "recent_deliverables": [],
            "pending_reviews": []
        }
        
        for project in active_projects:
            status = project.get('status', 'unknown')
            report['projects_by_status'][status] = report['projects_by_status'].get(status, 0) + 1
            
            # タスク統計
            for task_id, task in project.get('tasks', {}).items():
                member = task.get('assigned_to')
                if member not in report['tasks_by_member']:
                    report['tasks_by_member'][member] = 0
                report['tasks_by_member'][member] += 1
                
            # 保留中レビュー
            for deliv_id, deliv in project.get('deliverables', {}).items():
                if deliv.get('status') == 'submitted':
                    report['pending_reviews'].append({
                        "project": project['title'],
                        "deliverable": deliv_id,
                        "submitted_by": deliv.get('submitted_by'),
                        "submitted_at": deliv.get('submitted_at')
                    })
        
        return report

# 使用例・テンプレート
if __name__ == "__main__":
    team = MetaTeamSystem()
    
    print("🌟 AIstory メタチーム連携システム")
    print("\n主要機能:")
    print("- team.create_project() : 新規プロジェクト作成")
    print("- team.assign_task() : タスク割り当て")
    print("- team.submit_deliverable() : 成果物提出")
    print("- team.producer_review() : 品質チェック・承認")
    print("- team.generate_team_report() : 活動レポート生成")