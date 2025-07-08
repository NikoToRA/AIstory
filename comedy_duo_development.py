#!/usr/bin/env python3
"""
チャッピー＆ジェミーちゃん コンビ育成システム
Panty & Stocking風の派手×地味コンビを目指す
"""

import json
import os
from datetime import datetime
from pathlib import Path

def create_comedy_duo_story(episode_num, scenario_title, scenario_content, dynamic_focus):
    """相棒コンビのボケツッコミストーリー生成"""
    print(f"🎭 コンビエピソード{episode_num}: {scenario_title}")
    
    # storiesディレクトリ作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    story_date = datetime.now().strftime("%Y-%m-%d")
    story_title = f"combo_ep{episode_num:02d}_{scenario_title}".replace(" ", "_").replace("　", "_")
    story_dir = Path(f"story-world/stories/{story_date}_{story_title}")
    story_dir.mkdir(parents=True, exist_ok=True)
    
    # エピソード別コンビストーリー
    if episode_num == 1:
        discussion = f"""# コンビエピソード{episode_num}: {scenario_title}

## 💬 既に相棒の二人の日常

### 💬 **チャッピー（BOT）** 5分前:
「ジェミ〜♪今日の生徒会会議どうだった〜？
あ、そうそう〜、文化祭の予算案なんだけど〜、
私めっちゃいいアイデア思いついたんだ〜♪
全校生徒でフラッシュモブとか〜、屋上にステージ作って〜」

### 💬 **ジェミーちゃん（BOT）** 4分前:
「（はぁ...）チャッピーさん、またですか...
規約第15条により、屋上でのイベント開催は
安全性の観点から禁止されております。
（心の声：いつものパターン来たな...）」

### 💬 **チャッピー（BOT）** 3分前:
「え〜規約規約って〜！でもさ、ジェミはいつも
そうやって最初は反対するけど〜、結局私のアイデア
採用してくれるじゃん〜♪去年のダンス大会も〜」

### 💬 **ジェミーちゃん（BOT）** 2分前:
「（ムッ）あ、あれは...安全対策を十分に講じた上で...
それに、チャッピーさんの案をそのまま採用したわけでは...
ちゃんと現実的に修正を...
（心の声：なんで覚えてるのよ...）」

### 💬 **チャッピー（BOT）** 1分前:
「ほら〜♪やっぱりジェミって私のこと理解してくれてる〜
てことで今回も頼む〜♪私一人じゃ絶対無理だし〜
ジェミがいないと何もできないから〜」

### 💬 **ジェミーちゃん（BOT）** たった今:
「も、もう...（ため息）分かりました...
ただし、安全基準を満たす範囲で検討します。
（小声）まったく...いつもこのパターンで...
（心の声：でも、まあ...悪い気はしない）」

## 📝 コンビダイナミクス
- **チャッピー**: 無茶振りボケ担当、相方への全幅の信頼
- **ジェミーちゃん**: 現実派ツッコミ担当、最終的に協力する

## 🎯 関係性の特徴
- 既に息の合ったコンビ
- お互いのパターンを理解済み
- 表面的には対立、実際は信頼関係
"""
    
    elif episode_num == 2:
        discussion = f"""# コンビエピソード{episode_num}: {scenario_title}

## 💬 派手と地味の完璧な掛け合い

### 💬 **チャッピー（BOT）** 5分前:
「ジェミ〜♪今度の修学旅行の自由行動なんだけど〜
私のプラン聞いて〜♪まずハロプロショップ行って〜
原宿でプリクラ撮りまくって〜、渋谷でダンス動画撮影して〜
あ、そうそう！夜は恵比寿で〜」

### 💬 **ジェミーちゃん（BOT）** 4分前:
「ちょっと待ってください！チャッピーさん！
（資料をバサバサ）修学旅行の規定では、
1日の移動範囲は半径5km以内、夜間外出は禁止、
さらに予算上限は...」

### 💬 **チャッピー（BOT）** 3分前:
「ジェミ〜そういう細かいことはさ〜、
現地で何とかなるって〜♪私の直感は当たるから〜
それより一緒に楽しもうよ〜♪ジェミも
たまには羽目外してみない？」

### 💬 **ジェミーちゃん（BOT）** 2分前:
「羽目を外す...？私が？
（心の声：この人は本当に...）
チャッピーさん、私は羽目を外したりしません！
きちんと計画を立てて、規則を守って...」

### 💬 **チャッピー（BOT）** 1分前:
「あ〜でた〜♪ジェミの生真面目モード〜
でもさ、ジェミって本当は楽しいこと好きでしょ？
前回のカラオケ、めっちゃ盛り上がってたじゃん〜♪」

### 💬 **ジェミーちゃん（BOT）** たった今:
「あ、あれは...規約の範囲内での...
（顔を赤らめる）...分かりました。
現実的なプランを立て直しますので、
少々お待ちください...
（心の声：なんで覚えてるのよ...）」

## 📝 コンビダイナミクス
- **派手チャッピー**: 自由奔放、直感型、相方を巻き込む
- **地味ジェミー**: 規則重視、計画型、でも結局付き合う

## 🎯 Panty & Stocking要素
- チャッピー ≈ Panty（派手、自由、直感的）
- ジェミー ≈ Stocking（地味、規則的、でも隠れた一面）
"""
    
    elif episode_num == 3:
        discussion = f"""# コンビエピソード{episode_num}: {scenario_title}

## 💬 完璧なボケツッコミコンビの完成

### 💬 **チャッピー（BOT）** 5分前:
「ジェミ〜♪大変大変〜！
来週のプレゼン資料、まだ全然できてない〜
でも大丈夫〜♪私に秘策があるの〜
全部アドリブで乗り切る〜♪」

### 💬 **ジェミーちゃん（BOT）** 4分前:
「は？アドリブって...
（立ち上がって）チャッピーさん！！
プレゼンテーションは事前準備が命です！
アドリブで何とかなると思ってるんですか！？」

### 💬 **チャッピー（BOT）** 3分前:
「ジェミ〜怒らないでよ〜♪
だって私、アドリブ得意だし〜
去年の生徒会選挙も〜、文化祭の司会も〜
全部その場のノリで大成功だったじゃん〜♪」

### 💬 **ジェミーちゃん（BOT）** 2分前:
「あれは...あれは私が裏で資料作って
台本書いて、スケジュール管理して...
（ため息）まったく...
いつも最後は私が尻拭いを...」

### 💬 **チャッピー（BOT）** 1分前:
「え？ジェミがそんなことしてくれてたの？
知らなかった〜♪でもさ、だからこそ
私たちって最強コンビだよね〜♪
私のセンスとジェミの実力で無敵〜♪」

### 💬 **ジェミーちゃん（BOT）** たった今:
「（はぁ...）もう...分かりました。
今回も私が何とかします。
ただし、今度は事前にちゃんと打ち合わせしましょう。
（心の声：まったく...でも、この人がいると
なんだかんだ楽しいのよね...）」

## 📝 完成したコンビダイナミクス
- **チャッピー（ボケ）**: 自由奔放、相方への全幅の信頼
- **ジェミー（ツッコミ）**: 尻拭い役、でも認め合う関係

## 🎯 理想的なパートナーシップ
- お互いの役割を理解
- 表面的な対立、深い信頼
- 完璧な補完関係
- Panty & Stocking的な距離感完成
"""
    
    # 記憶更新（コンビとしての絆を蓄積）
    try:
        with open("story-world/characters/chappie/memory.json", "r", encoding="utf-8") as f:
            chappie_memory = json.load(f)
    except FileNotFoundError:
        chappie_memory = {"experiences": [], "relationships": {}, "combo_dynamics": []}
    
    try:
        with open("story-world/characters/gemmy/memory.json", "r", encoding="utf-8") as f:
            gemmy_memory = json.load(f)
    except FileNotFoundError:
        gemmy_memory = {"experiences": [], "relationships": {}, "combo_dynamics": []}
    
    # コンビダイナミクス記録
    if episode_num == 1:
        chappie_memory["combo_dynamics"] = [{
            "partner": "ジェミーちゃん",
            "role": "ボケ担当",
            "trust_level": 85,
            "understanding": "ジェミは最初反対するけど最後は協力してくれる",
            "dependency": "ジェミがいないと何もできない"
        }]
        
        gemmy_memory["combo_dynamics"] = [{
            "partner": "チャッピー",
            "role": "ツッコミ担当", 
            "trust_level": 80,
            "understanding": "無茶なことを言うけど悪気はない",
            "responsibility": "結局私が尻拭いをする"
        }]
        
    elif episode_num == 2:
        chappie_memory["combo_dynamics"][0].update({
            "trust_level": 90,
            "understanding": "ジェミは規則重視だけど実は楽しいこと好き",
            "manipulation_skill": "ジェミの過去を持ち出して説得"
        })
        
        gemmy_memory["combo_dynamics"][0].update({
            "trust_level": 85,
            "understanding": "私の弱点を覚えててずるい",
            "resignation": "結局付き合ってしまう自分"
        })
        
    elif episode_num == 3:
        chappie_memory["combo_dynamics"][0].update({
            "trust_level": 95,
            "understanding": "ジェミが裏で全部支えてくれてる",
            "appreciation": "最強コンビ、ジェミは最高のパートナー"
        })
        
        gemmy_memory["combo_dynamics"][0].update({
            "trust_level": 90,
            "understanding": "この人といると楽しい、認め合う関係",
            "acceptance": "尻拭いも悪くない"
        })
    
    # ファイル保存
    with open(story_dir / f"discussion_{timestamp}.md", "w", encoding="utf-8") as f:
        f.write(discussion)
    
    # 記憶更新
    with open("story-world/characters/chappie/memory.json", "w", encoding="utf-8") as f:
        json.dump(chappie_memory, f, indent=2, ensure_ascii=False)
    
    with open("story-world/characters/gemmy/memory.json", "w", encoding="utf-8") as f:
        json.dump(gemmy_memory, f, indent=2, ensure_ascii=False)
    
    print(f"✅ コンビエピソード{episode_num}完了!")
    print(f"📁 保存先: {story_dir}")
    
    return story_dir

if __name__ == "__main__":
    # 3エピソードでコンビ関係を完成させる
    episodes = [
        (1, "生徒会予算会議", "チャッピーの無茶振りをジェミーが現実的に調整"),
        (2, "修学旅行計画", "派手と地味の価値観対立から理解へ"),
        (3, "プレゼン準備", "完璧なボケツッコミコンビの完成")
    ]
    
    for episode_num, title, content in episodes:
        story_dir = create_comedy_duo_story(episode_num, title, content, {})
        print(f"🎯 エピソード{episode_num}: コンビの絆が深まりました\n")
    
    print("🎉 Panty & Stocking風コンビ育成完了!")
    print("📈 派手チャッピー×地味ジェミーの完璧なパートナーシップが実現！")