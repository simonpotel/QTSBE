from datetime import datetime
import discord
import time

bot_start_time = time.time()

def create_embed(title, description, color):
    """
    This function creates an embed with 
    title, description, and color 
    for Discord.
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    return embed

def format_time(seconds):
    """
    This function converts a given duration in seconds 
    into a formatted string representing hours, minutes, and seconds.

    Example: format_time(3665) will return "1h 1m 5s"
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

async def send_or_reply_embed(destination, title, description, color, is_reply=False):
    """
    This function creates an embed using the function create_embed,
    gets the time since the bot was started using the global variable bot_start_time,
    and sets this Bot uptime in the footer.
    Then it sends this embed either to a channel or as a reply to a message.
    """
    # Truncate title if it's too long
    if len(title) > 256:
        title = title[:253] + "..."  # Keep it within 256 characters including "..."
    
    # Create embed
    embed = create_embed(title, description, color)

    # Get Bot Uptime
    uptime_seconds = int(time.time() - bot_start_time)
    uptime_str = format_time(uptime_seconds)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Set footer
    embed.set_footer(text=f"Bot uptime: {uptime_str}, date: {date}")

    # Send embed
    if is_reply:
        return await destination.reply(embed=embed)
    else:
        return await destination.send(embed=embed)

async def send_embed(channel, title, description, color):
    """
    This function sends an embed to a channel.
    """
    return await send_or_reply_embed(channel, title, description, color, is_reply=False)

async def reply_embed(message, title, description, color):
    """
    This function sends an embed as a reply to a message.
    """
    return await send_or_reply_embed(message, title, description, color, is_reply=True)

async def error(message, error):
    """
    Sends an error embed in the channel.
    """
    if not message: return
    return await send_embed(message.channel, "❌ Error", error, discord.Color.brand_red())
