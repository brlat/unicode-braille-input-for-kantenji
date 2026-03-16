#!/usr/bin/env python3
"""
NVDAアドオンパッケージ(.nvda-addon)をビルドするスクリプト。

使い方:
    python build.py

出力: numericBrailleInput-1.0.0.nvda-addon
"""
import os
import zipfile

ADDON_DIR = os.path.join(os.path.dirname(__file__), "addon")
OUTPUT_NAME = "numericBrailleInput-1.0.0.nvda-addon"


def build():
    output_path = os.path.join(os.path.dirname(__file__), OUTPUT_NAME)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(ADDON_DIR):
            # __pycache__ を除外
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for file in files:
                if file.endswith(".pyc"):
                    continue
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, ADDON_DIR)
                zf.write(full_path, arcname)
                print(f"  追加: {arcname}")
    print(f"\nビルド完了: {output_path}")


if __name__ == "__main__":
    build()
