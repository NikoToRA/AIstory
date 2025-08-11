#!/usr/bin/env python3
"""
AIstory Image Management System
画像をストーリー保存庫に保存・管理するシステム
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import hashlib

class ImageManager:
    def __init__(self):
        self.base_path = Path("story-world/images")
        self.base_path.mkdir(exist_ok=True)
    
    def save_image(self, image_path: str, title: str, description: str = "", tags: list = None) -> dict:
        """
        画像をストーリー保存庫に保存
        
        Args:
            image_path: 保存したい画像のパス
            title: 画像のタイトル
            description: 画像の説明
            tags: タグリスト
            
        Returns:
            保存された画像の情報
        """
        if tags is None:
            tags = []
            
        # タイムスタンプ付きフォルダ名生成
        timestamp = datetime.now().strftime("%Y-%m-%d")
        safe_title = self._sanitize_filename(title)
        folder_name = f"{timestamp}_{safe_title}"
        
        # 保存先ディレクトリ作成
        save_dir = self.base_path / folder_name
        save_dir.mkdir(exist_ok=True)
        
        # 画像ファイルコピー
        image_source = Path(image_path)
        if not image_source.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
            
        original_filename = f"original{image_source.suffix}"
        save_path = save_dir / original_filename
        shutil.copy2(image_source, save_path)
        
        # ファイルハッシュ計算
        file_hash = self._calculate_hash(save_path)
        
        # メタデータ作成
        metadata = {
            "title": title,
            "description": description,
            "tags": tags,
            "original_filename": image_source.name,
            "saved_filename": original_filename,
            "file_hash": file_hash,
            "created_at": datetime.now().isoformat(),
            "folder_path": str(save_dir.relative_to(Path("."))),
            "file_size": save_path.stat().st_size
        }
        
        # メタデータ保存
        metadata_path = save_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 画像が保存されました: {save_dir}")
        return metadata
    
    def list_images(self) -> list:
        """保存された画像一覧を取得"""
        images = []
        for folder in self.base_path.iterdir():
            if folder.is_dir():
                metadata_path = folder / "metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        images.append(metadata)
        return sorted(images, key=lambda x: x['created_at'], reverse=True)
    
    def find_images_by_tag(self, tag: str) -> list:
        """タグで画像を検索"""
        all_images = self.list_images()
        return [img for img in all_images if tag in img.get('tags', [])]
    
    def _sanitize_filename(self, filename: str) -> str:
        """ファイル名に使用できない文字を削除"""
        import re
        safe_name = re.sub(r'[^\w\-_\.]', '_', filename)
        return safe_name[:50]  # 長すぎる場合は切り詰め
    
    def _calculate_hash(self, file_path: Path) -> str:
        """ファイルのMD5ハッシュを計算"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

# 使用例
if __name__ == "__main__":
    manager = ImageManager()
    
    # 使用方法の表示
    print("🖼️  AIstory Image Manager")
    print("使用方法:")
    print("manager.save_image('path/to/image.png', 'タイトル', '説明', ['タグ1', 'タグ2'])")
    print("manager.list_images() # 全画像一覧")
    print("manager.find_images_by_tag('タグ名') # タグ検索")