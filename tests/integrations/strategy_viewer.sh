strategy="QTS_fibo"
multi_positions="False"

specific_symbols=(
    "BTC/USDC" "ETH/USDC" "BNB/USDC" "ADA/USDC" "XRP/USDC" "DOGE/USDC" 
    "LTC/USDC" "DOT/USDC" "UNI/USDC" "LINK/USDC" "LUNA/USDC" "SOL/USDC" 
    "AVAX/USDC" "POL/USDC" "ATOM/USDC" "XLM/USDC" "TRX/USDC" "AAVE/USDC"
)

for symbol in "${specific_symbols[@]}"; do
    data="Binance_${symbol//\//}_1d"
    python integrations/plotly/main.py -strategy "$strategy" -data "$data" -multi_positions "$multi_positions" -symbol "$symbol"
done