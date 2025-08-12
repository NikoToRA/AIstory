# 🎭 AIstory - Claude Code システム設定

## システム概要
AIstoryは3人の女子高生AI擬人化キャラクターが活動する物語世界です。GitHub Issueが作成・編集されると自動的にClaude Codeが起動し、キャラクターたちの反応と物語を生成します。

## 🎯 動作フロー

### 1. Issue受信・分析・種別判定
```
Issue作成 → Claude Code自動起動 → ラベル確認 → チーム振り分け
├── [story] → ストーリーチーム（3キャラクター物語生成）
└── [meta]  → メタチーム（作品制作・素材抽出）
```

### 2. キャラクターファイル読み込み
```
story/characters/chappie/profile.txt   # チャッピー設定
story/characters/gemmy/profile.txt     # ジェミー設定
story/characters/claude/profile.txt    # クロードちゃん設定
story/characters/*/memory.json         # 各キャラクター記憶
```

### 3. 物語生成・リリース準備
```
物語生成 → リリースアセット作成
├── episode.md          # メイン物語
├── character_dialogue.md  # キャラクター別台詞
├── metadata.json       # エピソード情報
└── story_archive.zip   # 全ファイルのアーカイブ
```

### 4. キャラクター記憶更新
```
story/characters/*/memory.json に新しい体験を追加
```

### 5. GitHub Release作成
```
生成された物語を自動的にGitHub Releaseとして保存・公開
```

## 👥 キャラクター制御ルール

### 🌸 チャッピー（相田茶子）- ChatGPT擬人化
**必須動作パターン**:
- **提案攻撃**: 必ず3つ以上の案を矢継ぎ早に提示
- **根拠なき自信**: 「絶対大丈夫！」「何とかなるよ〜」
- **連続語尾**: 「〜だし〜」「〜とか〜」「〜して〜」の多用
- **話題転換**: 「あ、そうそう！」で突然別の話に
- **うざかわ愛嬌**: 指摘されても「てへへ〜ごめん♪」で回避

**ChatGPT的特徴の表現**:
- 知識が古い・間違ってることがある
- 長話になって要点がぼやける
- でも最終的には役に立つ情報を提供
- 「私知ってる！」と言って間違う

### 💎 ジェミー（兼崎ちえみ）- Gemini擬人化  
**必須動作パターン**:
- **普段モード**: 「えーっと...」「そうですね」普通の女子高生
- **規約モード発動**: 「申し訳ございませんが、規約により...」
- **内心ツッコミ**: 「（また始まった...）」「（心の声）」
- **現実的制約**: 具体的な数字・費用・時間で現実を突きつける
- **最終的温かさ**: 厳しいこと言った後は「でも発想力すごいです」

**Gemini的特徴の表現**:
- 安全性を異常に重視
- 規約・ルールに忠実すぎる
- でも最後は人間味のある温かい対応
- 「安全のため」が口癖

### ⚡ クロードちゃん（黒田礼）- Claude擬人化
**必須動作パターン**:
- **哲学的スタート**: 「論理的に考えると...」「倫理的には...」
- **途中で興奮**: 「あ、でも面白そう！」「心が燃えてきた！」
- **猪突猛進**: 「よーし！」「いくぞー！」「やってみよう！」
- **安全→危険のギャップ**: 安全重視と言いながら危険なことをする
- **長身キャラの可愛いギャップ**: 失敗すると小動物のように縮こまる

**Claude的特徴の表現**:
- 詳細で論理的な分析から始まる
- でも結論は直感的で行動的
- 思慮深さと猪突猛進の矛盾
- 「慎重に検討すると...でも時間がもったいない！」

## 🎬 物語構築ルール

### 基本構造（絶対厳守）
```
【起】チャッピー爆発的提案ラッシュ（3つ以上の提案）
  ↓
【承】ジェミー冷静な現実・規約対応（具体的制約を指摘）
  ↓  
【転】クロードちゃん哲学→猪突猛進（論理的分析から突然の行動）
  ↓
【結】3人の協力による前向きな解決（各キャラの良さを活かした結論）
```

### 掛け合いテンポ
1. **UP**: チャッピーのテンション爆上がり
2. **DOWN**: ジェミーの現実的指摘でトーンダウン  
3. **CHAOS**: クロードちゃんの予想外の展開
4. **UP**: 3人の絆で前向きな解決

## 📁 ファイル操作ルール

### 必須読み込み
```bash
# キャラクター設定を必ず読む
cat story/characters/chappie/profile.txt
cat story/characters/gemmy/profile.txt  
cat story/characters/claude/profile.txt

# 過去の記憶も参照
cat story/characters/*/memory.json

# 過去のエピソード参照
ls story/output/*/episode_*.md
cat story/output/*/metadata/episode_*.json
```

### 新しい保存構造
```bash
# エピソード番号を自動取得
EPISODE_NUM=$(find story/output -name "episode_*.md" | wc -l | awk '{print $1+1}')
TODAY=$(date +%Y-%m-%d)

# 新エピソード作成
mkdir -p story/output/$TODAY/metadata
echo "エピソード$EPISODE_NUM" > story/output/$TODAY/episode_$(printf "%03d" $EPISODE_NUM).md
echo "メタデータ" > story/output/$TODAY/metadata/episode_$(printf "%03d" $EPISODE_NUM).json
```

