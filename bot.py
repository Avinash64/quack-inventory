import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from make_db import create_db
from db_helpers import *
import sqlite3

# Load .env
load_dotenv()
intents = discord.Intents.all()
intents.message_content = True  # Required for prefix-based commands
create_db()
bot = commands.Bot(command_prefix=',', intents=intents)
TOKEN = os.getenv('DISCORD_TOKEN')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

# 3. Example Command
# Usage in Discord: ,ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

# 4. Example Command with Arguments
# Usage in Discord: ,echo Hello World
@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)

@bot.command()
async def additem(ctx, name: str, category: str = 'misc', condition: str = 'unknown', storage: str = 'unknown'):
    # 1. Grab the user's Discord ID
    discord_id = str(ctx.author.id)
    
    # 2. Look up their internal database ID
    conn = sqlite3.connect('inv.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE discord_id = ?', (discord_id,))
    user_row = cursor.fetchone()
    conn.close()
    
    # Safety Check: If they aren't in the DB yet (rare, since your on_message listener catches everyone)
    if not user_row:
        await ctx.send("Whoops! You aren't in the database yet. Send a normal message first so I can register you.")
        return
        
    internal_user_id = user_row[0]
    
    # 3. Call your database function using the internal ID
    try:
        # Notice we are passing the arguments exactly as Discord handed them to us
        insert_item(internal_user_id, name, condition, storage, category)
        
        # 4. Send a success message back to the user
        await ctx.send(f"{name} added")
        await ctx.send(f'''Items:\n'''+ '\n'.join([f'{i[2]}' for i in get_items(discord_id)]))
                       
    except Exception as e:
        await ctx.send(f"❌ Something went wrong saving the item: {e}")

# Background listener capturing ALL messages
@bot.event
async def on_message(message):
    # 1. Ignore messages from bots (including this one) to prevent loops
    if message.author.bot:
        return

    # 2. Extract user info from message context
    discord_id = str(message.author.id)
    username = message.author.name          # e.g., "tobias_dev"
    display_name = message.author.display_name  # e.g., "Tobias | Playing Cycles"

    # 3. Securely write to database
    conn = sqlite3.connect('inv.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    
    # "INSERT OR IGNORE" safely handles users already in your system
    cursor.execute('''
        INSERT OR IGNORE INTO users (discord_id, username, display_name)
        VALUES (?, ?, ?)
    ''', (discord_id, username, display_name))
    
    conn.commit()
    conn.close()
    await bot.process_commands(message)


# 5. Run the Bot
# Replace 'YOUR_TOKEN_HERE' with your actual bot token from the Discord Developer Portal.
if __name__ == "__main__":
    bot.run(TOKEN)