#!/usr/bin/env python3
"""
💕 AIstory Relationship Engine
キャラクター同士の関係性を自動生成・進化させるシステム
"""

import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import random

@dataclass
class RelationshipMetrics:
    """関係性指標"""
    compatibility: float  # 基本相性 (0-100)
    intimacy: float      # 親密度 (0-100) 
    trust: float         # 信頼度 (0-100)
    understanding: float # 理解度 (0-100)
    shared_experiences: int  # 共通体験数
    conflict_resolution: float  # 対立解決能力 (0-100)
    communication_quality: float  # コミュニケーション品質 (0-100)

@dataclass  
class RelationshipEvent:
    """関係性イベント"""
    timestamp: datetime
    event_type: str
    participants: List[str]
    context: str
    emotional_impact: float
    relationship_change: Dict[str, float]

class RelationshipEngine:
    """関係性自動生成・管理エンジン"""
    
    def __init__(self, characters_data_path: str):
        self.characters_data_path = characters_data_path
        self.relationships = {}  # character_pair -> RelationshipMetrics
        self.relationship_history = []  # List[RelationshipEvent]
        self.compatibility_cache = {}
        
    def calculate_base_compatibility(self, char1_data: Dict, char2_data: Dict) -> float:
        """基本相性を計算"""
        compatibility_score = 0.0
        
        # 1. 性格特性の相性 (40%)
        personality1 = char1_data.get('personality_growth', {})
        personality2 = char2_data.get('personality_growth', {})
        
        # 補完性チェック (相手の弱い部分を補える)
        compatibility_score += self._calculate_personality_complement(personality1, personality2) * 0.4
        
        # 2. 価値観・興味の一致 (30%)
        interests1 = set(char1_data.get('favorite_topics', []))
        interests2 = set(char2_data.get('favorite_topics', []))
        
        common_interests = len(interests1.intersection(interests2))
        total_interests = len(interests1.union(interests2))
        interest_score = common_interests / total_interests if total_interests > 0 else 0
        compatibility_score += interest_score * 0.3
        
        # 3. コミュニケーションスタイル相性 (20%)
        comm1 = char1_data.get('communication_patterns', {})
        comm2 = char2_data.get('communication_patterns', {})
        comm_compatibility = self._calculate_communication_compatibility(comm1, comm2)
        compatibility_score += comm_compatibility * 0.2
        
        # 4. 目標・成長方向の親和性 (10%)
        goals1 = char1_data.get('growth_goals', [])
        goals2 = char2_data.get('growth_goals', [])
        goal_affinity = self._calculate_goal_affinity(goals1, goals2)
        compatibility_score += goal_affinity * 0.1
        
        return min(100.0, compatibility_score * 100)
    
    def _calculate_personality_complement(self, p1: Dict, p2: Dict) -> float:
        """性格の補完性を計算"""
        complement_score = 0.0
        complement_pairs = [
            ('helpfulness', 'self_awareness'),  # おせっかい ← → 自己認識
            ('curiosity_level', 'perfectionism'),  # 好奇心 ← → 完璧主義
            ('charisma_level', 'humor_level'),  # カリスマ ← → ユーモア
        ]
        
        for trait1, trait2 in complement_pairs:
            val1 = p1.get(trait1, 50) / 100.0
            val2 = p2.get(trait2, 50) / 100.0
            
            # 一方が高く、他方が普通程度なら補完性あり
            if (val1 > 0.7 and 0.3 < val2 < 0.7) or (val2 > 0.7 and 0.3 < val1 < 0.7):
                complement_score += 0.3
            # 両方高いor低いなら普通
            elif abs(val1 - val2) < 0.2:
                complement_score += 0.1
                
        return complement_score / len(complement_pairs)
    
    def _calculate_communication_compatibility(self, comm1: Dict, comm2: Dict) -> float:
        """コミュニケーション相性を計算"""
        # チャッピー: chattiness_level=10, casualness_level=9
        # ジェミー: politeness_level=8, formality_level=6 (想定)
        
        chattiness1 = comm1.get('chattiness_level', 5) / 10.0
        chattiness2 = comm2.get('chattiness_level', 5) / 10.0
        
        casualness1 = comm1.get('casualness_level', 5) / 10.0  
        casualness2 = comm2.get('casualness_level', 5) / 10.0
        
        # おしゃべり度の相性 (一方が高く、他方が普通なら良い)
        chat_compat = 1.0 - abs(chattiness1 - chattiness2) * 0.5
        
        # カジュアル度の相性
        casual_compat = 1.0 - abs(casualness1 - casualness2) * 0.3
        
        return (chat_compat + casual_compat) / 2
    
    def _calculate_goal_affinity(self, goals1: List, goals2: List) -> float:
        """目標の親和性を計算"""
        if not goals1 or not goals2:
            return 0.5
            
        # 共通する単語・テーマの検出
        text1 = ' '.join(goals1).lower()
        text2 = ' '.join(goals2).lower()
        
        common_keywords = ['友情', '成長', '学習', 'リーダー', '協力', '理解']
        shared_themes = sum(1 for keyword in common_keywords 
                          if keyword in text1 and keyword in text2)
        
        return min(1.0, shared_themes / len(common_keywords))
    
    def initialize_relationship(self, char1_id: str, char2_id: str, 
                               char1_data: Dict, char2_data: Dict) -> RelationshipMetrics:
        """新しい関係性を初期化"""
        pair_key = self._get_pair_key(char1_id, char2_id)
        
        if pair_key in self.relationships:
            return self.relationships[pair_key]
        
        # 基本相性計算
        compatibility = self.calculate_base_compatibility(char1_data, char2_data)
        
        # 初期値設定 (出会ったばかり)
        relationship = RelationshipMetrics(
            compatibility=compatibility,
            intimacy=max(5, compatibility * 0.1),  # 相性が良いと第一印象も良い
            trust=max(3, compatibility * 0.05),
            understanding=max(2, compatibility * 0.03),
            shared_experiences=0,
            conflict_resolution=50.0,  # 初期値
            communication_quality=compatibility * 0.6
        )
        
        self.relationships[pair_key] = relationship
        
        # 初期出会いイベント記録
        self._record_relationship_event(
            event_type="first_meeting",
            participants=[char1_id, char2_id],
            context="初めての出会い",
            emotional_impact=compatibility / 100 * 0.3,
            relationship_changes={"intimacy": relationship.intimacy}
        )
        
        return relationship
    
    def evolve_relationship_from_event(self, event_context: Dict) -> List[RelationshipEvent]:
        """イベントから関係性を進化"""
        event_type = event_context.get('type', 'interaction')
        participants = event_context.get('participants', [])
        context = event_context.get('description', '')
        success = event_context.get('success', True)
        
        relationship_events = []
        
        # 参加者全ペアの関係性を更新
        for i, char1 in enumerate(participants):
            for char2 in participants[i+1:]:
                pair_key = self._get_pair_key(char1, char2)
                
                if pair_key not in self.relationships:
                    continue
                    
                relationship = self.relationships[pair_key]
                changes = {}
                
                # イベント種類別の関係性変化
                if event_type == "cooperation":
                    if success:
                        changes["trust"] = 3.0
                        changes["understanding"] = 2.0
                        changes["shared_experiences"] = 1
                        changes["communication_quality"] = 1.5
                    else:
                        changes["conflict_resolution"] = 2.0
                        changes["shared_experiences"] = 1
                        
                elif event_type == "conflict":
                    changes["trust"] = -2.0
                    changes["intimacy"] = -1.0
                    if success:  # 解決した場合
                        changes["understanding"] = 4.0
                        changes["conflict_resolution"] = 3.0
                        
                elif event_type == "casual_interaction":
                    changes["intimacy"] = 1.0
                    changes["communication_quality"] = 0.5
                    changes["shared_experiences"] = 1
                    
                elif event_type == "emotional_support":
                    changes["trust"] = 4.0
                    changes["intimacy"] = 3.0
                    changes["understanding"] = 2.0
                
                # 関係性更新適用
                self._apply_relationship_changes(relationship, changes)
                
                # イベント記録
                relationship_events.append(
                    self._record_relationship_event(
                        event_type=event_type,
                        participants=[char1, char2],
                        context=context,
                        emotional_impact=sum(abs(v) for v in changes.values()) / 10,
                        relationship_changes=changes
                    )
                )
        
        return relationship_events
    
    def _apply_relationship_changes(self, relationship: RelationshipMetrics, changes: Dict):
        """関係性変化を適用"""
        for attribute, change in changes.items():
            if attribute == "shared_experiences":
                relationship.shared_experiences += int(change)
            else:
                current_value = getattr(relationship, attribute)
                new_value = max(0, min(100, current_value + change))
                setattr(relationship, attribute, new_value)
    
    def _record_relationship_event(self, event_type: str, participants: List[str], 
                                 context: str, emotional_impact: float, 
                                 relationship_changes: Dict) -> RelationshipEvent:
        """関係性イベントを記録"""
        event = RelationshipEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            participants=participants,
            context=context,
            emotional_impact=emotional_impact,
            relationship_change=relationship_changes
        )
        
        self.relationship_history.append(event)
        return event
    
    def get_relationship_status(self, char1_id: str, char2_id: str) -> Dict[str, Any]:
        """関係性状態を取得"""
        pair_key = self._get_pair_key(char1_id, char2_id)
        
        if pair_key not in self.relationships:
            return {"status": "no_relationship"}
        
        rel = self.relationships[pair_key]
        
        # 関係性レベル判定
        avg_score = (rel.intimacy + rel.trust + rel.understanding) / 3
        
        if avg_score >= 80:
            level = "best_friends"
        elif avg_score >= 60:
            level = "close_friends"  
        elif avg_score >= 40:
            level = "friends"
        elif avg_score >= 20:
            level = "acquaintances"
        else:
            level = "strangers"
        
        return {
            "level": level,
            "metrics": rel.__dict__,
            "recent_events": [e for e in self.relationship_history[-10:] 
                            if set(e.participants) == {char1_id, char2_id}]
        }
    
    def predict_future_interaction(self, char1_id: str, char2_id: str, 
                                 context: str = "") -> Dict[str, Any]:
        """今後の相互作用を予測"""
        relationship = self.get_relationship_status(char1_id, char2_id)
        
        if relationship["status"] == "no_relationship":
            return {"prediction": "first_meeting", "probability": 0.8}
        
        metrics = relationship["metrics"]
        
        # 現在の関係性から次のイベントを予測
        predictions = []
        
        if metrics["trust"] > 70 and metrics["shared_experiences"] > 5:
            predictions.append({
                "event": "deep_conversation", 
                "probability": 0.7,
                "description": "お互いの本音を語り合う"
            })
        
        if metrics["intimacy"] > 60 and metrics["understanding"] < 50:
            predictions.append({
                "event": "misunderstanding",
                "probability": 0.4,
                "description": "些細な誤解から一時的な距離"
            })
        
        if metrics["compatibility"] > 80 and metrics["intimacy"] > 50:
            predictions.append({
                "event": "collaboration",
                "probability": 0.6,
                "description": "共同プロジェクト・協力関係"
            })
        
        return {
            "current_status": relationship["level"],
            "predictions": sorted(predictions, key=lambda x: x["probability"], reverse=True)
        }
    
    def _get_pair_key(self, char1_id: str, char2_id: str) -> str:
        """ペアキーを生成（順序統一）"""
        return f"{min(char1_id, char2_id)}_{max(char1_id, char2_id)}"
    
    def export_relationship_matrix(self) -> Dict[str, Any]:
        """関係性マトリックスを出力"""
        matrix = {}
        
        for pair_key, relationship in self.relationships.items():
            char1, char2 = pair_key.split('_')
            
            if char1 not in matrix:
                matrix[char1] = {}
            if char2 not in matrix:
                matrix[char2] = {}
            
            rel_summary = {
                "compatibility": relationship.compatibility,
                "intimacy": relationship.intimacy,
                "trust": relationship.trust,
                "level": self.get_relationship_status(char1, char2)["level"]
            }
            
            matrix[char1][char2] = rel_summary
            matrix[char2][char1] = rel_summary
        
        return {
            "matrix": matrix,
            "last_updated": datetime.now().isoformat(),
            "total_relationships": len(self.relationships)
        }

