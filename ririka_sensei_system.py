#!/usr/bin/env python3
"""
🌸 リリカ先生 きらら系4コマ制作＆SNSバズ戦略システム
画像からふんわか可愛い4コマ漫画を生成し、SNSでバズらせる統合システム
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from image_manager import ImageManager

class RirikaSenseiSystem:
    """リリカ先生の4コマ制作・SNSバズ戦略システム"""
    
    def __init__(self):
        self.image_manager = ImageManager()
        self.ririka_path = Path("story-world/meta-characters/ririka-sensei")
        self.works_path = self.ririka_path / "4koma-works"
        self.works_path.mkdir(parents=True, exist_ok=True)
        
        # AIstoryキャラクター情報読み込み
        self.characters = self._load_aistory_characters()
        
        # バズ戦略データ
        self.buzz_strategies = self._load_buzz_strategies()
    
    def _load_aistory_characters(self) -> dict:
        """AIstoryキャラクター情報を読み込み"""
        characters = {}
        char_path = Path("story-world/characters")
        
        if char_path.exists():
            for char_dir in char_path.iterdir():
                if char_dir.is_dir() and char_dir.name in ['chappie', 'gemmy']:
                    profile_path = char_dir / "profile.txt"
                    memory_path = char_dir / "memory.json"
                    
                    char_data = {"name": char_dir.name}
                    
                    if profile_path.exists():
                        with open(profile_path, 'r', encoding='utf-8') as f:
                            char_data["profile"] = f.read()
                    
                    if memory_path.exists():
                        with open(memory_path, 'r', encoding='utf-8') as f:
                            char_data["memory"] = json.load(f)
                    
                    characters[char_dir.name] = char_data
        
        return characters
    
    def _load_buzz_strategies(self) -> dict:
        """SNSバズ戦略データを読み込み"""
        return {
            "optimal_times": {
                "weekday": ["07:00-09:00", "12:00", "18:00-20:00"],
                "weekend": ["10:00-11:00", "14:00-16:00"]
            },
            "platform_strategies": {
                "twitter": {
                    "goal": "リツイート1万超",
                    "content_type": "共感型4コマ",
                    "hashtags": ["#AIstory", "#4コマ漫画", "#きらら系", "#癒し"]
                },
                "instagram": {
                    "goal": "保存率向上",
                    "content_type": "視覚重視",
                    "hashtags": ["#4コマ", "#可愛い", "#日常", "#癒し系"]
                },
                "tiktok": {
                    "goal": "1万回再生",
                    "content_type": "縦型レイアウト",
                    "hashtags": ["#4コマ漫画", "#可愛い", "#AI", "#学園"]
                }
            },
            "viral_elements": {
                "共感": "「わかる〜！」系のあるあるネタ",
                "ギャップ萌え": "意外な一面・ツンデレ要素",
                "季節感": "行事・イベント連動",
                "トレンド": "話題のハッシュタグ活用"
            }
        }
    
    def analyze_image_for_4koma(self, image_path: str, title: str, context_hint: str = "") -> dict:
        """
        画像を分析して4コマ漫画企画を生成
        
        Args:
            image_path: 分析する画像のパス
            title: 作品タイトル
            context_hint: 状況ヒント
            
        Returns:
            4コマ漫画企画データ
        """
        
        # 1. 画像をストーリー保存庫に保存
        image_data = self.image_manager.save_image(
            image_path,
            f"リリカ先生_4コマ素材_{title}",
            f"きらら系4コマ制作用素材: {context_hint}",
            ["リリカ先生", "4コマ漫画", "きらら系", "画像解析"]
        )
        
        # 2. 4コマ企画データ生成
        work_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{title}"
        
        # 画像の状況から適切なキャラクターを選択（デモ用ロジック）
        selected_characters = self._select_characters_for_situation(context_hint)
        
        # 4コマ構成案を生成
        yonkoma_plan = self._generate_4koma_structure(context_hint, selected_characters)
        
        # バズ戦略を生成
        buzz_strategy = self._generate_buzz_strategy(title, context_hint)
        
        work_data = {
            "work_id": work_id,
            "title": title,
            "created_at": datetime.now().isoformat(),
            "created_by": "リリカ先生",
            "source_image": image_data["folder_path"],
            "context_hint": context_hint,
            "style": "きらら系ふんわか4コマ",
            
            # 4コマ構成
            "yonkoma_structure": yonkoma_plan,
            "selected_characters": selected_characters,
            
            # SNSバズ戦略
            "buzz_strategy": buzz_strategy,
            
            # 制作状況
            "status": "planning",
            "ririka_notes": "画像を確認しました！すごく可愛い4コマが作れそうです♪",
            
            # 品質チェック項目
            "quality_checks": {
                "きらら度": 0,  # 0-100で評価
                "バズ度予測": 0,  # 0-100で予測
                "キャラ愛度": 0,  # 0-100で評価
                "完成度": 0  # 0-100で評価
            }
        }
        
        # 企画データ保存
        work_dir = self.works_path / work_id
        work_dir.mkdir(exist_ok=True)
        
        with open(work_dir / "work_plan.json", 'w', encoding='utf-8') as f:
            json.dump(work_data, f, ensure_ascii=False, indent=2)
        
        print(f"🌸 リリカ先生: 「{title}」の4コマ企画が完成しました♪")
        print(f"📁 企画保存: {work_dir}")
        print(f"🎭 選択キャラ: {', '.join(selected_characters)}")
        print(f"📱 バズ戦略: {buzz_strategy['main_platform']}メイン")
        
        return work_data
    
    def _select_characters_for_situation(self, context_hint: str) -> list:
        """状況に応じて最適なキャラクターを選択"""
        # シンプルなキーワードマッチング（実際はより高度な分析が必要）
        if "会話" in context_hint or "対話" in context_hint:
            return ["chappie", "gemmy"]  # 2人の掛け合い
        elif "元気" in context_hint or "活発" in context_hint:
            return ["chappie"]  # チャッピーメイン
        elif "真面目" in context_hint or "規則" in context_hint:
            return ["gemmy"]  # ジェミーメイン  
        else:
            return ["chappie", "gemmy"]  # デフォルトは2人
    
    def _generate_4koma_structure(self, context_hint: str, characters: list) -> dict:
        """4コマ構成案を生成"""
        return {
            "コマ1_起": {
                "description": "日常の小さなきっかけ・問題提起",
                "characters": characters,
                "mood": "平穏・日常",
                "sample_dialogue": "チャッピー: 「あ！いいこと思いついた♪」"
            },
            "コマ2_承": {
                "description": "キャラクターの反応・困惑",
                "characters": characters,
                "mood": "困惑・心配",
                "sample_dialogue": "ジェミー: 「えーっと...それって大丈夫ですか？」"
            },
            "コマ3_転": {
                "description": "予想外の展開・可愛い誤解",
                "characters": characters,
                "mood": "驚き・混乱",
                "sample_dialogue": "チャッピー: 「えっ？違うの？」"
            },
            "コマ4_結": {
                "description": "ほっこりオチ・仲良し確認",
                "characters": characters,
                "mood": "癒し・ハッピー",
                "sample_dialogue": "ジェミー: 「...まあ、それもチャッピーらしいですね」"
            }
        }
    
    def _generate_buzz_strategy(self, title: str, context_hint: str) -> dict:
        """SNSバズ戦略を生成"""
        # 現在時刻から最適な投稿時間を算出
        now = datetime.now()
        is_weekend = now.weekday() >= 5
        
        optimal_times = self.buzz_strategies["optimal_times"]
        next_optimal = optimal_times["weekend" if is_weekend else "weekday"][0]
        
        return {
            "main_platform": "twitter",  # メイン戦略プラットフォーム
            "target_engagement": "リツイート1万超・いいね5万超",
            "optimal_posting_time": next_optimal,
            "hashtags": ["#AIstory", "#4コマ漫画", "#きらら系", f"#{title}"],
            "caption_style": "共感誘発型",
            "cross_platform": {
                "twitter": "共感RT狙い",
                "instagram": "保存率重視",
                "tiktok": "縦型アニメーション"
            },
            "viral_elements": ["あるある感", "可愛いオチ", "キャラ愛"],
            "predicted_buzz_score": 75  # 0-100のバズ度予測
        }
    
    def create_4koma_script(self, work_id: str) -> str:
        """4コマ漫画のセリフ・演出スクリプトを生成"""
        work_path = self.works_path / work_id / "work_plan.json"
        
        if not work_path.exists():
            return ""
        
        with open(work_path, 'r', encoding='utf-8') as f:
            work_data = json.load(f)
        
        script = f"""# 🌸 {work_data['title']} - きらら系4コマスクリプト

