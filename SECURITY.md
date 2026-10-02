# Security

This repository is public. Never commit Telegram bot tokens, database credentials, chat IDs, exported user lists, or production database files.

## Previously exposed credentials and user data

Historical revisions contained:

- a Telegram bot token;
- database connection credentials;
- Telegram chat IDs/usernames in generated CSV files;
- a tracked SQLite database.

Treat the historical Telegram token and database credentials as compromised even though the current branch removes them.

Before reusing this project:

1. Revoke the old Telegram token with BotFather and generate a new token.
2. Rotate/delete the historical database user/password; create a new least-privilege application database account.
3. Store replacement values only in runtime environment variables.
4. Confirm the old Telegram token and database credentials no longer work.
5. Review Telegram/database provider logs where available for unexpected historical access.

## Database privacy

Telegram chat IDs, usernames, names, and registration records are personal data and must not be committed to a public repository.

Use a private production database and a least-privilege database account. Local SQLite databases and generated CSV files are ignored by Git.

## Required environment variables

See `.env.example`. Real values belong in the deployment platform's secret store or a local ignored `.env` file.

## Legacy dependencies

The project was originally built for Python 3.6 and an old python-telegram-bot API. Security hardening of credentials does not make that dependency stack current. Migrate the bot to a supported Python and python-telegram-bot release before production deployment.
