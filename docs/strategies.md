# Strategy Development Guide

This directory contains all trading strategies that will be automatically loaded by the API. The system will recursively scan and load all Python files in this directory and its subdirectories.

## Directory Structure

```
api/strategies/
├── default.py          # Base template for new strategies
├── rsi_example/        # Example implementation
└── your_strategy/      # Your custom strategy folder
```

## Implementation Requirements

### 1. Strategy Organization
- Create a new folder for your strategy (recommended)
- Or add single strategy files directly in this directory
- Best Practice: Use a private repository and clone it here

### 2. Required Components

Each strategy must implement these three components:

#### 2.1 Indicators Class
```python
class Indicators(object):
    def __init__(self, data):
        self.data = data  # Historical price data
        self.indicators = self.calculate_indicators()

    def calculate_indicators(self):
        # Extract price data
        data_open = [row[1] for row in self.data]
        
        # Calculate your indicators
        indicators = {
            "RSI": get_RSI(data_open),
            # Add more indicators as needed
        }
        return {k: list(v) for k, v in indicators.items()}
```

#### 2.2 Buy Signal Function
```python
def buy_signal(open_position, data, index_check, indicators, current_price=None):
    """
    Parameters:
        open_position (bool): Whether a position is currently open
        data (list): Historical price data
        index_check (int): Current index being checked
        indicators (dict): Calculated indicators
        current_price (float, optional): Live price for real-time trading
    
    Returns:
        tuple: (signal, price)
            signal: 1 for buy, 0 for no action
            price: Entry price or None
    """
    # Your buy logic here
    return 0, None
```

#### 2.3 Sell Signal Function
```python
def sell_signal(open_position, data, index_check, indicators, current_price=None):
    """
    Parameters:
        [Same as buy_signal]
    
    Returns:
        tuple: (signal, price)
            signal: 1 for sell, 0 for no action
            price: Exit price or None
    """
    # Your sell logic here
    return 0, None
```
