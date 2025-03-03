import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import webbrowser
import sys

class ChartTheme:
    def __init__(self, theme='white'):
        self.theme = theme
        self.colors = {
            "Background": theme,
            "increasing_line": "black",
            "increasing_fill": "white",
            "decreasing_line": "black",
            "decreasing_fill": "black",
            "shapes": "#8288b0",
            "MA_100": "#B8336A",
            "MA_40": "#FF9B42",
            "MA_20": "#F4D35E",
            "MA_9": "#F95738",
            "MA_21": "#F4D35E",
            "MA_200": "#6A0572",
            "RSI": "#77C67E",
            "EMA": "#FF85A1",
            "EMA_MACD": "#FF85A1",
            "MACD": "#5E4AE3",
            "Normalize_MACD": "#947BD3",
            "Bollinger_Lower": "#09917b",
            "Bollinger_Rolling": "#0078ff",
            "Bollinger_Upper": "#c9313f",
            "Else": "#8FF7A7"
        }

class DataExtractor:
    @staticmethod
    def extract_ohlc(data):
        dates, opens, highs, lows, closes, volume = zip(*data)
        return dates, opens, highs, lows, closes

    @staticmethod
    def extract_indicators(json_data):
        return json_data['result'][0]

    @staticmethod
    def extract_trades(trades):
        trade_indices = list(range(1, len(trades) + 1))
        trade_ratios = [trade['ratio'] for trade in trades if 'ratio' in trade]
        return trade_indices, trade_ratios

class TraceBuilder:
    def __init__(self, theme):
        self.theme = theme

    def build_candlestick(self, dates, opens, highs, lows, closes):
        return go.Candlestick(
            x=dates, open=opens, high=highs, low=lows, close=closes,
            name="Price",
            increasing_line_color=self.theme.colors['increasing_line'],
            decreasing_line_color=self.theme.colors['decreasing_line'],
            increasing_fillcolor=self.theme.colors['increasing_fill'],
            decreasing_fillcolor=self.theme.colors['decreasing_fill']
        )

    def build_trade_traces(self, trades, json_data):
        traces = []
        buy_dates = [trade['buy_date'] for trade in trades]
        buy_prices = [trade['buy_price'] for trade in trades]
        buy_indices = [trade['buy_index'] for trade in trades]
        buy_signals = [trade['buy_signals']['Buy_Signal'] for trade in trades]

        sell_dates = [trade['sell_date'] for trade in trades]
        sell_prices = [trade['sell_price'] for trade in trades]
        sell_indices = [trade['sell_index'] for trade in trades]
        sell_signals = [trade['sell_signals']['Sell_Signal'] for trade in trades]

        ratios = [float(ratio) for ratio in json_data["stats"]["positions"]["all_ratios"]]

        buy_hover_texts = [f"Index: {index}<br>Price: {price}<br>Date: {date}<br>Buy Signal: {buy_signal}"
                          for index, price, date, buy_signal in zip(buy_indices, buy_prices, buy_dates, buy_signals)]
        sell_hover_texts = [f"Index: {index}<br>Price: {price}<br>Date: {date}<br>Ratio: {ratio}<br>Sell Signal: {sell_signal}"
                           for index, price, date, ratio, sell_signal in zip(sell_indices, sell_prices, sell_dates, ratios, sell_signals)]

        traces.extend([
            go.Scatter(x=buy_dates, y=buy_prices, mode='markers', name='Buy',
                      marker=dict(symbol='triangle-up', color='#16DB93', size=10),
                      hovertext=buy_hover_texts, hoverinfo='text'),
            go.Scatter(x=sell_dates, y=sell_prices, mode='markers', name='Sell',
                      marker=dict(symbol='triangle-down', color='#EFEA5A', size=10),
                      hovertext=sell_hover_texts, hoverinfo='text')
        ])
        return traces

