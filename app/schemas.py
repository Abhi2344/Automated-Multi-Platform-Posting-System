import re
from urllib.parse import urlsplit
from pydantic import BaseModel, ConfigDict, Field, field_validator

URL_PATTERN = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
TRAILING_URL_PUNCTUATION = ".,!?;:)]}"

def extract_single_url(message: str) -> str:
    matches = URL_PATTERN.findall(message)
    if len(matches) != 1:
        raise ValueError("Message must contain exactly one HTTP or HTTPS CTA link.")
    url = matches[0].rstrip(TRAILING_URL_PUNCTUATION)
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("The CTA link must be a valid HTTP or HTTPS URL.")
    if any(char.isspace() for char in url):
        raise ValueError("The CTA URL must not contain whitespace.")
    return url

class PostingRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    message: str = Field(min_length=1, max_length=200, description="Text with exactly one HTTP(S) CTA link.")

    @field_validator("message")
    @classmethod
    def validate_cta_link(cls, value: str) -> str:
        extract_single_url(value)
        return value

class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: str | None = None
    public_access: bool = False
    date: str | None = None
    time: str | None = None
    error: str | None = None

class PostingResponse(BaseModel):
    success: bool
    results: list[PlatformResult]
