import flask
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as Gif
import requests
import dash_bootstrap_components as dbc
from wikinearbyarticles.bin.wna import wna

# TODO add animations
# TODO between graphs as they are updated, extending graphs
fw_points_global = {}
bw_points_global = {}
art_link_bw = ""
art_link_fw = ""
bw_dropdown_value = ""
fw_dropdown_value = ""
summary = ""

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    dbc.themes.BOOTSTRAP,
]

app = dash.Dash(
    __name__,
    # external_stylesheets=[dbc.themes.DARKLY]
    external_stylesheets=external_stylesheets,
)

server = app.server
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

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(id="fw-points"),
                dcc.Store(id="bw-points"),
                dcc.Store(id="art_link_bw"),
                dcc.Store(id="art_link_fw"),
                dcc.Store(id="bw_dropdown_value"),
                dcc.Store(id="fw_dropdown_value"),
                dcc.Store(id="summary"),
            ]
        ),
        html.Div(
            dbc.Modal(
                [
                    dbc.ModalHeader(
                        [
                            html.P(
                                "Have Patience Please",
                                style={
                                    "font-size": "17px",
                                    "letter-spacing": "2px",
                                    "text-align": "center",
                                    "margin": "auto",
                                },
                            )
                        ],
                    ),
                    dbc.ModalBody(
                        [
                            html.P(
                                "the site takes a couple seconds to load, just hold on :)"
                            )
                        ],
                        style={"font-size": "14px"},
                    ),
                ],
                id="sad-intro",
                is_open=True,
                scrollable=True,
                centered=True,
            )
        ),
        html.Div(
            html.P(
                "wiki nearby articles",
                style={
                    "font-size": "72px",
                    # "fontFamily": "monospace",
                    "letter-spacing": "5px",
                    "text-align": "center",
                    "font-weight": "light",
                    "color": "#525252",
                    "text-shadow": "1.5px 1.5px lightgrey",
                },
            )
        ),
        html.Div(
            [
                html.Div(
                    html.Button("Show me around", id="open-help"),
                    style={
                        "text-align": "center",
                    },
                ),
                html.Div(
                    dbc.Modal(
                        [
                            dbc.ModalHeader(
                                [
                                    html.P(
                                        "What  is  this?",
                                        style={
                                            "font-size": "17px",
                                            "letter-spacing": "2px",
                                            "text-align": "center",
                                            "margin": "auto",
                                        },
                                    )
                                ],
                            ),
                            dbc.ModalBody(
                                [
                                    html.P(
                                        "This website helps you find connections between wikipedia articles."
                                    ),
                                    html.Div(
                                        Gif.GifPlayer(
                                            gif="assets/dropdown.gif",
                                            still="assets/dropdown.png",
                                        )
                                    ),
                                    html.P(
                                        "Use the dropdown to create connections. In the first graph, which has blue points, the dropdown has names of articles that are mentioned in the parent article. For example, the wikipedia article of Atom mentions the wikipedia article of Electron. The Cluster of Atom will have Electron as a point. You can similarly expand the cluster of Electron and see what articles are mentioned in it's article. You can do that by selecting electron from the dropdown. "
                                    ),
                                    html.P(
                                        "The second graph is the exact opposite of the first graph. Here, the articles that mention the article of Atom, surround it. For example, the wikipedia article of Albert Einstein mentions the wikipedia article of Atom. Hence, it is a point in the cluster of Atom. If you select Albert Einstein from the dropdown, all the articles which mention Albert Einstein will surround it. "
                                    ),
                                ],
                                style={"font-size": "14px"},
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close", id="close-help", className="ml-auto"
                                )
                            ),
                        ],
                        id="help",
                        # is_open=True,
                        size="xl",
                        scrollable=True,
                    )
                ),
            ]
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
        html.Div(
            [
                html.Div(
                    html.P(id="main-article-summary"),
                    style={
                        "font-size": "17px",
                        "letter-spacing": "2px",
                        # "fontFamily": "monospace",
                        "margin": "0  auto",
                        "display": "center",
                        "width": "60%",
                        "text-align": "center",
                        # 'padding-left':'10%', 'padding-right':'10%',
                        "border": "none",
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
                    html.P("article directs to these articles"),
                    style={
                        "width": "100%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="choose-section-forward",
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
                    dcc.Dropdown(id="points-fw", placeholder="expand articles"),
                    style={
                        "width": "90%",
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
                        "height": "1000px",
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
                        "height": "1000px",
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
                        "height": "1000px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                        "overflow": "hidden",
                        "padding-left": "1px",
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    html.P("article is directed from these articles"),
                    style={
                        "width": "100%",
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
                    dcc.Dropdown(
                        id="choose-section-backward",
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
                    dcc.Dropdown(id="points-bw", placeholder="expand articles"),
                    style={
                        "width": "90%",
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
                        "height": "1000px",
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
                        "height": "1000px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                        "margin": "auto",
                        "overflow": "hidden",
                        "padding-left": "1px",
                    },
                ),
            ]
        ),
    ]
)


@app.callback(
    dash.dependencies.Output("help", "is_open"),
    [
        dash.dependencies.Input("open-help", "n_clicks"),
        dash.dependencies.Input("close-help", "n_clicks"),
    ],
    [dash.dependencies.State("help", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# this callback will only work when the article link is changed
@app.callback(
    [
        dash.dependencies.Output("forwards", "figure"),
        dash.dependencies.Output("main-article-summary", "children"),
        dash.dependencies.Output("points-fw", "options"),
        dash.dependencies.Output("fw-points", "data"),
        dash.dependencies.Output("fw_dropdown_value", "data"),
        dash.dependencies.Output("art_link_fw", "data"),
        dash.dependencies.Output("summary", "data"),
        # dash.dependencies.Output("choose-section-forward", "options"),
    ],
    [
        dash.dependencies.Input("submit", "n_clicks"),
        dash.dependencies.Input("points-fw", "value"),
        dash.dependencies.Input("fw-points", "data"),
        dash.dependencies.Input("fw_dropdown_value", "data"),
        dash.dependencies.Input("art_link_fw", "data"),
        dash.dependencies.Input("summary", "data"),
        # dash.dependencies.Input("choose-section-forward", "value"),
    ],
    [dash.dependencies.State("art_link", "value")],
)
def update_output(
    clicks,
    val_fw,  # the value of the option selected in the dropdown for the forwards graph
    forward_points,  # the points that were saved in dcc.Store
    forward_points_dropdown,  # the list of the options mentioned in the dropdown
    link_saved,  # the link as saved in dcc.Store
    summary_saved,
    link,  # the link when the graph updates
):

    print("submit", "n_clicks"),
    print("points-fw", "value"),
    print("fw-points", "data"),
    print("fw_dropdown_value", "data"),
    print("art_link_fw", "data"),
    print("summary", "data"),
    # global art_link_fw
    # global fw_points_global
    # global fw_dropdown_value
    # global summary

    # fw_dropdown_value = val_fw

    summary_callback = summary_saved
    if link_saved != link:
        forward_points = {}
        link_saved = link
        forward_points_dropdown = None

        title = art_link_fw.split("/")[-1]
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
            "formatversion": "2",
        }
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        summary_callback = DATA["query"]["pages"][0]["extract"]

    forwards = wna(
        link=link_saved,
        prop_params="links",
        points=forward_points,
        plot_all_points=False,  # this plots a limited number of points, the number can be limited too
    )

    # this sets the center of the new cluster to be formed
    forwards.collect_points(center=fw_dropdown_value)

    # drop is True specifies that the points to return should be returned for the dropdown
    forward_points_dropdown, section = forwards.return_points(drop=True)

    # generating items for the dropdown list below
    forward_points_dropdown = [
        {"label": item, "value": item} for item in forward_points_dropdown
    ]

    forward_points = forwards.return_points(drop=False)
    dash.callback_context.response.set_cookie(
        "fw points", json.dumps(fw_points_global, indent=4)
    )

    forwards = forwards.plot()
    forwards["layout"] = net_layout

    return (
        forwards,  # the figure
        summary_callback,  # the summary to be updated, this shouldn't be updated in every callback
        forward_points_dropdown,  # points for the dropdown
        forward_points,  # complete points package, stored in dcc.Store
        fw_dropdown_value,  # the value of the dropdown selected
        link_saved,  # the value of the link which is stored in dcc.Store
        summary_saved,  # summary stored in dcc.Store
    )


@app.callback(
    [
        dash.dependencies.Output("backwards", "figure"),
        dash.dependencies.Output("points-bw", "options"),
        # dash.dependencies.Output("choose-section-backward", "options"),
    ],
    [
        dash.dependencies.Input("submit", "n_clicks"),
        dash.dependencies.Input("points-bw", "value"),
        # dash.dependencies.Input("choose-section-backward", "value"),
    ],
    [dash.dependencies.State("art_link", "value")],
)
def update_output(
    clicks,
    val_bw,
    # selected_section,
    link,
):
    global art_link_bw
    global bw_points_global
    global bw_dropdown_value
    bw_dropdown_value = val_bw

    if art_link_bw != link:
        bw_points_global = {}
        print("seems like link updated...")
        print("bw points", bw_points_global)
        art_link_bw = link
        bw_dropdown_value = None

    backwards = wna(
        link=art_link_bw,
        prop_params="linkshere",
        points=bw_points_global,
        plot_all_points=False,
    )
    backwards.collect_points(center=bw_dropdown_value)
    bw_points, section = backwards.return_points(drop=True)
    bw_points = [{"label": item, "value": item} for item in bw_points]
    section = [{"label": "part" + str(ind + 1), "value": ind} for ind in range(section)]

    bw_points_global = backwards.return_points(drop=False)
    backwards = backwards.plot(dot_color="#ff3b3b")
    backwards["layout"] = net_layout

    return backwards, bw_points


@app.callback(
    dash.dependencies.Output("forward-hover-description", "children"),
    dash.dependencies.Input("forwards", "hoverData"),
)
def show_hover_text(data):
    # print(data)
    if data is not None:
        data = data["points"][0]
        if "hovertext" not in data.keys():
            print("hovering on lines")
            text = "hover on points to see article summary"
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
    else:
        text = "Loading..."
    return text


@app.callback(
    dash.dependencies.Output("backward-hover-description", "children"),
    dash.dependencies.Input("backwards", "hoverData"),
)
def show_hover_text(data):
    if data is not None:
        data = data["points"][0]
        if "hovertext" not in data.keys():
            print("hovering on lines")
            text = "hover on points to see article summary"
        else:
            print("hovering on point ", end="")
            art_name = data["hovertext"]
            print(art_name)
            wna_hover = wna(link=art_name, prop_params="linkshere")
            hover = wna_hover.article_summary_for_hover(
                collect_points=False, number_of_lines=8
            )
            # print(hover, type(hover))
            text = hover["query"]["pages"][0]["extract"]
            if text == "":
                text = "no summary available"
            print("got hover data")
    else:
        text = "Loading..."
    return text


def run(host="127.0.0.1", debug=True):
    app.run_server(debug=debug, host=host, port=3004)


if __name__ == "__main__":
    run()
