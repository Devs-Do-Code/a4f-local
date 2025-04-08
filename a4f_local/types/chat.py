from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal

# Placeholder models based loosely on OpenAI's Chat Completion API
# These should be refined when implementing a chat provider.

class ChatCompletionMessageParam(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str | List[Dict[str, Any]] # Content can be string or complex (e.g., for vision)
    # name: Optional[str] = None # Optional name for tool/assistant roles
    # tool_call_id: Optional[str] = None # For tool responses

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatCompletionMessageParam]
    # Add other common parameters like temperature, max_tokens, stream, etc. as needed
    temperature: Optional[float] = Field(default=1.0)
    max_tokens: Optional[int] = None
    stream: Optional[bool] = Field(default=False)

    class Config:
        extra = 'allow' # Allow provider-specific params

# Placeholder for the response structure
class ChoiceDelta(BaseModel):
    content: Optional[str] = None
    role: Optional[Literal["assistant"]] = None
    # tool_calls: Optional[List[Any]] = None # Placeholder

class Choice(BaseModel):
    index: int
    message: Optional[ChatCompletionMessageParam] = None # For non-streaming
    delta: Optional[ChoiceDelta] = None # For streaming
    finish_reason: Optional[str] = None

class ChatCompletion(BaseModel):
    id: str
    object: Literal["chat.completion", "chat.completion.chunk"]
    created: int
    model: str
    choices: List[Choice]
    # usage: Optional[CompletionUsage] = None # Placeholder for token usage info

    class Config:
        extra = 'allow'
