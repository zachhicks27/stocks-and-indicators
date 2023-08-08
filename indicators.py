class Indicator:
    def __init__(self, data, color=None):
        self.data = data
        self.color = color

    def calculate(self):
        raise NotImplementedError("Each indicator must implement the calculate method.")

class SMA(Indicator):
    def __init__(self, data, window=14, color=None):
        super().__init__(data, color)
        self.window = window

    def calculate(self):
        return self.data['Close'].rolling(window=self.window).mean()
    
    def get_plot_data(self):
        sma_values = self.calculate()
        return {
            'x': sma_values.index,
            'y': sma_values.values,
            'type': 'line',
            'name': f'SMA-{self.window}',
            'line': {'color': self.color}
        }
