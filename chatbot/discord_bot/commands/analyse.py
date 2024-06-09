import discord
import requests
import json
import tempfile
import os
import plotly.io as pio
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import customtkinter as ctk
from discord_bot.embeds import reply_embed

chart_colors = {
    "Price": "#6c7386",
    "MA_100": "#B8336A",
    "MA_40": "#FF9B42",
    "MA_20": "#F4D35E",
    "Test": "#C73E1D",
    "RSI": "#9AB87A",
    "EMA": "#F0A7A0",
    "EMA_MACD": "#F0A7A0",
    "MACD": "#5E4AE3",
    "Normalize_MACD": "#947BD3",
    "Bollinger_Lower": "#A682FF",
    "Bollinger_Rolling": "#A682FF",
    "Bollinger_Upper": "#A682FF",
}

async def fetch_and_show_data(message, data_file, strategy):
    url = f"http://127.0.0.1:5000/QTSBE/{data_file}/{strategy}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        # create temp file for the discord attachment
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json', mode='w', encoding='utf-8') as temp_file:
            temp_file_name = temp_file.name
            json.dump(json_data, temp_file, indent=4)

        # extract stats
        drawdown_stats = json_data.get('stats', {}).get('drawdown:', {})
        positions_stats = json_data.get('stats', {}).get('positions', {})

        # create an embed with the stats
        embed = discord.Embed(
            title=":chart_with_downwards_trend: Analyse",
            description="Stats for the given data and strategy:",
            color=discord.Color.dark_orange()
        )

        embed.add_field(name="Average Drawdown", value=f"{drawdown_stats.get('average_drawdown', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Max Drawdown", value=f"{drawdown_stats.get('max_drawdown', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Max Drawdown Period", value=f"{drawdown_stats.get('max_drawdown_period', ['N/A', 'N/A'])[0]} to {drawdown_stats.get('max_drawdown_period', ['N/A', 'N/A'])[1]}", inline=False)
        embed.add_field(name="Stability Ratio", value=f"{drawdown_stats.get('stability_ratio', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Total Drawdown", value=f"{drawdown_stats.get('total_drawdown', 'N/A'):.4f}", inline=False)

        embed.add_field(name="Average Position Duration", value=f"{positions_stats.get('average_position_duration', 'N/A'):.2f}", inline=False)
        embed.add_field(name="Average Ratio", value=f"{positions_stats.get('average_ratio', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Daily Average Ratio", value=f"{positions_stats.get('daily_average_ratio', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Hourly Average Ratio", value=f"{positions_stats.get('hourly_average_ratio', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Max Cumulative Ratio", value=f"{positions_stats.get('max_cumulative_ratio', 'N/A'):.4f}", inline=False)
        embed.add_field(name="Max Loss", value=f"{positions_stats.get('max_loss', 'N/A'):.6f}", inline=False)
        embed.add_field(name="Max Loss Buy Index", value=f"{positions_stats.get('max_loss_buy_index', 'N/A')}", inline=False)
        embed.add_field(name="Max Loss Sell Index", value=f"{positions_stats.get('max_loss_sell_index', 'N/A')}", inline=False)

        file_json = discord.File(temp_file_name, filename=f"{data_file}_{strategy}.json")
        
        # generate figure
        fig = generate_plot_figure(json_data, data_file, strategy)
        os.makedirs('display/python/saved_results/', exist_ok=True)
        plot_html_filename = 'display/python/saved_results/plot.html'
        fig.write_html(plot_html_filename)
        file_html = discord.File(plot_html_filename, filename=f"{data_file}_{strategy}.html")

        # create temp file for the image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png', mode='wb') as temp_image:
            temp_image_name = temp_image.name
            pio.write_image(fig, temp_image_name)

        file_image = discord.File(temp_image_name, filename=f"{data_file}_{strategy}.png")

        await message.reply(embed=embed, files=[file_json, file_html,file_image])

        # delete the temporary files
        os.remove(temp_file_name)
        os.remove(temp_image_name)

    except requests.RequestException as e:
        await reply_embed(message, "❌ Error", f"Request failed: {e}", discord.Color.brand_red())
    except Exception as e:
        await reply_embed(message, "❌ Error", f"An unexpected error occurred: {e}", discord.Color.brand_red())

