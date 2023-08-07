import yfinance as yf
import pandas as pd
import os

class StockData:
    CACHE_DIR = "stock_cache"  # Directory to store cached stock data

    def __init__(self, ticker, start_date, end_date, source="yfinance"):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.source = source
        self.data = None

        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)

    def fetch_data(self):
        if self.source == "yfinance":
            self.data = self._fetch_from_yfinance()
        # Add other sources as needed, like:
        # elif self.source == "another_source":
        #     self.data = self._fetch_from_another_source()

        if self.data is not None:
            self._cache_data()

    def _fetch_from_yfinance(self):
        try:
            stock_data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
            return stock_data
        except Exception as e:
            print(f"Error fetching data for {self.ticker} from yfinance: {e}")
            return None

    def _cache_data(self):
        cache_path = os.path.join(self.CACHE_DIR, f"{self.ticker}_{self.start_date}_to_{self.end_date}.csv")
        self.data.to_csv(cache_path)

    def load_cached_data(self):
        cache_path = os.path.join(self.CACHE_DIR, f"{self.ticker}_{self.start_date}_to_{self.end_date}.csv")
        if os.path.exists(cache_path):
            self.data = pd.read_csv(cache_path, index_col=0, parse_dates=True)
            return True
        return False

    def get_data(self):
        if not self.load_cached_data():
            self.fetch_data()
        return self.data
