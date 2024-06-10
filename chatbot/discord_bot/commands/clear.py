import discord 
from discord_bot.embeds import send_embed, error 

async def clear(client, message, args):
    """
    Discord command that delete all the messages in the channel
    """
    try:
        await message.channel.purge(limit=None) # Delete all the messages of the channel

        await send_embed(
            message.channel,
            "✅ Success",
            "All messages have been deleted.",
            discord.Color.yellow()
        )
        
    except Exception as e:
        print(f"Error during message deletion: {e}")
        await error(message.channel, f"Error during message deletion.\n {e}")
