import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import json
import dash_bootstrap_components as dbc
from wikinearbyarticles.bin.wna import WNA
from wikinearbyarticles.bin.util import random_cluster_center

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
    "font": {"family": "monospace", "size": 10},
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
                                    "font-size": "18px",
                                    "width": "100%",
                                    "text-align": "center",
                                    "text-spacing": "1px",
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
    if n_intervals is None:
        points = {}
        for cookie, val in flask.request.cookies.items():
            dash.callback_context.response.delete_cookie(cookie)
    else:
        points = json.loads(flask.request.cookies["points"])

    auto = WNA(
        link=link,
        points_in_one_shot=5,
        prop_params="links",
        points=points,
        plot_all_points=False,
    )

    if not points:
        print("adding *main*...")
        auto.collect_points()
        points = auto.return_points(drop=False)
    else:
        center = random_cluster_center(points=points)
        print(f"adding {center}...")
        auto.collect_points(center=center)
        points = auto.return_points(drop=False)

    auto = auto.plot(dot_color="#ff3b3b")
    auto["layout"] = net_layout

    dash.callback_context.response.set_cookie(
        "points", json.dumps(points).encode("utf-8")
    )

    return auto


def run(host="127.0.0.1", debug=True):
    app.run_server(
        debug=debug,
        host=host,
        port=8042,
    )


if __name__ == "__main__":
    run()
