# Automated Multi-Platform Posting System

A FastAPI service that accepts one short message containing exactly one CTA URL and attempts to publish it independently to five platforms.

## Platforms

| Platform | API | Required configuration |
|---|---|---|
| Bluesky | AT Protocol XRPC | BLUESKY_IDENTIFIER, BLUESKY_APP_PASSWORD |
| Mastodon | Mastodon REST API | MASTODON_BASE_URL, MASTODON_ACCESS_TOKEN |
| Reddit | Reddit OAuth API | REDDIT_ACCESS_TOKEN, REDDIT_SUBREDDIT |
| Telegram | Telegram Bot API | TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID |
| Discord | Discord Webhook API | DISCORD_WEBHOOK_URL |

Each integration is isolated. A failed or unconfigured platform does not prevent attempts on the other platforms. Credentials are read from environment variables and must never be committed.

## Requirements

- Python 3.10+
- API credentials for each platform you want to enable

## Setup

~~~bash
git clone https://github.com/Abhi2344/Automated-Multi-Platform-Posting-System.git
cd Automated-Multi-Platform-Posting-System
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
~~~

Copy .env.example to .env and fill in the credentials for the platforms you want to use.

~~~bash
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
~~~

Open http://localhost:4000/docs for interactive API documentation. Health check: http://localhost:4000/health.

## API

### POST /posting

Request:

~~~json
{
  "message": "Check out our latest business platform https://example.com"
}
~~~

Rules:
- Message must contain 1–200 characters.
- Exactly one HTTP or HTTPS URL is required.
- Platform selection is internal; clients cannot select destinations.

The endpoint returns one result per platform. Top-level success is true when at least one platform succeeds. Successful platforms include the returned post URL (when available), public-access indicator, and UTC date/time. Failed platforms include an error message and do not stop other integrations.

## Platform setup notes

- **Bluesky:** Create an app password in account settings. The app password is used to create a session and publish a feed record.
- **Mastodon:** Create an application on your Mastodon instance and use an access token with permission to write statuses. Posts are requested with public visibility.
- **Reddit:** Use Reddit OAuth with the submit scope. Set a subreddit you are allowed to post in. Moderation, subreddit rules, and account restrictions can still reject submissions.
- **Telegram:** Add your bot to the target chat/channel and grant posting permission. For a public channel URL, set TELEGRAM_CHANNEL_USERNAME without the @ sign. Private destinations do not have a public URL.
- **Discord:** Create a webhook in the destination channel. A Discord message URL is returned only when guild and channel IDs are configured. DISCORD_PUBLIC_ACCESS defaults to false because channel visibility cannot be inferred from a webhook response.

Official API documentation:
- [Bluesky AT Protocol](https://docs.bsky.app/)
- [Mastodon API](https://docs.joinmastodon.org/methods/statuses/)
- [Reddit API](https://www.reddit.com/dev/api/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Discord Webhooks](https://discord.com/developers/docs/resources/webhook)

## Run tests

~~~bash
pytest -q
~~~

## Security and limitations

- Never commit .env, access tokens, app passwords, or webhook URLs.
- Use dedicated app credentials and minimum permissions.
- A successful API response confirms that the provider accepted the post; public visibility can depend on account, channel, subreddit, moderation, and privacy settings.
- This version makes one publishing attempt per platform per request. It does not implement retries, scheduling, persistent audit storage, or duplicate-post prevention.
