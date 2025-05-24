import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html, dcc
from dash.dependencies import Input, Output
import random
from datetime import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

app.layout = dbc.Container([
    # Header
    dbc.Row(
        dbc.Col(html.H2("Autonomous Vehicle Dashboard", className="text-center text-primary mb-2"))
    ),

    # Main content
    dbc.Row([
        # Left column
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("System Status"),
                dbc.CardBody([
                    html.P("Model Name: VisionPilotNet-XL"),
                    html.P("GPU: NVIDIA Jetson AGX Orin"),
                    html.P(id="server-comm", children="Server Comm. Time: 0 ms"),
                    html.P(id="server-resp", children="Server Resp. Time: 0 ms"),
                    html.P(id="waypoints", children="Predicted Waypoints: []")
                ])
            ], className="mb-3"),
            dbc.Card([
                dbc.CardHeader("Sensor Output"),
                dbc.CardBody([
                    html.P(id="gps", children="GPS Coordinates: 0° N, 0° W"),
                    html.P(id="velocity", children="Velocity: 0 km/h")
                ])
            ])
        ], width=4),

        # Middle column
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    dbc.Button("Switch to Depth View", color="primary")
                ),
                dbc.CardBody(
                    html.P(
                        "This panel represents the operational status and communication link with the vehicle's hardware. Currently in simulated mode."
                    )
                )
            ], className="mb-3"),
            dbc.Card([
                dbc.CardHeader("⚡ Car Energy Consumption Data"),
                dbc.CardBody(html.P(id="energy", children="Current Output: 0 watts"))
            ])
        ], width=4),

        # Right column
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("RGB Camera Feed"),
                dbc.CardBody(
                    html.Img(
                        src="https://via.placeholder.com/600x400?text=Camera+Feed",
                        style={"width": "100%", "border-radius": "4px"}
                    )
                )
            ], className="mb-3"),
            dbc.Card([
                dbc.CardHeader("Vehicle Control"),
                dbc.CardBody(
                    dbc.Row([
                        dbc.Col(
                            daq.Gauge(
                                id="steering", label="Steering", min=-45, max=45, value=0, showCurrentValue=True
                            ), width=6
                        ),
                        dbc.Col(
                            daq.Gauge(
                                id="throttle", label="Throttle", min=0, max=100, value=0, showCurrentValue=True
                            ), width=6
                        )
                    ])
                )
            ])
        ], width=4)
    ]),

    # Quit button
    # dbc.Row(
    #     dbc.Col(
    #         dbc.Button("Quit Session", color="danger"),
    #         className="mt-4"
    #     )
    # ),

    # Interval for simulated updates
    dcc.Interval(id="interval", interval=1000, n_intervals=0)
], fluid=True)

# Callbacks to simulate dynamic values
@app.callback(
    [Output('server-comm', 'children'),
     Output('server-resp', 'children'),
     Output('waypoints', 'children'),
     Output('gps', 'children'),
     Output('velocity', 'children'),
     Output('energy', 'children'),
     Output('steering', 'value'),
     Output('throttle', 'value')],
    Input('interval', 'n_intervals')
)
def update_metrics(n):
    comm = f"Server Comm. Time: {random.uniform(10, 30):.2f} ms"
    resp = f"Server Resp. Time: {random.uniform(40, 80):.2f} ms"
    wpts = [(round(random.uniform(34,35),2), round(random.uniform(-119,-118),2)) for _ in range(3)]
    gps = f"GPS Coordinates: {wpts[0][0]}° N, {wpts[0][1]}° W"
    vel = f"Velocity: {random.uniform(0, 60):.2f} km/h"
    energy = f"Current Output: {random.randint(500,1200)} watts"
    steering = random.uniform(-30, 30)
    throttle = random.uniform(0, 100)
    return comm, resp, str(wpts), gps, vel, energy, steering, throttle

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080)