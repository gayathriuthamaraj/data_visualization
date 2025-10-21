import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

stocks = pd.read_csv(r"C:\Users\gayat\DATA VISUALIZATION\data_visualization\end_sem\stock_data.csv")

graph_1 = px.line(data_frame = stocks.sample(n = 500), x = "RSI", y = "MACD", color = "Target")

app = Dash()

app.layout = [
    html.Div(
        dcc.Dropdown(id = "drop_down", options = ["graph_1", "graph_2"])
    )
    ,
    html.Div(
        children = [dcc.Graph(id = "graph", figure = graph_1)]
        ,
        style = {"background-color" : "lightblue" }
    )
]

@app.callback(
    Output(component_id = "graph", component_property = "figure"),
    Input(component_id = "drop_down", component_property = "value")
)

def update_plot(value):
    if value == "graph_1":
        fig = px.line(stocks.sample(n=500), x="RSI", y="MACD", color="Target")
    else:
        fig = px.line(stocks.sample(n=500), x="Sentiment_Score", y="GDP_Growth", color="Target")
    return fig

if __name__ == "__main__":
    app.run(debug = True)