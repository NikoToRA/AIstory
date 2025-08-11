#!/usr/bin/env python3
"""
リリカ先生 漫画編集システム
画像解析からセリフ生成まで統合管理
"""

import json
from datetime import datetime
from pathlib import Path
from image_manager import ImageManager

class MangaEditor:
    """リリカ先生の漫画編集機能"""
    
    def __init__(self):
        self.image_manager = ImageManager()
        self.characters = self._load_characters()
    
    def _load_characters(self) -> dict:
        """既存キャラクター情報を読み込み"""
        characters = {}
        char_path = Path("story-world/characters")
        
        for char_dir in char_path.iterdir():
            if char_dir.is_dir():
                profile_path = char_dir / "profile.txt"
                if profile_path.exists():
                    with open(profile_path, 'r', encoding='utf-8') as f:
                        characters[char_dir.name] = f.read()
        
        return characters
    
    def analyze_and_create_manga(self, image_path: str, title: str, scenario_hint: str = "") -> dict:
        """
        画像を解析して漫画形式のセリフを生成
        
        Args:
            image_path: 解析する画像のパス
            title: 作品タイトル
            scenario_hint: シナリオヒント（オプション）
            
        Returns:
            漫画形式の作品データ
        """
        
        # 1. 画像をストーリー保存庫に保存
        image_data = self.image_manager.save_image(
            image_path, 
            title, 
            f"リリカ先生による漫画編集素材: {scenario_hint}",
            ["リリカ先生", "漫画編集", "画像解析"]
        )
        
        # 2. 漫画作品データ構造作成
        manga_work = {
            "title": title,
            "created_by": "リリカ先生",
            "created_at": datetime.now().isoformat(),
            "source_image": image_data["folder_path"],
            "scenario_hint": scenario_hint,
            "format": "manga_style",
            "panels": [],  # ここに4コマ等のパネルデータが入る
            "characters_involved": [],  # 参加キャラクター
            "editor_notes": "リリカ先生による画像解析・編集待ち"
        }
        
        # 3. 作品保存
        work_dir = Path("story-world/manga-works") / f"{datetime.now().strftime('%Y-%m-%d')}_{title}"
        work_dir.mkdir(parents=True, exist_ok=True)
        
        with open(work_dir / "manga_work.json", 'w', encoding='utf-8') as f:
            json.dump(manga_work, f, ensure_ascii=False, indent=2)
            
        print(f"🎬 リリカ先生: 画像を受け取りました")
        print(f"📁 保存場所: {work_dir}")
        print(f"🖼️  画像アーカイブ: {image_data['folder_path']}")
        
        return manga_work
    
    def generate_dialogue_template(self, character_names: list) -> str:
        """指定キャラクターの会話テンプレート生成"""
        template = "## 🎭 漫画セリフ案\n\n"
        
        for i, char_name in enumerate(character_names, 1):
            template += f"### パネル{i} - {char_name}\n"
            template += f"**{char_name}**: 「（セリフをここに入力）」\n"
            template += f"**表情**: （表情指定）\n"
            template += f"**演出**: （効果音・背景等）\n\n"
            
        return template
    
    def list_manga_works(self) -> list:
        """作成済み漫画作品一覧"""
        works = []
        works_path = Path("story-world/manga-works")
        
        if works_path.exists():
            for work_dir in works_path.iterdir():
                if work_dir.is_dir():
                    work_file = work_dir / "manga_work.json"
                    if work_file.exists():
                        with open(work_file, 'r', encoding='utf-8') as f:
                            works.append(json.load(f))
                            
        return sorted(works, key=lambda x: x['created_at'], reverse=True)

# リリカ先生のセリフ生成ガイド
RIRIKA_DIALOGUE_SYSTEM = """
🎬 リリカ先生セリフ生成ガイド

## 基本スタンス
- プロ編集者として的確なアドバイス
- 漫画制作の専門知識を活用
- キャラクターの魅力を引き出す演出提案
- 読者目線での品質管理

## セリフパターン例

### 画像受取時
「画像を確認しました。この状況なら{キャラクター名}の反応が面白そうですね」
「構図的に4コマ漫画に最適です。{演出提案}はいかがでしょう？」

### 編集提案時  
「ここは{キャラクター名}らしい{特徴}を活かしましょう」
「コマ割りを{提案}にすると、より読みやすくなります」

### 品質チェック時
「もう少し{キャラクター名}の個性を出せそうですね」
「セリフのテンポが良いですが、表情でより強調できます」

## 出力フォーマット
常に漫画制作の観点から具体的で建設的な提案を行う
"""

if __name__ == "__main__":
    editor = MangaEditor()
    print("🎬 リリカ先生 漫画編集システム起動")
    print("使用方法:")
    print("editor.analyze_and_create_manga('path/to/image.png', 'タイトル', 'シナリオヒント')")