import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from stock_data import StockData
from stock_chart import StockChart

# Initialize Dash app
app = dash.Dash(__name__)

# Layout for the app
app.layout = html.Div([
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': 'Apple', 'value': 'AAPL'}, {'label': 'Google', 'value': 'GOOGL'}],  # You can dynamically populate this list based on available data or user preferences.
        multi=True,
        value=['AAPL']
    ),
    dcc.DatePickerRange(
    id='date-picker-range',
    start_date='2021-01-01',  # Default start date
    end_date='2023-01-01',    # Default end date
    display_format='YYYY-MM-DD'
    ),
    dcc.Graph(id='stock-graph'),
    # ... add more components as needed
])

@app.callback(
    Output('stock-graph', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(selected_stocks, start_date='2021-01-01', end_date='2023-01-01'):
    # Using StockData and StockChart to fetch and visualize data
    stock_chart = StockChart()
    
    for stock in selected_stocks:
        stock_data = StockData(stock, start_date, end_date).get_data()
        stock_chart.add_stock(stock, stock_data)
    
    traces = stock_chart.plot()
    
    return {
        'data': traces,
        'layout': {
            'title': 'Stock Prices'
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
