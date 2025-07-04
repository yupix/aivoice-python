"""
A.I.VOICE Editor API Python Wrapper

This module provides a Python interface for controlling A.I.VOICE Editor
through its COM API.
"""

from enum import Enum
import json
import os
import clr

try:
    from typing import Required, TypedDict, List
except ImportError:
    # Python < 3.11 のサポート
    from typing import TypedDict, List
    from typing_extensions import Required


class HostStatus(Enum):
    """A.I.VOICE Editorのホストステータス"""
    NotRunning = 0
    NotConnected = 1
    Idle = 2
    Busy = 3


class TextEditMode(Enum):
    """テキスト入力モード"""
    Text = 0
    List = 1


class Style(TypedDict, total=False):
    """音声スタイルの設定"""
    Name: str  # スタイル名 (例: "J", "A", "S")
    Value: float  # スタイル値 (0.0-1.0)


class MergedVoice(TypedDict, total=False):
    """マージされた音声の設定"""
    BasePitchVoiceName: str  # ベースピッチボイス名
    MergedVoices: List[dict]  # マージされた音声のリスト


class VoicePreset(TypedDict, total=False):
    """A.I.VOICE ボイスプリセットの設定
    
    指定しなかったフィールドはデフォルト値が使用されます。
    """
    PresetName: Required[str]  # プリセット名
    VoiceName: Required[str]  # ボイス名
    MergedVoiceContainer: MergedVoice  # マージボイス設定
    Volume: float  # 音量 (0.0-2.0)
    Speed: float  # 話速 (0.5-4.0)
    Pitch: float  # 高さ (0.5-2.0)
    PitchRange: float  # 抑揚 (0.0-2.0)
    MiddlePause: int  # 短ポーズ時間 (ミリ秒)
    LongPause: int  # 長ポーズ時間 (ミリ秒)
    Styles: List[Style]  # スタイル設定のリスト


