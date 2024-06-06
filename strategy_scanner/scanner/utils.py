import math

def format_time(seconds):
    minutes = math.floor(seconds / 60)
    seconds = math.ceil(seconds % 60)
    return f"{minutes}m {seconds}s"