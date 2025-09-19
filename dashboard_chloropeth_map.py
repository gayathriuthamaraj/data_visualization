from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd


app = Dash(__name__)

# Use Plotly's built-in Gapminder dataset (has ISO country codes & geodata-ready fields)
gap = px.data.gapminder()
years = sorted(gap["year"].unique())
continents = sorted(gap["continent"].unique())
metrics = {
    "Life Expectancy": "lifeExp",
    "GDP per Capita": "gdpPercap",
    "Population": "pop",
}


app.layout = html.Div([
    html.H2("Global Indicators Dashboard (Choropleth + Context)"),

    # Controls
    html.Div([
        html.Div([
            html.Label("Metric"),
            dcc.Dropdown(
                id="metric",
                options=[{"label": k, "value": v} for k, v in metrics.items()],
                value="lifeExp",
                clearable=False,
            ),
        ], style={"flex": 1, "minWidth": 220, "marginRight": 8}),
        html.Div([
            html.Label("Continents"),
            dcc.Dropdown(
                id="continents",
                options=[{"label": c, "value": c} for c in continents],
                value=continents,
                multi=True,
            ),
        ], style={"flex": 1, "minWidth": 280, "marginRight": 8}),
        html.Div([
            html.Label("Year"),
            dcc.Slider(
                id="year",
                min=years[0], max=years[-1], step=None, value=2007,
                marks={str(y): str(y) for y in years},
                tooltip={"always_visible": False, "placement": "bottom"},
            ),
        ], style={"flex": 2, "minWidth": 320}),
    ], style={"display": "flex", "flexWrap": "wrap", "marginBottom": 12}),

    # Row 1: Choropleth + Top-10 bar
    html.Div([
        html.Div([dcc.Graph(id="choropleth")], style={"flex": 2, "minWidth": 420, "marginRight": 8}),
        html.Div([dcc.Graph(id="top10")], style={"flex": 1, "minWidth": 320}),
    ], style={"display": "flex", "flexWrap": "wrap", "marginBottom": 10}),

    # Row 2: Time series for selected country
    html.Div([
        html.Div([dcc.Graph(id="timeseries")], style={"flex": 1, "minWidth": 420}),
    ], style={"display": "flex", "flexWrap": "wrap"}),

    # Hidden store for selected country code (ISO-3)
    dcc.Store(id="selected-iso3"),
])
def _filter_df(selected_year: int, allowed_continents: list[str]) -> pd.DataFrame:
    df = gap[gap["year"] == selected_year]
    if allowed_continents:
        df = df[df["continent"].isin(allowed_continents)]
    return df


@app.callback(
    Output("choropleth", "figure"),
    Output("top10", "figure"),
    Input("metric", "value"),
    Input("continents", "value"),
    Input("year", "value"),
)
def update_maps(metric_col: str, continents_selected: list[str], year_value: int):
    df_year = _filter_df(year_value, continents_selected)

    # Choropleth map
    color_title = [k for k, v in metrics.items() if v == metric_col][0]
    choro = px.choropleth(
        df_year,
        locations="iso_alpha",
        color=metric_col,
        hover_name="country",
        hover_data={metric_col: ":,.0f" if metric_col != "lifeExp" else ":.1f", "continent": True},
        color_continuous_scale="Viridis",
        title=f"{color_title} ({year_value})",
        projection="natural earth",
    )
    choro.update_layout(margin=dict(l=10, r=10, t=50, b=0), height=520)

    # Top-10 bar chart for the selected metric
    top10_df = df_year.nlargest(10, metric_col).sort_values(metric_col, ascending=True)
    bar = px.bar(
        top10_df,
        x=metric_col,
        y="country",
        color="continent",
        orientation="h",
        title=f"Top 10 by {color_title} ({year_value})",
    )
    bar.update_layout(margin=dict(l=10, r=10, t=50, b=30), height=520)

    return choro, bar


@app.callback(
    Output("selected-iso3", "data"),
    Input("choropleth", "clickData"),
    prevent_initial_call=True,
)
def store_clicked_country(click_data):
    if not click_data:
        return None
    # clickData contains location (ISO-3) for choropleth points
    return click_data.get("points", [{}])[0].get("location")


@app.callback(
    Output("timeseries", "figure"),
    Input("selected-iso3", "data"),
    Input("metric", "value"),
)
def update_timeseries(iso3: str | None, metric_col: str):
    color_title = [k for k, v in metrics.items() if v == metric_col][0]
    if not iso3:
        # Default: world averages per year for selected metric
        df = gap.groupby("year", as_index=False)[metric_col].mean()
        fig = px.line(df, x="year", y=metric_col, markers=True,
                      title=f"Global Average {color_title} Over Time")
        fig.update_layout(margin=dict(l=10, r=10, t=50, b=30), height=360)
        return fig

    df = gap[gap["iso_alpha"] == iso3]
    country_name = df["country"].iloc[0] if not df.empty else iso3
    fig = px.line(df, x="year", y=metric_col, markers=True,
                  title=f"{country_name}: {color_title} Over Time")
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=30), height=360)
    return fig


if __name__ == "__main__":
    app.run(debug=True)