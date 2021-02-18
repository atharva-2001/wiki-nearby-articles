from dash_bootstrap_components.themes import DARKLY
import flask
import dash
import dash_core_components as dcc
from dash.dependencies import Input, State, Output
import dash_html_components as html
from dash_html_components.Div import Div
import dash_gif_component as Gif
import requests
import numpy as np
import dash_bootstrap_components as dbc
from wikinearbyarticles.bin.wna import wna

points = {}
external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    dbc.themes.BOOTSTRAP,
]

net_layout = {
    "height": 950,
    "width": 1800,
    "hoverlabel": {
        "font": {"family": "monospace"},
    },
    # "template": "plotly_dark",
    "font": {"family": "monospace", "size": 18},
    "scene": {
        "xaxis": {
            # "range": [-50, 50],
            "visible": False,
            "showticklabels": False,
        },
        "yaxis": {
            # "range": [-50, 50],
            "visible": False,
            "showticklabels": False,
        },
        "zaxis": {
            # "range": [-50, 50],
            "visible": False,
            "showticklabels": False,
        },
    },
    "margin": {
        "pad": 0,
        "t": 0,
        "r": 0,
        "l": 0,
        "b": 0,
    },
}


def random_cluster_center(points):
    filtered_points = []
    if points != {}:
        points = points[0]
        for key in points.keys():
            filtered_points += points[key]["point_names"]
            if key in points:
                filtered_points = [item for item in filtered_points if item != key]
                # print(filtered_points)
        r_int = np.random.randint(0, len(filtered_points) - 1)
        # print(r_int, len(filtered_points))
        return filtered_points[r_int]
    else:
        return None


app = dash.Dash(
    __name__,
    # external_stylesheets=[dbc.themes.DARKLY]
    external_stylesheets=external_stylesheets,
)


app.layout = html.Div(
    [
        html.Div(dcc.Graph(id="auto"), style={"width": "100vh", "height": "100vh"}),
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
    ]
)


@app.callback(
    dash.dependencies.Output("auto", "figure"),
    [
        dash.dependencies.Input("submit", "n_clicks"),
        dash.dependencies.Input("interval", "n_intervals"),
    ],
    dash.dependencies.State("art_link", "value"),
)
def update_data(clicks, n_intervals, link):
    global points

    auto = wna(
        link=link,
        points_in_one_shot=5,
        prop_params="links",
        points=points,
        plot_all_points=False,
    )

    center = random_cluster_center(points=points)
    print(f"adding {center}...")
    auto.collect_points(center=random_cluster_center(points=points))
    auto_points = auto.return_points(drop=False)
    points = auto_points

    auto = auto.plot(dot_color="#ff3b3b")
    auto["layout"] = net_layout

    return auto


def run(host="127.0.0.1", debug=True):
    app.run_server(
        debug=debug,
        host=host,
        port=8041,
        dev_tools_ui=False,
        dev_tools_props_check=False,
    )


if __name__ == "__main__":
    run()
