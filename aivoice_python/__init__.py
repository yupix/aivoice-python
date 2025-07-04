"""
A.I.VOICE Editor API Python Wrapper

A Python library for controlling A.I.VOICE Editor through its API.
"""

from .aivoice_control import (
    AIVoiceTTsControl, 
    HostStatus, 
    TextEditMode,
    VoicePreset,
    Style,
    MergedVoice
)

__version__ = "0.1.1"
__author__ = "yupix"
__email__ = "yupi0982@outlook.jp"

__all__ = [
    "AIVoiceTTsControl",
    "HostStatus", 
    "TextEditMode",
    "VoicePreset",
    "Style",
    "MergedVoice"
]
