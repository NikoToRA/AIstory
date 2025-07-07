# Story World Repository Structure

## 📁 Directory Layout

```
story-world/
├── README.md                    # 世界観紹介・使い方
├── config/                      # 設定ファイル
│   ├── world_settings.yaml     # 世界背景設定
│   └── output_formats.yaml     # アウトプット形式定義
├── characters/                  # キャラクター管理
│   ├── alice/
│   │   ├── profile.yaml        # 基本設定（性格・背景）
│   │   ├── memory.json         # 経験・記憶ログ
│   │   ├── relationships.json  # 他キャラとの関係値
│   │   └── growth.json         # 成長・変化記録
│   └── bob/
│       ├── profile.yaml
│       ├── memory.json
│       ├── relationships.json
│       └── growth.json
├── scenarios/                   # シナリオ・シチュエーション
│   ├── templates/              # テンプレート
│   │   ├── school_life.yaml
│   │   └── adventure.yaml
│   └── active/                 # 実行中シナリオ
│       └── current_episode.yaml
├── stories/                    # 生成されたコンテンツ
│   ├── 2024-01-01_cultural_festival/
│   │   ├── discussion.md       # キャラ間ディスカッション
│   │   ├── 4koma.png          # 四コマ漫画
│   │   ├── script.json        # 生成スクリプト
│   │   └── metadata.yaml      # メタデータ
│   └── 2024-01-02_sports_day/
├── engine/                     # 物語生成エンジン
│   ├── core/
│   │   ├── character_ai.py    # キャラクターAI
│   │   ├── memory_manager.py  # 記憶管理
│   │   ├── relationship.py    # 関係性管理
│   │   └── story_generator.py # 物語生成
│   ├── renderers/
│   │   ├── 4koma_renderer.py  # 四コマ生成
│   │   ├── novel_renderer.py  # 小説生成
│   │   └── image_renderer.py  # イラスト生成
│   └── utils/
│       ├── entertainment.py   # 面白さ評価
│       └── quality_check.py   # 品質チェック
├── assets/                     # リソース
│   ├── images/                # 背景・素材画像
│   ├── fonts/                 # フォント
│   └── templates/             # レイアウトテンプレート
└── logs/                      # システムログ
    ├── character_actions.log  # キャラ行動ログ
    └── generation_history.log # 生成履歴
```

## 🎭 重要ポイント

### エンターテイメント性担保
- `engine/utils/entertainment.py` - 面白さスコアリング
- キャラクター間の化学反応重視
- オチ・笑い・感動の自動検出

### 人間観察者向け設計
- `stories/` - 読みやすい形式で保存
- 生成過程も透明化（discussion.md）
- メタデータで品質・面白さ可視化