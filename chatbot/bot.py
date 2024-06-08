import discord
from discord import Activity, ActivityType
from discord_bot.config import get_bot_config

bot_config = get_bot_config()  

#async def help_command(message):
    #await message.channel.send("Help")

class MyClient(discord.Client):
    async def on_ready(self):
        """
        Triggered at every start of the bot
        """
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        await self.change_presence(activity=Activity(type=ActivityType.custom, name=" ", state="➡️ " + bot_config["prefix"] + "help"))  # Rich presence

    async def on_message(self, message):
        """
        Triggered at every message sent
        """
        if message.author.id == self.user.id: 
            return # No response to itself
              
        # Check if the message starts with the correct prefix
        if message.content.startswith(bot_config["prefix"]):
            command = message.content[len(bot_config["prefix"]):].split()[0]  # Extract command

client = MyClient(intents=discord.Intents.all())  # Declare the client object
client.run(bot_config["token"])  # Log in the client (bot)
