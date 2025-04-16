import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import os

# Change the working directory
os.chdir("c:/Users/aramamoorthy/Desktop/Build/Batt_An/E-Scooter")

# Print the current working directory to confirm the change
print("Current working directory:", os.getcwd())

# Load data
vehicle_df = pd.read_csv("scooter_fleet_vehicle_data.csv")
battery_df = pd.read_csv("scooter_battery_health_data.csv")

# Merge data
merged_df = pd.merge(vehicle_df, battery_df, on=["scooter_id", "date"])
merged_df["date"] = pd.to_datetime(merged_df["date"], format="%Y-%m-%d", errors="coerce")

# Init app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "E-Scooter Fleet Dashboard"

# Layout
app.layout = dbc.Container([
    html.H1("E-Scooter Fleet Analytics Dashboard", className="text-center mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="scooter-dropdown",
                options=[{"label": f"Scooter {i}", "value": i} for i in sorted(merged_df["scooter_id"].unique())],
                value=1,
                placeholder="Select a Scooter"
            )
        ], width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="soh-graph"), width=6),
        dbc.Col(dcc.Graph(id="battery-temp-graph"), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="usage-graph"), width=12),
    ]),
])

# Callbacks
@app.callback(
    [Output("soh-graph", "figure"),
     Output("battery-temp-graph", "figure"),
     Output("usage-graph", "figure")],
    [Input("scooter-dropdown", "value")]
)
def update_graphs(scooter_id):
    df = merged_df[merged_df["scooter_id"] == scooter_id]

    fig_soh = px.line(df, x="date", y="state_of_health", title="State of Health Over Time")
    fig_temp = px.line(df, x="date", y="battery_temperature_c", title="Battery Temperature (°C)")
    fig_usage = px.bar(df, x="date", y="usage_hours", title="Daily Usage Hours")

    return fig_soh, fig_temp, fig_usage

# Run server
if __name__ == '__main__':
    app.run(debug=True)
