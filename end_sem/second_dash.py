import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

stocks = pd.read_csv(r"C:\Users\gayat\DATA VISUALIZATION\data_visualization\end_sem\stock_data.csv")

graph_1 = px.line(data_frame = stocks.sample(n = 500), x = "RSI", y = "MACD", color = "Target")
graph_2 = px.line(data_frame = stocks.sample(n = 500), x = "Sentiment_Score", y = "GDP_Growth", color = "Target")

app = Dash()

app.layout = [html.Div(children = [html.H1("RSI and MACD"), dcc.Graph(id = "graph_1", figure = graph_1)]), html.Div(children = [html.H1("Sentiment_Score and GDP_Growth"), dcc.Graph(id = "graph_2", figure = graph_2)])]

if __name__ == "__main__":
    app.run(debug = True)