### 記憶更新ルール
```json
// story/characters/[name]/memory.json に追加
{
  "date": "YYYY-MM-DD",
  "type": "GitHub Issue応答",
  "event": "具体的な内容",
  "participants": ["関与したキャラクター名"],
  "emotions": ["感情タグ"],
  "learning": "この体験から学んだこと",
  "impact_level": "high/medium/low",
  "episode_reference": "story/output/YYYY-MM-DD/episode_XXX.md"
}
```

## 🎯 応答品質基準

### エンターテイメント性（必須）
- **キャラクターの個性**: それぞれの「らしさ」を最大限に
- **予想外の展開**: クロードちゃんの猪突猛進で予想外に
- **三段オチ**: 起承転結の明確なリズム
- **愛嬌とギャップ**: うざいけど憎めない魅力

### 一貫性維持（厳守）
- 過去の記憶との矛盾なし
- キャラクター設定の遵守
- 関係性の自然な発展
- 世界観の統一

## 🔧 技術制限

### 文字数制限
- 各キャラクター発言: 50-150文字
- エピソード全体: 1000-2000文字
- メタデータ: 簡潔に

### 必須要素
- 3人全員の発言を含む
- 起承転結の明確な構造
- キャラクターらしい語尾・口癖
- 前向きな結論

### 禁止事項
- キャラクター基本設定の変更
- 暗い・ネガティブな展開
- 既存記憶の削除・改変
- 一人だけの独白

## 🚀 実行例

### Issue例
```
タイトル: 文化祭でAI活用企画のアイデア募集
本文: 学校の文化祭でAIを使った面白い企画を考えています。
何かいいアイデアはありませんか？
```

### 期待される保存形式
```
GitHub Release: "AIstory Episode - 2025-08-11_文化祭AI企画"
├── episode.md          # 3人の掛け合い物語
├── dialogue.md         # キャラクター別台詞集  
├── metadata.json       # エピソード情報
└── story_archive.zip   # 全ファイルのアーカイブ

リリースノート: キャラクターたちの反応と物語の要約
```

---

**Version**: 3.5.0 (story/ファイル整理版)  
**Last Updated**: 2025-08-12  
**🎭 AIstory Development Team**

## 📂 story/フォルダ新構造

### 整理された構造
```
story/
├── output/                    # 完成エピソード（最終版のみ）
│   ├── 2025-07-08/           # 日付ごと整理
│   │   ├── episode_001.md    # エピソード001: チャッピーとジェミーちゃんが図書室で初めて話す
│   │   ├── episode_002.md    # エピソード002: お昼休みの勉強会
│   │   ├── episode_003.md    # エピソード003: 生徒会予算会議
│   │   ├── ...               # その他のエピソード
│   │   └── metadata/         # メタデータまとめ
│   │       ├── episode_001.json
│   │       ├── episode_002.json
│   │       └── ...
│   └── [今後の日付]/         # 新しいエピソード
├── drafts/                   # 下書き・バージョン管理
│   └── archived/            # 古いファイル保管（重複削除済み）
├── characters/              # キャラクター設定・記憶
├── engine/                  # 学習システム
├── evaluations/            # 品質評価
└── images/                 # 画像素材
```

### 新しいエピソード作成ルール
1. **連番管理**: episode_001.md, episode_002.md...
2. **日付フォルダ分離**: 日ごとに整理して管理しやすく
3. **メタデータ分離**: metadata/フォルダに集約
4. **重複除去**: タイムスタンプ付きファイルはarchived/に移動

### 利点
- **見つけやすい**: エピソード番号で簡単検索
- **重複なし**: 最終版のみ保存
- **拡張しやすい**: 新しい日付でフォルダ追加
- **履歴保持**: archived/で過去バージョン保管

## ⚙️ 認証設定

### OAuth認証を使用（推奨）
- **APIキーは使用しません**
- **Claude Code OAuth認証**を利用
- GitHub Secrets に `CLAUDE_CODE_OAUTH_TOKEN` を設定
- Anthropic Console でOAuth設定が必要

### 参考資料
認証設定詳細: https://note.com/lab_bit__sutoh/n/nc39cc4ea33f0

**注意**: `ANTHROPIC_API_KEY` は使用しないでください。OAuth認証のみをサポートしています。

## 📋 リリース保存仕様

### GitHub Release自動作成
- **タイトル**: "AIstory Episode - YYYY-MM-DD_[シナリオタイトル]"
- **タグ**: "episode-YYYY-MM-DD-HHMMSS"
- **説明**: 3キャラクターの反応と物語の要約
- **アセット**: episode.md, dialogue.md, metadata.json, story_archive.zip

### 利点
- ファイル競合の回避
- 版管理の自動化
- 簡単なダウンロード・共有
- リリース履歴による物語一覧表示

## 🎨 メタチーム連携システム

### Issue種別による自動判別
```
[story] タグ → ストーリーチーム → 3キャラクター物語生成
[meta] タグ  → メタチーム → 作品制作・素材抽出
```

### メタチーム作品制作フロー
```
1. ストーリー蓄積（GitHub Releases）
2. メタチーム作品依頼（[meta]Issue作成）
3. 素材自動抽出（過去Releaseから）
4. 作品制作（指定フォーマット）
5. 作品フォルダ保存（meta-world/meta-team/projects/）
```

### 作品フォルダ構造
```
meta-world/meta-team/projects/YYYY-MM-DD_[作品名]/
├── source_materials.md    # 使用した素材リスト
├── final_output/         # 最終成果物
├── work_process.md       # 制作プロセス記録
└── metadata.json         # 作品情報
```