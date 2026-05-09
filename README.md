# Atlas Bot — Satellite 05 (Violence)

> *"I don't care who it is — COME AT ME!"*

A Discord bot based on **Atlas**, Vegapunk's Satellite 05 — the embodiment of Violence, raw power, and hot-headedness.

## Commands

| Command | Description |
|---|---|
| `atlas punch @user` | Punch someone (logged in SQLite) |
| `atlas fight @user` | Challenge a user to a fight — fate decides the winner |
| `atlas score` | Show the fight wins and punch leaderboard |
| `atlas rage` | Atlas enters RAGE MODE |
| `atlas smash <thing>` | Atlas smashes something into pieces |
| `atlas siblings` | List all six Vegapunk satellites |
| `atlas?` | Show the help menu with a select dropdown |

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/atlas-bot.git
cd atlas-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your token
```bash
cp .env.example .env
```
Edit `.env` and paste your Discord bot token:
```
DISCORD_TOKEN=your_token_here
```

### 4. Run the bot
```bash
python bot.py
```

## Database

Atlas uses a local SQLite database (`atlas.db`) to store fight records and punch logs. Created automatically on first run.

## Discord Developer Portal Setup

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Create a new application named **Atlas**
3. Go to **Bot** → Create a bot
4. Under **Privileged Gateway Intents**, enable:
   - **Message Content Intent**
   - **Server Members Intent**
5. Copy the token into your `.env`
6. Under **OAuth2 → URL Generator**, select `bot` scope and the following permissions:
   - Send Messages, Embed Links, Read Message History, View Channels

## Cross-bot Awareness

Atlas reacts when sibling satellite names are mentioned in chat (Shaka, Lilith, Edison, Pythagoras, York). For full cross-bot awareness, run all 6 satellite bots in the same server.
