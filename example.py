#!/usr/bin/env python3
"""
A.I.VOICE Editor API Example

This example demonstrates how to use the aivoice_python library
to control A.I.VOICE Editor.
"""

import time
from aivoice_python import AIVoiceTTsControl, HostStatus


def main():
    # A.I.VOICE Editorの制御インスタンスを作成
    # カスタムパスを指定する場合は以下のようにします：
    # tts_control = AIVoiceTTsControl(editor_dir="C:\\MyPath\\AIVoice\\AIVoiceEditor\\")
    try:
        tts_control = AIVoiceTTsControl()  # デフォルトパスを使用
    except FileNotFoundError as e:
        print(f"エラー: {e}")
        return

    # A.I.VOICE Editor APIの初期化
    host_names = tts_control.get_available_host_names()
    if not host_names:
        print("利用可能なホストが見つかりません。")
        return
    
    host_name = host_names[0]
    tts_control.initialize(host_name)

    # A.I.VOICE Editorの起動
    current_status = tts_control.status
    print(f"Current status: {current_status}")
    if current_status.value == HostStatus.NotRunning.value:
        tts_control.start_host()

    # A.I.VOICE Editorへ接続
    tts_control.connect()
    host_version = tts_control.version
    print(f"{host_name} (v{host_version}) へ接続しました。")

    # 使用できるボイス名を取得
    voice_names = tts_control.voice_names
    print(f"利用可能なボイス名: {voice_names}")
    
    if voice_names:
        tts_control.current_voice_preset_name = voice_names[0]

    # テキストを設定
    tts_control.text = "Hello world! This is a test of A.I.VOICE Editor API."

    # 再生
    play_time = tts_control.get_play_time()
    tts_control.play()
    # Play()は再生完了を待たないので予め取得した再生時間+α分sleepで待つ
    time.sleep((play_time + 500) / 1000)

    # A.I.VOICE Editorとの接続を終了する
    tts_control.disconnect()
    print(f"{host_name} (v{host_version}) との接続を終了しました。")


if __name__ == "__main__":
    main()
