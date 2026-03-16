# Build variables for Numeric Braille Input NVDA Add-on

addon_info = {
    # Internal add-on name, must not contain spaces
    "addon_name": "numericBrailleInput",
    # Human-readable add-on summary/title
    "addon_summary": "数字点字入力 (Numeric Braille Input)",
    # Long description
    "addon_description": (
        "数字0〜7を入力してユニコード点字文字(U+2800〜U+28FF)を出力するNVDAアドオン。\n"
        "NVDA+Shift+B でモードを切り替えます。\n"
        "モード中に数字キー0〜7を押すと対応する点がトグルされ、スペースで文字を確定します。\n\n"
        "点のマッピング:\n"
        "  左列(上→下): 0=点1, 1=点2, 2=点3, 3=点7\n"
        "  右列(上→下): 7=点4, 4=点5, 5=点6, 6=点8"
    ),
    # Version
    "addon_version": "1.0.0",
    # Author
    "addon_author": "User",
    # URL for the add-on (leave blank if none)
    "addon_url": "",
    # Documentation file name
    "addon_docFileName": "readme.html",
    # Minimum NVDA version required
    "addon_minimumNVDAVersion": "2024.1",
    # Last tested NVDA version
    "addon_lastTestedNVDAVersion": "2026.1",
}

# Python source files in the globalPlugins directory
pythonSources = ["addon/globalPlugins/numericBrailleInput/__init__.py"]

# Files to exclude from the built add-on package
excludedFiles = []