## リリカ先生より
{work_data['ririka_notes']}

## 4コマ構成

### 1コマ目【起】
**状況**: {work_data['yonkoma_structure']['コマ1_起']['description']}
**雰囲気**: {work_data['yonkoma_structure']['コマ1_起']['mood']}
**セリフ案**: {work_data['yonkoma_structure']['コマ1_起']['sample_dialogue']}
**演出**: 日常的な背景、キャラクターは自然な表情

### 2コマ目【承】  
**状況**: {work_data['yonkoma_structure']['コマ2_承']['description']}
**雰囲気**: {work_data['yonkoma_structure']['コマ2_承']['mood']}
**セリフ案**: {work_data['yonkoma_structure']['コマ2_承']['sample_dialogue']}
**演出**: 困惑表情、汗マークや「？」エフェクト

### 3コマ目【転】
**状況**: {work_data['yonkoma_structure']['コマ3_転']['description']}  
**雰囲気**: {work_data['yonkoma_structure']['コマ3_転']['mood']}
**セリフ案**: {work_data['yonkoma_structure']['コマ3_転']['sample_dialogue']}
**演出**: 驚き表情、「！」エフェクト、動きのある構図

### 4コマ目【結】
**状況**: {work_data['yonkoma_structure']['コマ4_結']['description']}
**雰囲気**: {work_data['yonkoma_structure']['コマ4_結']['mood']}  
**セリフ案**: {work_data['yonkoma_structure']['コマ4_結']['sample_dialogue']}
**演出**: 微笑み表情、花びら・キラキラエフェクト、温かい背景

