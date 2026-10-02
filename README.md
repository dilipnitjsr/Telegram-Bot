# Telegram Bot Manager

Legacy Telegram bot manager for registration, scheduled messaging, and database-backed search.

> **Security notice:** this repository originally dates from 2018. A historical revision contained a Telegram bot token and the repository also tracked a local SQLite database. Rotate the historical bot token before reuse and do not commit user/chat databases.

## Configuration

Copy the example configuration for local development:

```bash
cp .env.example .env
```

Provide these values through your runtime environment:

```text
TELEGRAM_BOT_TOKEN
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

The active SQL-backed implementation is `core/chatapp.py`.

## Current security controls

- Telegram and database credentials are loaded from environment variables.
- Database search input uses parameterized SQL.
- Dynamic profile-field updates are limited to an explicit allow-list.
- Message delivery retries are bounded.
- Registration logging avoids printing names and Telegram IDs.
- Local databases, generated CSV user lists, and environment files are ignored by Git.

See [SECURITY.md](SECURITY.md) before deployment.

## Legacy runtime

The project currently uses an old python-telegram-bot API and an obsolete Python runtime declaration. A separate modernization pass is recommended before production deployment.

## Functional overview

The bot provides:

1. User registration.
2. Scheduled Telegram messages.
3. Database-backed keyword search.
4. Group/private chat list management.

The original API examples remain available in the Git history for reference.
