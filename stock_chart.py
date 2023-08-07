import plotly.graph_objs as go

class StockChart:
    def __init__(self):
        self.stocks = {}  # Dictionary: {ticker: dataframe, ...}
        self.indicators = {}  # Dictionary: {ticker: {indicator_name: data}, ...}

    def add_stock(self, ticker, data):
        """Add stock data."""
        self.stocks[ticker] = data

    def remove_stock(self, ticker):
        """Remove stock data."""
        if ticker in self.stocks:
            del self.stocks[ticker]
            if ticker in self.indicators:
                del self.indicators[ticker]

    def add_indicator(self, ticker, indicator_name, indicator_data):
        """Add indicator data for a stock."""
        if ticker not in self.indicators:
            self.indicators[ticker] = {}
        self.indicators[ticker][indicator_name] = indicator_data

    def remove_indicator(self, ticker, indicator_name):
        """Remove indicator data for a stock."""
        if ticker in self.indicators and indicator_name in self.indicators[ticker]:
            del self.indicators[ticker][indicator_name]

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
        for ticker, indicators in self.indicators.items():
            for name, data in indicators.items():
                trace = go.Scatter(
                    x=data.index,
                    y=data,
                    mode='lines',
                    name=f"{ticker} - {name}",
                    line=dict(dash='dash')  # Indicators could be dashed for distinction
                )
                traces.append(trace)

        return traces
