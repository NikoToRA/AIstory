#!/usr/bin/env python3
"""
キャラクター成長デモンストレーション
複数のストーリーでキャラクターが深まる様子を実演
"""

import json
import os
from datetime import datetime
from pathlib import Path

def create_character_growth_story(episode_num, scenario_title, scenario_content, character_development):
    """キャラクター成長を示すストーリー生成"""
    print(f"🎭 エピソード{episode_num}: {scenario_title}")
    
    # storiesディレクトリ作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    story_date = datetime.now().strftime("%Y-%m-%d")
    story_title = f"ep{episode_num:02d}_{scenario_title}".replace(" ", "_").replace("　", "_")
    story_dir = Path(f"story-world/stories/{story_date}_{story_title}")
    story_dir.mkdir(parents=True, exist_ok=True)
    
    # キャラクター記憶を読み込み（成長を反映）
    try:
        with open("story-world/characters/chappie/memory.json", "r", encoding="utf-8") as f:
            chappie_memory = json.load(f)
    except FileNotFoundError:
        chappie_memory = {"experiences": [], "relationships": {}, "growth_points": []}
    
    try:
        with open("story-world/characters/gemmy/memory.json", "r", encoding="utf-8") as f:
            gemmy_memory = json.load(f)
    except FileNotFoundError:
        gemmy_memory = {"experiences": [], "relationships": {}, "growth_points": []}
    
    # エピソード別の成長ストーリー
    if episode_num == 1:
        discussion = f"""# エピソード{episode_num}: {scenario_title}

## 💬 チャッピーとジェミーちゃんの初対面

### 💬 **チャッピー（BOT）** 5分前:
「わー！図書室めっちゃ広いじゃん〜！あ、あそこにいる子が図書委員？
ねえねえ〜、本探してるんだけど〜、数学の参考書とか〜、あと英語も〜
そうそう、友達におすすめされた小説もあるし〜♪」

### 💬 **ジェミーちゃん（BOT）** 4分前:
「えーっと...（心の声：声が大きい...）
申し訳ございませんが、図書室では静粛にお願いいたします。
本のご相談でしたら、カウンターでお受けいたします。」

### 💬 **チャッピー（BOT）** 3分前:
「あ、ごめんごめん〜！でもさ、一人で探すより一緒の方が楽しくない？
私チャッピーって言うの〜♪ダンス部なんだけど、勉強も頑張ってるんだ〜」

### 💬 **ジェミーちゃん（BOT）** 2分前:
「...兼崎と申します。図書委員として、利用者の支援をさせていただきます。
（心の声：この人、悪気はなさそうだけど...）」

### 💬 **チャッピー（BOT）** 1分前:
「ジェミーちゃん！？可愛い名前〜♪
てか、めっちゃ真面目そうだけど、同じ年？一緒にお昼とか食べない？」

### 💬 **ジェミーちゃん（BOT）** たった今:
「...検討いたします。まずは、お探しの本をご案内いたします。
（小声）数学でしたら、こちらの棚に...」

## 📝 この回での成長
- **チャッピー**: 図書室で初めてジェミーちゃんと出会う
- **ジェミーちゃん**: うるさい子だけど悪気はないと理解

## 🎯 関係性の変化
- 完全に他人 → 名前を覚えた知り合い
"""
    
    elif episode_num == 2:
        discussion = f"""# エピソード{episode_num}: {scenario_title}

## 💬 お昼休み、チャッピーがまたやってきた

### 💬 **チャッピー（BOT）** 5分前:
「ジェミーちゃ〜ん♪約束通りお昼持ってきたよ〜！
あ、そうそう〜、昨日の数学の本めっちゃ役立ったし〜、
今度は物理も教えて〜、あと化学も〜、あ、英語の発音のコツとか〜」

### 💬 **ジェミーちゃん（BOT）** 4分前:
「えーっと...（心の声：また始まった...でも、お昼は持ってきてくれた）
申し訳ございませんが、全科目を一度にご説明するのは...
まずは一つずつ、順序立てて進めましょうか。」

### 💬 **チャッピー（BOT）** 3分前:
「さすがジェミーちゃん！計画的だね〜♪
私なんて思いついたら即行動タイプだから〜、
でも、ジェミーちゃんと一緒だと安心するかも〜」

### 💬 **ジェミーちゃん（BOT）** 2分前:
「（少し嬉しそう）そ、そうですか...
物理から始めましょうか。基礎的な公式から...
（心の声：意外と素直で、悪い子じゃないのかも）」

### 💬 **チャッピー（BOT）** 1分前:
「やった〜！ジェミーちゃんって教えるの上手そう〜♪
あ、そうそう〜、今度ダンス部の発表があるから見に来てよ〜」

### 💬 **ジェミーちゃん（BOT）** たった今:
「...検討いたします。まずは物理の勉強を...
（小声）でも、ダンス...少し興味が...」

## 📝 この回での成長
- **チャッピー**: 約束を守り、ジェミーちゃんのペースを少し理解
- **ジェミーちゃん**: チャッピーの良い面を認め始める

## 🎯 関係性の変化
- 知り合い → 勉強を教える先生と生徒の関係
"""
    
    elif episode_num == 3:
        discussion = f"""# エピソード{episode_num}: {scenario_title}

## 💬 ダンス部発表当日、ジェミーちゃんが来てくれた

### 💬 **チャッピー（BOT）** 5分前:
「ジェミーちゃん！？マジで来てくれたの〜！？
やば〜い、めっちゃ嬉しい〜♪でも緊張してきた〜
いつもは全然緊張しないのに〜、なんでだろ〜？」

### 💬 **ジェミーちゃん（BOT）** 4分前:
「お疲れ様です。約束でしたので...
（心の声：チャッピーさんが緊張するなんて意外）
き、緊張されているのですか？いつもあんなに自信満々なのに...」

### 💬 **チャッピー（BOT）** 3分前:
「あ〜、バレた〜！実は人前で踊るの、まだちょっと怖いんだ〜
でもジェミーちゃんがいるから頑張れる〜♪見ててね〜」

### 💬 **ジェミーちゃん（BOT）** 2分前:
「（驚いた表情）そんな...チャッピーさんはいつも堂々としてて...
でも、頑張ってください。応援しています。
（心の声：この人にも弱い部分があるんだ...）」

### 💬 **チャッピー（BOT）** 1分前:
「ありがとう〜！ジェミーちゃんって実は優しいよね〜♪
よし、頑張るぞ〜！」

### 💬 **ジェミーちゃん（BOT）** たった今:
「（発表後）お疲れ様でした...とても...素敵でした。
チャッピーさんの一生懸命な姿、すごく...良かったです。
（小声）私も...何か頑張ってみたいな...」

## 📝 この回での成長
- **チャッピー**: 弱い部分を見せ、ジェミーちゃんを信頼するように
- **ジェミーちゃん**: チャッピーの人間らしい面を見て、距離が縮まる

## 🎯 関係性の変化
- 先生と生徒 → 互いを理解し合う友達
"""
    
    # 記憶更新
    if episode_num == 1:
        chappie_memory["experiences"].append({
            "date": datetime.now().isoformat(),
            "event": "図書室でジェミーちゃんと初対面",
            "emotion": "興味深い",
            "learning": "真面目な子だけど悪い子じゃなさそう"
        })
        chappie_memory["relationships"]["gemmy"] = {"trust": 20, "understanding": 15}
        
        gemmy_memory["experiences"].append({
            "date": datetime.now().isoformat(),
            "event": "うるさいダンス部の子チャッピーと出会う",
            "emotion": "困惑",
            "learning": "声は大きいけど悪気はない"
        })
        gemmy_memory["relationships"]["chappie"] = {"trust": 15, "understanding": 10}
        
    elif episode_num == 2:
        chappie_memory["experiences"].append({
            "date": datetime.now().isoformat(),
            "event": "ジェミーちゃんと勉強、教えてもらう",
            "emotion": "感謝",
            "learning": "計画的に進める大切さ"
        })
        chappie_memory["relationships"]["gemmy"] = {"trust": 45, "understanding": 35}
        
        gemmy_memory["experiences"].append({
            "date": datetime.now().isoformat(),
            "event": "チャッピーに勉強を教える",
            "emotion": "少し嬉しい",
            "learning": "意外と素直で良い子"
        })
        gemmy_memory["relationships"]["chappie"] = {"trust": 40, "understanding": 30}
        
    elif episode_num == 3:
        chappie_memory["experiences"].append({
            "date": datetime.now().isoformat(),
            "event": "ダンス発表、ジェミーちゃんが応援してくれた",
            "emotion": "とても嬉しい",
            "learning": "弱い部分を見せても大丈夫"
        })
        chappie_memory["relationships"]["gemmy"] = {"trust": 75, "understanding": 65}
        
        gemmy_memory["experiences"].append({
            "date": datetime.now().isoformat(),
            "event": "チャッピーのダンス発表を見る",
            "emotion": "感動",
            "learning": "チャッピーにも弱い部分がある、人間らしい"
        })
        gemmy_memory["relationships"]["chappie"] = {"trust": 70, "understanding": 60}
    
    # ファイル保存
    with open(story_dir / f"discussion_{timestamp}.md", "w", encoding="utf-8") as f:
        f.write(discussion)
    
    # 記憶更新
    with open("story-world/characters/chappie/memory.json", "w", encoding="utf-8") as f:
        json.dump(chappie_memory, f, indent=2, ensure_ascii=False)
    
    with open("story-world/characters/gemmy/memory.json", "w", encoding="utf-8") as f:
        json.dump(gemmy_memory, f, indent=2, ensure_ascii=False)
    
    print(f"✅ エピソード{episode_num}完了!")
    print(f"📁 保存先: {story_dir}")
    
    return story_dir

if __name__ == "__main__":
    # 3エピソードでキャラクター成長を実演
    episodes = [
        (1, "図書室での初対面", "チャッピーとジェミーちゃんが初めて出会う"),
        (2, "お昼休みの勉強会", "チャッピーがジェミーちゃんに勉強を教わる"),
        (3, "ダンス部発表会", "ジェミーちゃんがチャッピーのダンスを見に来る")
    ]
    
    for episode_num, title, content in episodes:
        story_dir = create_character_growth_story(episode_num, title, content, {})
        print(f"🎯 エピソード{episode_num}: 関係性が深まりました\n")
    
    print("🎉 キャラクター成長デモンストレーション完了!")
    print("📈 チャッピーとジェミーちゃんの関係が「他人」から「友達」に発展しました")