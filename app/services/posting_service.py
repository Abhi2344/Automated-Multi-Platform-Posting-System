import asyncio
from datetime import datetime, timezone
from app.config import get_settings
from app.platforms.bluesky import BlueskyPlatform
from app.platforms.discord import DiscordPlatform
from app.platforms.mastodon import MastodonPlatform
from app.platforms.reddit import RedditPlatform
from app.platforms.telegram import TelegramPlatform
from app.schemas import PlatformResult

def get_platforms():
    timeout = get_settings().request_timeout_seconds
    return [BlueskyPlatform(timeout), MastodonPlatform(timeout), RedditPlatform(timeout), TelegramPlatform(timeout), DiscordPlatform(timeout)]

async def post_to_platform(platform, message: str) -> PlatformResult:
    try:
        posted_url, public_access = await platform.post(message)
        now = datetime.now(timezone.utc)
        return PlatformResult(platform=platform.name, status="success", posted_url=posted_url, public_access=public_access, date=now.date().isoformat(), time=now.time().replace(tzinfo=None, microsecond=0).isoformat(), error=None)
    except Exception as exc:
        return PlatformResult(platform=platform.name, status="failed", posted_url=None, public_access=False, date=None, time=None, error=str(exc)[:500])

async def publish_message(message: str) -> list[PlatformResult]:
    platforms = get_platforms()
    return await asyncio.gather(*(post_to_platform(platform, message) for platform in platforms))
