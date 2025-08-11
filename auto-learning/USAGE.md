# 🤖 チャッピーちゃん自動学習システム 使用ガイド

## 🚀 クイックスタート

### 1. 初回セットアップ

```bash
# セットアップスクリプトを実行
./auto-learning/scripts/setup.sh
```

### 2. GitHub Secrets設定

1. GitHubリポジトリページで `Settings` → `Secrets and variables` → `Actions` に移動
2. `New repository secret` をクリック
3. `Name`: `ANTHROPIC_API_KEY`
4. `Secret`: あなたのClaude APIキーを入力

### 3. 使用方法

**超簡単！3ステップ：**

1. **画像を置く**: `auto-learning/new-images/` フォルダに新しい4コマ画像を保存
2. **GitHubにpush**: 変更をコミット＆プッシュ
3. **自動実行**: GitHub Actionsが自動でチャッピーちゃんを学習させる

```bash
# 例: 新しい画像を追加
cp ~/Desktop/新しい4コマ.png auto-learning/new-images/
git add .
git commit -m "Add new 4-koma for Chappie learning"
git push
```

## 🔄 自動化の流れ

```
新画像追加 → Push → GitHub Actions起動 → 画像分析 → キャラ更新 → コミット
    ↓           ↓           ↓            ↓         ↓        ↓
  📸画像      🚀自動      🤖Claude      📊分析    ✍️更新   💾保存
```

## 📁 ファイル構造

```
auto-learning/
├── new-images/              # 🆕 ここに新画像を置く
├── processed/               # ✅ 処理済み画像の保管場所
├── scripts/
│   ├── auto_learn.py       # 🧠 メイン学習スクリプト
│   ├── test_local.py       # 🧪 ローカルテスト用
│   └── setup.sh           # 🔧 セットアップスクリプト
└── README.md              # 📖 システム概要
```

## 🧪 ローカルテスト

本番前にローカルでテストできます：

```bash
# APIキーを設定
export ANTHROPIC_API_KEY="your-api-key-here"

# テスト画像をnew-images/フォルダに追加
cp test-image.png auto-learning/new-images/

# ローカルテスト実行
python auto-learning/scripts/test_local.py
```

## 📊 何が自動更新される？

### ✅ キャラクタープロファイル (`story-world/characters/chappie/profile.txt`)
- 新しいセリフパターンを追加
- キャラクター特徴を拡張
- 語尾や表現の傾向を学習

### ✅ キャラクターメモリ (`story-world/characters/chappie/memory.json`)
- 新しい体験を記録
- 感情的な成長を追跡
- 学習履歴を蓄積

## 🔍 処理結果の確認

### GitHub Actionsログで確認
1. GitHubリポジトリの `Actions` タブを開く
2. 最新の `Chappie Auto Learning System` ワークフローをクリック
3. 実行ログで処理状況を確認

### 自動コミットメッセージ
成功すると以下のようなコミットが自動作成されます：
```
🤖 Auto-update: Chappie character learned from new images

- Processed new 4-koma manga images
- Updated character profile and memory  
- Enhanced dialogue patterns and personality traits

🎭 Generated with Chappie Auto Learning System
```

## 🛠️ トラブルシューティング

### ❌ ワークフローが実行されない
- `ANTHROPIC_API_KEY` secretが正しく設定されているか確認
- `auto-learning/new-images/` に画像ファイルが入っているか確認

### ❌ 画像分析が失敗する
- 画像ファイルが破損していないか確認
- ファイル形式がPNG/JPG/JPEGか確認

### ❌ キャラクター更新が反映されない
- GitHub Actionsの実行権限が正しく設定されているか確認
- `GITHUB_TOKEN` の権限を確認

## 🎯 Tips

### 効果的な学習のために
- **高品質な画像**を使用する
- **テキストが読みやすい**4コマを選ぶ  
- **新しいセリフパターン**が含まれる作品を優先

### バッチ処理
複数の画像を一度に処理したい場合：
```bash
# 複数画像を一度にコピー
cp ~/Desktop/4koma-batch/*.png auto-learning/new-images/
git add . && git commit -m "Batch learning: multiple 4-koma images" && git push
```

## 🎉 完成！

これで **画像をフォルダに入れてpushするだけ** でチャッピーちゃんが自動的に学習・成長する システムの完成です！

**もうターミナル操作は不要！ブラウザだけでOK！** 🎊