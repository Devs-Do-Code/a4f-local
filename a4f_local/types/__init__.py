# This file makes the 'types' directory a Python package.
# It should export the defined Pydantic models/dataclasses.

from .audio import SpeechCreateRequest
# from .chat import ChatCompletionRequest, ChatCompletion # Uncomment when chat.py is implemented

__all__ = [
    "SpeechCreateRequest",
    # "ChatCompletionRequest", # Uncomment when chat.py is implemented
    # "ChatCompletion",      # Uncomment when chat.py is implemented
]
