import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

dataset = pd.read_csv(r"C:\Users\gayat\DATA VISUALIZATION\data_visualization\end_sem\AAPL_historical_data.csv")
dataset["Date"] = pd.to_datetime(dataset["Date"], utc=True)

app = Dash()

year_data = {str(i) : i for i in range(1981, 2025)}
year_data["all years"] = 0
app.layout = html.Div(
    children = [
        html.H1("Low and High Data: ")
        ,
        html.Div(
            children = [
                html.H2("Year: ", id = "title")
                ,
                dcc.Dropdown(id = "drop_down", options = [{"label": k, "value": v} for k, v in year_data.items()], value = 0)
                ,
                dcc.Graph(id = "graph")
            ]
        )
    ]
)

@app.callback(
    Output(component_id = "graph", component_property = "figure")
    ,
    Input(component_id = "drop_down", component_property = "value")
)
def update_plot_1(value):
    if value == 0:
        bar_fig = px.line(data_frame = dataset, x = "Date", y = ["High", "Close"], color_discrete_sequence = ["red", "blue"])
        return bar_fig
    else:
        bar_fig = px.line(data_frame = dataset[dataset["Date"].dt.year == value], x = "Date", y = ["High", "Close"], color_discrete_sequence = ["red", "blue"])
        return bar_fig
    
@app.callback(
    Output(component_id = "title", component_property = "children")
    ,
    Input(component_id = "drop_down", component_property = "value")
)
def update_plot_2(value):
    if value == 0:
        return "Year: All"
    else:
        return f"Year: {value}"
    

if __name__ == "__main__":
    app.run(debug = True)