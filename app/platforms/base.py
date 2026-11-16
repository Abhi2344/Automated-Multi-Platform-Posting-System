from abc import ABC, abstractmethod
import httpx

class BasePlatform(ABC):
    name: str

    def __init__(self, timeout: float = 20.0):
        self.timeout = timeout

    @abstractmethod
    async def post(self, message: str) -> tuple[str | None, bool]:
        """Publish a message and return its URL and public-access flag."""

    def client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=self.timeout, follow_redirects=True)

    @staticmethod
    def require_config(**values: str | None) -> None:
        missing = [name for name, value in values.items() if not value]
        if missing:
            raise RuntimeError("Missing configuration: " + ", ".join(missing))

    @staticmethod
    def check_response(response: httpx.Response) -> None:
        if response.is_error:
            detail = response.text[:500] or response.reason_phrase
            raise RuntimeError(f"HTTP {response.status_code}: {detail}")
