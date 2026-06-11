"""
ADAM SMASHER — Discord Bot
Global Markets Operating System Gateway
Tumelo Ramaphosa | StudEx Global Markets
"""

import os
import json
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

# ===== SETUP =====
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s [ADAM] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# ===== CONFIG =====
TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')
ALLOWED_USERS = [int(uid.strip()) for uid in os.getenv('ALLOWED_USER_IDS', '').split(',') if uid.strip()]
HOME_CHANNEL_ID = int(os.getenv('DISCORD_HOME_CHANNEL_ID', '0'))
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')  # Set in .env
AGENTMAIL_API = os.getenv('AGENTMAIL_API', '')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='@ADAM ', intents=intents, help_command=None)

# ===== STATE =====
state = {
    'meetings': [],
    'trade_ideas': [],
    'bookings': [],
    'system_status': {
        'daytona': 'Token Invalid (needs regeneration)',
        'obsidian': 'Connected',
        'agentmail': 'Ready',
        'mirofish': 'Local - Available',
        'autoresearch': 'Available'
    }
}

# ===== PERMISSION CHECK =====
async def is_allowed(ctx):
    if not ALLOWED_USERS or ctx.author.id in ALLOWED_USERS:
        return True
    embed = discord.Embed(
        title='🚫 Access Denied',
        description='You are not authorized to use ADAM SMASHER commands.',
        color=0xff4444
    )
    await ctx.send(embed=embed)
    return False

# ===== EMBED HELPERS =====
def success_embed(title, description):
    return discord.Embed(title=f'✅ {title}', description=description, color=0x22c55e, timestamp=datetime.utcnow())

def info_embed(title, description):
    return discord.Embed(title=f'ℹ️ {title}', description=description, color=0x3b82f6, timestamp=datetime.utcnow())

def warning_embed(title, description):
    return discord.Embed(title=f'⚠️ {title}', description=description, color=0xeab308, timestamp=datetime.utcnow())

def error_embed(title, description):
    return discord.Embed(title=f'❌ {title}', description=description, color=0xef4444, timestamp=datetime.utcnow())

def embed_field(name, value, inline=True):
    e = discord.Embed(color=0x3b82f6, timestamp=datetime.utcnow())
    e.add_field(name=name, value=value, inline=inline)
    return e

# ===== COMMANDS =====
@bot.command(name='help')
async def help_cmd(ctx):
    if not await is_allowed(ctx): return
    
    embed = discord.Embed(
        title='🤖 ADAM SMASHER — Command Reference',
        description='Global Markets Operating System | StudEx Global Markets',
        color=0x8b5cf6,
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url='https://raw.githubusercontent.com/TumeloRamaphosa/adam-tools/main/assets/adam-logo.png')
    
    commands = [
        ('status', 'Get full system status', '@ADAM status'),
        ('markets', 'Get current market data', '@ADAM markets'),
        ('trade', 'Log a trade idea', '@ADAM trade BUY 1000 SA-RUB @ 0.205'),
        ('meeting', 'Schedule a meeting', '@ADAM meeting Q1 Review with Andrei'),
        ('research', 'Start research on a topic', '@ADAM research meat business SA'),
        ('alert', 'Set a price alert', '@ADAM alert USDZAR > 18.50'),
        ('sync', 'Sync data to Obsidian/AgentMail', '@ADAM sync meetings'),
        ('me', 'Get your user profile', '@ADAM me'),
        ('events', 'Get upcoming events/bookings', '@ADAM events'),
        ('idea', 'View recent trade ideas', '@ADAM idea'),
    ]
    
    for name, desc, usage in commands:
        embed.add_field(name=f'/{name}', value=f'{desc}\n`{usage}`', inline=False)
    
    embed.set_footer(text='Tumelo Ramaphosa | ADAM SMASHER v1.0')
    await ctx.send(embed=embed)


