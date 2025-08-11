#!/usr/bin/env python3
"""
🧪 Local Test Script for Chappie Auto Learning
ローカルでテスト実行するためのスクリプト
"""

import os
import sys
from pathlib import Path

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(str(Path(__file__).parent.parent.parent))

from auto_learn import ChappieAutoLearner

def test_local():
    """ローカルテスト実行"""
    print("🧪 Starting local test of Chappie Auto Learning System...")
    
    # 環境変数チェック
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable is not set")
        print("💡 Set it with: export ANTHROPIC_API_KEY='your-api-key'")
        return False
    
    try:
        learner = ChappieAutoLearner()
        print("✅ ChappieAutoLearner initialized successfully")
        
        # 新しい画像があるかチェック
        image_files = list(learner.new_images_path.glob('*.png')) + \\
                     list(learner.new_images_path.glob('*.jpg')) + \\
                     list(learner.new_images_path.glob('*.jpeg'))
        
        if not image_files:
            print("📭 No test images found in auto-learning/new-images/")
            print("💡 Add some test images to auto-learning/new-images/ folder")
            return False
        
        print(f"📸 Found {len(image_files)} test images")
        
        # 学習を実行
        success = learner.process_new_images()
        
        if success:
            print("🎉 Local test completed successfully!")
            print("✅ Character profile and memory should be updated")
            return True
        else:
            print("❌ Local test failed - no updates were made")
            return False
            
    except Exception as e:
        print(f"💥 Local test error: {e}")
        return False

if __name__ == "__main__":
    success = test_local()
    exit(0 if success else 1)