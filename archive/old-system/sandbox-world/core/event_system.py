#!/usr/bin/env python3
"""
🎪 AIstory Event System
学校生活イベントを自動生成・管理するシステム
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    DAILY_ROUTINE = "daily_routine"
    RANDOM_ENCOUNTER = "random_encounter"
    SCHEDULED_EVENT = "scheduled_event"
    CHARACTER_INITIATED = "character_initiated"
    SEASONAL_EVENT = "seasonal_event"
    EMERGENCY_EVENT = "emergency_event"

@dataclass
class EventTemplate:
    """イベントテンプレート"""
    id: str
    name: str
    description: str
    event_type: EventType
    min_participants: int
    max_participants: int
    duration_minutes: int
    location: str
    prerequisites: List[str]
    emotional_impact: float  # -1.0 to 1.0
    relationship_effects: Dict[str, float]
    probability_weights: Dict[str, float]  # 条件別発生確率

class EventSystem:
    """イベント自動生成・管理システム"""
    
    def __init__(self):
        self.current_events = []  # 進行中のイベント
        self.event_history = []   # 過去のイベント
        self.event_templates = self._load_event_templates()
        self.school_schedule = self._initialize_school_schedule()
        self.seasonal_events = self._initialize_seasonal_events()
        
    def _load_event_templates(self) -> Dict[str, EventTemplate]:
        """イベントテンプレートを読み込み"""
        templates = {}
        
        # 日常ルーティンイベント
        templates["morning_greeting"] = EventTemplate(
            id="morning_greeting",
            name="朝の挨拶",
            description="登校時の自然な出会いと挨拶",
            event_type=EventType.DAILY_ROUTINE,
            min_participants=2,
            max_participants=4,
            duration_minutes=5,
            location="校門・昇降口",
            prerequisites=[],
            emotional_impact=0.2,
            relationship_effects={"intimacy": 0.5, "communication_quality": 1.0},
            probability_weights={"morning": 0.8, "friendship_level": 0.3}
        )
        
        templates["lunch_together"] = EventTemplate(
            id="lunch_together",
            name="一緒に昼食",
            description="昼休みに一緒にお弁当を食べる",
            event_type=EventType.RANDOM_ENCOUNTER,
            min_participants=2,
            max_participants=6,
            duration_minutes=25,
            location="教室・屋上・食堂",
            prerequisites=["friendship_level >= 20"],
            emotional_impact=0.4,
            relationship_effects={"intimacy": 2.0, "shared_experiences": 1},
            probability_weights={"lunch_time": 0.6, "friendship_level": 0.4}
        )
        
        templates["study_session"] = EventTemplate(
            id="study_session",
            name="勉強会",
            description="テスト前の勉強を一緒に行う",
            event_type=EventType.CHARACTER_INITIATED,
            min_participants=2,
            max_participants=5,
            duration_minutes=90,
            location="図書館・教室",
            prerequisites=["test_approaching"],
            emotional_impact=0.3,
            relationship_effects={"trust": 2.5, "understanding": 2.0, "cooperation": 3.0},
            probability_weights={"academic_need": 0.7, "helpfulness": 0.5}
        )
        
        templates["conflict_resolution"] = EventTemplate(
            id="conflict_resolution",
            name="誤解の解決",
            description="些細な誤解やすれ違いを解決する機会",
            event_type=EventType.EMERGENCY_EVENT,
            min_participants=2,
            max_participants=2,
            duration_minutes=20,
            location="放課後の教室・屋上",
            prerequisites=["relationship_tension > 30"],
            emotional_impact=0.8,
            relationship_effects={"understanding": 5.0, "trust": 3.0, "conflict_resolution": 4.0},
            probability_weights={"relationship_stress": 0.9}
        )
        
        templates["cultural_festival_prep"] = EventTemplate(
            id="cultural_festival_prep",
            name="文化祭準備",
            description="クラス出し物の準備作業",
            event_type=EventType.SEASONAL_EVENT,
            min_participants=3,
            max_participants=10,
            duration_minutes=120,
            location="教室・体育館",
            prerequisites=["season == autumn", "cultural_festival_approaching"],
            emotional_impact=0.6,
            relationship_effects={"cooperation": 4.0, "shared_experiences": 2, "trust": 2.0},
            probability_weights={"season_autumn": 1.0, "class_participation": 0.8}
        )
        
        templates["heart_to_heart"] = EventTemplate(
            id="heart_to_heart",
            name="本音の語り合い",
            description="お互いの本当の気持ちを話し合う特別な時間",
            event_type=EventType.CHARACTER_INITIATED,
            min_participants=2,
            max_participants=2,
            duration_minutes=30,
            location="屋上・放課後の教室",
            prerequisites=["trust >= 60", "intimacy >= 50"],
            emotional_impact=0.9,
            relationship_effects={"understanding": 6.0, "intimacy": 4.0, "trust": 3.0},
            probability_weights={"deep_friendship": 0.8, "emotional_readiness": 0.7}
        )
        
        return templates
    
    def _initialize_school_schedule(self) -> Dict[str, Any]:
        """学校スケジュールを初期化"""
        return {
            "weekday_schedule": {
                "08:00-08:30": "登校時間",
                "08:30-08:45": "朝のSHR", 
                "08:50-09:40": "1時間目",
                "09:50-10:40": "2時間目",
                "10:50-11:40": "3時間目", 
                "11:50-12:40": "4時間目",
                "12:40-13:25": "昼休み",
                "13:30-14:20": "5時間目",
                "14:30-15:20": "6時間目",
                "15:20-15:30": "帰りのSHR",
                "15:30-17:00": "部活動・自由時間",
                "17:00-": "下校時間"
            },
            "special_days": {
                "monday": ["全校朝礼"],
                "friday": ["清掃活動"],
                "test_week": ["午前授業", "午後自習"]
            }
        }
    
    def _initialize_seasonal_events(self) -> Dict[str, List[Dict]]:
        """季節イベントを初期化"""
        return {
            "spring": [
                {"name": "入学式", "month": 4, "duration_days": 1},
                {"name": "新入生歓迎会", "month": 4, "duration_days": 3},
                {"name": "春の遠足", "month": 5, "duration_days": 1}
            ],
            "summer": [
                {"name": "期末テスト", "month": 7, "duration_days": 5},
                {"name": "夏祭り準備", "month": 7, "duration_days": 10},
                {"name": "夏休み", "month": 8, "duration_days": 30}
            ],
            "autumn": [
                {"name": "文化祭", "month": 10, "duration_days": 3},
                {"name": "体育祭", "month": 10, "duration_days": 1},
                {"name": "修学旅行", "month": 11, "duration_days": 3}
            ],
            "winter": [
                {"name": "冬休み", "month": 12, "duration_days": 14},
                {"name": "卒業式準備", "month": 2, "duration_days": 7},
                {"name": "卒業式", "month": 3, "duration_days": 1}
            ]
        }
    
    def generate_daily_events(self, current_time: datetime, 
                            characters: Dict[str, Any], 
                            world_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """1日分のイベントを生成"""
        events = []
        
        # 1. 定期イベント (学校スケジュール基準)
        scheduled_events = self._generate_scheduled_events(current_time, world_context)
        events.extend(scheduled_events)
        
        # 2. キャラクター主導イベント
        character_events = self._generate_character_initiated_events(characters, world_context)
        events.extend(character_events)
        
        # 3. ランダム遭遇イベント
        random_events = self._generate_random_encounters(characters, world_context)
        events.extend(random_events)
        
        # 4. 緊急イベント (関係性の問題等)
        emergency_events = self._generate_emergency_events(characters, world_context)
        events.extend(emergency_events)
        
        # 5. 季節イベント
        seasonal_events = self._generate_seasonal_events(current_time, characters)
        events.extend(seasonal_events)
        
        return self._prioritize_and_filter_events(events, world_context)
    
    def _generate_scheduled_events(self, current_time: datetime, 
                                 world_context: Dict) -> List[Dict]:
        """スケジュール化されたイベントを生成"""
        events = []
        
        # 曜日チェック
        weekday = current_time.strftime("%A").lower()
        time_str = current_time.strftime("%H:%M")
        
        # 朝の挨拶イベント
        if "08:00" <= time_str <= "08:30":
            if random.random() < 0.7:  # 70%の確率
                events.append({
                    "template_id": "morning_greeting",
                    "scheduled_time": current_time,
                    "auto_participants": 2,
                    "context": "登校時の自然な出会い"
                })
        
        # 昼食イベント
        if "12:40" <= time_str <= "13:25":
            if random.random() < 0.5:  # 50%の確率
                events.append({
                    "template_id": "lunch_together",
                    "scheduled_time": current_time,
                    "auto_participants": random.randint(2, 4),
                    "context": "昼休みの交流タイム"
                })
                
        return events
    
    def _generate_character_initiated_events(self, characters: Dict, 
                                           world_context: Dict) -> List[Dict]:
        """キャラクター主導のイベントを生成"""
        events = []
        
        for char_id, char_data in characters.items():
            # キャラクターの性格・状況に基づいてイベント発起
            helpfulness = char_data.get('personality_growth', {}).get('helpfulness', 50)
            curiosity = char_data.get('personality_growth', {}).get('curiosity_level', 50)
            
            # おせっかいキャラは他人を助けるイベントを起こしやすい
            if helpfulness > 80 and random.random() < 0.3:
                events.append({
                    "template_id": "study_session",
                    "initiator": char_id,
                    "context": f"{char_data.get('character_name', char_id)}が勉強会を提案",
                    "target_participants": ["struggling_student"]
                })
            
            # 好奇心旺盛なキャラは新しい交流を求める
            if curiosity > 85 and random.random() < 0.2:
                events.append({
                    "template_id": "heart_to_heart",
                    "initiator": char_id,
                    "context": f"{char_data.get('character_name', char_id)}が深い話をしたがっている"
                })
        
        return events
    
    def _generate_random_encounters(self, characters: Dict, 
                                  world_context: Dict) -> List[Dict]:
        """偶然の遭遇イベントを生成"""
        events = []
        
        # 確率的に偶然の遭遇が発生
        if random.random() < 0.4:  # 40%の確率
            encounter_locations = ["図書館", "購買", "廊下", "屋上", "部活動場所"]
            location = random.choice(encounter_locations)
            
            events.append({
                "template_id": "random_encounter",
                "location": location,
                "participants_count": random.randint(2, 3),
                "context": f"{location}での偶然の出会い"
            })
        
        return events
    
    def _generate_emergency_events(self, characters: Dict, 
                                 world_context: Dict) -> List[Dict]:
        """緊急イベントを生成"""
        events = []
        
        # 関係性の問題を検出
        relationships = world_context.get('relationships', {})
        
        for pair_key, rel_data in relationships.items():
            if isinstance(rel_data, dict):
                tension = rel_data.get('tension', 0)
                misunderstanding = rel_data.get('misunderstanding', 0)
                
                # 関係性に問題がある場合、解決イベントを発生
                if tension > 30 or misunderstanding > 40:
                    if random.random() < 0.6:  # 60%の確率で解決機会
                        char1, char2 = pair_key.split('_')
                        events.append({
                            "template_id": "conflict_resolution", 
                            "participants": [char1, char2],
                            "context": "関係性修復の機会",
                            "urgency": "high"
                        })
        
        return events
    
    def _generate_seasonal_events(self, current_time: datetime, 
                                characters: Dict) -> List[Dict]:
        """季節イベントを生成"""
        events = []
        
        current_month = current_time.month
        season = self._get_season(current_month)
        
        seasonal_events = self.seasonal_events.get(season, [])
        
        for event_info in seasonal_events:
            if event_info["month"] == current_month:
                # まだ開催されていない季節イベントを追加
                events.append({
                    "template_id": "seasonal_event",
                    "event_name": event_info["name"],
                    "duration_days": event_info["duration_days"],
                    "season": season,
                    "context": f"{season}の特別イベント: {event_info['name']}"
                })
        
        return events
    
    def _get_season(self, month: int) -> str:
        """月から季節を取得"""
        if 3 <= month <= 5:
            return "spring"
        elif 6 <= month <= 8:
            return "summer"
        elif 9 <= month <= 11:
            return "autumn"
        else:
            return "winter"
    
    def _prioritize_and_filter_events(self, events: List[Dict], 
                                    world_context: Dict) -> List[Dict]:
        """イベントの優先度付けとフィルタリング"""
        # 緊急度による並び替え
        urgency_order = {"high": 3, "medium": 2, "low": 1, None: 1}
        events.sort(key=lambda x: urgency_order.get(x.get("urgency"), 1), reverse=True)
        
        # 1日に発生するイベント数を制限 (最大5つ)
        return events[:5]
    
    def execute_event(self, event: Dict, participants: List[str], 
                     world_context: Dict) -> Dict[str, Any]:
        """イベントを実行し結果を返す"""
        template_id = event.get("template_id")
        template = self.event_templates.get(template_id)
        
        if not template:
            return {"success": False, "error": "Unknown event template"}
        
        # イベント実行の成功判定
        success_probability = self._calculate_success_probability(event, participants, world_context)
        success = random.random() < success_probability
        
        # イベント結果を生成
        result = {
            "event_id": f"{template_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "template_id": template_id,
            "participants": participants,
            "start_time": datetime.now(),
            "duration": template.duration_minutes,
            "location": template.location,
            "success": success,
            "emotional_impact": template.emotional_impact * (1.2 if success else 0.8),
            "relationship_effects": template.relationship_effects.copy(),
            "narrative": self._generate_event_narrative(template, participants, success, event.get("context", ""))
        }
        
        # 失敗時は効果を減少
        if not success:
            for effect_key in result["relationship_effects"]:
                result["relationship_effects"][effect_key] *= 0.5
        
        return result
    
    def _calculate_success_probability(self, event: Dict, participants: List[str], 
                                     world_context: Dict) -> float:
        """イベント成功確率を計算"""
        base_probability = 0.7
        
        # 参加者の相性を考慮
        relationships = world_context.get('relationships', {})
        avg_compatibility = 0.5
        
        if len(participants) == 2:
            pair_key = f"{min(participants)}_{max(participants)}"
            rel_data = relationships.get(pair_key, {})
            avg_compatibility = rel_data.get('compatibility', 50) / 100
        
        # 相性による成功率調整
        compatibility_modifier = (avg_compatibility - 0.5) * 0.4
        
        return max(0.1, min(0.95, base_probability + compatibility_modifier))
    
    def _generate_event_narrative(self, template: EventTemplate, participants: List[str], 
                                success: bool, context: str) -> str:
        """イベントの物語を生成"""
        participant_names = ", ".join(participants)
        
        base_narrative = f"{participant_names}が{template.location}で{template.name}。"
        
        if success:
            base_narrative += f" {context}がきっかけで、{template.description}が自然に展開された。"
        else:
            base_narrative += f" {context}だったが、少し期待とは違う結果になった。"
        
        return base_narrative

# 使用例・テスト用
if __name__ == "__main__":
    # テスト実行
    event_system = EventSystem()
    
    # テスト用キャラクターデータ
    test_characters = {
        "chappie": {
            "character_name": "相田茶子",
            "personality_growth": {
                "helpfulness": 95,
                "curiosity_level": 90,
                "charisma_level": 90
            }
        },
        "gemmy": {
            "character_name": "兼崎ちえみ", 
            "personality_growth": {
                "perfectionism": 90,
                "self_awareness": 80,
                "helpfulness": 85
            }
        }
    }
    
    test_world_context = {
        "relationships": {
            "chappie_gemmy": {
                "compatibility": 75,
                "tension": 20,
                "misunderstanding": 10
            }
        }
    }
    
    # 1日分のイベント生成
    current_time = datetime.now().replace(hour=12, minute=45)  # 昼休み
    daily_events = event_system.generate_daily_events(
        current_time, test_characters, test_world_context
    )
    
    print(f"生成されたイベント数: {len(daily_events)}")
    for event in daily_events:
        print(f"- {event.get('template_id', 'unknown')}: {event.get('context', 'No context')}")
    
    # イベント実行テスト
    if daily_events:
        first_event = daily_events[0]
        result = event_system.execute_event(
            first_event, 
            ["chappie", "gemmy"], 
            test_world_context
        )
        print(f"\\nイベント実行結果:")
        print(f"成功: {result['success']}")
        print(f"物語: {result['narrative']}")
        print(f"関係性効果: {result['relationship_effects']}")