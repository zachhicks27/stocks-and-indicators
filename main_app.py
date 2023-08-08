import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from stock_data import StockData
from stock_chart import StockChart
from indicators import SMA
import pandas as pd

app = dash.Dash(__name__)

# Sample stock list for dropdown
stocks_list = ['AAPL', 'GOOGL', 'MSFT','SPY']

app.layout = html.Div([
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': stock, 'value': stock} for stock in stocks_list],
        multi=True,
        value=['AAPL']
    ),

    dcc.DatePickerRange(
        id='date-picker-range',
        start_date='2021-01-01',
        end_date='2023-01-01'
    ),

    html.Div([
        html.H5('Indicators'),
        
        html.Div([
            html.Label('SMA Window:'),
            dcc.Input(id='sma-window', type='number', value=14, min=1),
            dcc.Checklist(
                id='sma-toggle',
                options=[{'label': 'Show SMA', 'value': 'SMA'}],
                value=[]
            )
        ], id='sma-settings', className='indicator-setting'),
        
        # Further indicators can be added in similar containers here...
        
    ], id='indicator-settings'),

    dcc.Graph(id='stock-graph'),
    dcc.Graph(id='normalized-stock-graph')
])

def extract_setting(settings_divs, setting_id):
    for div in settings_divs:
        for component in div['props']['children']:
            if 'props' in component and component['props'].get('id') == setting_id:
                return component['props'].get('value')
    return []


@app.callback(
    [Output('stock-graph', 'figure'), Output('normalized-stock-graph', 'figure')],
    [
        Input('stock-dropdown', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('sma-toggle', 'value'),
        Input('sma-window', 'value')
        # ... any additional inputs for other indicators or settings
    ]
)
def update_graph(*args):
    ctx = dash.callback_context
    inputs = ctx.inputs

    # Extracting input values from the inputs dictionary
    selected_stocks = inputs['stock-dropdown.value']
    start_date = inputs['date-picker-range.start_date']
    end_date = inputs['date-picker-range.end_date']
    sma_toggle = inputs['sma-toggle.value']
    sma_window = int(inputs['sma-window.value'])  # Convert to integer
    # Backend validation to ensure non-negative window size
    sma_window = max(1, sma_window)
    
    stock_chart = StockChart()

    for stock in selected_stocks:
        stock_data = StockData(stock, start_date, end_date).get_data()
        stock_chart.add_stock(stock, stock_data)

        if sma_toggle and 'SMA' in sma_toggle:
            sma_indicator = SMA(stock_data, window=sma_window)
            stock_chart.add_indicator(stock, sma_indicator)

    traces = stock_chart.plot()

    normalized_stock_chart = StockChart()
    
    for stock in selected_stocks:
        stock_data = StockData(stock, start_date, end_date).get_data()
        normalized_data = pd.DataFrame(stock_chart.normalize_data(stock_data['Close']), columns=['Close'])
        normalized_stock_chart.add_stock(stock, normalized_data)

        if sma_toggle and 'SMA' in sma_toggle:
            norm_sma_indicator = SMA(normalized_data, window=sma_window)
            normalized_stock_chart.add_indicator(stock, norm_sma_indicator)

    normalized_traces = normalized_stock_chart.plot()

    return {
        'data': traces,
        'layout': {'title': 'Stock Prices with Indicators'}
    }, {
        'data': normalized_traces,
        'layout': {'title': 'Normalized Stock Prices with Indicators'}
    }


if __name__ == '__main__':
    app.run_server(debug=True)
