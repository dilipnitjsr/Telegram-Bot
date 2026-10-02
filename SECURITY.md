# Security

This repository is public. Never commit Telegram bot tokens, database credentials, chat IDs, exported user lists, or production database files.

## Previously exposed Telegram token

An older revision contained a Telegram bot token in source code. Treat that token as compromised even though the current branch removes it.

Rotate the bot token using BotFather before reusing this project:

1. Revoke the old token.
2. Generate a new token.
3. Store the replacement only in the runtime environment as `TELEGRAM_BOT_TOKEN`.
4. Confirm the old token no longer works.

## Database privacy

The repository previously tracked `db.sqlite3`. Telegram chat IDs, usernames, names, or registration records are personal data and must not be committed to a public repository.

Use a private production database and a least-privilege database account. Store credentials in environment variables only.

## Required environment variables

See `.env.example`. Real values belong in the deployment platform's secret store or a local ignored `.env` file.

## Legacy dependencies

The project was originally built for Python 3.6 and an old python-telegram-bot API. Security hardening of credentials does not make that dependency stack current. Migrate the bot to a supported Python and python-telegram-bot release before production deployment.
