#!/usr/bin/env python3
"""
ターミナル評価システム
生成された物語を10段階評価してフィードバックを蓄積
"""

import json
import os
from datetime import datetime
from pathlib import Path

class TerminalEvaluator:
    def __init__(self):
        self.evaluations_file = Path("story-world/evaluations/story_evaluations.json")
        
    def load_evaluations(self):
        """既存評価データ読み込み"""
        if self.evaluations_file.exists():
            with open(self.evaluations_file, 'r', encoding='utf-8') as f:
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
    
    def list_stories(self):
        """生成済み物語一覧表示"""
        stories_dir = Path("story-world/stories")
        if not stories_dir.exists():
            print("❌ storiesディレクトリが見つかりません")
            return []
        
        story_dirs = [d for d in stories_dir.iterdir() if d.is_dir()]
        story_dirs.sort()
        
        print("\n📚 生成済み物語一覧:")
        print("=" * 60)
        
        stories_info = []
        for i, story_dir in enumerate(story_dirs, 1):
            # メタデータ読み込み
            metadata_files = list(story_dir.glob("metadata_*.json"))
            if metadata_files:
                with open(metadata_files[0], 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                title = metadata.get('title', story_dir.name)
                ai_score = metadata.get('ai_evaluation', {}).get('total_score', 0)
                creation_date = metadata.get('creation_date', '')
                
                print(f"{i:2d}. {title}")
                print(f"    📅 作成: {creation_date[:19].replace('T', ' ')}")
                print(f"    📊 AI評価: {ai_score}/100")
                print(f"    📁 フォルダ: {story_dir.name}")
                print()
                
                stories_info.append({
                    'index': i,
                    'title': title,
                    'dir': story_dir,
                    'metadata': metadata
                })
        
        return stories_info
    
    def evaluate_story(self, story_info):
        """物語を評価"""
        print(f"\n📖 評価対象: {story_info['title']}")
        print("=" * 60)
        
        # AI評価表示
        ai_eval = story_info['metadata'].get('ai_evaluation', {})
        print("🤖 AI自動評価:")
        print(f"  🎪 面白さ: {ai_eval.get('entertainment_score', 0)}/100")
        print(f"  💬 会話品質: {ai_eval.get('dialogue_quality', 0)}/100")
        print(f"  🎭 キャラ一貫性: {ai_eval.get('character_consistency', 0)}/100")
        print(f"  📚 物語構成: {ai_eval.get('story_structure', 0)}/100")
        print(f"  🏆 総合: {ai_eval.get('total_score', 0)}/100")
        print()
        
        # ユーザー評価入力
        print("👤 あなたの評価をお聞かせください:")
        print()
        
        # 10段階評価
        while True:
            try:
                rating = int(input("⭐ 総合評価 (1-10): "))
                if 1 <= rating <= 10:
                    break
                print("❌ 1-10の数字で入力してください")
            except ValueError:
                print("❌ 数字で入力してください")
        
        # 良かった点
        print("\n👍 良かった点 (複数選択可、番号をカンマ区切りで入力):")
        good_options = [
            "チャッピーのキャラクターが良い",
            "ジェミーちゃんのキャラクターが良い", 
            "キャラクター同士の掛け合いが面白い",
            "会話のテンポが良い",
            "オチが面白い・意外",
            "物語の構成が良い",
            "設定・シチュエーションが良い",
            "読みやすい"
        ]
        
        for i, option in enumerate(good_options, 1):
            print(f"  {i}. {option}")
        
        good_points = []
        good_input = input("選択 (例: 1,3,5): ").strip()
        if good_input:
            try:
                indices = [int(x.strip()) for x in good_input.split(',')]
                good_points = [good_options[i-1] for i in indices if 1 <= i <= len(good_options)]
            except:
                pass
        
        # 改善点
        print("\n📝 改善点 (複数選択可、番号をカンマ区切りで入力):")
        improvement_options = [
            "チャッピーのキャラクターがブレている",
            "ジェミーちゃんのキャラクターがブレている",
            "会話が不自然",
            "話が長すぎる",
            "オチが弱い・つまらない", 
            "物語の構成が悪い",
            "設定が活かされていない",
            "読みにくい"
        ]
        
        for i, option in enumerate(improvement_options, 1):
            print(f"  {i}. {option}")
        
        improvement_points = []
        improvement_input = input("選択 (例: 2,4): ").strip()
        if improvement_input:
            try:
                indices = [int(x.strip()) for x in improvement_input.split(',')]
                improvement_points = [improvement_options[i-1] for i in indices if 1 <= i <= len(improvement_options)]
            except:
                pass
        
        # 詳細フィードバック
        print("\n💬 詳細フィードバック (自由記述、Enterで終了):")
        detailed_feedback = input().strip()
        
        # 昇格判定
        print("\n🚀 昇格判定:")
        print("1. 昇格させる（ネーム化して欲しい）")
        print("2. 昇格させない（このままで十分）") 
        print("3. 改善後に再検討")
        
        while True:
            try:
                promotion = int(input("選択 (1-3): "))
                if 1 <= promotion <= 3:
                    break
                print("❌ 1-3の数字で入力してください")
            except ValueError:
                print("❌ 数字で入力してください")
        
        promotion_map = {
            1: "promote",
            2: "complete", 
            3: "needs_improvement"
        }
        
        # 評価結果保存
        evaluation_result = {
            "story_id": story_info['dir'].name,
            "title": story_info['title'],
            "evaluation_date": datetime.now().isoformat(),
            "user_rating": rating,
            "good_points": good_points,
            "improvement_points": improvement_points,
            "detailed_feedback": detailed_feedback,
            "promotion_decision": promotion_map[promotion],
            "ai_evaluation": ai_eval
        }
        
        # データ保存
        self.save_evaluation(evaluation_result)
        
        # 結果表示
        print("\n✅ 評価完了!")
        print(f"📊 あなたの評価: {rating}/10")
        print(f"🚀 昇格判定: {promotion_map[promotion]}")
        
        return evaluation_result
    
    def save_evaluation(self, evaluation):
        """評価データ保存"""
        data = self.load_evaluations()
        data["stories"].append(evaluation)
        
        # 統計更新
        self.update_statistics(data)
        
        # ファイル保存
        self.evaluations_file.parent.mkdir(exist_ok=True)
        with open(self.evaluations_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def update_statistics(self, data):
        """統計情報更新"""
        stories = data["stories"]
        if not stories:
            return
        
        total = len(stories)
        user_ratings = [s["user_rating"] for s in stories]
        ai_scores = [s["ai_evaluation"].get("total_score", 0) for s in stories]
        promotions = len([s for s in stories if s["promotion_decision"] == "promote"])
        
        data["statistics"] = {
            "total_stories": total,
            "average_ai_score": round(sum(ai_scores) / len(ai_scores), 2),
            "average_user_rating": round(sum(user_ratings) / len(user_ratings), 2),
            "promotion_rate": round((promotions / total) * 100, 2),
            "user_satisfaction_trend": user_ratings[-10:]
        }
    
    def show_statistics(self):
        """統計情報表示"""
        data = self.load_evaluations()
        stats = data["statistics"]
        
        print("\n📊 評価統計:")
        print("=" * 40)
        print(f"📚 総物語数: {stats['total_stories']}")
        print(f"🤖 AI平均スコア: {stats['average_ai_score']}/100")
        print(f"👤 ユーザー平均評価: {stats['average_user_rating']}/10")
        print(f"🚀 昇格率: {stats['promotion_rate']}%")
        print()

def main():
    evaluator = TerminalEvaluator()
    
    while True:
        print("\n🎭 AIstory 評価システム")
        print("=" * 40)
        print("1. 物語一覧表示")
        print("2. 物語を評価する")
        print("3. 統計情報表示")
        print("4. 終了")
        
        choice = input("\n選択 (1-4): ").strip()
        
        if choice == "1":
            evaluator.list_stories()
        
        elif choice == "2":
            stories = evaluator.list_stories()
            if not stories:
                continue
            
            try:
                index = int(input(f"\n評価する物語の番号 (1-{len(stories)}): "))
                if 1 <= index <= len(stories):
                    evaluator.evaluate_story(stories[index-1])
                else:
                    print("❌ 無効な番号です")
            except ValueError:
                print("❌ 数字で入力してください")
        
        elif choice == "3":
            evaluator.show_statistics()
        
        elif choice == "4":
            print("👋 お疲れ様でした！")
            break
        
        else:
            print("❌ 1-4の数字で選択してください")

if __name__ == "__main__":
    main()