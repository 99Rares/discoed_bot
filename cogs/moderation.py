import asyncio
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    @commands.has_role('King')
    async def clear(self, ctx):
        """Clears all messages in the current channel, allowed only for users with the King role."""
        # Check if the user has the "King" role
        if ctx.author.guild_permissions.manage_messages or "King" in [role.name for role in ctx.author.roles]:
            await ctx.channel.purge()
            await ctx.send("All messages have been cleared.", delete_after=30)
        else:
            await ctx.send("You do not have permission to use this command.", delete_after=30)

    @commands.command(name='clear2')
    @commands.has_role('King')
    async def clear2(self, ctx):
        """Clears all messages in the current channel, allowed only for users with the King role."""
        # Check if the user has the "King" role
        if ctx.author.guild_permissions.manage_messages or "King" in [role.name for role in ctx.author.roles]:
            await ctx.send("Clearing messages...", delete_after=5)
            deleted = 0
            async for message in ctx.channel.history(limit=None):
                try:
                    await message.delete()
                    deleted += 1
                    await asyncio.sleep(1)  # Sleep to avoid hitting rate limits
                except discord.HTTPException as e:
                    print(f"Failed to delete message {message.id}: {e}")
                    continue
            await ctx.send(f"All {deleted} messages have been cleared.", delete_after=5)
        else:
            await ctx.send("You do not have permission to use this command.", delete_after=5)


    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You do not have the required role to use this command.", delete_after=30)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