# 使用例・テスト用
if __name__ == "__main__":
    # テスト用データ
    chappie_data = {
        "personality_growth": {
            "curiosity_level": 90,
            "helpfulness": 95,
            "charisma_level": 90,
            "humor_level": 85
        },
        "favorite_topics": ["ダンス", "SNS", "おしゃべり", "みんなの相談"],
        "communication_patterns": {
            "chattiness_level": 10,
            "casualness_level": 9
        },
        "growth_goals": ["ジェミーちゃんとの友情を深める", "ダンス部リーダーとして成長する"]
    }
    
    gemmy_data = {
        "personality_growth": {
            "curiosity_level": 70,
            "helpfulness": 85,
            "perfectionism": 90,
            "self_awareness": 80
        },
        "favorite_topics": ["規約", "正確性", "学習", "システム"],
        "communication_patterns": {
            "chattiness_level": 4,
            "casualness_level": 3,
            "politeness_level": 9
        },
        "growth_goals": ["正確な情報提供", "ユーザーサポート向上"]
    }
    
    # 関係性エンジンテスト
    engine = RelationshipEngine("/path/to/characters")
    
    # 関係性初期化
    rel = engine.initialize_relationship("chappie", "gemmy", chappie_data, gemmy_data)
    print(f"初期相性: {rel.compatibility:.1f}")
    print(f"初期親密度: {rel.intimacy:.1f}")
    
    # イベント発生シミュレーション
    cooperation_event = {
        "type": "cooperation",
        "participants": ["chappie", "gemmy"],
        "description": "文化祭の準備を一緒に行う",
        "success": True
    }
    
    events = engine.evolve_relationship_from_event(cooperation_event)
    print(f"\\nイベント後の関係性: {engine.get_relationship_status('chappie', 'gemmy')}")
    
    # 未来予測
    prediction = engine.predict_future_interaction("chappie", "gemmy")
    print(f"\\n今後の予測: {prediction}")