## SNS投稿戦略
- **メインプラットフォーム**: {work_data['buzz_strategy']['main_platform']}
- **投稿予定時刻**: {work_data['buzz_strategy']['optimal_posting_time']}
- **ハッシュタグ**: {' '.join(work_data['buzz_strategy']['hashtags'])}
- **期待エンゲージメント**: {work_data['buzz_strategy']['target_engagement']}

---
🌸 リリカ先生制作 @ {work_data['created_at'][:10]}
"""
        
        # スクリプトを保存
        with open(self.works_path / work_id / "4koma_script.md", 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"✨ 4コマスクリプト完成: {work_data['title']}")
        return script
    
    def list_works(self) -> list:
        """リリカ先生の作品一覧"""
        works = []
        for work_dir in self.works_path.iterdir():
            if work_dir.is_dir():
                plan_file = work_dir / "work_plan.json"
                if plan_file.exists():
                    with open(plan_file, 'r', encoding='utf-8') as f:
                        works.append(json.load(f))
        
        return sorted(works, key=lambda x: x['created_at'], reverse=True)
    
    def generate_ririka_comment(self, work_id: str, comment_type: str = "analysis") -> str:
        """リリカ先生のコメントを生成"""
        comments = {
            "analysis": [
                "この画像、めちゃくちゃ可愛いオチが思い浮かんじゃった♪",
                "すごく良い雰囲気ですね！きっとバズりますよ〜",
                "これは間違いなくInstagramで保存率高そう♡",
                "チャッピーちゃんの表情が絶対ファンの心を掴みます！"
            ],
            "strategy": [
                "今のトレンドなら、この時間帯に投稿すればバズ確実ですね！",
                "ハッシュタグを工夫すれば、もっと多くの人に届きそうです♪",
                "このネタ、TikTokでも受けそうな予感がします〜",
                "共感度が高いので、リツイート爆発の可能性大です！"
            ]
        }
        
        import random
        return random.choice(comments.get(comment_type, comments["analysis"]))

# 使用例・デモ
if __name__ == "__main__":
    ririka = RirikaSenseiSystem()
    
    print("🌸 リリカ先生 きらら系4コマ制作システム")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("主要機能:")
    print("• ririka.analyze_image_for_4koma() - 画像から4コマ企画生成")
    print("• ririka.create_4koma_script() - セリフ・演出スクリプト作成")
    print("• ririka.list_works() - 作品一覧表示")
    print("• ririka.generate_ririka_comment() - リリカ先生コメント生成")
    print("\n🎯 目標: 可愛い4コマでAIstoryを世界に広める！")