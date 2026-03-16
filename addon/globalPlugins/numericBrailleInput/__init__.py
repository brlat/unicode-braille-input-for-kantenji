# -*- coding: utf-8 -*-
# Numeric Braille Input NVDA Add-on
#
# 数字0〜7をキー入力して、対応するユニコード点字文字をクリップボードにコピーするアドオン。
#
# ユーザー定義の点番号マッピング:
#   左列(上→下): 0=点1, 1=点2, 2=点3, 3=点7
#   右列(上→下): 7=点4, 4=点5, 5=点6, 6=点8
#
# 使い方:
#   NVDA+Shift+W で数字点字入力モードのオン/オフを切り替え。
#   モード中は数字キー 0〜7 を押すと対応する点がトグルされる(アプリへは入力されない)。
#   スペースキーを押すとユニコード点字文字をクリップボードにコピーしてバッファをクリア。
#   その後 Ctrl+V で任意のアプリに貼り付けができる。
#   Escキーでバッファをクリア(クリップボードは変化しない)。

from __future__ import annotations

import globalPluginHandler
import api
import ui
from scriptHandler import script


# ユニコード点字ベースコードポイント
BRAILLE_BASE = 0x2800

# ユーザー数字 → ユニコード点字ビット値のマッピング
# ユニコード点字ビット: 点1=1, 点2=2, 点3=4, 点4=8, 点5=16, 点6=32, 点7=64, 点8=128
DIGIT_TO_BIT = {
    '0': 1,    # 点1 (左上)
    '1': 2,    # 点2 (左2番目)
    '2': 4,    # 点3 (左3番目)
    '3': 64,   # 点7 (左下)
    '4': 16,   # 点5 (右2番目)
    '5': 32,   # 点6 (右3番目)
    '6': 128,  # 点8 (右下)
    '7': 8,    # 点4 (右上)
}


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def __init__(self):
        super().__init__()
        self._active = False
        self._buffer: set = set()

    # ------------------------------------------------------------------
    # モード切り替えスクリプト
    # ------------------------------------------------------------------

    @script(
        description="数字点字入力モードの切り替え",
        gesture="kb:NVDA+shift+w",
        category="数字点字入力",
    )
    def script_toggleMode(self, gesture):
        if self._active:
            self._active = False
            self._buffer.clear()
            ui.message("数字点字入力モード オフ")
        else:
            self._active = True
            self._buffer.clear()
            ui.message("数字点字入力モード オン。数字0〜7を押してスペースで確定。")

    # ------------------------------------------------------------------
    # 数字キー 0〜7 — @script による静的バインド
    #
    # 動的バインド(bindGesture)ではなく静的バインドを使う理由:
    #   Ctrl+V 等のキー操作後に NVDA の修飾キー状態がずれると、動的バインドでは
    #   kb:0 ではなく kb:control+0 として解釈されてバインドが失われる場合がある。
    #   静的バインドはクラスレベルの __gestures__ に登録されるため影響を受けない。
    #
    # モードOFF時は gesture.send() でキーをアプリにそのまま通過させる。
    # gesture.send() は NVDA の ignoreInjection() で保護されており無限ループしない。
    # ------------------------------------------------------------------

    @script(gesture="kb:0")
    def script_digit0(self, gesture):
        if self._active: self._handle_digit('0')
        else: gesture.send()

    @script(gesture="kb:1")
    def script_digit1(self, gesture):
        if self._active: self._handle_digit('1')
        else: gesture.send()

    @script(gesture="kb:2")
    def script_digit2(self, gesture):
        if self._active: self._handle_digit('2')
        else: gesture.send()

    @script(gesture="kb:3")
    def script_digit3(self, gesture):
        if self._active: self._handle_digit('3')
        else: gesture.send()

    @script(gesture="kb:4")
    def script_digit4(self, gesture):
        if self._active: self._handle_digit('4')
        else: gesture.send()

    @script(gesture="kb:5")
    def script_digit5(self, gesture):
        if self._active: self._handle_digit('5')
        else: gesture.send()

    @script(gesture="kb:6")
    def script_digit6(self, gesture):
        if self._active: self._handle_digit('6')
        else: gesture.send()

    @script(gesture="kb:7")
    def script_digit7(self, gesture):
        if self._active: self._handle_digit('7')
        else: gesture.send()

    @script(gesture="kb:space")
    def script_commitBraille(self, gesture):
        """スペースキー: モードON時は点字をクリップボードにコピー、OFFは通常のスペース入力。"""
        if self._active: self._output_braille()
        else: gesture.send()

    @script(gesture="kb:escape")
    def script_cancelInput(self, gesture):
        """Escキー: モードON時はバッファクリア、OFFは通常のEsc。"""
        if self._active:
            self._buffer.clear()
            ui.message("キャンセルしました")
        else:
            gesture.send()

    # ------------------------------------------------------------------
    # ヘルパーメソッド
    # ------------------------------------------------------------------

    def _handle_digit(self, digit):
        """数字キーの押下: バッファにトグル追加/除去して現在状態を読み上げる。"""
        if digit in self._buffer:
            self._buffer.discard(digit)
        else:
            self._buffer.add(digit)
        self._announce_buffer()

    def _announce_buffer(self):
        """現在のバッファ状態を読み上げる。"""
        if not self._buffer:
            ui.message("クリア")
        else:
            ui.message(f"点: {' '.join(sorted(self._buffer))}")

    def _output_braille(self):
        """バッファ内の数字からユニコード点字文字を生成し、クリップボードにコピーする。
        貼り付けはユーザーが手動で Ctrl+V を行う。"""
        if not self._buffer:
            ui.message("入力がありません")
            return

        bits = 0
        for digit in self._buffer:
            bits |= DIGIT_TO_BIT[digit]

        braille_char = chr(BRAILLE_BASE + bits)
        self._buffer.clear()

        if api.copyToClip(braille_char, notify=False):
            ui.message(f"クリップボードにコピー: 点字 {braille_char}")
        else:
            ui.message("クリップボードへのコピーに失敗しました")
