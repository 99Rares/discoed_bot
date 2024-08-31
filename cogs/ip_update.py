import discord
from discord.ext import commands
import json
import os

class IPUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ip_data_file = 'ip_data.json'
        self.ip_data = self.load_ip_data()

    def load_ip_data(self):
        """Load IP data from a JSON file."""
        if os.path.exists(self.ip_data_file):
            with open(self.ip_data_file, 'r') as f:
                return json.load(f)
        return {}

    def save_ip_data(self):
        """Save IP data to a JSON file."""
        with open(self.ip_data_file, 'w') as f:
            json.dump(self.ip_data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        # Check if the message is in the 'ip-updates' channel
        if message.channel.name != 'ip-updates':
            return

        # Check if the message is an IP update
        if "Updated: " in message.content and "'s new IP Address is " in message.content:
            # Extract the domain and IP address
            parts = message.content.split("'s new IP Address is ")
            if len(parts) == 2:
                domain = parts[0].replace("Updated: ", "").strip()
                new_ip = parts[1].strip()

                # Check if this IP is new
                if domain in self.ip_data and self.ip_data[domain] == new_ip:
                    await message.delete()  # Delete the duplicate message
                else:
                    # Update the JSON with the new IP
                    self.ip_data[domain] = new_ip
                    self.save_ip_data()
                    # Optionally log the update or take further actions
                    print(f"Updated {domain} to {new_ip}")

async def setup(bot):
    await bot.add_cog(IPUpdate(bot))
