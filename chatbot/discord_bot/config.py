import json

def get_bot_config():
    """
    Function to read bot configuration from bot_config.json
    """
    with open("chatbot/config.json", "r") as f:
        return json.load(f)
