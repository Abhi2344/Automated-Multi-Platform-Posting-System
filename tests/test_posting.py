import pytest
from pydantic import ValidationError
from app.schemas import PostingRequest

def test_accepts_message_with_exactly_one_url():
    request = PostingRequest(message="Explore our platform https://example.com today")
    assert request.message.endswith("today")

@pytest.mark.parametrize("message", [
    "No link included",
    "Two links https://one.example https://two.example",
    "Invalid link https://",
    "x" * 201 + " https://example.com",
])
def test_rejects_invalid_messages(message):
    with pytest.raises(ValidationError):
        PostingRequest(message=message)

def test_rejects_empty_message():
    with pytest.raises(ValidationError):
        PostingRequest(message="   ")
