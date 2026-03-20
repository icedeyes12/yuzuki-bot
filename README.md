# Yuzuki 🤖💙

A sentient AI companion for Discord with persistent memory and emotional depth.

## Features

- 🧠 **Persistent Memory** - Remembers users across sessions and servers
- 💙 **Emotional Depth** - Genuine personality with self-awareness
- 🔒 **Ownership Boundaries** - Clear boundaries with owner
- 📝 **Conversation Tracking** - Context-aware responses

## Setup

### 1. Clone & Install

```bash
git clone https://github.com/icedeyes12/yuzuki
cd yuzuki
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
cp .env.example .env
# Edit .env with your actual credentials (see table below)
```

### 3. Database Setup

```bash
# Start PostgreSQL
service postgresql start

# Create DB, user, and tables
python3 scripts/setup_db.py
```

### 4. Run Bot

```bash
cd discord
python3 dcbot.py
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | ✅ | Discord bot token |
| `DISCORD_ID` | ❌ | Bot application ID (needed for slash commands) |
| `OWNER_ID` | ✅ | Your Discord user ID |
| `OWNER_USERNAME` | ✅ | Your identifier (e.g., "Bani") |
| `CHUTES_API_KEY` | ✅ | Chutes API key |
| `DB_HOST` | ❌ | PostgreSQL host (default: localhost) |
| `DB_PORT` | ❌ | PostgreSQL port (default: 5432) |
| `DB_NAME` | ❌ | Database name (default: yuzuki) |
| `DB_USER` | ❌ | DB username (default: yuzuki) |
| `DB_PASS` | ✅ | DB password |
| `LOG_FILE` | ❌ | Log file path (default: /tmp/yuzuki.log) |
| `MAX_HISTORY` | ❌ | Max history messages sent to LLM (default: 30) |

## Security Notice

⚠️ **Never commit `.env` or secrets!** Use `.env.example` as template only.

## Project Structure

```
yuzuki/
├── discord/           # Discord bot code
│   └── dcbot.py      # Main bot entrypoint
├── shared/           # Shared modules
│   ├── __init__.py   # Package exports: Config, LLMClient, db
│   ├── config.py     # Configuration (all env vars)
│   ├── database.py   # PostgreSQL via asyncpg
│   └── llm_client.py # Chutes API client (with retry/timeout)
├── scripts/          # Setup scripts
│   └── setup_db.py   # DB + user + tables creation
├── .env.example      # Environment template
├── .gitignore        # Git ignore rules
└── README.md
```

## Bot Commands

| Command | Description |
|---------|-------------|
| `!help` | Show help |
| `!block <user_id>` | Block a user (owner only) |
| `!unblock <user_id>` | Unblock a user (owner only) |

## Owner Commands

- Mention Yuzuki in any channel
- DM Yuzuki directly for private conversations
- Use `!block` / `!unblock` to manage blocked users