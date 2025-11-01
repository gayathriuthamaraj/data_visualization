import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash
from dash.dependencies import Input, Output

dataset = pd.read_csv(r"C:\Users\gayat\DATA VISUALIZATION\data_visualization\end_sem\India_Agriculture_Crop_Production_Cleaned.csv")

app = Dash()

app.layout = html.Div(
    children = [
        html.H1("Scatter plot between mid_year and yield: ", id = "title")
        ,
        dcc.Dropdown(id = "drop_down", options = [{"label": label, "value": label} for label in dataset.columns ])
        ,
        dcc.Graph(id = "graph")
    ]
)

@app.callback(
    Output(component_id = "graph", component_property = "figure")
    ,
    Input(component_id = "drop_down", component_property = "value")
)
def update_plot(value):
    line = px.line(data_frame = dataset, x = "start", y = value, color = "Crop")
    return line

if __name__ == "__main__":
    app.run(debug = True)