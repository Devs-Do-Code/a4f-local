import os
import sys
from pathlib import Path

# Ensure the package root is in the Python path for direct script execution
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from a4f_local import A4F
except ImportError:
    print("ERROR: Could not import A4F. Make sure the package is installed or run from the project root.")
    sys.exit(1)

def test_simple_tts():
    """Runs a simple TTS test compatible with pytest."""
    try:
        client = A4F()
        
        test_text = "This is a test of the text-to-speech system using the a4f-local package and provider 1."
        test_voice = "echo"
        output_filename = "test_output.mp3"
        output_path = Path(__file__).parent / output_filename

        print(f"Requesting TTS for voice '{test_voice}'...")
        audio_bytes = client.audio.speech.create(
            model="tts-1", 
            input=test_text,
            voice=test_voice
        )

        if isinstance(audio_bytes, bytes) and len(audio_bytes) > 100:
            print(f"SUCCESS: Received {len(audio_bytes)} bytes of audio.")
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            print(f"Saved output to: {output_path}")
        else:
            print(f"FAILED: Invalid audio data received (Type: {type(audio_bytes)}).")

    except Exception as e:
        print(f"FAILED: An error occurred during the test: {e}")
        raise # Re-raise exception for pytest to capture failure

# No need for __main__ block when using pytest
