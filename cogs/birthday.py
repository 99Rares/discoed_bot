import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import json
import os

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday_data = self.load_birthdays()
        self.check_birthdays.start()

    def load_birthdays(self):
        if os.path.exists("birthdays.json"):
            with open("birthdays.json", "r") as f:
                return json.load(f)
        return {}

    def save_birthdays(self):
        with open("birthdays.json", "w") as f:
            json.dump(self.birthday_data, f, indent=4)

    @commands.command(name='add_birthday')
    async def add_birthday(self, ctx, member: discord.Member, date: str):
        """Adds a birthday for a member. Date format: DD-MM-YYYY"""
        try:
            birthday = datetime.strptime(date, "%d-%m-%Y").date()
            self.birthday_data[str(member.id)] = {"name": member.name, "birthday": date}
            self.save_birthdays()
            await ctx.send(f"Added {member.name}'s birthday on {date}.")
        except ValueError:
            await ctx.send("Invalid date format. Please use DD-MM-YYYY.")

    @commands.command(name='remove_birthday')
    async def remove_birthday(self, ctx, member: discord.Member):
        """Removes a birthday entry for a member."""
        if str(member.id) in self.birthday_data:
            del self.birthday_data[str(member.id)]
            self.save_birthdays()
            await ctx.send(f"Removed {member.name}'s birthday.")
        else:
            await ctx.send(f"No birthday found for {member.name}.")

    @commands.command(name='list_birthdays')
    async def list_birthdays(self, ctx):
        """Lists all the recorded birthdays."""
        if not self.birthday_data:
            await ctx.send("No birthdays recorded.")
            return
        
        birthdays = ""
        for member_id, info in self.birthday_data.items():
            birthdays += f"{info['name']} - {info['birthday']}\n"
        
        await ctx.send(f"Recorded Birthdays:\n{birthdays}")

    @tasks.loop(hours=24)
    async def check_birthdays(self):
        """Checks daily for birthdays."""
        today = datetime.utcnow().date()
        
        for guild in self.bot.guilds:  # Iterate over all guilds the bot is in
            # Attempt to find the 'general' channel first
            general_channel = discord.utils.find(lambda c: c.name == 'general' and isinstance(c, discord.TextChannel), guild.channels)
            
            # If no 'general' channel is found, fall back to the first available text channel
            if not general_channel:
                general_channel = discord.utils.find(lambda c: isinstance(c, discord.TextChannel), guild.channels)

            # If a channel is found (either 'general' or the first text channel), proceed with the birthday check
            if general_channel:
                for member_id, info in self.birthday_data.items():
                    birthday = datetime.strptime(info["birthday"], "%d-%m-%Y").date()
                    if birthday.month == today.month and birthday.day == today.day:
                        await general_channel.send(f"🎉 Happy Birthday, {info['name']}! 🎂")
            else:
                # Log or handle cases where no text channel is found (very rare)
                print(f"No text channels found in guild {guild.name}")


    @check_birthdays.before_loop
    async def before_check_birthdays(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Birthday(bot))
