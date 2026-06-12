# ADAM SMASHER — Discord Bot Setup Guide

Complete guide to setting up the ADAM SMASHER Discord bot for StudEx Global Markets.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Create Discord Application](#create-discord-application)
3. [Get Bot Token](#get-bot-token)
4. [Enable Message Content Intent](#enable-message-content-intent)
5. [Configure Permissions](#configure-permissions)
6. [Invite Bot to Server](#invite-bot-to-server)
7. [Environment Setup](#environment-setup)
8. [Run the Bot](#run-the-bot)
9. [Run with PM2](#run-with-pm2)
10. [Testing Commands](#testing-commands)
11. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.11 or higher
- Discord account
- A Discord server where you have admin rights
- GitHub account (for sync feature)

---

## Create Discord Application

### Step 1: Go to Discord Developer Portal

Navigate to: [https://discord.com/developers/applications](https://discord.com/developers/applications)

### Step 2: Create New Application

1. Click the **"New Application"** button (top right)
2. Enter name: `ADAM SMASHER`
3. Select **Development** as the team (or Personal)
4. Click **Create**

### Step 3: Configure Application

In the General Information tab:

- **Name**: `ADAM SMASHER`
- **Description**: `Global Markets Operating System - StudEx Global Markets`
- **App Icon**: Upload the ADAM logo (optional)

Screenshot reference:
```
┌─────────────────────────────────────────┐
│  Discord Developer Portal               │
│  ─────────────────────────────────────  │
│  ADAM SMASHER                           │
│  General Information                    │
│  ─────────────────────────────────────  │
│  Name: [ADAM SMASHER            ]       │
│  Description: [Global Markets OS...]    │
│  App Icon: [Upload Image]               │
└─────────────────────────────────────────┘
```

---

## Get Bot Token

### Step 1: Navigate to Bot Section

In the left sidebar, click **"Bot"**

### Step 2: Create Bot

1. Click **"Add Bot"** button
2. Confirm by clicking **"Yes, do it!"**

### Step 3: Copy Token

1. Click **"Reset Token"** if this is your first time
2. Click **"Copy"** to copy the token
3. **IMPORTANT**: Save this token securely - it's only shown once!

Screenshot reference:
```
┌─────────────────────────────────────────┐
│  Bot                                    │
│  ─────────────────────────────────────  │
│  BUILD-A-BOT                            │
│  ─────────────────────────────────────  │
│  Token: [████████████████████████] Copy │
│  ─────────────────────────────────────  │
│  ⚠️ Resetting your token will           │
│  immediately invalidate the old token!  │
└─────────────────────────────────────────┘
```

**Token format**: `MTI5XXXXX.XXXXX.XXXXXXXXXXXXXXXXXXXXXXXX`

---

## Enable Message Content Intent

This is **required** for the bot to read commands.

### Step 1: Navigate to OAuth2 → URL Generator

### Step 2: Select Scopes

Check the following:
- ✅ `bot`
- ✅ `applications.commands`

### Step 3: Select Bot Permissions

Check these permissions:
- ✅ Send Messages
- ✅ Send Messages in Threads
- ✅ Embed Links
- ✅ Read Message History
- ✅ Add Reactions
- ✅ Use Slash Commands

### Step 4: Enable Privileged Intents

Back in the Bot section:

1. Scroll down to **"Privileged Gateway Intents"**
2. Enable:
   - ✅ **PRESENCE INTENT** (optional)
   - ✅ **SERVER MEMBERS INTENT** (optional)
   - ✅ **MESSAGE CONTENT INTENT** ⚠️ **REQUIRED**

Screenshot reference:
```
┌─────────────────────────────────────────┐
│  Privileged Gateway Intents             │
│  ─────────────────────────────────────  │
│  PRESENCE INTENT      [Toggle: OFF]     │
│  SERVER MEMBERS...   [Toggle: OFF]     │
│  MESSAGE CONTENT...  [Toggle: ON ] ⚠️   │
│  ─────────────────────────────────────  │
│  These are sensitive - enable only      │
│  what your bot needs                    │
└─────────────────────────────────────────┘
```

---

## Configure Permissions

### In OAuth2 → URL Generator

Generate an invite URL with these bot permissions:

```
📌 Permissions Integer: 6745459712
```

Or manually select:
- ✅ Send Messages
- ✅ Send TTS Messages
- ✅ Embed Links
- ✅ Attach Files
- ✅ Read Message History
- ✅ Add Reactions
- ✅ Use Slash Commands
- ✅ Manage Threads
- ✅ Connect (Voice)
- ✅ Speak (Voice)

---

## Invite Bot to Server

### Step 1: Generate Invite Link

1. Go to **OAuth2 → URL Generator**
2. Select scopes: `bot` and `applications.commands`
3. Select permissions (see above)
4. Copy the generated URL

### Step 2: Authorize

1. Open the invite URL in your browser
2. Select your Discord server
3. Click **"Authorize"**
4. Complete any CAPTCHA

Screenshot reference:
```
┌─────────────────────────────────────────┐
│  Authorize ADAM SMASHER                 │
│  ─────────────────────────────────────  │
│  [Select a server         ▼]            │
│  ─────────────────────────────────────  │
│ studex-global-markets                   │
│  ─────────────────────────────────────  │
│  Bot will be able to:                   │
│  • Read messages                        │
│  • Send messages                        │
│  • Manage channels                      │
│  ─────────────────────────────────────  │
│  [Authorize]                            │
└─────────────────────────────────────────┘
```

### Step 3: Verify Installation

The bot should appear in your server with status **"Online"** (green dot).

---

## Environment Setup

### Step 1: Navigate to Bot Directory

```bash
cd /workspace/adam-tools/discord-bot
```

### Step 2: Create .env File

```bash
cp .env.example .env
```

### Step 3: Edit .env File

```bash
nano .env  # or use your preferred editor
```

Configure the following:

```env
# REQUIRED - Bot Token from Discord Developer Portal
DISCORD_BOT_TOKEN=MTI5XXXXX.XXXXX.XXXXXXXXXXXXXXXXXXXXXXXX

# REQUIRED - Your Discord User ID (for authorization)
# Find your ID: Enable Developer Mode in Discord → Right-click your name → Copy ID
ALLOWED_USER_IDS=123456789012345678

# OPTIONAL - Channel IDs for automated posts
# Right-click a channel with Developer Mode enabled → Copy ID
DISCORD_HOME_CHANNEL_ID=123456789012345678
DISCORD_TRADES_CHANNEL_ID=123456789012345679

# OPTIONAL - GitHub Configuration
GITHUB_TOKEN=ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
GITHUB_REPO=TumeloRamaphosa/adam-tools

# OPTIONAL - Alert Thresholds
USDZAR_ALERT_THRESHOLD=18.50
RUBZAR_MOVE_THRESHOLD=0.01

# OPTIONAL - Webhook Server
WEBHOOK_SERVER_URL=http://localhost:5000
```

### Finding Your Discord User ID

1. Enable Developer Mode: Settings → Advanced → Developer Mode → ON
2. Right-click on your username in Discord
3. Select **"Copy User ID"**

### Finding Channel IDs

1. Enable Developer Mode (same as above)
2. Right-click on any channel
3. Select **"Copy Channel ID"**

---

## Run the Bot

### Option 1: Direct Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

### Option 2: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run
python bot.py
```

### Expected Output

```
2026-06-12 03:00:00 [ADAM] INFO: Starting ADAM SMASHER v2.0 Enhanced Discord Bot...
2026-06-12 03:00:00 [ADAM] INFO: Market monitor: Enabled (checks every 60 minutes)
2026-06-12 03:00:00 [ADAM] INFO: USD/ZAR threshold alert: 18.50
2026-06-12 03:00:00 [ADAM] INFO: RUB/ZAR move threshold: 1.0%
2026-06-12 03:00:00 [ADAM] INFO: ADAM SMASHER v2.0 is online! Logged in as ADAM SMASHER#1234
2026-06-12 03:00:00 [ADAM] INFO: Bot ID: 123456789012345678
```

---

## Run with PM2

PM2 keeps the bot running 24/7 and auto-restarts on crashes.

### Step 1: Install PM2

```bash
npm install -g pm2
```

### Step 2: Create Ecosystem File

Create `ecosystem.config.js`:

```javascript
module.exports = {
  apps: [{
    name: 'adam-smasher',
    script: 'bot.py',
    interpreter: 'python3',
    watch: false,
    autorestart: true,
    max_restarts: 10,
    min_uptime: '10s',
    error_file: 'logs/error.log',
    out_file: 'logs/out.log',
    time: true,
    env: {
      DISCORD_BOT_TOKEN: process.env.DISCORD_BOT_TOKEN,
      ALLOWED_USER_IDS: process.env.ALLOWED_USER_IDS,
      DISCORD_HOME_CHANNEL_ID: process.env.DISCORD_HOME_CHANNEL_ID,
      DISCORD_TRADES_CHANNEL_ID: process.env.DISCORD_TRADES_CHANNEL_ID,
      GITHUB_TOKEN: process.env.GITHUB_TOKEN,
      GITHUB_REPO: process.env.GITHUB_REPO
    }
  }]
};
```

### Step 3: Create Logs Directory

```bash
mkdir -p logs
```

### Step 4: Start with PM2

```bash
# Start
pm2 start ecosystem.config.js

# Save process list (auto-restart on reboot)
pm2 save

# Setup startup script
pm2 startup
```

### PM2 Commands

```bash
pm2 status              # Check status
pm2 logs adam-smasher   # View logs
pm2 restart adam-smasher  # Restart bot
pm2 stop adam-smasher   # Stop bot
pm2 delete adam-smasher # Remove from PM2
```

---

## Testing Commands

### In Discord, type these commands:

| Command | Description | Expected Response |
|---------|-------------|-------------------|
| `@ADAM help` | Show all commands | Command list embed |
| `@ADAM status` | System status | Status panel |
| `@ADAM markets` | Market data | Market prices |
| `@ADAM trade BUY 1000 SA-RUB @ 0.205` | Log trade | Trade confirmation |
| `@ADAM meeting Q1 Review` | Schedule meeting | Meeting confirmation |
| `@ADAM alert USDZAR > 18.50` | Set alert | Alert confirmation |
| `@ADAM sync` | Sync to GitHub | Sync status |
| `@ADAM me` | Your profile | User info |
| `@ADAM idea` | View trade ideas | Trade list |
| `@ADAM dm @User Hello!` | Send DM | DM confirmation |
| `@ADAM broadcast #general #alerts Hello!` | Broadcast | Broadcast status |

### Test Alert System

```bash
# Trigger manual market check
# The bot checks every hour automatically
```

### Test GitHub Sync

```bash
@ADAM sync meetings
```

---

## Webhook Server Setup

The webhook server receives events from Discord and stores messages for the HTML panel.

### Step 1: Start Webhook Server

```bash
python webhook_server.py
```

### Step 2: Access Dashboard

Open: `http://localhost:5000`

### Step 3: Configure Discord Webhook (Optional)

For receiving events without the bot running:

1. In Discord: Server Settings → Integrations → Webhooks
2. Create new webhook
3. Copy webhook URL
4. Paste in webhook server dashboard

---

## Troubleshooting

### Bot Not Responding

**Problem**: Bot is online but doesn't respond to commands.

**Solutions**:
1. ✅ Check Message Content Intent is enabled
2. ✅ Verify bot token is correct in .env
3. ✅ Make sure user ID is in ALLOWED_USER_IDS
4. ✅ Bot needs to be mentioned (`@ADAM help`)

### "Not Authorized" Error

**Problem**: Getting access denied message.

**Solutions**:
1. Check your Discord User ID is in ALLOWED_USER_IDS
2. Format: `ALLOWED_USER_IDS=123456789,987654321` (comma-separated)
3. Restart bot after changing .env

### Import Errors

**Problem**: `ModuleNotFoundError` when starting

**Solutions**:
```bash
pip install -r requirements.txt
```

### Token Invalid

**Problem**: `discord.errors.LoginFailure`

**Solutions**:
1. Reset token in Discord Developer Portal
2. Update DISCORD_BOT_TOKEN in .env
3. Make sure there are no spaces or quotes around the token

### Bot Goes Offline

**Problem**: Bot disconnects after running

**Solutions**:
1. Use PM2 for auto-restart
2. Check logs: `pm2 logs adam-smasher`
3. Ensure stable internet connection

### Permissions Error

**Problem**: Bot can't send messages

**Solutions**:
1. Re-invite bot with correct permissions
2. Check channel permissions (bot may be blocked)
3. Ensure bot role is above member roles

### Market Alerts Not Working

**Problem**: No automatic alerts

**Solutions**:
1. Bot must be running 24/7 (use PM2)
2. Check thresholds in .env
3. Alerts post to HOME_CHANNEL_ID

---

## File Structure

```
discord-bot/
├── bot.py              # Main bot file
├── webhook_server.py   # Webhook receiver
├── .env                # Configuration (create from .env.example)
├── .env.example        # Template for .env
├── state.json          # Persistent state (auto-created)
├── messages.json       # Stored messages (auto-created)
├── requirements.txt    # Python dependencies
├── ecosystem.config.js # PM2 config
└── SETUP.md           # This file
```

---

## Support

For issues or questions:
- Discord: discord.gg/CMVBmDQ5Fj
- GitHub Issues: github.com/TumeloRamaphosa/adam-tools/issues

---

**ADAM SMASHER v2.0** — Built for Tumelo Ramaphosa | StudEx Global Markets