#!/usr/bin/env python3
"""
A.I.VOICE TypedDict Usage Example

This example demonstrates how to use TypedDict for type-safe voice preset configuration.
"""

import json
from aivoice_python import AIVoiceTTsControl, VoicePreset, Style


def create_voice_preset() -> VoicePreset:
    """聞きやすい声のプリセットを作成します"""
    
    # 聞きやすさを重視したスタイル設定
    styles: list[Style] = [
        {"Name": "J", "Value": 0.2},  # 喜び - ほんの少し明るく
        {"Name": "A", "Value": 0.0},  # 怒り - 穏やかに
        {"Name": "S", "Value": 0.1},  # 悲しみ - ほんの少し落ち着いた感じ
    ]
    
    # 聞きやすい音声設定
    preset: VoicePreset = {
        "PresetName": "聞きやすい茜ちゃん",
        "VoiceName": "akane_west_emo_48", 
        "MergedVoiceContainer": {
            "BasePitchVoiceName": "",
            "MergedVoices": []
        },
        "Volume": 0.9,      # 少し控えめの音量
        "Speed": 0.85,      # ゆっくりめで聞き取りやすく
        "Pitch": 0.95,      # 少し低めで落ち着いた印象
        "PitchRange": 0.8,  # 抑揚を抑えて自然に
        "MiddlePause": 250,  # 短ポーズを長めにして余裕を持たせる
        "LongPause": 600,   # 長ポーズもゆったりと
        "Styles": styles
    }
    
    return preset


def create_energetic_voice_preset() -> VoicePreset:
    """元気で明るい声のプリセットを作成します"""
    
    styles: list[Style] = [
        {"Name": "J", "Value": 0.7},  # 喜び - 明るく元気に
        {"Name": "A", "Value": 0.1},  # 怒り - ちょっとだけ力強く
        {"Name": "S", "Value": 0.0},  # 悲しみ - なし
    ]
    
    preset: VoicePreset = {
        "PresetName": "元気な茜ちゃん",
        "VoiceName": "akane_west_emo_48",
        "MergedVoiceContainer": {
            "BasePitchVoiceName": "",
            "MergedVoices": []
        },
        "Volume": 1.1,      # 少し大きめ
        "Speed": 1.0,       # 標準的な速度
        "Pitch": 1.05,      # 少し高めで明るく
        "PitchRange": 1.3,  # 抑揚豊かに
        "MiddlePause": 150,  # 短めのポーズでテンポよく
        "LongPause": 350,   # 長ポーズも短めに
        "Styles": styles
    }
    
    return preset


def create_calm_voice_preset() -> VoicePreset:
    """落ち着いた大人っぽい声のプリセットを作成します"""
    
    styles: list[Style] = [
        {"Name": "J", "Value": 0.0},  # 喜び - 控えめに
        {"Name": "A", "Value": 0.0},  # 怒り - なし
        {"Name": "S", "Value": 0.3},  # 悲しみ - 落ち着いた印象
    ]
    
    preset: VoicePreset = {
        "PresetName": "落ち着いた茜ちゃん",
        "VoiceName": "akane_west_emo_48",
        "MergedVoiceContainer": {
            "BasePitchVoiceName": "",
            "MergedVoices": []
        },
        "Volume": 0.8,      # 控えめな音量
        "Speed": 0.75,      # ゆっくりと
        "Pitch": 0.85,      # 低めで大人っぽく
        "PitchRange": 0.6,  # 抑揚を抑えて安定感
        "MiddlePause": 300,  # 長めのポーズでゆったり
        "LongPause": 700,   # たっぷり間を取る
        "Styles": styles
    }
    
    return preset


