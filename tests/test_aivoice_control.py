"""
Basic tests for AIVoiceTTsControl
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# テスト用のパッケージパスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aivoice_python import HostStatus, TextEditMode


class TestHostStatus(unittest.TestCase):
    """HostStatus enumのテスト"""
    
    def test_host_status_values(self):
        """HostStatusの値が正しいかテスト"""
        self.assertEqual(HostStatus.NotRunning.value, 0)
        self.assertEqual(HostStatus.NotConnected.value, 1)
        self.assertEqual(HostStatus.Idle.value, 2)
        self.assertEqual(HostStatus.Busy.value, 3)


class TestTextEditMode(unittest.TestCase):
    """TextEditMode enumのテスト"""
    
    def test_text_edit_mode_values(self):
        """TextEditModeの値が正しいかテスト"""
        self.assertEqual(TextEditMode.Text.value, 0)
        self.assertEqual(TextEditMode.List.value, 1)


class TestAIVoiceTTsControl(unittest.TestCase):
    """AIVoiceTTsControlのテスト（モック使用）"""
    
    @patch('os.path.isfile')
    @patch('aivoice_python.aivoice_control.clr.AddReference')
    def test_initialization_success(self, mock_add_reference, mock_isfile):
        """正常な初期化のテスト"""
        # A.I.VOICE Editorがインストールされている場合をモック
        mock_isfile.return_value = True
        mock_add_reference.return_value = None
        
        # AI.Talk.Editor.Apiモジュールをモック
        mock_api_module = Mock()
        mock_tts_control_class = Mock()
        mock_api_module.TtsControl = mock_tts_control_class
        
        # clr.AddReferenceの後でインポートされるモジュールをモック
        with patch.dict('sys.modules', {'AI.Talk.Editor.Api': mock_api_module}):
            from aivoice_python import AIVoiceTTsControl
            
            control = AIVoiceTTsControl()
            self.assertIsNotNone(control)
            mock_add_reference.assert_called_once()
            mock_tts_control_class.assert_called_once()
    
    @patch('os.path.isfile')
    def test_initialization_failure(self, mock_isfile):
        """A.I.VOICE Editorが見つからない場合のテスト"""
        # A.I.VOICE Editorがインストールされていない場合をモック
        mock_isfile.return_value = False
        
        from aivoice_python import AIVoiceTTsControl
        
        with self.assertRaises(FileNotFoundError):
            AIVoiceTTsControl()
    
    @patch('os.path.isfile')
    @patch('aivoice_python.aivoice_control.clr.AddReference')
    def test_custom_editor_dir(self, mock_add_reference, mock_isfile):
        """カスタムエディターディレクトリのテスト"""
        # カスタムパスでのテスト
        mock_isfile.return_value = True
        mock_add_reference.return_value = None
        
        # AI.Talk.Editor.Apiモジュールをモック
        mock_api_module = Mock()
        mock_tts_control_class = Mock()
        mock_api_module.TtsControl = mock_tts_control_class
        
        custom_path = "D:\\MyApps\\AIVoice\\AIVoiceEditor"  # 末尾のバックスラッシュなし
        expected_path_with_slash = custom_path + "\\"
        
        with patch.dict('sys.modules', {'AI.Talk.Editor.Api': mock_api_module}):
            from aivoice_python import AIVoiceTTsControl
            
            control = AIVoiceTTsControl(editor_dir=custom_path)
            self.assertIsNotNone(control)
            
            # 正しいパスでDLLの存在確認が行われたかチェック
            expected_dll_path = expected_path_with_slash + "AI.Talk.Editor.Api.dll"
            mock_isfile.assert_called_with(expected_dll_path)
            
            # AddReferenceが正しいパスで呼ばれたかチェック
            expected_reference_path = expected_path_with_slash + "AI.Talk.Editor.Api"
            mock_add_reference.assert_called_with(expected_reference_path)


if __name__ == '__main__':
    unittest.main()
