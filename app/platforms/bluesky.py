from datetime import datetime, timezone
from app.platforms.base import BasePlatform

class BlueskyPlatform(BasePlatform):
    name = "Bluesky"

    async def post(self, message: str) -> tuple[str | None, bool]:
        from app.config import get_settings
        cfg = get_settings()
        self.require_config(BLUESKY_IDENTIFIER=cfg.bluesky_identifier, BLUESKY_APP_PASSWORD=cfg.bluesky_app_password)
        base = cfg.bluesky_pds_url.rstrip("/")
        async with self.client() as client:
            auth = await client.post(
                f"{base}/xrpc/com.atproto.server.createSession",
                json={"identifier": cfg.bluesky_identifier, "password": cfg.bluesky_app_password},
            )
            self.check_response(auth)
            session = auth.json()
            record = {
                "$type": "app.bsky.feed.post",
                "text": message,
                "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            }
            response = await client.post(
                f"{base}/xrpc/com.atproto.repo.createRecord",
                headers={"Authorization": f"Bearer {session['accessJwt']}"},
                json={"repo": session["did"], "collection": "app.bsky.feed.post", "record": record},
            )
            self.check_response(response)
            data = response.json()
            rkey = data["uri"].rsplit("/", 1)[-1]
            handle = session.get("handle") or cfg.bluesky_identifier
            return f"https://bsky.app/profile/{handle}/post/{rkey}", True
