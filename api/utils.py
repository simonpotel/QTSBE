import math

def clean_nans(value):
    """
    Recursively replace NaN and Infinity with None in a dictionary or list.
    """
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    elif isinstance(value, dict):
        return {k: clean_nans(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [clean_nans(v) for v in value]
    elif isinstance(value, tuple):
        return tuple(clean_nans(v) for v in value)
    return value
