from logging import PlaceHolder
import dash
from dash.dependencies import State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import math
import numpy as np
import requests
import re
import json
from wikinearbyarticles.bin.helpers import wna

# TODO add animations
# TODO between graphs as they are updated, extending graphs


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__,
    # external_stylesheets=[dbc.themes.DARKLY]
    external_stylesheets=external_stylesheets,
)

net_layout = {
    "height": 1200,
    "width": 800,
    "hoverlabel": {
        "font": {"family": "monospace"},
        # "hover"
    },
    # template = "plotly_dark",
    "font": {"family": "monospace", "size": 18},
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

app.layout = html.Div(
    [
        html.Div(
            html.P(
                "wiki nearby articles",
                style={
                    "font-size": "72px",
                    "fontFamily": "monospace",
                    "letter-spacing": "5px",
                    "text-align": "center",
                    "font-weight": "light",
                    "color": "#525252",
                },
            )
        ),
        html.Div(html.Hr()),
        html.Div(
            html.P("enter article link below"),
            style={
                "font-size": "13px",
                "letter-spacing": "2px",
                "fontFamily": "monospace",
                "margin": "0  auto",
                "display": "center",
                "width": "100%",
                "text-align": "center",
                # 'padding-left':'10%', 'padding-right':'10%',
                "border": "none",
                "border-bottom": "0px solid #5c5c5c",
                # "background-color": "#1a1a1a",
                "color": "#9c9c9c",
                "padding-bottom": "3px",
            },
        ),
        html.Div(
            [
                dcc.Input(
                    id="art_link",
                    className="text_input",
                    # placeholder = "enter wikipedia article link",
                    value="https://en.wikipedia.org/wiki/MissingNo.",
                    style={
                        "font-size": "18px",
                        "fontFamily": "monospace",
                        "margin": "0  auto",
                        "display": "center",
                        "width": "100%",
                        "text-align": "center",
                        "text-spacing": "1px",
                        # 'padding-left':'10%', 'padding-right':'10%',
                        "border": "none",
                        "border-bottom": "0.5px solid #5c5c5c",
                        # "background-color": "#1a1a1a",
                        "color": "#525252",
                        "padding-bottom": "3px",
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    html.P(id="main-article-summary"),
                    style={
                        "font-size": "17px",
                        "letter-spacing": "2px",
                        "fontFamily": "monospace",
                        "margin": "0  auto",
                        "display": "center",
                        "width": "60%",
                        "text-align": "center",
                        # 'padding-left':'10%', 'padding-right':'10%',
                        "border": "none",
                        # "border-bottom": "2px solid #5e5e5e",
                        # "background-color": "#1a1a1a",
                        "color": "#5e5e5e",
                        # "padding-bottom": "3px",
                        "padding-left": "10px",
                        "padding-right": "10px",
                        "padding-top": "10px",
                    },
                )
            ]
        ),
        html.Div(html.Br()),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="choose-section-forward",
                        # ! options will depend upon the link
                        # options = [{"label": f"section number: {i}", "value": f"{section}"} for i,section in enumerate(get_points(points = forward_points, points_in_one_plot= 15))]
                    ),
                    style={
                        "width": "10%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
                html.Div(
                    dcc.Dropdown(
                        id="choose-section-backward",
                        # ! options will depend upon the link
                        # options = [{"label": f"section number: {i}", "value": f"{section}"} for i,section in enumerate(get_points(points = backward_points, points_in_one_plot= 15))]
                    ),
                    style={
                        "width": "10%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
                html.Div(
                    dcc.Dropdown(
                        id="points-fw",
                        # ! options will depend upon the link
                        # options = [{"label": f"section number: {i}", "value": f"{section}"} for i,section in enumerate(get_points(points = backward_points, points_in_one_plot= 15))]
                    ),
                    style={
                        "width": "40%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
                html.Div(
                    dcc.Dropdown(
                        id="points-bw",
                        # ! options will depend upon the link
                        # options = [{"label": f"section number: {i}", "value": f"{section}"} for i,section in enumerate(get_points(points = backward_points, points_in_one_plot= 15))]
                    ),
                    style={
                        "width": "40%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    html.P("article directs to these articles"),
                    style={
                        "width": "48%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
                html.Div(
                    html.P(),
                    style={
                        "width": "2%",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
                html.Div(
                    html.P("article is directed from these articles"),
                    style={
                        "width": "48%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
            ]
        ),
        html.Div(html.Br()),
        html.Div(
            [
                html.Div(
                    html.Div(
                        dcc.Graph(
                            id="forwards",
                            responsive=True,
                            style={
                                "width": "100%",
                                "height": "100%",
                            },
                        ),
                        style={
                            "width": "100%",
                            "height": "100%",
                        },
                    ),
                    style={
                        "width": "68%",
                        "height": "800px",
                        "display": "inline-block",
                        "border": "3px #5c5c5c solid",
                        "padding-top": "5px",
                        "padding-left": "1px",
                        "overflow": "hidden",
                    },
                ),
                html.Div(
                    style={
                        "width": "2%",
                        "height": "800px",
                        "display": "inline-block",
                        "padding-top": "5px",
                        "overflow": "hidden",
                    }
                ),
                html.Div(
                    html.P(id="forward-hover-description"),
                    style={
                        "width": "26%",
                        "font-size": "15.5px",
                        "height": "800px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                        # "margin": "auto",
                        # "border": "3px #5c5c5c solid",
                        "overflow": "hidden",
                        # "padding-top": "350px",
                        # "padding-bottom": "350px",
                        "padding-left": "1px",
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    html.Div(
                        dcc.Graph(
                            id="backwards",
                            responsive=True,
                            style={"width": "100%", "height": "100%"},
                        ),
                        style={
                            "width": "100%",
                            "height": "100%",
                        },
                    ),
                    style={
                        "width": "68%",
                        "height": "800px",
                        "display": "inline-block",
                        "border": "3px #5c5c5c solid",
                        "padding-top": "5px",
                        "padding-left": "1px",
                        "overflow": "hidden",
                    },
                ),
                html.Div(
                    html.P(),
                    style={
                        "width": "2%",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
                html.Div(
                    html.P(id="backward-hover-description"),
                    style={
                        "width": "26%",
                        "font-size": "15.5px",
                        "height": "800px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                        "margin": "auto",
                        # "border": "3px #5c5c5c solid",
                        "overflow": "hidden",
                        # "padding-top": "350px",
                        # "padding-bottom": "350px",
                        "padding-left": "1px",
                    },
                ),
            ]
        ),
    ]
)

# art = art_from_origin(prop_params = "linkshere")
# _, _ = create_random_populated_sphere(radius=1000, points=art, plot_flag=True, show_lines_with_origin=True)


@app.callback(
    [
        dash.dependencies.Output("forwards", "figure"),
        dash.dependencies.Output("backwards", "figure"),
        dash.dependencies.Output("main-article-summary", "children"),
        dash.dependencies.Output("points-fw", "options"),
        dash.dependencies.Output("points-bw", "options"),
        
    ],
    dash.dependencies.Input("art_link", "value"),
)
def update_output(art_link):

    # article_name = art_link.split("/")[-1]
    # # print(article_name)
    # art = art_from_origin(prop_params = "links", article_name = article_name)
    # # print(art)
    # forwards = create_random_populated_sphere(radius=100, points=art, plot_flag=False, show_lines_with_origin=True)

    # art = art_from_origin(prop_params = "linkshere", article_name = article_name)
    # backwards = create_random_populated_sphere(radius=100, points=art, plot_flag=False, show_lines_with_origin=True, dot_color="#ff3b3b")

    # TODO this is a temporary solution, fix it
    title = art_link.split("/")[-1]
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "exsentences": "5",
        "exlimit": "1",
        "explaintext": "1",
        "formatversion": "2"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    summary = DATA["query"]["pages"][0]["extract"]

    forwards = wna(link=art_link, prop_params="links")
    fw_points = forwards.return_points()
    fw_points = [{"label": item, "value": item} for item in fw_points]
    forwards = forwards.plot_points()
    forwards["layout"] = net_layout

    backwards = wna(link=art_link, prop_params="linkshere")
    bw_points = backwards.return_points()
    bw_points = [{"label": item, "value": item} for item in bw_points]
    backwards = backwards.plot_points(dot_color="#ff3b3b")
    

    return (forwards, backwards, summary, fw_points, bw_points)


@app.callback(
    dash.dependencies.Output("forward-hover-description", "children"),
    dash.dependencies.Input("forwards", "hoverData"),
)
def show_hover_text(data):
    try:
        # print(data)
        data = data["points"][0]
        if "hovertext" not in data.keys():
            print("hovering on lines")
            text = ""
        else:
            print("hovering on point ", end="")
            art_name = data["hovertext"]
            print(art_name)
            wna_hover = wna(link=art_name, prop_params="links")
            hover = wna_hover.article_summary_for_hover(
                collect_points=False, number_of_lines=8
            )
            # print(hover, type(hover))
            text = hover["query"]["pages"][0]["extract"]
            if text == "":
                text = "no summary available"
            print("got hover data")
    except:
        text = ""
        pass
    return text


@app.callback(
    dash.dependencies.Output("backward-hover-description", "children"),
    dash.dependencies.Input("backwards", "hoverData"),
)
def show_hover_text(data):
    try:
        # print(data)
        data = data["points"][0]
        if "hovertext" not in data.keys():
            print("hovering on lines")
            text = ""
        else:
            print("hovering on point ", end="")
            art_name = data["hovertext"]
            print(art_name)
            wna_hover = wna(link=art_name, prop_params="links")
            hover = wna_hover.article_summary_for_hover(
                collect_points=False, number_of_lines=8
            )
            # print(hover, type(hover))
            text = hover["query"]["pages"][0]["extract"]
            if text == "":
                text = "no summary available"
            print("got hover data")
    except:
        text = ""
        pass
    return text

# @app.callback(
#     dash.dependencies.Output("points", "options"),
#     dash.dependencies.Input("forwards", "hoverData")
# )
# def update_hover_dropdown(data):
#     data = data["points"][0]
#     art_name = data["hovertext"]
#     wna_hover = wna(link=art_name, prop_params="links")
#     points = wna_hover.return_points()
#     return points
# @app.callback(
#     dash.dependencies.Output("forwards", "figure"),
#     [dash.dependencies.Input("art_link", "value")],
#     [State("forwards", "figure")]
# )
# def set_layout(value, fig):
#     fig["layout"] = net_layout
#     return fig


def run(port=8050, host="127.0.0.1", debug=True):
    app.run_server(debug=debug, port=port, host=host)


if __name__ == "__main__":
    run()
