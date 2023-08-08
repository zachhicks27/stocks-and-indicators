import plotly.graph_objs as go

class StockChart:
    def __init__(self):
        self.stocks = {}  # Dictionary: {ticker: dataframe, ...}
        self.indicators = {}  # Dictionary: {ticker: [indicator_traces], ...}

    def add_stock(self, ticker, data):
        """Add stock data."""
        self.stocks[ticker] = data

    def remove_stock(self, ticker):
        """Remove stock data."""
        if ticker in self.stocks:
            del self.stocks[ticker]
            if ticker in self.indicators:
                del self.indicators[ticker]

    def add_indicator(self, ticker, indicator):
        """Add indicator data for a stock."""
        indicator_data = indicator.get_plot_data()
        if ticker not in self.indicators:
            self.indicators[ticker] = []
        self.indicators[ticker].append(indicator_data)

    def remove_indicator(self, ticker, indicator_name):
        """Remove indicator data for a stock."""
        if ticker in self.indicators:
            self.indicators[ticker] = [ind for ind in self.indicators[ticker] if ind['name'] != f"{ticker} {indicator_name}"]
            if not self.indicators[ticker]:
                del self.indicators[ticker]
                
    def normalize_data(self, data):
        """Normalize stock data to percentage points starting from 0."""
        normalized = (data / data.iloc[0] - 1) * 100
        return normalized

    def plot(self):
        """Generate the Plotly traces for the stock data and indicators."""
        traces = []

        # Plot stock data
        for ticker, data in self.stocks.items():
            trace = go.Scatter(
                x=data.index,
                y=data['Close'],  # Assuming you're plotting closing prices
                mode='lines',
                name=ticker
            )
            traces.append(trace)

        # Plot indicators
        for ticker, indicator_list in self.indicators.items():
            for indicator_data in indicator_list:
                trace = go.Scatter(
                    x=indicator_data['x'],
                    y=indicator_data['y'],
                    mode='lines',
                    name=indicator_data['name'],
                    line=indicator_data.get('line', dict(dash='dash'))  # If no line style specified, default to dashed
                )
                traces.append(trace)

        return traces
