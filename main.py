import asyncio
import os
from dotenv import load_dotenv
import logging
import discord
from discord.ext import commands

# Load environment variables from .env file
load_dotenv()

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the BOT_TOKEN from the environment
TOKEN = os.getenv('BOT_TOKEN')

# Log the token for debugging (be careful with this in production)
logger.info(f"Token: {TOKEN}")

# Define intents (adjust as needed)
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

async def load_cogs(bot):
    cogs_directory = './cogs'
    for filename in os.listdir(cogs_directory):
        if filename.endswith('.py') and filename != "__init__.py":
            cog_name = f'cogs.{filename[:-3]}'
            try:
                await bot.load_extension(cog_name)
                logger.info(f'Successfully loaded cog: {cog_name}')
            except Exception as e:
                logger.error(f'Failed to load cog {cog_name}: {e}')

@bot.event
async def on_ready():
    logger.info(f'Bot connected as {bot.user}')

@bot.command(name='list_cogs')
async def list_cogs(ctx):
    """Lists all currently loaded cogs."""
    cogs = bot.cogs.keys()
    if cogs:
        await ctx.send(f"Loaded cogs:\n" + "\n".join(cogs))
    else:
        await ctx.send("No cogs are currently loaded.")

async def main():
    # Load all cogs before starting the bot
    await load_cogs(bot)
    await bot.start(TOKEN)

# Run the bot
asyncio.run(main())
