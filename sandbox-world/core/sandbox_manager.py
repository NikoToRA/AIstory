#!/usr/bin/env python3
"""
🎮 Sandbox World Manager
完全自律型箱庭システムの統合管理システム
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import time

from .relationship_engine import RelationshipEngine, RelationshipMetrics
from .event_system import EventSystem
from .autonomous_ai import AutonomousAI, CharacterState

class SandboxManager:
    """箱庭世界の統合管理システム"""
    
    def __init__(self, world_data_path: str, anthropic_api_key: Optional[str] = None):
        self.world_data_path = Path(world_data_path)
        self.running = False
        self.simulation_speed = 1.0  # 1.0 = リアルタイム
        
        # コアシステム初期化
        self.relationship_engine = RelationshipEngine(str(world_data_path))
        self.event_system = EventSystem()
        self.autonomous_ai = AutonomousAI(anthropic_api_key)
        
        # 世界状態
        self.characters = {}
        self.character_states = {}
        self.world_state = {
            "current_time": datetime.now(),
            "school_day": True,
            "weather": "晴れ",
            "special_events": [],
            "global_mood": 0.5
        }
        
        # 実行履歴
        self.daily_logs = []
        self.interaction_history = []
        
    async def initialize_world(self) -> bool:
        """世界を初期化"""
        try:
            # キャラクターデータ読み込み
            await self._load_characters()
            
            # 初期関係性設定
            await self._initialize_relationships()
            
            # キャラクター状態初期化
            self._initialize_character_states()
            
            print(f"🌍 Sandbox World initialized with {len(self.characters)} characters")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize world: {e}")
            return False
    
    async def _load_characters(self):
        """キャラクターデータを読み込み"""
        characters_dir = self.world_data_path / "story-world" / "characters"
        
        if not characters_dir.exists():
            raise FileNotFoundError(f"Characters directory not found: {characters_dir}")
        
        for char_dir in characters_dir.iterdir():
            if char_dir.is_dir():
                char_id = char_dir.name
                
                # memory.jsonから詳細データを読み込み
                memory_file = char_dir / "memory.json"
                if memory_file.exists():
                    with open(memory_file, 'r', encoding='utf-8') as f:
                        char_data = json.load(f)
                        self.characters[char_id] = char_data
                        
                        print(f"📝 Loaded character: {char_data.get('character_name', char_id)}")
    
    async def _initialize_relationships(self):
        """キャラクター間の初期関係性を設定"""
        character_ids = list(self.characters.keys())
        
        # 全ペアの関係性を初期化
        for i, char1_id in enumerate(character_ids):
            for char2_id in character_ids[i+1:]:
                char1_data = self.characters[char1_id]
                char2_data = self.characters[char2_id]
                
                relationship = self.relationship_engine.initialize_relationship(
                    char1_id, char2_id, char1_data, char2_data
                )
                
                print(f"💕 Initialized relationship: {char1_id} ↔ {char2_id} (compatibility: {relationship.compatibility:.1f})")
    
    def _initialize_character_states(self):
        """キャラクター状態を初期化"""
        for char_id, char_data in self.characters.items():
            # 性格に基づく初期状態設定
            personality = char_data.get("personality_growth", {})
            
            initial_state = CharacterState(
                energy=random.randint(60, 90),
                mood=0.2,  # 軽くポジティブ
                stress=random.randint(10, 30),
                social_battery=random.randint(50, 90),
                current_goal=self._generate_initial_goal(char_data),
                active_emotions=["neutral"],
                recent_memories=[]
            )
            
            self.character_states[char_id] = initial_state
    
    def _generate_initial_goal(self, char_data: Dict) -> str:
        """初期目標を生成"""
        goals = char_data.get("growth_goals", [])
        if goals:
            return random.choice(goals)
        else:
            return "今日を楽しく過ごす"
    
    async def start_simulation(self, duration_hours: Optional[int] = None):
        """シミュレーション開始"""
        self.running = True
        start_time = time.time()
        
        print(f"🚀 Starting sandbox simulation...")
        
        try:
            while self.running:
                if duration_hours and (time.time() - start_time) > duration_hours * 3600:
                    break
                
                # 1時間ごとのメインループ
                await self._simulation_tick()
                
                # 実行間隔調整 (simulation_speedに基づく)
                await asyncio.sleep(3600 / self.simulation_speed)  # 1時間 / 速度
                
        except KeyboardInterrupt:
            print("\\n⏹️ Simulation interrupted by user")
        except Exception as e:
            print(f"💥 Simulation error: {e}")
        finally:
            await self.stop_simulation()
    
    async def _simulation_tick(self):
        """シミュレーションの1ティック（1時間分）実行"""
        current_time = self.world_state["current_time"]
        
        print(f"\\n🕐 {current_time.strftime('%Y-%m-%d %H:%M')} - Simulation Tick")
        
        # 1. イベント生成
        daily_events = self.event_system.generate_daily_events(
            current_time, self.characters, self.world_state
        )
        
        # 2. 各キャラクターの自律行動決定
        character_decisions = {}
        for char_id, char_state in self.character_states.items():
            char_data = self.characters[char_id]
            
            decision = self.autonomous_ai.make_autonomous_decision(
                char_id, char_data, char_state, self.world_state
            )
            
            character_decisions[char_id] = decision
            
            print(f"🎭 {char_data.get('character_name', char_id)}: {decision['chosen_action']}")
            if 'dialogue' in decision.get('action_details', {}):
                print(f"   💬 \"{decision['action_details']['dialogue']}\"")
        
        # 3. イベント実行と関係性更新
        await self._execute_events_and_interactions(daily_events, character_decisions)
        
        # 4. キャラクター状態更新
        self._update_all_character_states(character_decisions)
        
        # 5. 世界状態更新
        self._update_world_state()
        
        # 6. ログ記録
        await self._log_simulation_tick(character_decisions, daily_events)
        
    async def _execute_events_and_interactions(self, events: List[Dict], 
                                             decisions: Dict[str, Any]):
        """イベント実行と相互作用処理"""
        
        # イベントによるキャラクター同士の関係性変化
        for event in events:
            if event.get("participants"):
                participants = event["participants"]
                
                # イベント実行
                event_result = self.event_system.execute_event(
                    event, participants, self.world_state
                )
                
                if event_result["success"]:
                    # 関係性更新
                    relationship_events = self.relationship_engine.evolve_relationship_from_event({
                        "type": event.get("template_id", "interaction"),
                        "participants": participants,
                        "description": event_result["narrative"],
                        "success": True
                    })
                    
                    print(f"📊 Event executed: {event_result['narrative']}")
                    
                    # 関係性変化をログ
                    for rel_event in relationship_events:
                        char1, char2 = rel_event.participants
                        relationship_status = self.relationship_engine.get_relationship_status(char1, char2)
                        print(f"   💕 {char1} ↔ {char2}: {relationship_status['level']}")
        
        # キャラクター決定による相互作用
        social_actions = [
            decision for decision in decisions.values()
            if decision.get("chosen_action") in ["approach_friend", "help_classmate", "start_conversation"]
        ]
        
        for decision in social_actions:
            await self._process_social_interaction(decision)
    
    async def _process_social_interaction(self, decision: Dict[str, Any]):
        """社交的行動の処理"""
        initiator = decision["character_id"]
        
        # 近くにいるキャラクターを見つけて相互作用
        available_targets = [
            char_id for char_id in self.characters.keys() 
            if char_id != initiator
        ]
        
        if available_targets:
            # 関係性レベルが高い相手を優先選択
            target_scores = {}
            for target in available_targets:
                rel_status = self.relationship_engine.get_relationship_status(initiator, target)
                if rel_status.get("level") != "no_relationship":
                    target_scores[target] = rel_status["metrics"]["intimacy"]
                else:
                    target_scores[target] = 0
            
            # 最も親しい相手を選択
            target = max(target_scores, key=target_scores.get)
            
            # 相互作用イベント生成
            interaction_event = {
                "type": "social_interaction",
                "participants": [initiator, target],
                "description": decision["action_details"]["dialogue"],
                "success": random.random() < 0.8  # 80%成功率
            }
            
            relationship_events = self.relationship_engine.evolve_relationship_from_event(interaction_event)
            
            print(f"🤝 Social interaction: {self.characters[initiator].get('character_name')} → {self.characters[target].get('character_name')}")
    
    def _update_all_character_states(self, decisions: Dict[str, Any]):
        """全キャラクターの状態を更新"""
        for char_id, decision in decisions.items():
            old_state = self.character_states[char_id]
            new_state = self.autonomous_ai.update_character_state_from_action(old_state, decision)
            self.character_states[char_id] = new_state
            
            # エネルギー回復 (時間経過による自然回復)
            if new_state.energy < 100:
                recovery = random.randint(2, 8)
                new_state.energy = min(100, new_state.energy + recovery)
    
    def _update_world_state(self):
        """世界状態を更新"""
        # 時間進行
        self.world_state["current_time"] += timedelta(hours=1)
        
        # 全体的な雰囲気計算
        total_mood = sum(state.mood for state in self.character_states.values())
        avg_mood = total_mood / len(self.character_states) if self.character_states else 0
        self.world_state["global_mood"] = (avg_mood + 1) / 2  # -1~1 を 0~1 に変換
        
        # 天気のランダム変化 (5%の確率)
        if random.random() < 0.05:
            weather_options = ["晴れ", "曇り", "雨", "雪"]
            self.world_state["weather"] = random.choice(weather_options)
    
    async def _log_simulation_tick(self, decisions: Dict[str, Any], events: List[Dict]):
        """シミュレーションティックをログ記録"""
        log_entry = {
            "timestamp": self.world_state["current_time"].isoformat(),
            "world_state": self.world_state.copy(),
            "character_decisions": decisions,
            "events": events,
            "character_states": {
                char_id: state.__dict__ for char_id, state in self.character_states.items()
            }
        }
        
        self.daily_logs.append(log_entry)
        
        # ログファイルへの保存 (1日分ずつ)
        if self.world_state["current_time"].hour == 0:  # 午前0時
            await self._save_daily_log()
    
    async def _save_daily_log(self):
        """1日分のログを保存"""
        if not self.daily_logs:
            return
            
        date_str = self.world_state["current_time"].strftime("%Y-%m-%d")
        log_file = self.world_data_path / "sandbox-logs" / f"{date_str}.json"
        
        # ディレクトリ作成
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # ログ保存
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.daily_logs, f, ensure_ascii=False, indent=2)
        
        print(f"📝 Daily log saved: {log_file}")
        self.daily_logs.clear()
    
    async def stop_simulation(self):
        """シミュレーション停止"""
        self.running = False
        
        # 最終ログ保存
        if self.daily_logs:
            await self._save_daily_log()
        
        # 関係性マトリックス出力
        relationship_matrix = self.relationship_engine.export_relationship_matrix()
        matrix_file = self.world_data_path / "sandbox-state" / "relationship_matrix.json"
        matrix_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(matrix_file, 'w', encoding='utf-8') as f:
            json.dump(relationship_matrix, f, ensure_ascii=False, indent=2)
        
        print(f"🏁 Simulation stopped. Final state saved.")
    
    def get_world_summary(self) -> Dict[str, Any]:
        """世界の現在状況を要約"""
        character_summaries = {}
        
        for char_id, char_data in self.characters.items():
            state = self.character_states.get(char_id)
            character_summaries[char_id] = {
                "name": char_data.get("character_name", char_id),
                "energy": state.energy if state else 0,
                "mood": state.mood if state else 0,
                "current_goal": state.current_goal if state else "不明",
                "total_experiences": char_data.get("total_experiences", 0)
            }
        
        return {
            "world_time": self.world_state["current_time"].isoformat(),
            "global_mood": self.world_state["global_mood"],
            "weather": self.world_state["weather"],
            "characters": character_summaries,
            "total_relationships": len(self.relationship_engine.relationships),
            "simulation_running": self.running
        }

# 使用例・テスト用
if __name__ == "__main__":
    import random
    
    async def main():
        # 箱庭マネージャー初期化
        sandbox = SandboxManager(
            world_data_path="/Users/suguruhirayama/Developer/haconiwa/AIstory-test",
            anthropic_api_key=None  # テスト時はAPI無し
        )
        
        # 世界初期化
        if await sandbox.initialize_world():
            # 現在状況表示
            summary = sandbox.get_world_summary()
            print(f"\\n🌍 World Summary:")
            print(f"Time: {summary['world_time']}")
            print(f"Global Mood: {summary['global_mood']:.2f}")
            print(f"Characters: {len(summary['characters'])}")
            
            # 短時間シミュレーション実行 (5分 = 5時間分)
            print(f"\\n🚀 Starting 5-hour simulation...")
            await sandbox.start_simulation(duration_hours=5)
        
    # 非同期実行
    asyncio.run(main())