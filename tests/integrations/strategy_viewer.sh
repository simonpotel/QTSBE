strategy="QTS_fibo"
multi_positions="False"

specific_symbols=(
    "BTC/USDT" "ETH/USDT" "BNB/USDT" "ADA/USDT" "XRP/USDT" "DOGE/USDT" 
    "LTC/USDT" "DOT/USDT" "UNI/USDT" "LINK/USDT" "LUNA/USDT" "SOL/USDT" 
    "AVAX/USDT" "POL/USDT" "ATOM/USDT" "XLM/USDT" "TRX/USDT" "AAVE/USDT"
)

for symbol in "${specific_symbols[@]}"; do
    data="Binance_${symbol//\//}_1d"
    python integrations/plotly/main.py -strategy "$strategy" -data "$data" -multi_positions "$multi_positions" -symbol "$symbol"
done