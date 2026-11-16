from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    request_timeout_seconds: float = 20.0
    bluesky_identifier: str | None = None
    bluesky_app_password: str | None = None
    bluesky_pds_url: str = "https://bsky.social"
    mastodon_base_url: str | None = None
    mastodon_access_token: str | None = None
    reddit_access_token: str | None = None
    reddit_subreddit: str | None = None
    reddit_post_title: str = "Update"
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    telegram_channel_username: str | None = None
    discord_webhook_url: str | None = None
    discord_guild_id: str | None = None
    discord_channel_id: str | None = None
    discord_public_access: bool = False

@lru_cache
def get_settings() -> Settings:
    return Settings()
