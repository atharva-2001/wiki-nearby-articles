from logging import PlaceHolder
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import math
import numpy as np
import requests 
import re
from wikinearbyarticles.bin import helpers

# TODO add animations 
# TODO between graphs as they are updated, extending graphs

def art_from_origin(prop_params, article_name): 
    '''
    prop params is the prop value in the api
    links,
    media
    linkehere etc
    returns and array containing the article link
    '''
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": article_name,
        "prop": prop_params,
        "pllimit": "max"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    # print(DATA)
    PAGES = DATA["query"]["pages"]

    art = []
    for k, v in PAGES.items():
        for l in v[prop_params]:
            art.append(l["title"])
    return art

def find_hover_text(str):
    lst = re.split(" ", str)
    lst = [" ".join(lst[i: i+3]) for i in range(0, len(lst), 3)]
    str = "<br>".join(["".join(item) for item in lst])
    return str

def get_points(points, points_in_one_plot):
    points = [points[i:i+points_in_one_plot] for i in range(0, len(points), points_in_one_plot)]
    return points

def create_random_populated_sphere(
    radius, points, plot_flag, show_lines_with_origin, 
    points_in_one_plot = 15, 
    plot_index = 0,
    line_color = "#5c5c5c",
    dot_color = "#525BCB"
):
    '''
    this function will return the figure and the coordinates in a tuple
    when asked to plot, it will plot it. 
    enter radius ... integer, radius of the sphere
    points...list having the markers
    plot_flag...boolean, whether or not to plot the sphere
    show_lines_with_origin...boolean, whether to show connections or not
    returns (coordinates of the sphere and the fig in a tuple)
    '''

    # ! this is going to change
    if len(points) <= points_in_one_plot: 
        pass
    else: 
        points = get_points(points=points, points_in_one_plot=points_in_one_plot)
        points = points[plot_index]
    # ! I will pass better points 
    
    coor = [[],[],[]]
    index = 0
    while True:
        if index > len(points)-1:
            break
        
        x = (-1)**np.random.randint(5, size = 1)[0] * radius * np.random.rand(1)[0]
        y = (-1)**np.random.randint(5, size = 1)[0] * radius * np.random.rand(1)[0]
        z = (-1)**np.random.randint(5, size = 1)[0] * radius * np.random.rand(1)[0]
  
        if math.sqrt(x**2 + y**2 + z**2) <= radius: 
            coor[0].append(x)
            coor[1].append(y)
            coor[2].append(z)
            index+=1

    # print(len(coor[0]), len(points))
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x = coor[0],
        y = coor[1],
        z = coor[2],
        text = points,
        marker=dict(
            size=5,
            color = dot_color,
            opacity=0.5
        ),
        mode = "markers+text",
        hovertext = [find_hover_text(article_summary_for_hover(article_name=point, number_of_lines=1)) for point in points],
        hoverinfo = "text"
    ))


    for x_coor,y_coor,z_coor,point in zip(coor[0], coor[1], coor[2], points): 
        fig.add_trace(go.Scatter3d(
        x = [x_coor,0],
        y = [y_coor,0],
        z = [z_coor,0],
        # text = points,
        # name = point,
        marker=dict(
            size=0.1,
            color = line_color,
            # colorscale='Viridis',   
            # opacity=1
            ),
        mode = "lines",
        hoverinfo = "none"
        # hovertemplate = f"{article_summary_for_hover(article_name=point, number_of_lines=2)}"
        ))

    fig.update_layout(
        height  = 800, width = 870,
        hoverlabel = {
            "font": {
                "family": "monospace"
            },
            # "hover"
        },
        # template = "plotly_dark",
        font = {
            "family": "monospace",
            "size": 18
        },
        scene = {
            "xaxis": {
                "visible": False,
                "showticklabels": False
            },
            "yaxis": {
                "visible": False,
                "showticklabels": False
            },
            "zaxis": {
                "visible": False,
                "showticklabels": False
            }
        },
        margin = {
            "pad": 0,
            "t": 0,
            "r": 0,
            "l": 0,
            "b": 0,
        }
    )
    fig.update_traces(showlegend = False)   
    if plot_flag == True:
        fig.show()


    return fig

def article_summary_for_hover(article_name, number_of_lines):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": article_name,
        "prop": "extracts",
        "exsentences":number_of_lines,
        "exlimit": "1",
        "explaintext": "1",
        "formatversion": "2"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA["query"]["pages"][0]
    return PAGES["extract"]

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, 
        # external_stylesheets=[dbc.themes.DARKLY]
        external_stylesheets=external_stylesheets
        )

