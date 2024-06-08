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
                #replied_message_id = message.reference.message_id
                #original_message = await message.channel.fetch_message(replied_message_id)
                bot_reacted_emojis = [reaction.emoji for reaction in message.reactions if reaction.me]
                if "1️⃣" in bot_reacted_emojis or "2️⃣" in bot_reacted_emojis:
                    reacted_emojis_count = {emoji: bot_reacted_emojis.count(emoji) for emoji in ["1️⃣", "2️⃣"]}
                    if reacted_emojis_count["1️⃣"] > 0 and reacted_emojis_count["2️⃣"] > 0:
                        await message.remove_reaction("1️⃣", self.user)
                        await message.remove_reaction("2️⃣", self.user)
                        if reaction.emoji == "1️⃣":
                            #logic
                            print("1")
                        elif reaction.emoji == "2️⃣":
                            #logic
                            print("2")

client = MyClient(intents=discord.Intents.all())  # client object
client.run(bot_config["token"])  # log the client (bot client)