def main():
    """メイン処理"""
    
    # 3種類のプリセットを作成
    presets = {
        "聞きやすい茜ちゃん": create_voice_preset(),
        "元気な茜ちゃん": create_energetic_voice_preset(), 
        "落ち着いた茜ちゃん": create_calm_voice_preset()
    }
    
    try:
        # A.I.VOICE制御
        tts_control = AIVoiceTTsControl()
        
        # 初期化
        host_names = tts_control.get_available_host_names()
        if host_names:
            tts_control.initialize(host_names[0])
            tts_control.connect()
            print(f"利用可能なプリセット: {tts_control.voice_preset_names}")
            # 3つのプリセットを試してみる
            test_texts = [
                ("聞きやすい茜ちゃん", "こんにちは！聞きやすい声でお話ししています。長時間聞いても疲れにくい設定にしました。"),
                ("元気な茜ちゃん", "みなさん、こんにちは〜！元気いっぱいの声でお話ししています！"),
                ("落ち着いた茜ちゃん", "落ち着いた大人っぽい声で、ゆっくりとお話しします。リラックスしてお聞きください。")
            ]
            
            for preset_name, text in test_texts:

                if preset_name not in tts_control.voice_preset_names:
                    tts_control.add_voice_preset(presets[preset_name])

                print(f"\n=== {preset_name}なプリセットでテスト ===")
                
                # プリセット設定を更新
                tts_control.set_voice_preset(presets[preset_name])
                # 現在のプリセット名を更新
                tts_control.current_voice_preset_name = preset_name
                
                # テキスト設定・再生
                tts_control.text = text
                play_time = tts_control.get_play_time()
                print(f"テキスト: {text}")
                print(f"再生時間: {play_time}ms")
                
                tts_control.play()
                
                import time
                time.sleep((play_time + 1000) / 1000)  # 少し長めに待機
            
            tts_control.disconnect()
            print("\n全プリセットでの再生完了！")
            
    except FileNotFoundError:
        print("A.I.VOICE Editor が見つかりません")
    except Exception as e:
        print(f"エラー: {e}")


def demo_voice_comparison():
    """音声比較デモ"""
    print("=== 音声プリセット比較 ===")
    
    presets = [
        ("聞きやすい", create_voice_preset()),
        ("元気", create_energetic_voice_preset()),
        ("落ち着いた", create_calm_voice_preset())
    ]
    
    for name, preset in presets:
        print(f"\n【{name}なプリセット】")
        print(f"  音量: {preset['Volume']}")
        print(f"  速度: {preset['Speed']}")
        print(f"  音程: {preset['Pitch']}")
        print(f"  抑揚: {preset['PitchRange']}")
        print(f"  短ポーズ: {preset['MiddlePause']}ms")
        print(f"  長ポーズ: {preset['LongPause']}ms")
        
        styles_info = []
        for style in preset['Styles']:
            if style['Value'] > 0:
                style_names = {"J": "喜び", "A": "怒り", "S": "悲しみ"}
                styles_info.append(f"{style_names[style['Name']]}: {style['Value']}")
        
        print(f"  感情: {', '.join(styles_info) if styles_info else 'ニュートラル'}")


def validate_preset_json(json_str: str) -> bool:
    """JSONがVoicePresetの形式に適合するかチェック"""
    try:
        data = json.loads(json_str)
        
        # 必須フィールドのチェック
        required_fields = [
            "PresetName", "VoiceName", "MergedVoiceContainer",
            "Volume", "Speed", "Pitch", "PitchRange", 
            "MiddlePause", "LongPause", "Styles"
        ]
        
        for field in required_fields:
            if field not in data:
                print(f"必須フィールド '{field}' が見つかりません")
                return False
        
        # スタイルの形式チェック
        if not isinstance(data["Styles"], list):
            print("Styles は配列である必要があります")
            return False
            
        for style in data["Styles"]:
            if not isinstance(style, dict) or "Name" not in style or "Value" not in style:
                print("Styles の要素は Name と Value を持つ必要があります")
                return False
        
        print("プリセットJSON形式は正常です！")
        return True
        
    except json.JSONDecodeError:
        print("無効なJSON形式です")
        return False


if __name__ == "__main__":
    # サンプルJSONの検証
    sample_json = '''
    {
        "PresetName":"琴葉 茜",
        "VoiceName":"akane_west_emo_48",
        "MergedVoiceContainer":{"BasePitchVoiceName":"","MergedVoices":[]},
        "Volume":1,
        "Speed":1,
        "Pitch":1,
        "PitchRange":1,
        "MiddlePause":150,
        "LongPause":370,
        "Styles":[{"Name":"J","Value":0},{"Name":"A","Value":0},{"Name":"S","Value":0}]
    }
    '''
    
    print("=== 音声プリセット比較 ===")
    demo_voice_comparison()
    
    print("\n=== サンプルJSONの検証 ===")
    validate_preset_json(sample_json)
    
    print("\n=== 聞きやすい音声プリセットのテスト ===")
    main()
