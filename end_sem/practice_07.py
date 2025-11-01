import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

dataset = pd.read_csv(r"C:\Users\gayat\DATA VISUALIZATION\data_visualization\end_sem\India_Agriculture_Crop_Production_Cleaned.csv")
dataset["start"] = pd.to_datetime(dataset["start"], utc = True)
dataset["end"] = pd.to_datetime(dataset["end"], utc = True)
dataset["mid_year"] = (
    dataset["start"].dt.year + dataset["end"].dt.year
) / 2
dataset["mid_year"] = dataset["mid_year"].astype(int)

grouped_df = (
    dataset.groupby(["Crop", "mid_year"], as_index=False)
    .agg({"Yield": "mean"})
)
grouped_df = grouped_df.sort_values(["Crop", "mid_year"])

app = Dash()

graph_1 = px.line(data_frame = grouped_df, x = "mid_year", y = "Yield", color = "Crop")

app.layout = html.Div(
    children = [
        html.Div(
            children = [
                html.H2("Crop Yields Over Time: "),
                dcc.Graph(id = "graph_1", figure = graph_1)
            ]
        )
    ]
)


if __name__ == "__main__":
    app.run(debug = True)