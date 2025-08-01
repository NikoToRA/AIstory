# AIstory ワークフロー設計

## 🎯 Issue完結→選別昇格システム

### フェーズ1: Issue完結型ストーリー生成

#### 1️⃣ ユーザー投稿
```
GitHub Issue作成
├── タイトル: [シナリオ] 文化祭の準備
├── ラベル: scenario
└── 内容: シチュエーション詳細
```

#### 2️⃣ 自動キャラクター反応
```
GitHub Actions起動
├── キャラ分析: チャッピー・ジェミーちゃんが反応
├── 会話生成: Issue内でコメント形式での議論
├── 物語構築: 起承転結のテキスト物語
└── 記憶更新: キャラクター経験として保存
```

#### 3️⃣ 成果物生成
```
stories/[日付]_[タイトル]/
├── discussion.md     # キャラクター会話ログ
├── story.md         # 完成物語（テキスト）
├── metadata.yaml    # 面白さスコア・評価
└── characters_after.json # 更新された記憶
```

### フェーズ2: 品質評価・選別システム

#### 🏆 自動評価基準
```yaml
評価項目:
  entertainment_score: 0-100 # 面白さ
  character_consistency: 0-100 # キャラ一貫性
  story_structure: 0-100 # 物語構成
  dialogue_quality: 0-100 # 会話品質
  
昇格条件:
  総合スコア: 70以上
  特に面白さ: 80以上
```

#### 🎖️ ユーザー評価
```
GitHub Reactions活用:
👍 面白い (promotion候補)
❤️ 超面白い (即昇格)
🚀 次のステップへ (昇格確定)
```

### フェーズ3: 昇格・ネーム化システム

#### 📝 昇格トリガー
1. **自動昇格**: スコア80以上 + 👍3個以上
2. **手動昇格**: ユーザーが🚀リアクション
3. **特別昇格**: ❤️リアクション2個以上

#### 🎨 ネーム作成プロセス
```
昇格物語
├── ネーム化Issue自動作成
├── セリフ・コマ割り生成
├── 場面描写・構図指示
└── 4コマネーム完成

成果物:
├── 4koma_name.md    # ネーム（セリフ+場面）
├── visual_notes.md  # 作画指示
└── promotion_log.md # 昇格履歴
```

## 🔄 具体的フロー例

### ステップ1: Issue投稿
```
[シナリオ] チャッピーとジェミーが図書室で出会う
```

### ステップ2: キャラ反応
```
チャッピー: 「あ、ジェミーじゃん！何してるの？」
ジェミー: 「申し訳ございません、規約により静粛にお願いします」
チャッピー: 「え〜、マジで？つまんな〜い」
```

### ステップ3: 自動評価
```
entertainment_score: 75
dialogue_quality: 85
→ 昇格候補
```

### ステップ4: ユーザー判定
```
ユーザーが👍リアクション
→ 昇格決定
```

### ステップ5: ネーム化
```
新しいIssue自動作成:
「[ネーム化] チャッピーとジェミーが図書室で出会う」

4コマネーム生成:
1コマ: 図書室、ジェミー一人で本整理
2コマ: チャッピー登場「あ、ジェミーじゃん！」  
3コマ: ジェミー「規約により〜」、チャッピー困り顔
4コマ: チャッピー「つまんな〜い」、ジェミー微笑み
```

## 🎯 実装優先度

### Phase A: 基本Issue完結システム
- [x] キャラクター設定完了
- [ ] GitHub Actions基本フロー  
- [ ] 会話生成システム
- [ ] 記憶更新システム

### Phase B: 評価・選別システム  
- [ ] 自動評価アルゴリズム
- [ ] GitHub Reactions連携
- [ ] 昇格判定システム

### Phase C: ネーム化システム
- [ ] ネーム自動生成
- [ ] 4コマ構成システム
- [ ] 作画指示生成

## 📊 成功指標

### 短期目標（1ヶ月）
- Issue投稿→会話生成: 24時間以内
- 面白い物語率: 30%以上
- ユーザー満足度: 70%以上

### 中期目標（3ヶ月）  
- 昇格率: 20%以上
- ネーム化成功率: 80%以上
- キャラクター成長実感: あり

### 長期目標（6ヶ月）
- 自動4コマ生成実現
- 複数キャラ対応
- コミュニティ形成