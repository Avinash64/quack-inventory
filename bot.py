import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
# Load .env
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True  # Required for prefix-based commands

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

# 5. Run the Bot
# Replace 'YOUR_TOKEN_HERE' with your actual bot token from the Discord Developer Portal.
if __name__ == "__main__":
    bot.run(TOKEN)