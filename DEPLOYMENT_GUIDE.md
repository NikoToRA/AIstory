# 🚀 GitHub Issue キャラクター自動会話システム 稼働ガイド

## 📋 現在の準備状況

### ✅ **完成済み**
- [x] GitHub Actions ワークフロー (`.github/workflows/aistory.yml`)
- [x] キャラクター設定 (`characters/*/profile.txt`)
- [x] AI制御ルール (`claude.md`)
- [x] Issue テンプレート (`.github/ISSUE_TEMPLATE/scenario.yml`)
- [x] 評価システム (`evaluations/`)
- [x] ローカルテスト成功

### 🔧 **残り設定項目**
- [ ] GitHub Secrets 設定
- [ ] GitHub Actions 権限設定  
- [ ] 本番テスト実行

## 🔑 **GitHub Secrets 設定手順**

### Step 1: Anthropic API Key 取得
1. https://console.anthropic.com にアクセス
2. API Keys セクション
3. 新しいキーを作成・コピー

### Step 2: GitHub Secrets 設定
```
リポジトリ → Settings → Secrets and variables → Actions
+ New repository secret

Name: ANTHROPIC_API_KEY
Secret: [取得したAPIキー]
```

## ⚙️ **GitHub Actions 権限設定**

### Step 1: Actions 権限有効化
```
リポジトリ → Settings → Actions → General
→ "Allow all actions and reusable workflows" 選択
```

### Step 2: トークン権限設定
```
Settings → Actions → General → Workflow permissions
→ "Read and write permissions" 選択
→ "Allow GitHub Actions to create and approve pull requests" チェック
```

## 🎯 **稼働テスト手順**

### Phase 1: 基本動作テスト
```
1. Issue テンプレートでシナリオ投稿
2. GitHub Actions 起動確認
3. エラーログチェック
4. キャラクターコメント生成確認
```

### Phase 2: 完全フロー テスト
```
1. シナリオ投稿
2. キャラクター会話生成
3. 物語ファイル作成
4. 評価スコア表示
5. 昇格判定システム
```

## 📱 **ユーザー体験フロー**

### 🎭 **シナリオ投稿**
```
スマホ → GitHub → New Issue → シナリオテンプレート選択
タイトル: [シナリオ] 体育祭の準備
内容: チャッピーとジェミーちゃんが体育祭の準備で協力
```

### 💬 **自動キャラクター反応**
```
2-3分後：
🎭 チャッピー（BOT）:
「体育祭〜！やば〜い、超楽しそうじゃん！
ジェミーちゃんも一緒にやろうよ〜♪」

🎭 ジェミーちゃん（BOT）:
「体育祭の準備ですね。効率的に進めましょう。
役割分担を明確にした方が良いかと...」

🎭 チャッピー（BOT）:
「え〜役割分担って〜？私はダンス系担当で〜」

🎭 ジェミーちゃん（BOT）:
「申し訳ございませんが、規約により適切な
役割分担が必要です。まず計画を...」

🎭 チャッピー（BOT）:
「あ、またジェミーちゃんの規約モード出た〜！
でも頼りになるよね♪」
```

### 📊 **自動評価・物語生成**
```
5分後：
🤖 AIstory System:
📖 物語完成！
📊 AI評価: 82/100
🎪 面白さ: 85/100 
💬 会話品質: 79/100
🚀 昇格候補！👍で投票してください

📁 生成ファイル:
- stories/2024-01-08_sports_festival/discussion.md
- stories/2024-01-08_sports_festival/story.md
- stories/2024-01-08_sports_festival/metadata.json
```

## 🔄 **継続運用**

### 📈 **学習・改善サイクル**
```
1. ユーザー評価収集
2. 評価データ分析  
3. キャラクター設定調整
4. 物語品質向上
5. 新キャラクター追加
```

### 📱 **スマホ最適化**
- Issue テンプレートはスマホで入力しやすい設計
- 生成物語もスマホで読みやすい
- GitHub モバイルアプリ完全対応

## 🚨 **注意事項**

### 🔐 **セキュリティ**
- API キーは絶対に公開しない
- GitHub Secrets で安全に管理
- 定期的なキー更新推奨

### 💰 **API使用量**
- Claude API は従量課金
- 1物語あたり約$0.01-0.05
- 月間使用量監視推奨

### 📊 **品質管理**
- 自動評価 + ユーザー評価の二重チェック
- 不適切コンテンツ防止機能
- 定期的な設定見直し

## 🎯 **稼働開始準備完了チェックリスト**

- [ ] ANTHROPIC_API_KEY 設定済み
- [ ] GitHub Actions 権限設定済み
- [ ] Issue テンプレート動作確認済み
- [ ] キャラクター設定最終確認済み
- [ ] 評価システム動作確認済み

**✅ 全項目完了後、即座に本格稼働可能！**

---

## 🎊 **稼働後の世界**

### 📱 **いつでもどこでも**
```
電車内 → スマホでシナリオ投稿
仕事中 → 昼休みにキャラクター会話確認
家で → 完成した物語を楽しむ
```

### 🎭 **成長するキャラクター**
```
初期: ぎこちない会話
1週間後: 自然な掛け合い
1ヶ月後: 深い関係性・複雑な物語
3ヶ月後: ユーザー好みを学習した最適化
```

### 🌍 **拡張する世界**
```
追加可能なキャラクター：
- クロード先輩（哲学系）
- ノーション（計画系）
- キャンバ（デザイン系）
- パワポ先生（プレゼン系）
```

**🚀 GitHub Issue → AIキャラクター自動会話システム、完全実現可能です！**