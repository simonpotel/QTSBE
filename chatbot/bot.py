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
                await message.reply(":file_folder: Attachement(s) in your message, analyse..")
                for attachment in message.attachments:
                    filename = attachment.filename
                    if filename.endswith(".py"):
                        file_content = await attachment.read()
                        await message.reply("<:python:1249089145855283301> Python file has been scanned")
                        content = file_content.decode("utf-8")
                        print(content)  
            else:
                await message.channel.send("?¿?")

client = MyClient(intents=discord.Intents.all())  # client object
client.run(bot_config["token"])  # log the client (bot client)