from dash import Dash, dcc, html
import plotly.express as px


app = Dash(__name__)

# Simple figure using Plotly Express' built-in iris dataset
fig = px.scatter(
    px.data.iris(),
    x="sepal_width",
    y="sepal_length",
    color="species",
    title="Dash Hello World: Iris Scatter",
)

app.layout = html.Div([
    html.H3("Dash Hello World"),
    dcc.Graph(figure=fig),
])


if __name__ == "__main__":
    app.run(debug=True)

