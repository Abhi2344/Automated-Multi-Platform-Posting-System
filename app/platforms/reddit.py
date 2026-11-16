from app.platforms.base import BasePlatform

class RedditPlatform(BasePlatform):
    name = "Reddit"

    async def post(self, message: str) -> tuple[str | None, bool]:
        from app.config import get_settings
        cfg = get_settings()
        self.require_config(REDDIT_ACCESS_TOKEN=cfg.reddit_access_token, REDDIT_SUBREDDIT=cfg.reddit_subreddit)
        async with self.client() as client:
            response = await client.post(
                "https://oauth.reddit.com/api/submit",
                headers={"Authorization": f"Bearer {cfg.reddit_access_token}", "User-Agent": "AutomatedMultiPlatformPostingSystem/1.0"},
                data={"sr": cfg.reddit_subreddit, "kind": "self", "title": cfg.reddit_post_title, "text": message, "resubmit": "true"},
            )
            self.check_response(response)
            payload = response.json()
            errors = payload.get("json", {}).get("errors", [])
            if errors:
                raise RuntimeError(f"Reddit rejected the post: {errors}")
            data = payload.get("json", {}).get("data", {})
            permalink = data.get("url") or data.get("permalink")
            if permalink and permalink.startswith("/"):
                permalink = "https://www.reddit.com" + permalink
            return permalink, bool(permalink)
