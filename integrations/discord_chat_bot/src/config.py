import json

def get_bot_config():
    """
    Function to read bot configuration from bot_config.json
    """
    with open("integration/discord_chat_bot/configs/bot.json", "r") as f:
        return json.load(f)
