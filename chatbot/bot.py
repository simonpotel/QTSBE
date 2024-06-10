import discord
from discord import Activity, ActivityType
from discord_bot.embeds import reply_embed
from discord_bot.config import get_bot_config
from discord_bot.commands.clear import clear
from discord_bot.commands.analyse import analyse
#from discord_bot.commands.scan import scan

bot_config = get_bot_config()  

commands = { 
    'clear': clear,
    'analyse': analyse
}

async def help(client, message, args):
    cmdslist = ""
    for i in commands:
        cmdslist += bot_config["prefix"] + i + "\n"
    await reply_embed(message, 
                      "📜 Commands list", 
                      cmdslist, 
                      discord.Color.yellow()
                      ) 


commands["help"] = help

class MyClient(discord.Client):
    async def on_ready(self):
        """
        Triggered at every start of the bot
        """
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        await self.change_presence(activity=Activity(type=ActivityType.custom, name=" ", state="➡️ " + bot_config["prefix"] + "help"))  # Rich presence

    async def on_message(self, message):
        if message.author.id == self.user.id: return  # No respond to itself
        
        # Imperative security that make the bot interract only on the configured discord channel (usage and logs channels)
        if str(message.guild.id) != bot_config["discord_id"]: return  

        content = message.content[len(bot_config["prefix"]):].split() # Separate command and arguments
        if not content: return # Security if there is no command and only prefix

        if message.content[:len(bot_config["prefix"])] != bot_config["prefix"]: return # Not good prefix command

        command = content[0] 
        args = content[1:]

        if command in commands: # Verify that the command sent is in commands list
            await commands[command](self, message, args) 


client = MyClient(intents=discord.Intents.all())  # client object
client.run(bot_config["token"])  # log the client (bot client)
