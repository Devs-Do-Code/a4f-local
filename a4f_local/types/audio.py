from pydantic import BaseModel, Field
from typing import Literal, Optional

# Based on OpenAI's API documentation for /v1/audio/speech

class SpeechCreateRequest(BaseModel):
    """
    Pydantic model for TTS request, mirroring OpenAI's structure.
    """
    model: str = Field(..., description="One of the available TTS models, e.g., tts-1 or tts-1-hd")
    input: str = Field(..., max_length=4096, description="The text to generate audio from. The maximum length is 4096 characters.")
    voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer", "ash", "coral", "sage"] = Field(..., description="The voice to use for synthesis.")
    response_format: Optional[Literal["mp3", "opus", "aac", "flac", "wav", "pcm"]] = Field(
        default="mp3",
        description="The format to audio in. Supported formats are mp3, opus, aac, flac, wav, and pcm."
    )
    speed: Optional[float] = Field(
        default=1.0,
        ge=0.25,
        le=4.0,
        description="The speed of the generated audio. Select a value from 0.25 to 4.0. 1.0 is the default."
    )

    # Allow extra fields to accommodate potential provider-specific parameters
    # passed via **kwargs in the client method, although ideally these should
    # be handled explicitly during translation if possible.
    class Config:
        extra = 'allow'

# Note: The response from OpenAI's API is typically the raw audio bytes.
# If a structured response object were needed (e.g., containing metadata),
# it would be defined here as well (e.g., class AudioResponse(BaseModel): ...).
# For now, the client expects raw bytes directly from the engine.