class PlotlyVisualizer:
    def __init__(self):
        self.theme = ChartTheme()
        self.data_extractor = DataExtractor()
        self.trace_builder = TraceBuilder(self.theme)

    def create_subplots_layout(self, indicators, trade_ratios):
        rows = 2
        cols = 1
        bound_hundred_plot = any(ind in indicators for ind in ['RSI', 'ATR', 'ATR_MA'])

        if bound_hundred_plot and trade_ratios:
            cols += 1
        if not bound_hundred_plot and not trade_ratios:
            rows = 1

        row_heights = [0.7, 0.3] if cols == 1 and rows == 2 else [0.75, 0.25] if cols == 2 and rows == 2 else [1]
        column_widths = [1] if cols == 1 else [0.75, 0.25]

        return make_subplots(rows=rows, cols=cols, shared_xaxes='all',
                           vertical_spacing=0.25, row_heights=row_heights,
                           column_widths=column_widths)

    def plot_json_data_in_gui(self, json_data, data_file, strategy):
        dates, opens, highs, lows, closes = self.data_extractor.extract_ohlc(json_data['data'])
        indicators = self.data_extractor.extract_indicators(json_data)
        trades = json_data['result'][1]
        trade_indices, trade_ratios = self.data_extractor.extract_trades(trades)

        fig = self.create_subplots_layout(indicators, trade_ratios)
        fig.add_trace(self.trace_builder.build_candlestick(dates, opens, highs, lows, closes), row=1, col=1)

        if trade_ratios:
            self._add_trade_ratio_traces(fig, trade_indices, trade_ratios, json_data, 'RSI' in indicators)

        self._add_indicator_traces(fig, indicators, dates)
        self._add_trade_traces(fig, trades, json_data)
        self._update_layout(fig, data_file, strategy)
        self._save_and_show(fig, data_file, strategy)

    def _add_trade_ratio_traces(self, fig, trade_indices, trade_ratios, json_data, bound_hundred_plot):
        row, col = (1, 2) if bound_hundred_plot else (2, 1)
        fig.add_trace(go.Scatter(x=trade_indices, y=trade_ratios, mode='lines',
                               name='Trade Ratios', line=dict(color='#DBB4AD')), row=row, col=col)

        cumulative_ratios = [float(ratio) for ratio in json_data["stats"]["positions"]["cumulative_ratios"]]
        fig.add_trace(go.Scatter(x=trade_indices, y=cumulative_ratios, mode='lines',
                               name='Cumulative Ratios', line=dict(color='#D30C7B')), row=row, col=col)

        moving_avg = [sum(cumulative_ratios[:i+1])/(i+1) for i in range(len(cumulative_ratios))]
        fig.add_trace(go.Scatter(x=trade_indices, y=moving_avg, mode='lines',
                               name='Moving Avg Cumulative Ratios', line=dict(color='#FFE3DC')), row=row, col=col)

        self._add_ratio_shapes(fig, trade_indices, trade_ratios, row, col)

    def _add_indicator_traces(self, fig, indicators, dates):
        for indicator, values in indicators.items():
            color = self.theme.colors.get(indicator, self.theme.colors['Else'])
            row = 2 if indicator in ['RSI', 'ATR', 'ATR_MA'] else 1
            fig.add_trace(go.Scatter(x=dates, y=values, mode='lines',
                                   name=indicator, line=dict(color=color)), row=row, col=1)

    def _add_trade_traces(self, fig, trades, json_data):
        traces = self.trace_builder.build_trade_traces(trades, json_data)
        for trace in traces:
            fig.add_trace(trace, row=1, col=1)

    def _add_ratio_shapes(self, fig, trade_indices, trade_ratios, row, col):
        min_ratio = min(trade_ratios)
        shapes = [
            dict(type="line", x0=min(trade_indices), y0=1, x1=max(trade_indices), y1=1,
                 line=dict(color=self.theme.colors['shapes'], width=1.5)),
            dict(type="line", x0=min(trade_indices), y0=min_ratio, x1=max(trade_indices), y1=min_ratio,
                 line=dict(color='red', width=1.5, dash='dash'))
        ]
        for shape in shapes:
            fig.add_shape(**shape, row=row, col=col)

    def _update_layout(self, fig, data_file, strategy):
        fig.update_layout(
            title=f"{data_file} ({strategy})",
            xaxis_title='Date',
            yaxis_title='Price',
            xaxis_rangeslider_visible=False,
            plot_bgcolor=self.theme.colors['Background'],
            paper_bgcolor=self.theme.colors['Background'],
            font=dict(color="black" if self.theme.theme == 'white' else "white"),
            yaxis=dict(gridcolor=self.theme.colors['Background']),
            xaxis=dict(gridcolor=self.theme.colors['Background']),
            yaxis2=dict(gridcolor=self.theme.colors['Background']),
            xaxis2=dict(gridcolor=self.theme.colors['Background'])
        )

    def _save_and_show(self, fig, data_file, strategy):
        directory = 'integrations/plotly/saved_results/'
        os.makedirs(directory, exist_ok=True)
        plot_filename = f'plot_{data_file}_{strategy}.html'
        fig.write_html(directory + plot_filename)

        if sys.platform == "darwin":
            safari_path = 'open -a /Applications/Safari.app %s'
            webbrowser.get(safari_path).open('file://' + os.path.realpath(os.path.join('integrations', 'plotly', 'saved_results', plot_filename)))
        else:
            fig.show()

def plot_json_data_in_gui(json_data, data_file, strategy):
    visualizer = PlotlyVisualizer()
    visualizer.plot_json_data_in_gui(json_data, data_file, strategy)


