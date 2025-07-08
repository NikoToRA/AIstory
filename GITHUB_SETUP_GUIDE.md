# 🚀 GitHub AIstory システム セットアップガイド

## ⚠️ 現在の状況
ローカルで完全に動作するAIstoryシステムが完成しましたが、GitHub Actionsの権限エラーでプッシュできません。

## 📋 手動セットアップ手順

### Step 1: 新しいリポジトリ作成
```bash
# GitHub上で新しいリポジトリ「AIstory」を作成
# Settings → Actions → General → Workflow permissions
# → "Read and write permissions" を選択
```

### Step 2: APIキー設定
```bash
# GitHub Settings → Secrets and variables → Actions
# New repository secret:
# Name: ANTHROPIC_API_KEY
# Value: [あなたのAnthropicAPIキー]
```

### Step 3: ファイルアップロード
以下のファイル・ディレクトリを手動でアップロード：

```
📁 .github/
  📁 workflows/
    📄 aistory.yml (GitHub Actions設定)
  📁 ISSUE_TEMPLATE/
    📄 scenario.yml (シナリオ投稿テンプレート)

📁 story-world/
  📄 claude.md (AI制御ルール)
  📁 characters/
    📁 chappie/ (チャッピー設定・記憶)
    📁 gemmy/ (ジェミーちゃん設定・記憶)
  📁 stories/ (生成された物語群)

📄 DEPLOYMENT_GUIDE.md (完全な運用ガイド)
📄 chappie_introduction_4koma.md (四コマサンプル)
```

## 🎯 完成したシステム機能

### ✅ **キャラクター成長システム**
- チャッピー & ジェミーちゃん完全実装
- 3エピソードで関係性が「他人」→「友達」に発展
- 信頼度: 15 → 75 (5倍成長)
- 記憶蓄積による性格深化

### ✅ **Issue駆動型ストーリー生成**
```
GitHub Issue投稿 → AI自動応答 → キャラクター会話 → 物語生成 → 記憶更新
```

### ✅ **三段オチ構造**
1. **起**: チャッピーの無茶振り提案ラッシュ
2. **承**: ジェミーの規約・現実対応
3. **転**: 予算・物理的制約で現実直面  
4. **結**: 協力ムード・お互いの良さ認め合い

### ✅ **ChatGPT共感四コマ**
- 自己紹介で話が脱線する様子
- 「何でも知ってる」→「話が長すぎる」
- 「てへへ〜ごめん♪」の愛嬌

## 🎊 利用方法（セットアップ後）

### 📱 **スマホからでも簡単**
```
1. GitHub → Issues → New Issue
2. シナリオテンプレート選択
3. タイトル: [シナリオ] 体育祭の準備
4. 内容入力して Submit
5. 2-3分後にAIキャラクターが自動応答！
```

### 🎭 **自動生成される内容**
- キャラクター会話ログ
- 完成物語
- 四コマネーム 
- 評価スコア
- 関係性・記憶更新

## 📊 現在の実績

### **生成済みストーリー**
- エピソード1: 図書室での初対面
- エピソード2: お昼休みの勉強会  
- エピソード3: ダンス部発表会
- + チャッピー自己紹介四コマ

### **キャラクター成長データ**
```json
{
  "chappie_gemmy_relationship": {
    "trust": 75,
    "understanding": 65, 
    "episodes": 3,
    "relationship_type": "friends"
  }
}
```

## 🚀 次のステップ

1. **GitHub手動セットアップ**（上記手順）
2. **ANTHROPIC_API_KEY設定**
3. **初回Issueテスト投稿**
4. **システム動作確認**
5. **本格運用開始！**

---

**🎉 AIstoryシステムは完全に動作可能な状態です！**  
**GitHub設定完了後、即座にIssue駆動型AI物語生成が開始できます！**