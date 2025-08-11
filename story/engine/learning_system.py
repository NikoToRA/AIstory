#!/usr/bin/env python3
"""
AIstory Learning System
ユーザー評価からAI改善点を学習するシステム
"""

import json
import statistics
from datetime import datetime
from pathlib import Path

class LearningSystem:
    def __init__(self, evaluations_path="evaluations/story_evaluations.json"):
        self.evaluations_path = Path(evaluations_path)
        self.data = self.load_evaluations()
    
    def load_evaluations(self):
        """評価データを読み込み"""
        if self.evaluations_path.exists():
            with open(self.evaluations_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "stories": [],
            "evaluation_history": [],
            "learning_patterns": {
                "high_rated_features": [],
                "low_rated_features": [],
                "improvement_suggestions": []
            },
            "statistics": {
                "total_stories": 0,
                "average_ai_score": 0,
                "average_user_rating": 0,
                "promotion_rate": 0,
                "user_satisfaction_trend": []
            }
        }
    
    def add_evaluation(self, story_data, user_rating, user_feedback):
        """新しい評価を追加"""
        evaluation_entry = {
            "story_id": story_data["story_id"],
            "issue_number": story_data["issue_number"],
            "creation_date": story_data["creation_date"],
            "ai_evaluation": story_data["ai_evaluation"],
            "user_evaluation": {
                "rating": user_rating,
                "feedback": user_feedback,
                "evaluation_date": datetime.now().isoformat()
            },
            "final_status": self.determine_status(story_data["ai_evaluation"], user_rating),
            "learning_points": self.extract_learning_points(user_rating, user_feedback)
        }
        
        self.data["stories"].append(evaluation_entry)
        self.update_statistics()
        self.update_learning_patterns()
        self.save_evaluations()
        
        return evaluation_entry
    
    def determine_status(self, ai_eval, user_rating):
        """昇格判定"""
        ai_score = ai_eval.get("total_score", 0)
        
        if user_rating >= 9:
            return "promoted_to_manga"
        elif user_rating >= 7 and ai_score >= 75:
            return "promoted_to_manga"
        elif user_rating >= 5:
            return "completed"
        else:
            return "needs_improvement"
    
    def extract_learning_points(self, rating, feedback):
        """学習ポイント抽出"""
        points = []
        
        if rating >= 8:
            points.append("高評価要因を分析")
        if rating <= 3:
            points.append("低評価要因を改善")
        
        # フィードバックからキーワード抽出
        if "ギャル" in feedback or "チャッピー" in feedback:
            points.append("チャッピーのキャラクター特性に注目")
        if "規約" in feedback or "ジェミー" in feedback:
            points.append("ジェミーちゃんのキャラクター特性に注目")
        if "会話" in feedback:
            points.append("対話品質に注目")
        if "オチ" in feedback:
            points.append("物語構成に注目")
            
        return points
    
    def update_statistics(self):
        """統計情報更新"""
        stories = self.data["stories"]
        if not stories:
            return
        
        total = len(stories)
        ai_scores = [s["ai_evaluation"]["total_score"] for s in stories]
        user_ratings = [s["user_evaluation"]["rating"] for s in stories]
        promotions = len([s for s in stories if s["final_status"] == "promoted_to_manga"])
        
        self.data["statistics"] = {
            "total_stories": total,
            "average_ai_score": round(statistics.mean(ai_scores), 2),
            "average_user_rating": round(statistics.mean(user_ratings), 2),
            "promotion_rate": round((promotions / total) * 100, 2),
            "user_satisfaction_trend": user_ratings[-10:]  # 直近10件
        }
    
    def update_learning_patterns(self):
        """学習パターン更新"""
        high_rated = [s for s in self.data["stories"] if s["user_evaluation"]["rating"] >= 7]
        low_rated = [s for s in self.data["stories"] if s["user_evaluation"]["rating"] <= 4]
        
        # 高評価の特徴分析
        high_features = []
        for story in high_rated:
            ai_eval = story["ai_evaluation"]
            if ai_eval.get("dialogue_quality", 0) >= 80:
                high_features.append("高品質な対話")
            if ai_eval.get("entertainment_score", 0) >= 85:
                high_features.append("高い面白さ")
        
        # 低評価の特徴分析
        low_features = []
        for story in low_rated:
            ai_eval = story["ai_evaluation"]
            if ai_eval.get("character_consistency", 0) < 70:
                low_features.append("キャラクター一貫性不足")
            if ai_eval.get("story_structure", 0) < 70:
                low_features.append("物語構成の問題")
        
        # 改善提案生成
        suggestions = []
        if "キャラクター一貫性不足" in low_features:
            suggestions.append("profile.txtの特徴をより強く反映")
        if "物語構成の問題" in low_features:
            suggestions.append("起承転結をより明確に")
        if len(high_rated) > 0:
            suggestions.append("高評価作品の手法を他作品にも適用")
        
        self.data["learning_patterns"] = {
            "high_rated_features": list(set(high_features)),
            "low_rated_features": list(set(low_features)),
            "improvement_suggestions": suggestions
        }
    
    def get_improvement_suggestions(self):
        """改善提案取得"""
        return self.data["learning_patterns"]["improvement_suggestions"]
    
    def get_success_patterns(self):
        """成功パターン取得"""
        return self.data["learning_patterns"]["high_rated_features"]
    
    def save_evaluations(self):
        """評価データ保存"""
        self.evaluations_path.parent.mkdir(exist_ok=True)
        with open(self.evaluations_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

# 使用例
if __name__ == "__main__":
    learning = LearningSystem()
    
    # サンプル評価追加
    sample_story = {
        "story_id": "2024-01-08_test",
        "issue_number": 1,
        "creation_date": "2024-01-08T10:00:00Z",
        "ai_evaluation": {
            "entertainment_score": 85,
            "dialogue_quality": 78,
            "character_consistency": 92,
            "story_structure": 80,
            "total_score": 83.75
        }
    }
    
    learning.add_evaluation(sample_story, 8, "チャッピーのギャル語が面白い")
    print("評価を追加しました")
    print(f"改善提案: {learning.get_improvement_suggestions()}")