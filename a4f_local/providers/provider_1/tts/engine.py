import requests
import logging
from ....types.audio import SpeechCreateRequest

# Optional: Import from provider_1.config if URL/headers/secrets were stored there
# from ..config import PROVIDER_URL, PROVIDER_HEADERS # Example if config.py existed

logger = logging.getLogger(__name__)

# Define standard OpenAI voices supported by this specific provider (OpenAI.fm)
# Includes standard voices and potentially newer ones if the backend supports them.
SUPPORTED_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer", "ash", "coral", "sage"]

# Headers based on the reverse-engineered request in the guide
# Consider moving sensitive or frequently changing parts to a config file or env vars later
PROVIDER_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,hi;q=0.8",
    "dnt": "1",
    "origin": "https://www.openai.fm",
    "referer": "https://www.openai.fm/", # Simplified referer, adjust if needed
    # Using a generic user-agent might be less likely to break than a specific worker JS referer
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}
PROVIDER_URL = "https://www.openai.fm/api/generate"

def create_speech(*, request: SpeechCreateRequest) -> bytes:
    """
    Generates speech using the OpenAI.fm reverse-engineered API.
    This function acts as the engine for the 'tts' capability of 'provider_1'.

    Args:
        request: An object matching OpenAI's SpeechCreateRequest schema,
                 containing input text, voice, model, etc.

    Returns:
        MP3 audio content as bytes on success.

    Raises:
        ValueError: If the requested voice is not supported by this provider.
        requests.exceptions.RequestException: If the API call fails (network issue, bad status code).
        # Consider adding custom exceptions for specific API errors if identifiable
    """
    logger.info(f"Provider 1 (OpenAI.fm) received TTS request for voice: {request.voice}")

    # --- Input Validation ---
    if request.voice not in SUPPORTED_VOICES:
        logger.error(f"Unsupported voice requested for Provider 1: {request.voice}")
        raise ValueError(f"Provider 'OpenAI.fm TTS' does not support voice: {request.voice}. Supported: {SUPPORTED_VOICES}")

    # --- Input Translation (OpenAI Schema -> Provider API Schema) ---
    # The OpenAI.fm API requires a 'prompt' field which isn't standard in OpenAI's TTS.
    # We need to construct it. The guide suggests a placeholder.
    # Future improvement: Allow passing custom prompts via kwargs or infer based on input/speed/etc.
    # Note: OpenAI's 'speed' parameter isn't directly supported by the example API call.
    if request.speed != 1.0:
         logger.warning(f"Provider 1 (OpenAI.fm) does not support the 'speed' parameter (requested: {request.speed}). Using default speed.")

    # Constructing the 'prompt' based on the guide's simplified example
    voice_prompt = f"Voice: {request.voice}. Standard clear voice."
    logger.debug(f"Constructed voice prompt for OpenAI.fm: '{voice_prompt}'")

    payload = {
        "input": request.input,
        "prompt": voice_prompt,
        "voice": request.voice, # Directly maps from the validated OpenAI voice
        "vibe": "null" # As per the reverse-engineered request
    }
    logger.debug(f"Payload for OpenAI.fm API: {payload}")

    # --- API Call ---
    try:
        logger.info(f"Calling OpenAI.fm API at {PROVIDER_URL}")
        response = requests.post(PROVIDER_URL, headers=PROVIDER_HEADERS, data=payload, timeout=60) # Added timeout
        response.raise_for_status() # Raises HTTPError for 4xx/5xx responses

        # --- Output Translation (Provider API Response -> OpenAI Expected Output) ---
        # The OpenAI.fm API returns raw MP3 bytes directly in the response body on success.
        # This matches the expected output format (bytes) for the client's speech.create method.
        # No further translation is needed for the success case here.
        audio_content = response.content
        logger.info(f"Successfully received {len(audio_content)} bytes of audio data from OpenAI.fm.")
        return audio_content

    except requests.exceptions.Timeout:
        logger.error(f"Timeout occurred while calling OpenAI.fm API: {PROVIDER_URL}")
        raise # Re-raise the timeout exception
    except requests.exceptions.HTTPError as http_err:
        # Log specific HTTP errors
        error_body = http_err.response.text
        logger.error(f"HTTP error occurred calling OpenAI.fm API: {http_err.response.status_code} - {http_err.response.reason}. Response: {error_body[:500]}") # Log first 500 chars
        # Re-raise the original exception, potentially wrap in a custom one later
        raise http_err
    except requests.exceptions.RequestException as req_err:
        # Catch other request errors (DNS failure, connection refused, etc.)
        logger.error(f"Network error occurred calling OpenAI.fm API: {req_err}")
        raise req_err # Re-raise
    except Exception as e:
        # Catch any other unexpected errors during the process
        logger.exception(f"An unexpected error occurred in Provider 1 TTS engine: {e}")
        raise e # Re-raise
