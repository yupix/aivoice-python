# A.I.VOICE Python Library

A Python wrapper for A.I.VOICE Editor API that makes it easy to control A.I.VOICE Editor from Python.

## Features

✨ **Easy to use**: Simple Python interface for A.I.VOICE Editor API  
🎵 **Voice synthesis**: Generate speech from text using A.I.VOICE voices  
🔧 **Full control**: Access to all A.I.VOICE Editor functions  
🛡️ **Type safety**: Full type hints for better development experience  

## Requirements

- Windows OS
- A.I.VOICE Editor (v1.3.0 or later)
- Python 3.8+
- pythonnet

## Installation

```bash
pip install aivoice-python
```

## Quick Start

```python
import time
from aivoice_python import AIVoiceTTsControl, HostStatus

# Create A.I.VOICE controller (using default installation path)
tts_control = AIVoiceTTsControl()

# Or specify custom installation path:
# tts_control = AIVoiceTTsControl(editor_dir="C:\\MyPath\\AIVoice\\AIVoiceEditor\\")

# Initialize API
host_name = tts_control.get_available_host_names()[0]
tts_control.initialize(host_name)

# Start A.I.VOICE Editor if not running
if tts_control.status == HostStatus.NotRunning:
    tts_control.start_host()

# Connect to A.I.VOICE Editor
tts_control.connect()

# Set text and play
tts_control.text = "Hello, A.I.VOICE!"
play_time = tts_control.get_play_time()
tts_control.play()

# Wait for playback to complete
time.sleep((play_time + 500) / 1000)

# Disconnect
tts_control.disconnect()
```

## API Reference

### AIVoiceTTsControl

Main class for controlling A.I.VOICE Editor.

#### Constructor

- `AIVoiceTTsControl(editor_dir: str = None)` - Create controller instance
  - `editor_dir`: Custom A.I.VOICE Editor installation path (optional)

#### Properties

- `text: str` - Text to synthesize
- `current_voice_preset_name: str` - Current voice preset name
- `voice_names: List[str]` - Available voice names
- `voice_preset_names: List[str]` - Available voice preset names
- `status: HostStatus` - Current host status
- `version: str` - Host version

#### Methods

- `initialize(service_name: str)` - Initialize API
- `connect()` - Connect to A.I.VOICE Editor
- `disconnect()` - Disconnect from A.I.VOICE Editor
- `start_host()` - Start A.I.VOICE Editor
- `play()` - Start/pause playback
- `stop()` - Stop playback
- `get_play_time() -> int` - Get playback duration in milliseconds
- `save_audio_to_file(path: str)` - Save audio to file

### Enums

#### HostStatus
- `NotRunning` - A.I.VOICE Editor is not running
- `NotConnected` - Not connected to A.I.VOICE Editor
- `Idle` - Connected and idle
- `Busy` - Connected and busy

#### TextEditMode
- `Text` - Text mode
- `List` - List mode

## Examples

### Custom Installation Path

If A.I.VOICE Editor is installed in a non-standard location:

```python
from aivoice_python import AIVoiceTTsControl

# Specify custom installation path
tts_control = AIVoiceTTsControl(editor_dir="D:\\MyApps\\AIVoice\\AIVoiceEditor\\")
# ... rest of the code ...
```

### Save Audio to File

```python
from aivoice_python import AIVoiceTTsControl

tts_control = AIVoiceTTsControl()
# ... initialization code ...

tts_control.text = "Hello, World!"
tts_control.save_audio_to_file("output.wav")
```

### Use Different Voice

```python
from aivoice_python import AIVoiceTTsControl

tts_control = AIVoiceTTsControl()
# ... initialization code ...

# Get available voices
voices = tts_control.voice_names
print(f"Available voices: {voices}")

# Set voice
if voices:
    tts_control.current_voice_preset_name = voices[1]  # Use second voice
```

## Error Handling

```python
from aivoice_python import AIVoiceTTsControl

try:
    tts_control = AIVoiceTTsControl()
except FileNotFoundError as e:
    print(f"A.I.VOICE Editor not found: {e}")
    # Try with custom path
    try:
        tts_control = AIVoiceTTsControl(editor_dir="C:\\MyPath\\AIVoice\\AIVoiceEditor\\")
    except FileNotFoundError:
        print("Please install A.I.VOICE Editor v1.3.0 or later.")
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues, please create an issue on the GitHub repository.
