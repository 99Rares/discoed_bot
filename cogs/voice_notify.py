import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class VoiceNotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Check if the user has joined a voice channel
        if before.channel is None and after.channel is not None:
            guild = member.guild
            
            # Try to get the "updates" channel
            target_channel = discord.utils.find(lambda c: c.name == 'updates' and isinstance(c, discord.TextChannel), guild.channels)
            
            # If no "updates" channel, fall back to "general"
            if target_channel is None:
                target_channel = discord.utils.find(lambda c: c.name == 'general' and isinstance(c, discord.TextChannel), guild.channels)
            
            # If no "general" channel, fall back to the first available text channel
            if target_channel is None:
                target_channel = discord.utils.find(lambda c: isinstance(c, discord.TextChannel), guild.channels)
            
            if target_channel:
                message = f"@everyone {member.display_name} has joined the voice channel: {after.channel.name}"
                await target_channel.send(message)
                logger.info(f"Notified {target_channel.name} about {member.display_name} joining {after.channel.name}")
            else:
                logger.warning(f"No suitable text channel found in guild {guild.name} to notify about {member.display_name} joining {after.channel.name}")

async def setup(bot):
    await bot.add_cog(VoiceNotify(bot))
