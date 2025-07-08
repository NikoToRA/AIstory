# 評価蓄積システム

## 📊 評価データ構造

### story_evaluations.json
```json
{
  "stories": [
    {
      "story_id": "2024-01-08_cultural_festival",
      "issue_number": 1,
      "creation_date": "2024-01-08T10:00:00Z",
      "ai_evaluation": {
        "entertainment_score": 85,
        "dialogue_quality": 78,
        "character_consistency": 92,
        "story_structure": 80,
        "total_score": 83.75
      },
      "user_evaluation": {
        "rating": 8,
        "feedback": "キャラクターの掛け合いが面白い",
        "evaluation_date": "2024-01-08T15:30:00Z"
      },
      "final_status": "promoted_to_manga",
      "learning_points": [
        "チャッピーのギャル語が効果的",
        "ジェミーとの対比が良い",
        "オチが予想外で面白い"
      ]
    }
  ],
  "evaluation_history": [
    {
      "date": "2024-01-08",
      "total_stories": 1,
      "average_ai_score": 83.75,
      "average_user_rating": 8.0,
      "promotion_rate": 100
    }
  ]
}
```

## 🎯 評価基準・学習項目

### AI評価項目 (自動)
- **entertainment_score**: 0-100 面白さ
- **dialogue_quality**: 0-100 会話品質
- **character_consistency**: 0-100 キャラ一貫性
- **story_structure**: 0-100 物語構成

### ユーザー評価 (10段階)
- **1-2**: つまらない (改善必要)
- **3-4**: 普通以下 (要調整)
- **5-6**: 普通 (平均的)
- **7-8**: 面白い (昇格候補)
- **9-10**: 非常に面白い (確実昇格)

## 🧠 学習・改善システム

### 評価パターン分析
```yaml
高評価の特徴:
  - チャッピーのギャル語使用率: 高
  - キャラ対比度: 強
  - オチの意外性: あり
  - 会話テンポ: 良い

低評価の特徴:
  - 長すぎる説明: あり
  - キャラ崩壊: あり
  - オチなし: あり
  - 会話が不自然: あり
```

### 改善指針生成
```yaml
次回改善点:
  - チャッピーのうざかわ要素強化
  - ジェミーの融通利かなさ強調
  - オチを必ず入れる
  - 会話のテンポアップ
```