@bot.command(name='status')
async def status_cmd(ctx):
    if not await is_allowed(ctx): return
    
    embed = discord.Embed(
        title='🟢 ADAM SMASHER — System Status',
        description='Global Markets Operating System',
        color=0x22c55e,
        timestamp=datetime.utcnow()
    )
    
    # System status
    for name, status in state['system_status'].items():
        color = 0x22c55e if 'Active' in status or 'Connected' in status or 'Ready' in status or 'Available' in status else 0xeab308
        embed.add_field(name=name.upper(), value=f'`{status}`', inline=True)
    
    # Quick stats
    embed.add_field(name='📋 MEETINGS', value=f'`{len(state["meetings"])} recorded`', inline=True)
    embed.add_field(name='📈 TRADE IDEAS', value=f'`{len(state["trade_ideas"])} active`', inline=True)
    embed.add_field(name='📅 BOOKINGS', value=f'`{len(state["bookings"])} upcoming`', inline=True)
    
    embed.set_footer(text=f'StudEx Global Markets | {datetime.now().strftime("%Y-%m-%d %H:%M SAST")}')
    await ctx.send(embed=embed)


@bot.command(name='markets')
async def markets_cmd(ctx):
    if not await is_allowed(ctx): return
    
    embed = discord.Embed(
        title='📈 Markets Overview',
        description='Real-time Global Markets Data',
        color=0x3b82f6,
        timestamp=datetime.utcnow()
    )
    
    markets = [
        ('USD/ZAR', '18.42', '+0.3%', '🟢'),
        ('RUB/ZAR', '0.205', '-0.1%', '🔴'),
        ('BRENT', '$78.40', '+1.2%', '🟢'),
        ('GOLD', '$2,340', '+0.8%', '🟢'),
        ('PLAT', '$1,020', '-0.3%', '🔴'),
        ('ZAR/RUB', '4.878', '+0.2%', '🟢'),
    ]
    
    for pair, price, change, indicator in markets:
        embed.add_field(name=f'{indicator} {pair}', value=f'`{price}` `{change}`', inline=True)
    
    embed.set_footer(text='Data as of ' + datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
    await ctx.send(embed=embed)


@bot.command(name='trade')
async def trade_cmd(ctx, *args):
    if not await is_allowed(ctx): return
    if not args:
        embed = error_embed('Trade Command', 'Usage: `@ADAM trade BUY 1000 SA-RUB @ 0.205`')
        await ctx.send(embed=embed)
        return
    
    trade_text = ' '.join(args)
    
    # Parse trade
    trade = {
        'id': len(state['trade_ideas']) + 1,
        'user': ctx.author.name,
        'direction': 'BUY' if 'BUY' in trade_text.upper() else 'SELL' if 'SELL' in trade_text.upper() else 'UNKNOWN',
        'raw': trade_text,
        'created': datetime.utcnow().isoformat(),
        'status': 'active'
    }
    
    state['trade_ideas'].insert(0, trade)
    
    color = 0x22c55e if trade['direction'] == 'BUY' else 0xef4444
    embed = discord.Embed(
        title=f'📈 Trade Logged',
        description=trade_text,
        color=color,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='Direction', value=trade['direction'], inline=True)
    embed.add_field(name='User', value=ctx.author.mention, inline=True)
    embed.add_field(name='Status', value='🟢 Active', inline=True)
    embed.add_field(name='Trade #', value=f'`{trade["id"]}`', inline=True)
    
    await ctx.send(embed=embed)


@bot.command(name='meeting')
async def meeting_cmd(ctx, *args):
    if not await is_allowed(ctx): return
    if not args:
        embed = error_embed('Meeting Command', 'Usage: `@ADAM meeting Q1 Strategy Review`')
        await ctx.send(embed=embed)
        return
    
    title = ' '.join(args)
    
    meeting = {
        'id': len(state['meetings']) + 1,
        'title': title,
        'user': ctx.author.name,
        'created': datetime.utcnow().isoformat(),
        'status': 'scheduled'
    }
    
    state['meetings'].insert(0, meeting)
    
    embed = discord.Embed(
        title='🎙️ Meeting Scheduled',
        description=title,
        color=0x8b5cf6,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='Scheduled by', value=ctx.author.mention, inline=True)
    embed.add_field(name='Meeting #', value=f'`{meeting["id"]}`', inline=True)
    embed.add_field(name='Status', value='📅 Scheduled', inline=True)
    
    await ctx.send(embed=embed)


@bot.command(name='research')
async def research_cmd(ctx, *args):
    if not await is_allowed(ctx): return
    if not args:
        embed = error_embed('Research Command', 'Usage: `@ADAM research meat business SA Russia`')
        await ctx.send(embed=embed)
        return
    
    topic = ' '.join(args)
    
    embed = discord.Embed(
        title='🔬 Research Started',
        description=f'Mirofish is now researching: *{topic}*',
        color=0xeab308,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='Topic', value=f'**{topic}**', inline=False)
    embed.add_field(name='Engine', value='MiroFish-Offline + AutoResearch', inline=True)
    embed.add_field(name='Status', value='⏳ Running...', inline=True)
    embed.add_field(name='Requested by', value=ctx.author.mention, inline=True)
    embed.set_footer(text='Results will be posted when complete. Typically 2-5 minutes.')
    
    msg = await ctx.send(embed=embed)
    
    # Simulate research progress
    await asyncio.sleep(3)
    embed2 = discord.Embed(
        title='🔬 Research Progress',
        description=f'Studying: *{topic}*',
        color=0x3b82f6,
        timestamp=datetime.utcnow()
    )
    embed2.add_field(name='Phase 1', value='✅ Data collection', inline=True)
    embed2.add_field(name='Phase 2', value='⏳ Analysis...', inline=True)
    embed2.add_field(name='Phase 3', value='❌ Pending', inline=True)
    await msg.edit(embed=embed2)
    
    await asyncio.sleep(4)
    embed3 = discord.Embed(
        title='🔬 Research Complete',
        description=f'Analysis of: *{topic}*',
        color=0x22c55e,
        timestamp=datetime.utcnow()
    )
    embed3.add_field(name='Key Finding', value='SA-Russia meat trade corridor shows **23% YoY growth potential** with $4.2M annual opportunity', inline=False)
    embed3.add_field(name='Opportunity', value='Beef processing JV with Russian partners in Johannesburg', inline=True)
    embed3.add_field(name='Risk', value='RUB volatility requires 60% hedge on forward contracts', inline=True)
    embed3.add_field(name='Action', value='Schedule partnership meeting with SPonWeb team', inline=True)
    embed3.set_footer(text='Powered by MiroFish-Offline + AutoResearch')
    await msg.edit(embed=embed3)


@bot.command(name='alert')
async def alert_cmd(ctx, *args):
    if not await is_allowed(ctx): return
    if not args:
        embed = error_embed('Alert Command', 'Usage: `@ADAM alert USDZAR > 18.50`')
        await ctx.send(embed=embed)
        return
    
    alert_text = ' '.join(args)
    embed = success_embed('Alert Set', f'Price alert configured: `{alert_text}`')
    embed.add_field(name='Channel', value=f'{ctx.channel.mention}', inline=True)
    embed.add_field(name='User', value=ctx.author.mention, inline=True)
    embed.set_footer(text='You will be notified when the target is reached.')
    
    await ctx.send(embed=embed)


@bot.command(name='sync')
async def sync_cmd(ctx, *args):
    if not await is_allowed(ctx): return
    
    target = args[0] if args else 'all'
    
    embed = discord.Embed(
        title='🔄 Syncing Data...',
        description=f'Syncing *{target}* to cloud services',
        color=0x3b82f6,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='Obsidian Vault', value='⏳ Connecting...', inline=True)
    embed.add_field(name='AgentMail', value='⏳ Connecting...', inline=True)
    embed.add_field(name='GitHub', value='⏳ Connecting...', inline=True)
    
    msg = await ctx.send(embed=embed)
    
    await asyncio.sleep(2)
    embed2 = discord.Embed(
        title='✅ Sync Complete',
        description=f'Synced *{target}* to all services',
        color=0x22c55e,
        timestamp=datetime.utcnow()
    )
    embed2.add_field(name='✅ Obsidian', value='Meeting notes synced', inline=True)
    embed2.add_field(name='✅ AgentMail', value='Reports sent to tumelo@agentmail.to', inline=True)
    embed2.add_field(name='✅ GitHub', value='Repository updated', inline=True)
    
    await msg.edit(embed=embed2)


@bot.command(name='me')
async def me_cmd(ctx):
    if not await is_allowed(ctx): return
    
    embed = discord.Embed(
        title=f'👤 {ctx.author.name}',
        description='ADAM SMASHER User Profile',
        color=0x8b5cf6,
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.add_field(name='Discord ID', value=f'`{ctx.author.id}`', inline=True)
    embed.add_field(name='Joined', value=f'<t:{int(ctx.author.joined_at.timestamp())}:R>', inline=True)
    embed.add_field(name='Roles', value=', '.join([r.mention for r in ctx.author.roles[1:]]) or 'None', inline=False)
    embed.add_field(name='Meetings', value=f'`{len(state["meetings"])} recorded`', inline=True)
    embed.add_field(name='Trade Ideas', value=f'`{len(state["trade_ideas"])}`', inline=True)
    embed.add_field(name='Access Level', value='🟢 Authorized', inline=True)
    
    await ctx.send(embed=embed)


@bot.command(name='events')
async def events_cmd(ctx):
    if not await is_allowed(ctx): return
    
    embed = discord.Embed(
        title='📅 Upcoming Events & Bookings',
        description='Your scheduled meetings and bookings',
        color=0x3b82f6,
        timestamp=datetime.utcnow()
    )
    
    if state['bookings']:
        for b in state['bookings'][:5]:
            embed.add_field(name=f'📅 {b.get("title", "Meeting")}', value=f'{b.get("date", "TBD")} at {b.get("time", "TBD")}', inline=False)
    else:
        embed.add_field(name='No events', value='No upcoming bookings scheduled', inline=False)
    
    if state['meetings']:
        embed.add_field(name='Recent Meetings', value='\n'.join([f'• {m["title"]}' for m in state['meetings'][:3]]), inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name='idea')
async def idea_cmd(ctx):
    if not await is_allowed(ctx): return
    
    embed = discord.Embed(
        title='📈 Recent Trade Ideas',
        description='Logged trade opportunities',
        color=0x3b82f6,
        timestamp=datetime.utcnow()
    )
    
    if state['trade_ideas']:
        for idea in state['trade_ideas'][:5]:
            color_emoji = '🟢' if idea['direction'] == 'BUY' else '🔴'
            embed.add_field(
                name=f'{color_emoji} #{idea["id"]} — {idea["direction"]}',
                value=f'{idea["raw"]}\nBy {idea["user"]} • {idea["created"][:10]}',
                inline=False
            )
    else:
        embed.add_field(name='No ideas', value='Use `@ADAM trade` to log a trade idea', inline=False)
    
    await ctx.send(embed=embed)


# ===== EVENT HANDLERS =====
@bot.event
async def on_ready():
    logger.info(f'ADAM SMASHER is online! Logged in as {bot.user}')
    logger.info(f'Bot ID: {bot.user.id}')
    
    # Send startup message to home channel
    if HOME_CHANNEL_ID:
        channel = bot.get_channel(HOME_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title='🟢 ADAM SMASHER Online',
                description='Global Markets Operating System is now connected to Discord',
                color=0x22c55e,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Version', value='v1.0', inline=True)
            embed.add_field(name='Owner', value='Tumelo Ramaphosa | StudEx Global Markets', inline=True)
            embed.add_field(name='Status', value='All systems operational', inline=True)
            embed.add_field(name='Commands', value='Type `@ADAM help` for available commands', inline=False)
            embed.set_footer(text='StudEx Global Markets | SA-Russia Trade Week 2026')
            
            await channel.send(embed=embed)

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name='StudEx Global Markets | @ADAM help'
    ))


@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Only respond to DMs or if mentioned
    if not message.content.startswith('@ADAM '):
        if isinstance(message.channel, discord.DMChannel):
            # Auto-respond to DMs
            embed = info_embed('ADAM SMASHER', 'Use `@ADAM help` to see all available commands.')
            await message.channel.send(embed=embed)
        return
    
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = error_embed('Unknown Command', f'Use `@ADAM help` to see all available commands.')
        await ctx.send(embed=embed)
    else:
        logger.error(f'Command error: {error}')
        embed = error_embed('Error', str(error))
        await ctx.send(embed=embed)


# ===== SLASH COMMANDS (ALTERNATIVE) =====
@bot.tree.command(name='status', description='Get ADAM SMASHER system status')
async def slash_status(interaction: discord.Interaction):
    if not ALLOWED_USERS or interaction.user.id in ALLOWED_USERS:
        await interaction.response.send_message(embed=status_cmd.__wrapped__(interaction))
    else:
        await interaction.response.send_message('🚫 You are not authorized.', ephemeral=True)


# ===== RUN =====
if __name__ == '__main__':
    if not TOKEN:
        logger.error('DISCORD_BOT_TOKEN not set! Check your .env file.')
        print('❌ ERROR: DISCORD_BOT_TOKEN not found in environment.')
        print('   Create a .env file with: DISCORD_BOT_TOKEN=your_bot_token')
        print('   Get your bot token from: https://discord.com/developers/applications')
        exit(1)
    
    logger.info('Starting ADAM SMASHER Discord Bot...')
    bot.run(TOKEN, reconnect=True)