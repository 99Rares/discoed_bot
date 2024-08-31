import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help_command(self, ctx, *commands: str):
        """Shows this message"""
        # If no specific command is mentioned, list all commands
        if not commands:
            embed = discord.Embed(title="Help", description="List of available commands:")
            for command in self.bot.commands:
                if not command.hidden:
                    embed.add_field(name=command.name, value=command.help or "No description", inline=False)
            await ctx.send(embed=embed)
        else:
            # If a specific command is mentioned, show detailed help for that command
            for command_name in commands:
                command = self.bot.get_command(command_name)
                if command:
                    embed = discord.Embed(title=f"Help: {command.name}", description=command.help or "No description")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"Command `{command_name}` not found.")

# Setup function for the cog
async def setup(bot):
    await bot.add_cog(Help(bot))
