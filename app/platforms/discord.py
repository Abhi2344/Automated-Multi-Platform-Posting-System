from app.platforms.base import BasePlatform

class DiscordPlatform(BasePlatform):
    name = "Discord"

    async def post(self, message: str) -> tuple[str | None, bool]:
        from app.config import get_settings
        cfg = get_settings()
        self.require_config(DISCORD_WEBHOOK_URL=cfg.discord_webhook_url)
        separator = "&" if "?" in cfg.discord_webhook_url else "?"
        async with self.client() as client:
            response = await client.post(f"{cfg.discord_webhook_url}{separator}wait=true", json={"content": message})
            self.check_response(response)
            data = response.json()
            url = None
            if cfg.discord_guild_id and cfg.discord_channel_id and data.get("id"):
                url = f"https://discord.com/channels/{cfg.discord_guild_id}/{cfg.discord_channel_id}/{data['id']}"
            return url, bool(url and cfg.discord_public_access)
