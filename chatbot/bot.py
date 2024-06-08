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
        if message.author.id == self.user.id: 
            return # No response to itself

        if message.channel.name == "chat":
            if message.attachments:  
                answer = await message.reply(":file_folder: Attachement(s) in your message, analyse..")
                for attachment in message.attachments:
                    filename = attachment.filename
                    if filename.endswith(".py"):
                        file_content = await attachment.read()
                        file_content = file_content.decode("utf-8")
                        await answer.edit(content=f"<:python:1249089145855283301> Python file : {filename}\nSelect your action :\n:one: = Simple Analyse with Binance Pair of your choice\n:two: = Global Scan with every Pairs of Binance")
                        await answer.add_reaction("1️⃣")  
                        await answer.add_reaction("2️⃣")  

            else:
                await message.channel.send("?¿?")

    async def on_reaction_add(self, reaction, user):
        if not user.bot:  
            message = reaction.message
            if message.reference:
                replied_message_id = message.reference.message_id
                original_message = await message.channel.fetch_message(replied_message_id)
                await original_message.reply(f"{user.name} reacted {reaction.emoji}")

client = MyClient(intents=discord.Intents.all())  # client object
client.run(bot_config["token"])  # log the client (bot client)
