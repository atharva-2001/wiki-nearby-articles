import flask
import dash
import dash_core_components as dcc
from dash.dependencies import Input, State, Output
import dash_html_components as html
from dash_html_components.Div import Div
import dash_gif_component as Gif
import requests
import dash_bootstrap_components as dbc
from wikinearbyarticles.bin.wna import wna

points = {}
external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    dbc.themes.BOOTSTRAP,
]

net_layout = {
    "height": 1200,
    "width": 800,
    "hoverlabel": {
        "font": {"family": "monospace"},
        # "hover"
    },
    # template = "plotly_dark",
    "font": {"family": "monospace", "size": 15},
    "scene": {
        "xaxis": {"visible": False, "showticklabels": False},
        "yaxis": {"visible": False, "showticklabels": False},
        "zaxis": {"visible": False, "showticklabels": False},
    },
    "margin": {
        "pad": 0,
        "t": 0,
        "r": 0,
        "l": 0,
        "b": 0,
    },
}
app = dash.Dash(
    __name__,
    # external_stylesheets=[dbc.themes.DARKLY]
    external_stylesheets=external_stylesheets,
)


app.layout = html.Div(
    html.Div(dcc.Graph(id="auto")),
    html.Div(
        [
            html.Div(id="target"),
            html.Div(
                children=[
                    html.Div(
                        dcc.Input(
                            id="art_link",
                            className="text_input",
                            # placeholder = "enter wikipedia article link",
                            value="https://en.wikipedia.org/wiki/Atom",
                            style={
                                # "padding-left": "10%",
                                "font-size": "18px",
                                # "fontFamily": "monospace",
                                "width": "100%",
                                "text-align": "center",
                                "text-spacing": "1px",
                                # 'padding-left':'10%', 'padding-right':'10%',
                                "border": "0px none",
                                "border-bottom": "0.5px solid #5c5c5c",
                                # "background-color": "#1a1a1a",
                                "color": "#525252",
                                "-webkit-box-shadow": "0 2px 2px -2px grey",
                                "-moz-box-shadow": "0 2px 2px -2px grey",
                                "box-shadow": "0 2px 2px -2px grey",
                            },
                        ),
                        style={
                            "display": "inline-block",
                            "width": "100%",
                            "padding-bottom": "8px",
                            # "box-shadow": " 10px 0px px 0px lightgrey",
                        },
                    ),
                    html.Div(
                        html.Button(
                            id="submit",
                            type="submit",
                            children="ok",
                            style={"width": "100%"},
                        ),
                        style={
                            "display": "inline-block",
                            "width": "10%",
                            "padding-bottom": "15px",
                            # "padding-right": "10%",
                        },
                    ),
                ],
                style={
                    "padding-left": "10%",
                    "padding-right": "10%",
                    "text-align": "center",
                },
            ),
        ]
    ),
    dcc.Interval(id="interval"),
)


@app.callback(
    [
        dash.dependencies.Output("auto", "extendData"),
    ],
    [
        dash.dependencies.Input("submit", "n_clicks"),
        dash.dependencies.Input("interval", "n_interval"),
    ],
    dash.dependencies.State("art_link", "value"),
)
def update_data(clicks, link):
    global points
    auto = wna(
        link=link,
        prop_params="links",
        points=points,
        plot_all_points=False,
    )

    auto.collect_points(center=None)  # ! get random centers
    auto_points = auto.return_points(drop=False)
    auto = auto.plot()
    auto["layout"] = net_layout
