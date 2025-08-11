# 🤖 チャッピーちゃん自動学習システム

## 概要
新しい4コマ漫画画像が追加されると、自動的にテキストを抽出してチャッピーちゃんのキャラクター設定を更新するシステム

## 使用方法
1. `auto-learning/new-images/` フォルダに新しい画像を保存
2. GitHubにpushすると自動実行
3. キャラクター設定が自動更新されPRが作成される

## ディレクトリ構造
```
auto-learning/
├── new-images/          # 新しい画像を置くフォルダ
├── processed/           # 処理済み画像の移動先
├── scripts/             # 自動処理スクリプト
└── .github/workflows/   # GitHub Actions設定
```

## セットアップ手順
1. GitHub Secretsに Claude API キーを設定
2. 必要な権限を付与
3. ワークフローを有効化