app.layout = html.Div([
    
    html.Div(
        html.P(
            "wiki nearby articles",
            style = {
                "font-size": "72px",
                "fontFamily": "monospace",
                "letter-spacing": "5px",
                "text-align": "center",
                "font-weight": "light",
                "color": "#525252"
            }
        )
    ),
    html.Div(
        html.Hr(),
        style = {
            "padding-bottom": "1px"
        }
    ),
    # html.Div(
    #     html.Hr()
    # ),
    html.Div(
        html.P("enter article link below"),
        style={
                "font-size": "13px",
                "letter-spacing": "2px",
                "fontFamily": "monospace",
                "margin": "0  auto",
                "display": "center",
                'width': '100%',
                'text-align': 'center',
                # 'padding-left':'10%', 'padding-right':'10%',
                "border": "none",
                "border-bottom": "2px solid #5c5c5c",
                # "background-color": "#1a1a1a",
                "color": "#9c9c9c",
                "padding-bottom": "3px"
                }
    ),

    html.Div([
        dcc.Input(id = "art_link", 
        className = "text_input",
        # placeholder = "enter wikipedia article link",
        value = "https://en.wikipedia.org/wiki/MissingNo.",
        style={
                "font-size": "18px",
                "fontFamily": "monospace",
                "margin": "0  auto",
                "display": "center",
                'width': '100%',
                'text-align': 'center',
                "text-spacing": "1px",
                # 'padding-left':'10%', 'padding-right':'10%',
                "border": "none",
                "border-bottom": "2px solid #5c5c5c",
                # "background-color": "#1a1a1a",
                "color": "#525252",
                "padding-bottom": "3px"
                }),

    ]),
    html.Div([
        html.Div(
            dcc.Dropdown(
            id = "choose-section-forward",
            # ! options will depend upon the link
            # options = [{"label": f"section number: {i}", "value": f"{section}"} for i,section in enumerate(get_points(points = forward_points, points_in_one_plot= 15))]
        )),
        html.Div(dcc.Dropdown(
            id = "choose-section-backward",
            # ! options will depend upon the link
            # options = [{"label": f"section number: {i}", "value": f"{section}"} for i,section in enumerate(get_points(points = backward_points, points_in_one_plot= 15))]
        ))
        
    ]),
    html.Div([
        html.Div(
            html.P("article directs to these articles"),
            style = {
                "width": "48%",
                "font-size": "18px",
                "letter-spacing": "5px",
                "font-family": "monospace",
                "display": "inline-block",
                "text-align": "center"
            }
        ),
        html.Div(
            html.P(),
            style = {
                "width": "2%",
                "display": "inline-block",
                "text-align": "center"
            }
        ),
        html.Div(
            html.P("article is directed from these articles"),
            style = {
                "width": "48%",
                "font-size": "18px",
                "letter-spacing": "5px",
                "font-family": "monospace",
                "display": "inline-block",
                "text-align": "center"
            }
        ),
        
    ]),
    html.Div([
        html.Div(
            dcc.Graph(
                id = "forwards",
                responsive = True
            ),
            style = {
                "width": "48%",
                "display": "inline-block",
                "border":"3px #5c5c5c solid",
                "padding-top": "5px",
                "padding-right": "1px"
                
            }
        ),
        html.Div(style = {
                "width": "2%",
                "display": "inline-block",
                "padding-top": "5px"
                # "border":"9px gray solid",
                # "padding": "10px"
            }),
        html.Div(
            dcc.Graph(
                id = "backwards",
                responsive = True
            ),
            style = {
                "width": "48%",
                "display": "inline-block",
                "border":"3px #5c5c5c solid",
                "padding-top": "5px",
                "padding-left": "1px"
                # "padding": "2px"
            }
        )
    ])
])

# art = art_from_origin(prop_params = "linkshere")
# _, _ = create_random_populated_sphere(radius=1000, points=art, plot_flag=True, show_lines_with_origin=True)

@app.callback([
    dash.dependencies.Output("forwards", "figure"),
    dash.dependencies.Output("backwards", "figure")
],
    dash.dependencies.Input("art_link", "value")
)
def update_output(art_link):
    
    article_name = art_link.split("/")[-1]
    # print(article_name)
    art = art_from_origin(prop_params = "links", article_name = article_name)
    # print(art)
    forwards = create_random_populated_sphere(radius=100, points=art, plot_flag=False, show_lines_with_origin=True)

    art = art_from_origin(prop_params = "linkshere", article_name = article_name)
    backwards = create_random_populated_sphere(radius=100, points=art, plot_flag=False, show_lines_with_origin=True, dot_color="#ff3b3b")

    return (forwards, backwards)


if __name__ == '__main__':
  app.run_server(debug=True)