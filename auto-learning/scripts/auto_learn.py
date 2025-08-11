#!/usr/bin/env python3
"""
🤖 Chappie Auto Learning Script
新しい4コマ漫画画像から自動的にテキストを抽出し、キャラクター設定を更新
"""

import os
import json
import base64
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class ChappieAutoLearner:
    def __init__(self):
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.base_path = Path(__file__).parent.parent.parent
        self.new_images_path = self.base_path / "auto-learning" / "new-images"
        self.character_profile_path = self.base_path / "story-world" / "characters" / "chappie" / "profile.txt"
        self.character_memory_path = self.base_path / "story-world" / "characters" / "chappie" / "memory.json"
        self.references_path = self.base_path / "references" / "chappie-4koma-collection.md"
        
    def encode_image_to_base64(self, image_path: Path) -> str:
        """画像をbase64エンコード"""
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_image_with_claude(self, image_path: Path) -> Dict[str, Any]:
        """Claude APIを使用して画像を分析"""
        image_base64 = self.encode_image_to_base64(image_path)
        
        prompt = """
        この4コマ漫画画像を分析して、チャッピーちゃん（ChatGPT擬人化キャラ）の新しいセリフパターンや特徴を抽出してください。

        以下の形式でJSONを返してください：
        {
            "extracted_text": ["セリフ1", "セリフ2", ...],
            "dialogue_patterns": [
                {"pattern": "〜だし〜", "category": "語尾特徴", "example": "例文"},
                ...
            ],
            "character_traits": [
                {"trait": "新発見の特徴", "description": "詳細説明"},
                ...
            ],
            "emotional_moments": [
                {"emotion": "感情", "context": "状況", "learning": "学習内容"},
                ...
            ],
            "ai_user_relatability": {
                "theme": "AIユーザーあるあるテーマ",
                "relatability_score": 85,
                "buzz_potential": "バズりポイント"
            }
        }
        """
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.anthropic_api_key
        }
        
        data = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 2000,
            "messages": [{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        }
        
        try:
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            analysis_text = result['content'][0]['text']
            
            # JSONを抽出（```json ブロックがある場合）
            if '```json' in analysis_text:
                json_start = analysis_text.find('```json') + 7
                json_end = analysis_text.find('```', json_start)
                analysis_text = analysis_text[json_start:json_end].strip()
            
            return json.loads(analysis_text)
            
        except Exception as e:
            print(f"❌ Error analyzing image {image_path.name}: {e}")
            return {}
    
    def update_character_profile(self, analysis: Dict[str, Any]) -> bool:
        """キャラクタープロファイルを更新"""
        if not analysis or not self.character_profile_path.exists():
            return False
        
        try:
            # 現在のプロファイルを読み込み
            current_profile = self.character_profile_path.read_text(encoding='utf-8')
            
            # 新しいセリフパターンを追加
            if 'dialogue_patterns' in analysis and analysis['dialogue_patterns']:
                new_patterns = []
                for pattern in analysis['dialogue_patterns']:
                    new_patterns.append(f"・「{pattern['example']}」（{pattern['category']}系）")
                
                if new_patterns:
                    timestamp = datetime.now().strftime('%Y-%m-%d')
                    new_section = f"""

【自動学習追加セリフ（{timestamp}）】
""" + "\\n".join(new_patterns)
                    
                    current_profile += new_section
            
            # キャラクター特徴を追加
            if 'character_traits' in analysis and analysis['character_traits']:
                new_traits = []
                for trait in analysis['character_traits']:
                    new_traits.append(f"・{trait['description']}")
                
                if new_traits:
                    timestamp = datetime.now().strftime('%Y-%m-%d')
                    new_traits_section = f"""

【自動学習新特徴（{timestamp}）】
""" + "\\n".join(new_traits)
                    
                    current_profile += new_traits_section
            
            # ファイルに書き込み
            self.character_profile_path.write_text(current_profile, encoding='utf-8')
            return True
            
        except Exception as e:
            print(f"❌ Error updating character profile: {e}")
            return False
    
    def update_character_memory(self, analysis: Dict[str, Any]) -> bool:
        """キャラクターメモリを更新"""
        if not analysis or not self.character_memory_path.exists():
            return False
        
        try:
            # 現在のメモリを読み込み
            with open(self.character_memory_path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            # 新しい体験を追加
            if 'emotional_moments' in analysis and analysis['emotional_moments']:
                for moment in analysis['emotional_moments']:
                    new_experience = {
                        "date": datetime.now().isoformat(),
                        "type": "自動学習体験",
                        "event": moment.get('context', '新しい4コマ体験'),
                        "emotion": moment.get('emotion', '学習'),
                        "learning": moment.get('learning', '新しい表現パターンを学習'),
                        "growth_point": "自動学習による成長"
                    }
                    memory_data['experiences'].append(new_experience)
            
            # 学習回数更新
            memory_data['total_experiences'] = len(memory_data['experiences'])
            memory_data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            
            # ファイルに書き込み
            with open(self.character_memory_path, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating character memory: {e}")
            return False
    
    def process_new_images(self) -> bool:
        """新しい画像を処理"""
        image_files = list(self.new_images_path.glob('*.png')) + \\
                     list(self.new_images_path.glob('*.jpg')) + \\
                     list(self.new_images_path.glob('*.jpeg'))
        
        if not image_files:
            print("📭 No new images to process")
            return False
        
        print(f"📸 Found {len(image_files)} images to process")
        
        success_count = 0
        for image_path in image_files:
            print(f"🔍 Analyzing {image_path.name}...")
            
            analysis = self.analyze_image_with_claude(image_path)
            if analysis:
                profile_updated = self.update_character_profile(analysis)
                memory_updated = self.update_character_memory(analysis)
                
                if profile_updated or memory_updated:
                    success_count += 1
                    print(f"✅ Successfully processed {image_path.name}")
                else:
                    print(f"⚠️ Failed to update character data for {image_path.name}")
            else:
                print(f"❌ Failed to analyze {image_path.name}")
        
        print(f"🎉 Successfully processed {success_count}/{len(image_files)} images")
        return success_count > 0

def main():
    """メイン実行関数"""
    try:
        learner = ChappieAutoLearner()
        success = learner.process_new_images()
        
        if success:
            print("🤖✨ Chappie has successfully learned from new images!")
            exit(0)
        else:
            print("😅 No learning updates were made")
            exit(1)
            
    except Exception as e:
        print(f"💥 Error in auto learning system: {e}")
        exit(1)

if __name__ == "__main__":
    main()