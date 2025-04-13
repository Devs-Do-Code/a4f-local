# Changelog

All notable changes to this project are documented here.

## [0.1.1] - 2025-04-14

- Added support for new OpenAI TTS voices: ash, coral, and sage. These voices can now be used in TTS requests if supported by the backend API.
- Updated type validation and provider engine to accept the new voices.
- Improved README with clearer installation instructions and updated roadmap.

## [0.1.0] - 2025-04-10

- Initial release of a4f-local.
- Introduced the core A4F client class for unified access to reverse-engineered AI provider APIs.
- Implemented provider discovery mechanism.
- Added Pydantic types for TTS requests.
- Included example TTS provider (provider_1) using OpenAI.fm reverse-engineered API.
- Added basic import-based test script (tests/test_tts.py).
- Provided pyproject.toml for packaging and distribution.
- Added LICENSE file with custom license.
- Included comprehensive README and .gitignore.
