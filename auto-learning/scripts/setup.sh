#!/bin/bash
# 🤖 Chappie Auto Learning System Setup Script

echo "🤖 Setting up Chappie Auto Learning System..."

# Python実行権限を付与
chmod +x auto-learning/scripts/auto_learn.py

# テスト用の画像フォルダを作成
mkdir -p auto-learning/new-images
mkdir -p auto-learning/processed

# .gitignore を更新（大きな画像ファイルを除外）
cat >> .gitignore << 'EOF'

# Auto Learning System
auto-learning/new-images/*.png
auto-learning/new-images/*.jpg
auto-learning/new-images/*.jpeg
auto-learning/processed/*/
EOF

echo "✅ Setup completed!"
echo ""
echo "🔧 Next steps:"
echo "1. Go to GitHub repository Settings > Secrets and variables > Actions"
echo "2. Add a new secret: ANTHROPIC_API_KEY"
echo "3. Set your Claude API key as the value"
echo "4. Push this code to GitHub"
echo "5. Put new images in auto-learning/new-images/ and push to trigger learning"
echo ""
echo "🚀 Ready to use!"