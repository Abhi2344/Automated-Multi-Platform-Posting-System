from app.platforms.base import BasePlatform

class TelegramPlatform(BasePlatform):
    name = "Telegram"

    async def post(self, message: str) -> tuple[str | None, bool]:
        from app.config import get_settings
        cfg = get_settings()
        self.require_config(TELEGRAM_BOT_TOKEN=cfg.telegram_bot_token, TELEGRAM_CHAT_ID=cfg.telegram_chat_id)
        async with self.client() as client:
            response = await client.post(
                f"https://api.telegram.org/bot{cfg.telegram_bot_token}/sendMessage",
                json={"chat_id": cfg.telegram_chat_id, "text": message, "link_preview_options": {"is_disabled": False}},
            )
            self.check_response(response)
            payload = response.json()
            if not payload.get("ok"):
                raise RuntimeError(payload.get("description", "Telegram API returned an unsuccessful response."))
            result = payload["result"]
            username = (cfg.telegram_channel_username or "").lstrip("@")
            url = f"https://t.me/{username}/{result['message_id']}" if username else None
            return url, bool(url)