class AIVoiceTTsControl:
    """A.I.VOICE Editor API制御クラス"""
    
    def __init__(self, editor_dir: str = None):
        """
        A.I.VOICE Editor API制御クラスを初期化します。
        
        Parameters
        ----------
        editor_dir : str, optional
            A.I.VOICE Editorのインストールディレクトリパス。
            指定されない場合は、デフォルトのインストールパスを使用します。
            例: "C:\\Program Files\\AI\\AIVoice\\AIVoiceEditor\\"
        """
        # A.I.VOICE Editor APIの初期化
        if editor_dir is None:
            self._editor_dir = os.environ.get("ProgramW6432", "") + "\\AI\\AIVoice\\AIVoiceEditor\\"
        else:
            # パスの末尾にバックスラッシュを確実に付ける
            self._editor_dir = editor_dir.rstrip("\\") + "\\"
        
        dll_path = self._editor_dir + "AI.Talk.Editor.Api.dll"
        if not os.path.isfile(dll_path):
            raise FileNotFoundError(f"A.I.VOICE Editor API DLL が見つかりません: {dll_path}")
        
        # pythonnet DLLの読み込み
        clr.AddReference(self._editor_dir + "AI.Talk.Editor.Api")
        from AI.Talk.Editor.Api import TtsControl
        
        self.tts_control = TtsControl()

    @property
    def current_voice_preset_name(self) -> str:
        """現在のボイスプリセット名を取得または設定します。"""
        return self.tts_control.CurrentVoicePresetName
    
    @current_voice_preset_name.setter
    def current_voice_preset_name(self, value: str) -> None:
        self.tts_control.CurrentVoicePresetName = value

    @property
    def master_control(self) -> str:
        """マスターコントロールの各値を表す JSON 形式の文字列を取得または設定します。"""
        return self.tts_control.MasterControl
    
    @master_control.setter
    def master_control(self, value: str) -> None:
        self.tts_control.MasterControl = value

    @property
    def is_initialized(self) -> bool:
        """APIが初期化されているかどうかを取得します。"""
        return self.tts_control.IsInitialized

    @property
    def text(self) -> str:
        """テキスト形式の入力テキストを取得または設定します。"""
        return self.tts_control.Text

    @text.setter
    def text(self, value: str) -> None:
        self.tts_control.Text = value

    @property
    def text_edit_mode(self) -> TextEditMode:
        """選択されているテキスト入力形式を取得または設定します。"""
        return TextEditMode(self.tts_control.TextEditMode)

    @text_edit_mode.setter
    def text_edit_mode(self, value: TextEditMode) -> None:
        self.tts_control.TextEditMode = value.value

    @property
    def text_selection_length(self) -> int:
        """テキスト形式の入力テキストの選択文字数を取得または設定します。"""
        return self.tts_control.TextSelectionLength

    @text_selection_length.setter
    def text_selection_length(self, value: int) -> None:
        self.tts_control.TextSelectionLength = value

    @property
    def text_selection_start(self) -> int:
        """テキスト形式の入力テキストの選択開始位置を取得または設定します。"""
        return self.tts_control.TextSelectionStart

    @text_selection_start.setter
    def text_selection_start(self, value: int) -> None:
        self.tts_control.TextSelectionStart = value

    @property
    def version(self) -> str:
        """ホストプログラムのバージョンを取得します。"""
        return self.tts_control.Version

    @property
    def status(self) -> HostStatus:
        """ホストプログラムのステータスを取得します。"""
        raw_status = self.tts_control.Status
        
        # C#のEnumから文字列が返ってくる場合の対応
        if isinstance(raw_status, str):
            status_mapping = {
                "NotRunning": HostStatus.NotRunning,
                "NotConnected": HostStatus.NotConnected,
                "Idle": HostStatus.Idle,
                "Busy": HostStatus.Busy
            }
            return status_mapping.get(raw_status, HostStatus.NotConnected)
        
        # 数値の場合はそのまま変換
        try:
            return HostStatus(raw_status)
        except ValueError:
            return HostStatus.NotConnected

    @property
    def voice_names(self) -> list[str]:
        """利用可能なボイス名を取得します。"""
        raw_names = self.tts_control.VoiceNames
        # C#のString[]をPythonのlistに変換
        return list(raw_names) if raw_names else []

    @property
    def voice_preset_names(self) -> list[str]:
        """登録されているボイスプリセット名を取得します。"""
        raw_names = self.tts_control.VoicePresetNames
        # C#のString[]をPythonのlistに変換
        return list(raw_names) if raw_names else []

    def add_list_item(self, voice_preset_name: str, text: str) -> None:
        """リスト形式の末尾に行を追加します。"""
        self.tts_control.AddListItem(voice_preset_name, text)

    def add_voice_preset(self, voice_preset: VoicePreset) -> None:
        """新規ボイスプリセットを作成し JSON 形式で指定された各値を設定します。"""
        self.tts_control.AddVoicePreset(json.dumps(voice_preset, ensure_ascii=False))

    def clear_list_items(self):
        """リスト形式の行をすべて削除します。"""
        self.tts_control.ClearListItems()

    def connect(self):
        """A.I.VOICE Editor へ接続します。

        ホストプログラムへ接続後、10分間 API を介した操作が行われない状態が続くと自動的に接続が解除されます。
        """
        self.tts_control.Connect()

    def disconnect(self):
        """ホストプログラムとの接続を解除します。"""
        self.tts_control.Disconnect()

    def get_available_host_names(self) -> list[str]:
        """利用可能なホストの名称のリストを取得します。"""
        raw_names = self.tts_control.GetAvailableHostNames()
        # C#のString[]をPythonのlistに変換
        return list(raw_names) if raw_names else []

    def get_list_count(self) -> int:
        """リストのアイテム数を取得します。"""
        return self.tts_control.GetListCount()

    def get_list_selection_count(self) -> int:
        """リスト形式の選択行数を取得します。"""
        return self.tts_control.GetListSelectionCount()

    def get_list_selection_indices(self) -> list[int]:
        """リスト形式で選択されている行のインデックスを取得します。"""
        raw_indices = self.tts_control.GetListSelectionIndices()
        # C#の配列をPythonのlistに変換
        return list(raw_indices) if raw_indices else []

    def get_list_sentence(self, index: int) -> str:
        """リスト形式の選択行のセンテンスを取得します。"""
        return self.tts_control.GetListSentence(index)

    def get_list_voice_preset(self) -> str:
        """リスト形式の選択行のボイスプリセット名を取得します。"""
        return self.tts_control.GetListVoicePreset()

    def get_play_time(self) -> int:
        """読み上げ音声の再生時間を取得します。"""
        return self.tts_control.GetPlayTime()

    def get_voice_preset(self, preset_name: str) -> str:
        """引数で指定された名称のボイスプリセットの各値を JSON 形式で取得します。"""
        return VoicePreset(json.load(self.tts_control.GetVoicePreset(preset_name)))

    def initialize(self, service_name: str):
        """APIを初期化します。"""
        self.tts_control.Initialize(service_name)

    def insert_list_item(self, voice_preset_name: str, text: str) -> None:
        """リスト形式の選択位置に行を挿入します。"""
        self.tts_control.InsertListItem(voice_preset_name, text)

    def play(self):
        """音声の再生を開始または一時停止します。

        再生が完了するまで待機しません。
        """
        self.tts_control.Play()

    def reload_phrase_dictionary(self):
        """フレーズ辞書を再読込みします。"""
        self.tts_control.ReloadPhraseDictionary()

    def reload_symbol_dictionary(self):
        """記号ポーズ辞書を再読込みします。"""
        self.tts_control.ReloadSymbolDictionary()

    def reload_voice_preset(self):
        """ボイスプリセットを再読込みします。"""
        self.tts_control.ReloadVoicePreset()

    def reload_word_dictionary(self):
        """単語辞書を再読込みします。"""
        self.tts_control.ReloadWordDictionary()

    def remove_list_item(self, index: int) -> None:
        """リスト形式の選択行を削除します。"""
        self.tts_control.RemoveListItem(index)

    def save_audio_to_file(self, path: str) -> None:
        """テキストの読み上げ音声を指定されたファイルに保存します。
        
        ホストプログラムで選択されているテキスト入力形式で保存が行われます。
        path で指定したファイルパスの拡張子がホストプログラムの音声保存時のファイル形式と一致しない場合、ファイル形式に応じた拡張子が付加されます。
        ホストプログラムの「音声ファイルパスの指定方法」が「ファイル命名規則」の場合、引数で指定されたパスは無視されます。
        ホストプログラムでフレーズが編集状態の場合、その編集内容は読み上げに反映されません。
        ホストプログラムで単語が編集状態の場合、その編集内容は読み上げに反映されません。 
        """
        self.tts_control.SaveAudioToFile(path)

    def set_list_selection_indexes(self, index: int) -> None:
        """リスト形式の単一行を選択状態にします。"""
        self.tts_control.SetListSelectionIndices(index)

    def set_list_selection_indices(self, indices: list[int]) -> None:
        """リスト形式の任意の複数行を選択状態にします。"""
        self.tts_control.SetListSelectionIndices(indices)

    def set_list_selection_range(self, start_index: int, length: int) -> None:
        """リスト形式の任意の範囲行を選択状態にします。

        Parameters
        ----------
        start_index : int
            選択開始行のインデックス（0スタート）
        length : int
            選択状態にする行数
        """
        self.tts_control.SetListSelectionRange(start_index, length)

    def set_list_sentence(self, sentence: str, synthesize: bool) -> None:
        """リスト形式の選択行のセンテンスを設定します。"""
        self.tts_control.SetListSentence(sentence, synthesize)

    def set_list_voice_preset(self, voice_preset_name: str) -> None:
        """リスト形式の選択行のボイスプリセット名を設定します。"""
        self.tts_control.SetListVoicePreset(voice_preset_name)

    def set_voice_preset(self, voice_preset: VoicePreset) -> None:
        """既存のボイスプリセットに JSON 形式で指定された各値を設定します。"""
        self.tts_control.SetVoicePreset(json.dumps(voice_preset, ensure_ascii=False))

    def start_host(self):
        """ホストプログラムを起動します。"""
        self.tts_control.StartHost()

    def stop(self):
        """音声の再生を停止します。"""
        self.tts_control.StopHost()

    def terminate_host(self):
        """ホストプログラムを終了します。"""
        self.tts_control.TerminateHost()
