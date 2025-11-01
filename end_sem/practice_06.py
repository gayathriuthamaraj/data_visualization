import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

#load the dataset "India_Agriculture_Crop_Production_Cleaned.csv"
dataset = pd.read_csv(r"India_Agriculture_Crop_Production_Cleaned.csv")

#dash app object
app = Dash()

#layout
app.layout = html.Div(
    children = [
        html.H1("Indian Agriculture Crop Production")
        ,
        dcc.RangeSlider(
            id = "range_slider"
            ,
            min = 1997
            ,
            max = 2021
            ,
            value = [1997,2021]
            ,
            step = 1
            ,
            vertical = False
        )
        ,
        html.Div(
            children = [
                html.H2("Yield between 1997 and 2021", id = "title")
                ,
                dcc.Graph(id = "graph_main")
            ]
        )
    ]
)

@app.callback(
    Output("graph_main", "figure"),
    Input("range_slider", "value")
)
def update_plot(year_range):
    start, end = year_range
    copy_dataset = dataset.copy(deep=True)

    # ensure datetime type
    copy_dataset["start"] = pd.to_datetime(copy_dataset["start"], utc=True)
    copy_dataset["end"] = pd.to_datetime(copy_dataset["end"], utc=True)

    # filter by years
    copy_dataset = copy_dataset[
        (copy_dataset["start"].dt.year >= start) &
        (copy_dataset["end"].dt.year <= end)
    ]

    # mid-year for x-axis
    copy_dataset["mid_year"] = (
        copy_dataset["start"].dt.year + copy_dataset["end"].dt.year
    ) / 2

    bar = px.histogram(
        data_frame=copy_dataset,
        x="Season",
        y="Yield",
        color="State",
        title=f"Crop Yield from {start} to {end}"
    )
    return bar


if __name__ == "__main__":
    app.run(debug = True)