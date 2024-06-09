from discord_bot.embeds import reply_embed
import discord
import requests
import json
import tempfile
import os

async def fetch_and_show_data(message, data_file, strategy):
    url = f"http://127.0.0.1:5000/QTSBE/{data_file}/{strategy}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        
        # create temp file for the discord attachement
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json', mode='w', encoding='utf-8') as temp_file:
            temp_file_name = temp_file.name
            json.dump(json_data, temp_file, indent=4)
        
        file = discord.File(temp_file_name, filename=f"{data_file}_{strategy}.json")
        embed = discord.Embed(
            title=f":chart_with_downwards_trend: Analyse {data_file} {strategy}",
            description=f"Full JSON data on attachement.\nRequest URL: {url}",
            color=discord.Color.dark_orange()
        )
        
        await message.reply(embed=embed, file=file)
        
        # delete the temporary file
        os.remove(temp_file_name)
    except requests.RequestException as e:
        await reply_embed(message, "❌ Error", f"Request failed: {e}", discord.Color.brand_red())
    except Exception as e:
        await reply_embed(message, "❌ Error", f"An unexpected error occurred: {e}", discord.Color.brand_red())

async def analyse(client, message, args):
    if len(args) < 2:
        await reply_embed(message, "❌ Error", "You need to provide both the data and strategy arguments.", discord.Color.brand_red())
        return

    data = args[0]
    strategy = args[1]
    await fetch_and_show_data(message, data, strategy)
