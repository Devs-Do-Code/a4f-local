# This file makes 'tts' a package within 'provider_1'.
# It exports the main engine function for this capability.

from .engine import create_speech

__all__ = ['create_speech'] # Required for the discovery mechanism convention
