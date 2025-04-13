# a4f-local

[![PyPI version](https://img.shields.io/pypi/v/a4f-local.svg?style=flat-square)](https://pypi.org/project/a4f-local/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/a4f-local.svg?style=flat-square)](https://pypi.org/project/a4f-local/)

A unified, professional Python wrapper for various reverse-engineered AI provider APIs, designed to be **OpenAI-compatible** and **easy to use**.

---

## Key Features

- **Unified API:** Call multiple unofficial AI providers with a single, OpenAI-like interface.
- **Modular:** Easily extend with new providers and capabilities.
- **Supports Text-to-Speech (TTS):** Initial implementation includes OpenAI.fm reverse-engineered TTS.
- **OpenAI-Compatible:** Accepts and returns data in the same format as OpenAI's official API.
- **Simple to Use:** Designed for developers of all skill levels.

---

## Installation

Install directly from PyPI:

```bash
pip install -U a4f-local
```

---

## Usage Example

```python
from a4f_local import A4F

client = A4F()

try:
    audio_bytes = client.audio.speech.create(
        model="tts-1",  # Model name (currently informational)
        input="Hello from a4f-local!",
        voice="alloy"   # Choose a supported voice
    )
    with open("output.mp3", "wb") as f:
        f.write(audio_bytes)
    print("Generated output.mp3")
except Exception as e:
    print(f"An error occurred: {e}")
```

---

## Supported Voices

The following voice names are supported (mapped to OpenAI's official voices):

- `alloy`
- `echo`
- `fable`
- `onyx`
- `nova`
- `shimmer`

Use one of these as the `voice` parameter in your TTS requests.

---

## How It Works

- You interact with the `A4F` client **just like OpenAI's Python SDK**.
- The client **automatically discovers** available providers and their capabilities.
- When you call a method (e.g., `client.audio.speech.create()`), it **routes the request** to the appropriate provider.
- The provider **translates** the OpenAI-compatible request into its own API format, calls the API, and **translates the response back**.

---

## Roadmap

- **More Providers:** Support for chat, image generation, and other AI capabilities.
- **Configuration:** Easier ways to configure API keys and provider preferences.
- **Async Support:** Async versions of API calls.
- **Better Error Handling:** More informative error messages and exceptions.

---

## License

See the [LICENSE](LICENSE) file for details. This software is **not** open source in the traditional sense. Please review the license terms carefully before use.

---

## Disclaimer

This package uses **reverse-engineered, unofficial APIs**. These may break or change at any time. Use at your own risk.

---

## More Information

More detailed documentation, tutorials, and examples will be published here and on PyPI.

For now, refer to the example above and the source code for guidance.

---
