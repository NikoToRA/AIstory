#!/usr/bin/env python3
"""
🎬 AIstory World Content Extraction Engine
運営会社視点からの世界観切り出しシステム
"""

import json
import datetime
from pathlib import Path
from typing import Dict, List, Any

class WorldExtractor:
    """世界観切り出しエンジン"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.meta_world_path = self.base_path / "meta-world"
        self.story_world_path = self.base_path / "story-world"
        
    def load_company_data(self) -> Dict[str, Any]:
        """運営会社データを読み込み"""
        company_file = self.meta_world_path / "company" / "aistory-entertainment.json"
        with open(company_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_department_data(self, department: str) -> Dict[str, Any]:
        """部署データを読み込み"""
        dept_file = self.meta_world_path / "departments" / f"{department}.json"
        with open(dept_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_character_summary(self) -> Dict[str, Any]:
        """全キャラクターの成長データを要約"""
        characters = {}
        
        # チャッピーちゃんデータ読み込み
        chappie_memory = self.story_world_path / "characters" / "chappie" / "memory.json"
        if chappie_memory.exists():
            with open(chappie_memory, 'r', encoding='utf-8') as f:
                chappie_data = json.load(f)
                
                characters["チャッピー"] = {
                    "total_experiences": chappie_data.get("total_experiences", 0),
                    "personality_growth": chappie_data.get("personality_growth", {}),
                    "latest_learning": chappie_data.get("experiences", [])[-1] if chappie_data.get("experiences") else None,
                    "popularity_metrics": {
                        "charisma_level": chappie_data.get("personality_growth", {}).get("charisma_level", 0),
                        "community_building": chappie_data.get("personality_growth", {}).get("community_building", 0),
                        "fan_engagement": "高"
                    }
                }
        
        return characters
    
    def generate_content_brief(self, content_type: str, target_audience: str) -> Dict[str, Any]:
        """コンテンツ企画書を自動生成"""
        company_data = self.load_company_data()
        content_strategy = self.load_department_data("content-strategy")
        character_data = self.extract_character_summary()
        
        brief = {
            "project_title": f"AIstory {content_type} プロジェクト",
            "generated_date": datetime.datetime.now().isoformat(),
            "company_context": {
                "mission": company_data["company_philosophy"]["mission"],
                "target_audience": target_audience,
                "brand_guidelines": company_data["content_guidelines"]
            },
            "character_status": character_data,
            "content_recommendations": self._generate_recommendations(content_type, character_data),
            "success_metrics": self._define_success_metrics(content_type, target_audience),
            "production_timeline": self._create_timeline(content_type)
        }
        
        return brief
    
    def _generate_recommendations(self, content_type: str, character_data: Dict) -> List[str]:
        """コンテンツ推奨事項を生成"""
        recommendations = []
        
        if content_type == "4koma":
            # チャッピーの成長度に基づく推奨
            chappie = character_data.get("チャッピー", {})
            charisma = chappie.get("personality_growth", {}).get("charisma_level", 0)
            
            if charisma >= 85:
                recommendations.append("チャッピーのカリスマ性を活かした新規ファン獲得向けコンテンツ")
                recommendations.append("親近感アピール要素を強化したコミュニティ向けエピソード")
            
            recommendations.extend([
                "AIあるあるネタでの共感性重視",
                "教育価値とエンターテイメントのバランス",
                "キャラクター成長を感じられる展開"
            ])
            
        elif content_type == "educational":
            recommendations.extend([
                "チャッピーの失敗談を活用した「AI学習の落とし穴」解説",
                "実用的なAI活用tips中心の構成",
                "初心者にも分かりやすい専門用語解説"
            ])
            
        return recommendations
    
    def _define_success_metrics(self, content_type: str, audience: str) -> Dict[str, Any]:
        """成功指標を定義"""
        base_metrics = {
            "engagement_rate": "5%以上",
            "educational_impact": "理解度向上20%",
            "brand_recognition": "AIstory認知度向上"
        }
        
        if content_type == "4koma":
            base_metrics.update({
                "viral_potential": "10,000シェア以上",
                "character_popularity": "好感度維持95%以上"
            })
        elif content_type == "educational":
            base_metrics.update({
                "learning_completion": "完走率80%以上",
                "practical_application": "実践率30%以上"
            })
            
        return base_metrics
    
    def _create_timeline(self, content_type: str) -> Dict[str, str]:
        """制作スケジュールを作成"""
        base_timeline = {
            "企画": "1週間",
            "制作": "2週間", 
            "レビュー": "3日",
            "公開": "即日"
        }
        
        if content_type == "educational":
            base_timeline["制作"] = "3週間"
            base_timeline["教育価値検証"] = "1週間"
            
        return base_timeline
    
    def export_content_package(self, content_type: str, target_audience: str) -> str:
        """コンテンツパッケージを出力"""
        brief = self.generate_content_brief(content_type, target_audience)
        
        # 出力ファイル名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.base_path / f"content-packages/{content_type}_{target_audience}_{timestamp}.json"
        
        # ディレクトリ作成
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # ファイル出力
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(brief, f, ensure_ascii=False, indent=2)
        
        return str(output_file)

def main():
    """メイン実行関数"""
    extractor = WorldExtractor()
    
    # 4コマ漫画向けコンテンツパッケージ生成
    package_path = extractor.export_content_package("4koma", "AI学習者")
    print(f"📦 Content package generated: {package_path}")
    
    # 教育コンテンツパッケージ生成  
    edu_package = extractor.export_content_package("educational", "初心者")
    print(f"📚 Educational package generated: {edu_package}")

if __name__ == "__main__":
    main()