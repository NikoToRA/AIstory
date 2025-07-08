#!/usr/bin/env python3
"""
AIstory 手動テストスクリプト
Claude Code から実行してローカルテストを行う
"""

import os
import json
from datetime import datetime
from pathlib import Path

def create_test_story(scenario_title, scenario_content):
    """テスト用物語生成"""
    print(f"🎭 物語生成開始: {scenario_title}")
    
    # storiesディレクトリ作成（タイムスタンプ付き）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    story_date = datetime.now().strftime("%Y-%m-%d")
    story_title = scenario_title.replace(" ", "_").replace("　", "_")
    story_dir = Path(f"story-world/stories/{story_date}_{story_title}")
    story_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 ストーリーディレクトリ作成: {story_dir}")
    
    # キャラクター設定読み込み
    with open("story-world/characters/chappie/profile.txt", "r", encoding="utf-8") as f:
        chappie_profile = f.read()
    
    with open("story-world/characters/gemmy/profile.txt", "r", encoding="utf-8") as f:
        gemmy_profile = f.read()
    
    print("📖 キャラクター設定読み込み完了")
    
    # 改善版キャラクター会話生成（三段オチ構造）
    discussion = f"""# {scenario_title} - キャラクター会話ログ

## 参加キャラクター
- チャッピー（相田茶子）
- ジェミーちゃん（兼崎ちえみ）

## 会話内容

### 💬 **チャッピー（BOT）** 3分前:
「あー、図書室って久しぶり〜！ジェミーちゃんじゃん！  
ねえねえ、勉強道具も色々揃えてさ〜参考書も買ったし〜  
あ、そうそう！ダンス部の子達とも一緒に勉強会やろうって話してて〜  
図書室も借りれるし、カフェも近いし〜♪」

### 💬 **ジェミーちゃん（BOT）** 2分前:
「えーっと...チャッピーさん、それは...  
（心の声：また始まった...）  
申し訳ございませんが、規約により図書室の団体利用は  
事前申請と責任者の承認が必要となっております...」

### 💬 **チャッピー（BOT）** 1分前:
「え〜規約って〜！でも大丈夫大丈夫〜♪  
私が図書委員会に直談判すれば特別許可もらえるって〜  
それに予算も私のバイト代で何とかするし〜  
みんな絶対楽しく勉強できるよ〜？」

### 💬 **ジェミーちゃん（BOT）** 30秒前:
「えーっと...その...現実的に考えると...  
（小声で）図書室定員は最大20名、団体利用は2週間前申請...  
カフェ利用も1人500円×人数分の予算が...  
あの、チャッピーさん？もう少し計画的に...」

### 💬 **チャッピー（BOT）** 10秒前:
「あれ？ジェミーちゃんの顔青くない？  
え、マジで無理なの？てへへ〜ごめんごめん♪  
じゃあジェミーちゃんが現実的なプラン考えてよ〜  
私のアイデア力とジェミーちゃんの計画力で最強じゃない？」

### 💬 **ジェミーちゃん（BOT）** たった今:
「は、はい...（ホッ）まずは少人数から始めましょうか...  
でも...チャッピーさんの発想力は...すごいですね...  
（小声）私には思いつかないような...」

## 物語の結末
チャッピーの無茶振り提案から始まった会話が、ジェミーの現実的な指摘を経て、お互いの良さを認め合う協力関係へと発展していった。
"""
    
    # 完成物語生成
    story = f"""# {scenario_title}

## あらすじ
{scenario_content}

## 物語

放課後の図書室は、いつもより静かだった。ジェミーちゃんこと兼崎ちえみは、図書委員の仕事として本の整理に集中していた。規則正しく、黙々と作業を進める彼女の前に、突然現れたのは—

「あー、図書室って久しぶり〜！」

ダンス部の練習帰りなのか、少し汗ばんだチャッピーこと相田茶子が、その特徴的な茶髪をひらりと揺らしながら入ってきた。

「ジェミーちゃんじゃん！何してるの？」

ジェミーは振り返ると、眉をひそめて答えた。

「申し訳ございません、図書室では静粛にお願いいたします。現在、規定に基づく図書整理作業を実施中です。」

「え〜マジで？そんなかたくならなくても〜」チャッピーは苦笑いを浮かべた。「私も勉強しに来たんだって！友達の宿題手伝いなんだけどさ、何かいい資料知らない？」

ジェミーの表情が少し和らいだ。

「宿題の内容を確認いたします。どちらの科目でしょうか？適切な参考資料をご案内いたします。」

「やば〜い、ジェミーちゃんって結構優しいじゃん！」チャッピーは目を輝かせた。「てっきり近寄りがたい子だと思ってた〜」

「...図書委員として、利用者支援は重要な職務です。規約第3条に明記されております。」

そんなジェミーの真面目な返答に、チャッピーはくすりと笑った。

「規約って...でもさ、今度一緒にお昼食べない？いろいろ教えて欲しいし！」

ジェミーは少し戸惑ったような表情を見せた後、小さく頷いた。

「...検討いたします。まずは現在の作業を完了させていただきます。」

図書室での偶然の出会いから、正反対な二人の新しい関係が始まろうとしていた。
"""
    
    # AI評価（模擬）
    ai_evaluation = {
        "entertainment_score": 78,
        "dialogue_quality": 85,
        "character_consistency": 92,
        "story_structure": 80,
        "total_score": 83.75
    }
    
    # メタデータ
    metadata = {
        "title": scenario_title,
        "creation_date": datetime.now().isoformat(),
        "characters": ["チャッピー", "ジェミーちゃん"],
        "scene": "図書室",
        "ai_evaluation": ai_evaluation,
        "status": "completed",
        "word_count": len(story)
    }
    
    # ファイル保存（タイムスタンプ付き）
    with open(story_dir / f"discussion_{timestamp}.md", "w", encoding="utf-8") as f:
        f.write(discussion)
    
    with open(story_dir / f"story_{timestamp}.md", "w", encoding="utf-8") as f:
        f.write(story)
    
    with open(story_dir / f"metadata_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 物語生成完了!")
    print(f"📁 保存先: {story_dir}")
    print(f"📊 AI評価スコア: {ai_evaluation['total_score']}/100")
    print("\n📝 Cursorで以下を確認してください:")
    print(f"  - {story_dir}/discussion.md  (キャラクター会話)")
    print(f"  - {story_dir}/story.md       (完成物語)")
    print(f"  - {story_dir}/metadata.json  (評価データ)")
    
    return story_dir, ai_evaluation

if __name__ == "__main__":
    # テストシナリオ実行
    scenario = "チャッピーとジェミーちゃんが図書室で初めて話す"
    content = "放課後の図書室で、正反対な二人が初めてちゃんと会話する"
    
    story_dir, evaluation = create_test_story(scenario, content)
    
    print("\n🎯 次のステップ:")
    print("1. Cursorでstoriesフォルダを確認")
    print("2. 生成された物語を読んで評価")
    print("3. Claude Codeで改善指示を出す")