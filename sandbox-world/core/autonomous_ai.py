#!/usr/bin/env python3
"""
🤖 Autonomous AI Engine
キャラクターが独自の意思決定を行う自律行動システム
"""

import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import os

@dataclass
class ActionOption:
    """行動選択肢"""
    id: str
    name: str
    description: str
    energy_cost: int  # 1-10
    emotional_reward: float  # -1.0 to 1.0
    social_impact: float  # -1.0 to 1.0 (他者への影響)
    prerequisites: List[str]
    personality_alignment: Dict[str, float]  # 性格特性との親和性

@dataclass
class CharacterState:
    """キャラクターの現在状態"""
    energy: int  # 0-100
    mood: float  # -1.0 to 1.0
    stress: int  # 0-100
    social_battery: int  # 0-100 (社交的エネルギー)
    current_goal: str
    active_emotions: List[str]
    recent_memories: List[Dict[str, Any]]

class AutonomousAI:
    """自律行動AIエンジン"""
    
    def __init__(self, anthropic_api_key: Optional[str] = None):
        self.api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        self.action_templates = self._initialize_action_templates()
        self.decision_history = []
        self.context_memory = {}
        
    def _initialize_action_templates(self) -> Dict[str, ActionOption]:
        """行動テンプレートを初期化"""
        actions = {}
        
        # 社交的行動
        actions["approach_friend"] = ActionOption(
            id="approach_friend",
            name="友達に話しかける",
            description="近くにいる友達に自分から声をかける",
            energy_cost=2,
            emotional_reward=0.4,
            social_impact=0.3,
            prerequisites=["friendship_level >= 20"],
            personality_alignment={"helpfulness": 0.8, "charisma_level": 0.6}
        )
        
        actions["help_classmate"] = ActionOption(
            id="help_classmate",
            name="クラスメイトを助ける",
            description="困っている人を見つけて手助けする",
            energy_cost=4,
            emotional_reward=0.7,
            social_impact=0.5,
            prerequisites=["someone_needs_help"],
            personality_alignment={"helpfulness": 0.9, "curiosity_level": 0.4}
        )
        
        actions["start_conversation"] = ActionOption(
            id="start_conversation",
            name="新しい話題を振る",
            description="面白い話題や最近の出来事について話し始める",
            energy_cost=3,
            emotional_reward=0.3,
            social_impact=0.4,
            prerequisites=["social_battery >= 30"],
            personality_alignment={"charisma_level": 0.7, "humor_level": 0.5}
        )
        
        # 学習・成長行動
        actions["study_quietly"] = ActionOption(
            id="study_quietly",
            name="静かに勉強する",
            description="一人で集中して勉強に取り組む",
            energy_cost=6,
            emotional_reward=0.2,
            social_impact=-0.1,
            prerequisites=["test_approaching"],
            personality_alignment={"perfectionism": 0.8, "self_awareness": 0.6}
        )
        
        actions["practice_hobby"] = ActionOption(
            id="practice_hobby",
            name="趣味の練習",
            description="ダンスや特技の練習をする",
            energy_cost=5,
            emotional_reward=0.6,
            social_impact=0.1,
            prerequisites=["free_time"],
            personality_alignment={"curiosity_level": 0.7}
        )
        
        # 感情管理行動
        actions["take_break"] = ActionOption(
            id="take_break",
            name="休憩する",
            description="疲れたときに少し休む",
            energy_cost=-3,  # エネルギー回復
            emotional_reward=0.2,
            social_impact=0.0,
            prerequisites=["energy < 30 OR stress > 60"],
            personality_alignment={"self_awareness": 0.8}
        )
        
        actions["seek_advice"] = ActionOption(
            id="seek_advice",
            name="相談する",
            description="信頼できる人に悩みを相談する",
            energy_cost=3,
            emotional_reward=0.5,
            social_impact=0.2,
            prerequisites=["stress > 50", "trusted_friend_available"],
            personality_alignment={"trust": 0.8, "openness": 0.6}
        )
        
        # 探索・冒険行動
        actions["explore_school"] = ActionOption(
            id="explore_school",
            name="学校探索",
            description="普段行かない場所を探索してみる",
            energy_cost=4,
            emotional_reward=0.4,
            social_impact=0.1,
            prerequisites=["curiosity_level >= 70"],
            personality_alignment={"curiosity_level": 0.9, "adventurousness": 0.7}
        )
        
        return actions
    
    def make_autonomous_decision(self, character_id: str, character_data: Dict[str, Any], 
                               current_state: CharacterState, 
                               world_context: Dict[str, Any]) -> Dict[str, Any]:
        """自律的な意思決定を実行"""
        
        # 1. 利用可能な行動選択肢を生成
        available_actions = self._get_available_actions(
            character_data, current_state, world_context
        )
        
        if not available_actions:
            return self._default_action(character_id, current_state)
        
        # 2. 各行動の評価値を計算
        action_scores = {}
        for action_id, action in available_actions.items():
            score = self._evaluate_action(
                action, character_data, current_state, world_context
            )
            action_scores[action_id] = score
        
        # 3. 最適行動を選択（確率的）
        chosen_action_id = self._select_action_probabilistically(action_scores)
        chosen_action = available_actions[chosen_action_id]
        
        # 4. AI推論による行動詳細化（Claude API使用）
        action_details = self._enhance_action_with_ai(
            character_id, character_data, chosen_action, current_state, world_context
        )
        
        # 5. 決定結果を記録
        decision_result = {
            "character_id": character_id,
            "timestamp": datetime.now(),
            "chosen_action": chosen_action_id,
            "action_details": action_details,
            "reasoning": action_details.get("reasoning", ""),
            "expected_outcomes": action_details.get("expected_outcomes", {}),
            "state_before": current_state.__dict__.copy()
        }
        
        self.decision_history.append(decision_result)
        
        return decision_result
    
    def _get_available_actions(self, character_data: Dict, state: CharacterState, 
                             world_context: Dict) -> Dict[str, ActionOption]:
        """現在利用可能な行動選択肢を取得"""
        available = {}
        
        for action_id, action in self.action_templates.items():
            if self._check_prerequisites(action.prerequisites, character_data, state, world_context):
                available[action_id] = action
        
        return available
    
    def _check_prerequisites(self, prerequisites: List[str], character_data: Dict, 
                           state: CharacterState, world_context: Dict) -> bool:
        """前提条件をチェック"""
        for prereq in prerequisites:
            if not self._evaluate_condition(prereq, character_data, state, world_context):
                return False
        return True
    
    def _evaluate_condition(self, condition: str, character_data: Dict, 
                          state: CharacterState, world_context: Dict) -> bool:
        """条件を評価"""
        try:
            # 動的条件評価
            if ">=" in condition:
                var, threshold = condition.split(" >= ")
                value = self._get_variable_value(var.strip(), character_data, state, world_context)
                return value >= float(threshold)
            elif "<" in condition:
                var, threshold = condition.split(" < ")
                value = self._get_variable_value(var.strip(), character_data, state, world_context)
                return value < float(threshold)
            elif ">" in condition:
                var, threshold = condition.split(" > ")
                value = self._get_variable_value(var.strip(), character_data, state, world_context)
                return value > float(threshold)
            elif condition in ["someone_needs_help", "trusted_friend_available", "free_time", "test_approaching"]:
                return world_context.get(condition, False)
            else:
                return True
        except:
            return False
    
    def _get_variable_value(self, var_name: str, character_data: Dict, 
                          state: CharacterState, world_context: Dict) -> float:
        """変数値を取得"""
        if var_name in ["energy", "stress", "social_battery"]:
            return getattr(state, var_name)
        elif var_name == "friendship_level":
            return world_context.get("average_friendship_level", 30)
        elif var_name in character_data.get("personality_growth", {}):
            return character_data["personality_growth"][var_name]
        else:
            return 0
    
    def _evaluate_action(self, action: ActionOption, character_data: Dict, 
                        state: CharacterState, world_context: Dict) -> float:
        """行動の評価値を計算"""
        score = 0.0
        
        # 1. 性格特性との親和性 (40%)
        personality_score = 0.0
        personality_growth = character_data.get("personality_growth", {})
        
        for trait, weight in action.personality_alignment.items():
            trait_value = personality_growth.get(trait, 50) / 100.0
            personality_score += trait_value * weight
        
        if action.personality_alignment:
            personality_score /= len(action.personality_alignment)
        
        score += personality_score * 0.4
        
        # 2. 現在状態との適合性 (30%)
        state_score = 0.0
        
        # エネルギーコストと現在エネルギーの関係
        if action.energy_cost <= state.energy:
            state_score += 0.5
        else:
            state_score -= 0.3  # エネルギー不足ペナルティ
        
        # 気分と行動の感情報酬の関係
        if state.mood < 0 and action.emotional_reward > 0:
            state_score += 0.3  # 気分改善行動にボーナス
        
        # ストレスと社交行動の関係
        if state.stress > 60 and action.social_impact > 0.3:
            state_score -= 0.2  # 高ストレス時は社交行動を避けがち
        
        score += state_score * 0.3
        
        # 3. 期待される報酬 (20%)
        reward_score = (action.emotional_reward + 1) / 2  # -1~1 を 0~1 に変換
        score += reward_score * 0.2
        
        # 4. 社会的影響の好ましさ (10%)
        social_score = 0.5  # 中性
        if action.social_impact > 0:
            # 社交的キャラは社会的影響を好む
            charisma = personality_growth.get("charisma_level", 50) / 100.0
            social_score = 0.5 + (action.social_impact * charisma * 0.5)
        
        score += social_score * 0.1
        
        return max(0.0, min(1.0, score))
    
    def _select_action_probabilistically(self, action_scores: Dict[str, float]) -> str:
        """確率的に行動を選択"""
        if not action_scores:
            return "take_break"  # デフォルト行動
        
        # ソフトマックス関数で確率分布を計算
        scores = np.array(list(action_scores.values()))
        temperatures = 2.0  # 探索性の調整
        
        exp_scores = np.exp(scores / temperatures)
        probabilities = exp_scores / np.sum(exp_scores)
        
        # 確率的選択
        actions = list(action_scores.keys())
        chosen_index = np.random.choice(len(actions), p=probabilities)
        
        return actions[chosen_index]
    
    def _enhance_action_with_ai(self, character_id: str, character_data: Dict, 
                              action: ActionOption, state: CharacterState, 
                              world_context: Dict) -> Dict[str, Any]:
        """AI推論で行動を詳細化"""
        
        # Claude APIが利用可能な場合はAI推論を実行
        if self.api_key:
            try:
                return self._call_claude_for_action_enhancement(
                    character_id, character_data, action, state, world_context
                )
            except Exception as e:
                print(f"AI enhancement failed: {e}")
        
        # フォールバック：ルールベースの詳細化
        return self._rule_based_enhancement(character_id, character_data, action, state)
    
    def _call_claude_for_action_enhancement(self, character_id: str, character_data: Dict,
                                          action: ActionOption, state: CharacterState,
                                          world_context: Dict) -> Dict[str, Any]:
        """Claude APIを呼び出して行動を詳細化"""
        
        import requests
        
        # キャラクター情報の要約
        character_summary = {
            "name": character_data.get("character_name", character_id),
            "personality": character_data.get("personality_growth", {}),
            "current_mood": state.mood,
            "energy": state.energy,
            "recent_goal": state.current_goal
        }
        
        prompt = f"""
        キャラクター「{character_summary['name']}」が「{action.name}」という行動を取ろうとしています。
        
        キャラクター情報:
        {json.dumps(character_summary, ensure_ascii=False, indent=2)}
        
        選択した行動:
        - 名前: {action.name}
        - 説明: {action.description}
        
        以下の形式でJSONを返してください:
        {{
            "dialogue": "キャラクターが言いそうなセリフ",
            "internal_thought": "キャラクターの心の声",
            "specific_actions": ["具体的な行動1", "具体的な行動2"],
            "reasoning": "なぜこの行動を選んだかの理由",
            "expected_outcomes": {{
                "emotional_change": "期待される感情変化",
                "relationship_impact": "他者への影響予測"
            }}
        }}
        """
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        
        data = {
            "model": "claude-3-haiku-20240307",  # 高速・低コスト版
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['content'][0]['text']
            
            # JSONを抽出
            if '```json' in content:
                json_start = content.find('```json') + 7
                json_end = content.find('```', json_start)
                content = content[json_start:json_end].strip()
            
            return json.loads(content)
        else:
            raise Exception(f"API call failed: {response.status_code}")
    
    def _rule_based_enhancement(self, character_id: str, character_data: Dict,
                              action: ActionOption, state: CharacterState) -> Dict[str, Any]:
        """ルールベースの行動詳細化（フォールバック）"""
        
        character_name = character_data.get("character_name", character_id)
        personality = character_data.get("personality_growth", {})
        
        # チャッピーちゃんの特徴的なセリフパターンを使用
        dialogue_templates = {
            "approach_friend": [
                "おはよ〜♪ 今日も一日がんばろうね〜",
                "あ、{}ちゃん！ちょっと話さない？",
                "みんな〜♪ 何してるの〜？"
            ],
            "help_classmate": [
                "大丈夫？何か手伝えることあるよ〜♪",
                "困ってるなら聞いてよ〜！私が何とかするから〜",
                "一緒にやろうよ〜♪ 一人より楽しいし〜"
            ],
            "start_conversation": [
                "そういえばさ〜、この前のテストどうだった？",
                "今度の文化祭、何やる予定〜？",
                "あ！それ面白そうじゃん〜♪"
            ]
        }
        
        dialogue = random.choice(
            dialogue_templates.get(action.id, ["えーっとね〜..."])
        )
        
        return {
            "dialogue": dialogue,
            "internal_thought": f"今日は{action.description}してみよう♪",
            "specific_actions": [action.description],
            "reasoning": f"{character_name}らしい自然な行動選択",
            "expected_outcomes": {
                "emotional_change": "ポジティブな気分向上",
                "relationship_impact": "友好的な関係促進"
            }
        }
    
    def _default_action(self, character_id: str, state: CharacterState) -> Dict[str, Any]:
        """デフォルト行動（何も特別なことをしない）"""
        return {
            "character_id": character_id,
            "timestamp": datetime.now(),
            "chosen_action": "observe",
            "action_details": {
                "dialogue": "うーん、何しようかな〜",
                "internal_thought": "特にやることないかも...",
                "specific_actions": ["周りを観察する"],
                "reasoning": "適切な行動が見つからない",
                "expected_outcomes": {
                    "emotional_change": "特になし",
                    "relationship_impact": "変化なし"
                }
            },
            "state_before": state.__dict__.copy()
        }
    
    def update_character_state_from_action(self, state: CharacterState, 
                                         action_result: Dict[str, Any]) -> CharacterState:
        """行動結果から キャラクター状態を更新"""
        action_id = action_result.get("chosen_action")
        
        if action_id in self.action_templates:
            action = self.action_templates[action_id]
            
            # エネルギーの変化
            new_energy = max(0, min(100, state.energy - action.energy_cost))
            
            # 気分の変化
            mood_change = action.emotional_reward * 0.3
            new_mood = max(-1.0, min(1.0, state.mood + mood_change))
            
            # 社交バッテリーの変化
            social_change = int(action.social_impact * 10)
            new_social_battery = max(0, min(100, state.social_battery + social_change))
            
            # 新しい状態を作成
            updated_state = CharacterState(
                energy=new_energy,
                mood=new_mood,
                stress=max(0, state.stress - 5),  # 行動によりストレス軽減
                social_battery=new_social_battery,
                current_goal=state.current_goal,
                active_emotions=state.active_emotions,
                recent_memories=state.recent_memories + [action_result]
            )
            
            return updated_state
        
        return state

# 使用例・テスト用
if __name__ == "__main__":
    # テスト用データ
    test_character_data = {
        "character_name": "相田茶子",
        "personality_growth": {
            "helpfulness": 95,
            "curiosity_level": 90,
            "charisma_level": 90,
            "humor_level": 85
        }
    }
    
    test_state = CharacterState(
        energy=75,
        mood=0.3,
        stress=20,
        social_battery=80,
        current_goal="友達との関係を深める",
        active_emotions=["happy", "energetic"],
        recent_memories=[]
    )
    
    test_world_context = {
        "someone_needs_help": True,
        "trusted_friend_available": True,
        "free_time": True,
        "average_friendship_level": 60
    }
    
    # 自律AIエンジン実行
    ai_engine = AutonomousAI()
    
    decision = ai_engine.make_autonomous_decision(
        "chappie", test_character_data, test_state, test_world_context
    )
    
    print(f"選択された行動: {decision['chosen_action']}")
    print(f"セリフ: {decision['action_details']['dialogue']}")
    print(f"推論: {decision['action_details']['reasoning']}")
    
    # 状態更新テスト
    updated_state = ai_engine.update_character_state_from_action(test_state, decision)
    print(f"\\n更新後エネルギー: {updated_state.energy}")
    print(f"更新後気分: {updated_state.mood:.2f}")