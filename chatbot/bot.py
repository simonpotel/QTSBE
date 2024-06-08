import discord
from discord import Activity, ActivityType
from discord_bot.config import get_bot_config
import os
import requests 
import asyncio
import json 

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

        if message.content.startswith(bot_config["prefix"]):
            command = message.content[len(bot_config["prefix"]):].split()[0]  # Extract command
            if command == "analyse" or command == "scan":
                if len(message.attachments) > 1:  
                    await message.reply(":x: Too much attachements. Can't detect strategy file.")
                else:
                    file = message.attachments[0]
                    filename = file.filename
                    if filename.endswith(".py"):
                        file_content = await file.read()
                        file_content = file_content.decode("utf-8")
                        reply_message = await message.reply(f"Action : {command}")
                        await reply_message.edit(content="Adding the file to the API")

                        file_path = os.path.join("api", "strategies", "_temp.py")
                        with open(file_path, "w", encoding="utf-8") as temp_file:
                            temp_file.write(file_content)

                        await asyncio.sleep(3)

                        url = f"http://127.0.0.1:5000/QTSBE/Binance_BTCUSDT_1d/_temp"

                        try:
                            response = requests.get(url)
                            response.raise_for_status()
                            json_data = json.loads(response.text)
                            formatted_json = json.dumps(json_data["stats"], indent=4)
                            response_message = f"API Request : {url}\n\nContent:\n\n{formatted_json}\n"

                            max_message_length = 1800 
                            if len(response_message) > max_message_length:
                                start = 0
                                end = max_message_length
                                while start < len(response_message):
                                    part = response_message[start:end]
                                    if len(part) > max_message_length:
                                        part = part[:max_message_length]
                                    await message.channel.send(f"\n{part}\n")
                                    start = end
                                    end += max_message_length
                            else:
                                await reply_message.edit(content=response_message)

                        except requests.RequestException as e:
                            await reply_message.edit(content=f"Request failed: {e}")
                        os.remove(file_path)
            else:
                await message.channel.send("?¿?")
client = MyClient(intents=discord.Intents.all())  # client object
client.run(bot_config["token"])  # log the client (bot client)
