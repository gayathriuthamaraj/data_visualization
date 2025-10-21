import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

stock_data = pd.read_csv(r"C:\Users\gayat\DATA VISUALIZATION\data_visualization\end_sem\stock_data.csv")
app = Dash()

line_graph = px.scatter(data_frame = stock_data.sample(n = 500), x = "Open", y = "Close", color = "Target")
bar_graph = px.scatter(data_frame = stock_data.sample(n = 500), x = "Bollinger_Upper", y = "Bollinger_Lower", color = "Target")

app.layout = [html.H1("Bollinger_Upper and Bollinger_Lower Data"), 
              html.Div(children = [dcc.Graph(id = "line_graph", figure = line_graph), dcc.Graph(id = "bar_graph", figure = bar_graph)])]

if __name__ == "__main__":
    app.run(debug = True)