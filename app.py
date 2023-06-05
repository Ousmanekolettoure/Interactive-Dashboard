# Step 1: Import necessary libraries
import blpapi
import pandas as pd
from xbbg import blp
from datetime import datetime, timedelta
import xlsxwriter
import blpapi
import pandas as pd
import plotly.graph_objects as go
from xbbg import blp
from datetime import timedelta
from plotly.subplots import make_subplots
import plotly.io as pio  # Imported 'pio'
from datetime import datetime, timedelta
import blpapi
from xbbg import blp
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import xlsxwriter

def get_historical_data(ticker_dict, start_date=None, end_date=None):
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365 * 5)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
        
    data_frames = []
    for category, tickers in ticker_dict.items():
        for ticker, name in tickers.items():
            data = blp.bdh(
                tickers=ticker,
                flds=['PX_LAST'],
                start_date=start_date,
                end_date=end_date
            )
            # If DataFrame is empty, print the ticker and continue with the next one
            if data.empty:
                print(f"No data returned for {ticker}")
                continue
            data.columns = [name]
            data_frames.append(data)
    return pd.concat(data_frames, axis=1)

    

# Define tickers and their names, organized by asset type or type of data
ticker_dict = {
    'Bonds': {
        'USGG10YR Index': '10Y Bond Yield',
        'USGG5YR Index': '5Y Bond Yield',
        'USGG2YR Index': '2Y Bond Yield',
        'USGG3M Index': '3M Bond Yield',
        'USGGBE10 Index': 'US Breakeven Inflation 10 Year',
        'USGGBE1 Index': 'US Breakeven Inflation 1 Month',
        'USGGBE3 Index': 'US Breakeven Inflation 3 Year',
        'USGGBE2 Index': 'US Breakeven Inflation 2 Year',
    },
    'Yield Curves': {
        'FDTR Index': 'Federal Funds Effective Rate',
        'USYC2Y10 Index': '2Y-10Y Yield Curve',
        'USYC5Y30 Index': '5Y-30Y Yield Curve',
        'USYC1030 Index': '10Y-30Y Yield Curve',
        'USYC5Y10 Index': '5Y-10Y Yield Curve',
        'USYC2Y5Y Index': '2Y-5Y Yield Curve',
        'USYC3M10 Index': '3M-10Y Yield Curve',
        'USYC2Y30 Index': '2Y-30Y Yield Curve',
        'USYC3M5Y Index': '3M-5Y Yield Curve',
        'USYC2030 Index': '20Y-30Y Yield Curve',
        'USYC5Y7Y Index': '5Y-7Y Yield Curve',
        'USYC7Y10 Index': '7Y-10Y Yield Curve',
        'USYC2Y3Y Index': '2Y-3Y Yield Curve',
        'USYC3Y5Y Index': '3Y-5Y Yield Curve',
        'USYC3Y10 Index': '3Y-10Y Yield Curve',
        'USYC1020 Index': '10Y-20Y Yield Curve',
        'USYC3M2Y Index': '3M-2Y Yield Curve',
        'USYC7Y30 Index': '7Y-30Y Yield Curve',
        'USYC2Y7Y Index': '2Y-7Y Yield Curve',
        'USYC5Y20 Index': '5Y-20Y Yield Curve',
        'USYC1M3M Index': '1M-3M Yield Curve',
        'USYC2Y20 Index': '2Y-20Y Yield Curve',
        'USYC1Y2Y Index': '1Y-2Y Yield Curve',
    },
    'Indexes': {
        'INDU Index': 'Dow Jones Industrial Average',
        'NDX Index': 'Nasdaq 100 Index',
        'VIX Index': 'CBOE Volatility Index',
        'SPY Equity': 'SPDR S&P 500 ETF Trust',
        'BBDXY Index': 'US Financial Conditions Index',
        'SX5E Index': 'Euro Stoxx 50 Index',
        'HSI Index': 'Hang Seng Index',
    },
    'Currencies': {
        'USDJPY Curncy': 'US Dollar vs Japanese Yen Exchange Rate',
        'GBPJPY Curncy': 'British Pound vs Japanese Yen Exchange Rate',
        'EURJPY Curncy': 'Euro vs Japanese Yen Exchange Rate',
        'USDAUD Curncy': 'US Dollar vs Australian Dollar Exchange Rate',
        'USDNZD Curncy': 'US Dollar vs New Zealand Dollar Exchange Rate',
        'EURAUD Curncy': 'Euro vs Australian Dollar Exchange Rate',
        'EURNZD Curncy': 'Euro vs New Zealand Dollar Exchange Rate',
        'GBPAUD Curncy': 'British Pound vs Australian Dollar Exchange Rate',
        'GBPNZD Curncy': 'British Pound vs New Zealand Dollar Exchange Rate',
    },
    'Commodities': {
        'XAU Curncy': 'Gold',
        'XAG Curncy': 'Silver',
        'CL1 Comdty': 'WTI Crude Oil Futures',
        'HG1 Comdty': 'Copper Futures',
    },
}



# Get historical data
historical_data = get_historical_data(ticker_dict=ticker_dict)

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash

# Define the app
app = JupyterDash(__name__)
server = app.server  # crucial for deploying on Azure
# Define the layout of the app
app.layout = html.Div([
    html.H1("My Interactive Financial Dashboard"),
    dcc.Dropdown(
        id='xaxis-column',
        options=[{'label': i, 'value': i} for i in [''] + list(historical_data.columns)],
        value='10Y Bond Yield'
    ),
    dcc.Dropdown(
        id='yaxis-column',
        options=[{'label': i, 'value': i} for i in [''] + list(historical_data.columns)],
        value='2Y-10Y Yield Curve'
    ),
    dcc.Dropdown(
        id='zaxis-column',
        options=[{'label': i, 'value': i} for i in [''] + list(historical_data.columns)],
        value=''
    ),
    dcc.Graph(id='my-graph')
])

# Define the callback
@app.callback(
    Output('my-graph', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('zaxis-column', 'value')]
)
def update_graph(xaxis_column_name, yaxis_column_name, zaxis_column_name):
    data = []
    if xaxis_column_name:
        data.append(go.Scatter(
            x=historical_data.index,
            y=historical_data[xaxis_column_name],
            mode='lines',
            name=xaxis_column_name
        ))
    if yaxis_column_name:
        data.append(go.Scatter(
            x=historical_data.index,
            y=historical_data[yaxis_column_name],
            mode='lines',
            name=yaxis_column_name,
            yaxis='y2'
        ))
    if zaxis_column_name:
        data.append(go.Scatter(
            x=historical_data.index,
            y=historical_data[zaxis_column_name],
            mode='lines',
            name=zaxis_column_name,
            yaxis='y3'
        ))
    return {
        'data': data,
        'layout': go.Layout(
            xaxis={'title': xaxis_column_name},
            yaxis={'title': yaxis_column_name},
            yaxis2={'title': yaxis_column_name, 'overlaying': 'y', 'side': 'right'},
            yaxis3={'title': zaxis_column_name, 'overlaying': 'y', 'side': 'right', 'anchor': 'free'},
            title='Time Series with Rangeslider',
            showlegend=True,
            autosize=False,
            height=800,  # increase height
            width=1500   # increase width
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)

