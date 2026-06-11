# ADAM SMASHER — Discord Bot Setup Guide

## Quick Setup (5 minutes)

### Step 1: Create Discord Bot
1. Go to https://discord.com/developers/applications
2. Click "New Application" → Name it "ADAM SMASHER"
3. Go to "Bot" section → Click "Add Bot"
4. Under "Token", click "Reset Token" → **COPY AND SAVE IT NOW** (you won't see it again)
5. Scroll down to "Privileged Gateway Intents":
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ PRESENCE INTENT

### Step 2: Get Your User ID
1. In Discord, enable Developer Mode (Settings → Advanced → Developer Mode)
2. Right-click your profile → "Copy User ID"
3. Save this number

### Step 3: Get Your Channel ID
1. In Discord, right-click your target channel → "Copy Channel ID"
2. This is where ADAM will send system notifications

### Step 4: Invite Bot to Server
1. Go to OAuth2 → URL Generator
2. Scopes: ✅ bot, ✅ applications.commands
3. Bot Permissions: Administrator
4. Copy the generated URL → open in browser → select your server

### Step 5: Configure & Run
```bash
# Navigate to bot folder
cd /workspace/adam-tools/discord-bot

# Copy and edit .env
cp .env.example .env
nano .env   # fill in your values

# Run the bot
python3 bot.py
```

### Step 6: Keep Bot Running (PM2)
```bash
# Install PM2
npm install -g pm2

# Start bot with PM2 (runs in background)
pm2 start bot.py --name adam-smasher

# Check status
pm2 status

# View logs
pm2 logs adam-smasher

# Restart after reboot
pm2 save
pm2 startup
```

## Bot Commands

| Command | Description |
|---------|-------------|
| `@ADAM help` | Show all commands |
| `@ADAM status` | Get system status |
| `@ADAM markets` | Get market data |
| `@ADAM trade [idea]` | Log a trade idea |
| `@ADAM meeting [title]` | Schedule a meeting |
| `@ADAM research [topic]` | Start Mirofish research |
| `@ADAM alert [condition]` | Set price alert |
| `@ADAM sync` | Sync to Obsidian/AgentMail |
| `@ADAM me` | Your user profile |
| `@ADAM events` | Upcoming events |
| `@ADAM idea` | View trade ideas |

## Troubleshooting

**Bot not responding?**
- Check the bot has MESSAGE CONTENT INTENT enabled
- Verify the bot is online (green dot in Discord)
- Check .env has correct DISCORD_BOT_TOKEN

**"Access Denied" errors?**
- Make sure your Discord User ID is in ALLOWED_USER_IDS
- Separate multiple IDs with commas

**Bot goes offline?**
- Use PM2 to keep it running: `pm2 start bot.py --name adam-smasher`
- Check logs: `pm2 logs adam-smasher`

## Running on Daytona (when token is fixed)
```bash
# Clone your repo to Daytona
git clone https://github.com/TumeloRamaphosa/adam-tools.git
cd adam-tools/discord-bot

# Install dependencies
pip install discord.py python-dotenv aiohttp

# Run
python3 bot.py
```

## Architecture

```
Discord Server
    │
    ├── @ADAM help        → Shows command reference
    ├── @ADAM status      → System status (Daytona, Obsidian, AgentMail)
    ├── @ADAM markets     → Real-time market data
    ├── @ADAM trade       → Logs trade ideas → GitHub
    ├── @ADAM meeting     → Schedules meetings → Obsidian
    ├── @ADAM research    → Triggers Mirofish + AutoResearch
    ├── @ADAM sync        → Syncs data to all services
    │
    └── DM to bot         → Auto-responds with help

ADAM SMASHER also monitors:
    ├── Trade Week events
    ├── Market alerts
    ├── Meeting schedules
    └── Meat business opportunities
```