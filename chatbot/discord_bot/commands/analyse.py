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

        # extract stats
        drawdown_stats = json_data.get('stats', {}).get('drawdown:', {})
        positions_stats = json_data.get('stats', {}).get('positions', {})

        # create an embed with the stats
        embed = discord.Embed(
            title=":chart_with_downwards_trend: Analyse",
            description="Stats for the given data and strategy:",
            color=discord.Color.dark_orange()
        )

        embed.add_field(name="Average Drawdown", value=f"{drawdown_stats.get('average_drawdown', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Max Drawdown", value=f"{drawdown_stats.get('max_drawdown', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Max Drawdown Period", value=f"{drawdown_stats.get('max_drawdown_period', ['N/A', 'N/A'])[0]} to {drawdown_stats.get('max_drawdown_period', ['N/A', 'N/A'])[1]}", inline=False)
        embed.add_field(name="Stability Ratio", value=f"{drawdown_stats.get('stability_ratio', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Total Drawdown", value=f"{drawdown_stats.get('total_drawdown', 'N/A'):.4f}", inline=False)

        embed.add_field(name="Average Position Duration", value=f"{positions_stats.get('average_position_duration', 'N/A'):.2f}", inline=False)
        embed.add_field(name="Average Ratio", value=f"{positions_stats.get('average_ratio', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Daily Average Ratio", value=f"{positions_stats.get('daily_average_ratio', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Hourly Average Ratio", value=f"{positions_stats.get('hourly_average_ratio', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Max Cumulative Ratio", value=f"{positions_stats.get('max_cumulative_ratio', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Max Loss", value=f"{positions_stats.get('max_loss', 'N/A'):.6f}", inline=False)
        embed.add_field(name="Max Loss Buy Index", value=f"{positions_stats.get('max_loss_buy_index', 'N/A')}", inline=False)
        embed.add_field(name="Max Loss Sell Index", value=f"{positions_stats.get('max_loss_sell_index', 'N/A')}", inline=False)

        file = discord.File(temp_file_name, filename=f"{data_file}_{strategy}.json")
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
