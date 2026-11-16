from app.platforms.base import BasePlatform

class MastodonPlatform(BasePlatform):
    name = "Mastodon"

    async def post(self, message: str) -> tuple[str | None, bool]:
        from app.config import get_settings
        cfg = get_settings()
        self.require_config(MASTODON_BASE_URL=cfg.mastodon_base_url, MASTODON_ACCESS_TOKEN=cfg.mastodon_access_token)
        base = cfg.mastodon_base_url.rstrip("/")
        async with self.client() as client:
            response = await client.post(
                f"{base}/api/v1/statuses",
                headers={"Authorization": f"Bearer {cfg.mastodon_access_token}"},
                json={"status": message, "visibility": "public"},
            )
            self.check_response(response)
            data = response.json()
            return data.get("url"), bool(data.get("url"))
