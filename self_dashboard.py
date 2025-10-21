from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

df = pd.read_csv(r"C:\Users\gayat\DATA VISUALIZATION\data_visualization\retail_sales_dataset.csv")

app = Dash(__name__)

# # Simple figure using Plotly Express' built-in iris dataset
# fig = px.line(
#     df,
#     x="Date",
#     y="Weekly_Sales",
#     color="Store",
#     title="Walmart Weekly Sales",
# )

df["Month"] = pd.to_datetime(df["Date"]).dt.month
monthly_df = df.groupby(["Month"]).sum()
fig = px.line(
    monthly_df,
    x="Date",
    y="Total Amount",
    title="Monthly Sales",
)

app.layout = html.Div([
    html.H3("Monthly Sales"),
    dcc.Graph(figure=fig),
])


if __name__ == "__main__":
    app.run(debug=True)