def generate_plot_figure(json_data, data_file, strategy):
    dates, opens, highs, lows, closes = extract_ohlc_data(json_data['data'])
    indicators = extract_indicators(json_data)
    trades = json_data['result'][1]
    trade_indices, trade_ratios = extract_trade_data(trades)
    rows = 1
    cols = 1
    
    if 'RSI' or 'Normalize_MACD' in indicators:
        price_row_height = 0.7
        rsi_row_height = 0.3
        rows += 1
    else:
        price_row_height = 1.0
        rsi_row_height = 0.0

    row_heights=[price_row_height]
    if 'RSI' or 'Normalize_MACD' in indicators:
        row_heights.append(rsi_row_height)

    if len(trade_ratios) > 0: cols += 1

    column_widths = [0.7] * cols  
    if cols > 1:
        column_widths[0] = 0.7  

    fig = make_subplots(rows=rows, cols=cols, shared_xaxes=True, vertical_spacing=0.25,
                        row_heights=row_heights,
                        column_widths=column_widths) 

    fig.add_trace(go.Candlestick(x=dates, open=opens, high=highs, low=lows, close=closes), row=1, col=1)

    for indicator in indicators:
        row = 1
        if indicator == 'RSI' or indicator == 'Normalize_MACD': row += 1
        fig.add_trace(go.Scatter(x=dates, y=indicators[indicator], mode='lines', name=indicator, line=dict(color=chart_colors[indicator])), row=row, col=1)

    if len(trade_ratios) > 0:
        fig.add_trace(go.Scatter(x=trade_indices, y=trade_ratios, mode='lines', name='Trade Ratios', line=dict(color=chart_colors['Test'])), row=1, col=2)
        cumulative_ratios = [float(cumultative_ratio) for cumultative_ratio in json_data["stats"]["positions"]["cumulative_ratios"]]
        fig.add_trace(go.Scatter(x=trade_indices, y=cumulative_ratios, mode='lines', name='Cumulative Ratios', line=dict(color=chart_colors['MA_100'])), row=1, col=2)

    buy_dates = [trade['buy_date'] for trade in trades]
    buy_prices = [trade['buy_price'] for trade in trades]
    buy_indices = [trade['buy_index'] for trade in trades]  
    buy_signals = [trade['buy_signals']['Buy_Signal'] for trade in trades] 

    sell_dates = [trade['sell_date'] for trade in trades]
    sell_prices = [trade['sell_price'] for trade in trades]
    sell_indices = [trade['sell_index'] for trade in trades]  
    sell_signals = [trade['sell_signals']['Sell_Signal'] for trade in trades] 

    ratios = [float(ratio) for ratio in json_data["stats"]["positions"]["all_ratios"]]

    # hover texts for the markets
    buy_hover_texts = [f"Index: {index}<br>Price: {price}<br>Date: {date}<br>Buy Signal: {buy_signal}" for index, price, date, buy_signal in zip(buy_indices, buy_prices, buy_dates, buy_signals)]
    sell_hover_texts = [f"Index: {index}<br>Price: {price}<br>Date: {date}<br>Ratio: {ratio}<br>Sell Signal: {sell_signal}" for index, price, date, ratio, sell_signal in zip(sell_indices, sell_prices, sell_dates, ratios, sell_signals)]

    # plot buy/sell markes
    fig.add_trace(go.Scatter(
        x=buy_dates, 
        y=buy_prices, 
        mode='markers', 
        name='Buy', 
        marker=dict(symbol='triangle-up', color='#B0FE76', size=10),
        hovertext=buy_hover_texts,  
        hoverinfo='text'  
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=sell_dates, 
        y=sell_prices, 
        mode='markers', 
        name='Sell', 
        marker=dict(symbol='triangle-down', color='#2DC7FF', size=10),
        hovertext=sell_hover_texts,  
        hoverinfo='text' 
    ), row=1, col=1)

    # layout
    fig.update_layout(title=f"{data_file} ({strategy})",
                    xaxis_title='Date',
                    yaxis_title='Price',
                    xaxis_rangeslider_visible=False,
                    plot_bgcolor='#161a25',
                    paper_bgcolor='#161a25',
                    font=dict(color='white'),
                    yaxis=dict(gridcolor='#6c7386'),
                    xaxis=dict(gridcolor='#6c7386'),
                    yaxis2=dict(gridcolor='#6c7386'), 
                    xaxis2=dict(gridcolor='#6c7386')) 

    if 'RSI' or 'Normalize_MACD' in indicators:
        fig.update_yaxes(range=[0, 100], row=2, col=1)
        fig.add_shape(type="line", x0=min(dates), y0=50, x1=max(dates), y1=50, row=2, col=1, line=dict(color="LightSkyBlue", width=3))

    return fig

def extract_ohlc_data(data):
    dates, opens, highs, lows, closes, volume = zip(*data)
    return dates, opens, highs, lows, closes

def extract_indicators(json_data):
    indicators = {}
    for indicator in json_data['result'][0]:
        indicators[indicator] = json_data['result'][0][indicator]
    return indicators

def extract_trade_data(trades):
    trade_indices = list(range(1, len(trades) + 1))
    trade_ratios = [trade['ratio'] for trade in trades if 'ratio' in trade]
    return trade_indices, trade_ratios

async def analyse(client, message, args):
    if len(args) < 2:
        await reply_embed(message, "❌ Error", "You need to provide both the data and strategy arguments.", discord.Color.brand_red())
        return

    data = args[0]
    strategy = args[1]
    await fetch_and_show_data(message, data, strategy)
