import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Load CSV
df = pd.read_csv(r"C:\Users\gayat\DATA VISUALIZATION\data_visualization\end_sem\AAPL_historical_data.csv")
df["Date"] = pd.to_datetime(df["Date"], utc=True)

def_graph = px.line(df, x="Date", y=["Open", "Close"], color_discrete_sequence=["red", "blue"])

app = Dash(__name__)

year_list = [f"{i}" for i in range(1981, 2025)]

app.layout = html.Div([
    html.H1("Stock Dataset Based on Years"),

    html.Div([
        dcc.Dropdown(
            id="drop_down",
            options=[{"label": year, "value": year} for year in year_list],
            value="2024"  
        )
    ], style={"width": "200px"}),

    html.Div([
        html.H2("All Groups", id="title"),
        dcc.Graph(id="graph", figure=def_graph)
    ])
])

@app.callback(
    Output("graph", "figure"),
    Input("drop_down", "value")
)
def update_graph(value):
    filtered_df = df[df["Date"].dt.year == int(value)]
    fig = px.line(
        filtered_df,
        x="Date",
        y=["Open", "Close"],
        color_discrete_sequence=["red", "blue"],
        title=f"Stock Prices for {value}"
    )
    return fig

@app.callback(
    Output("title", "children"),
    Input("drop_down", "value")
)
def update_title(value):
    return f"Stock Prices for the Year {value}"

if __name__ == "__main__":
    app.run(debug=True)
