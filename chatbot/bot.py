import discord
from discord import Activity, ActivityType
from discord_bot.config import get_bot_config

bot_config = get_bot_config()  

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

        if message.channel.name == "chat":
            if message.attachments:  
                await message.channel.send("File has been detected")
                for attachment in message.attachments:
                    filename = attachment.filename
                    if filename.endswith(".py"):
                        file_content = await attachment.read()
                        print(file_content.decode("utf-8"))  
            else:
                await message.channel.send("Unknown")

client = MyClient(intents=discord.Intents.all())  # client object
client.run(bot_config["token"])  # log the client (bot client)