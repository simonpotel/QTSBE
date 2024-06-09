from discord_bot.embeds import reply_embed
import discord 

async def analyse(client, message, args):
    return await reply_embed(
            message,
            ":chart_with_downwards_trend: Analyse",
            f"```void```",
            discord.Color.dark_orange()
        )