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

def create_random_populated_sphere(radius, points, plot_flag, show_lines_with_origin):
    '''
    this function will return the figure and the coordinates in a tuple
    when asked to plot, it will plot it. 
    enter radius ... integer, radius of the sphere
    points...list having the markers
    plot_flag...boolean, whether or not to plot the sphere
    show_lines_with_origin...boolean, whether to show connections or not
    returns (coordinates of the sphere and the fig in a tuple)
    '''
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

    print(len(coor[0]), len(points))
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x = coor[0],
        y = coor[1],
        z = coor[2],
        text = points,
        marker=dict(
            size=5,
            colorscale='Viridis',   # choose a colorscale
            opacity=0.8
        ),
        mode = "markers+text"
    ))


    for x_coor,y_coor,z_coor in zip(coor[0], coor[1], coor[2]): 
        fig.add_trace(go.Scatter3d(
        x = [x_coor,0],
        y = [y_coor,0],
        z = [z_coor,0],
        # text = points,
        marker=dict(
            size=0.1,
            color = "#303030",
            # colorscale='Viridis',   
            opacity=0.8
        ),
        mode = "lines"))

    fig.update_layout(
        height  =1000, width = 1000,
        template = "plotly_dark",
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
        }
    )
    fig.update_traces(showlegend = False)   
    if plot_flag == True:
        fig.show()


    return fig


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([
    
    html.Div(
        html.P(
            "wiki nearby articles",
            style = {
                "font-size": "72px",
                "fontFamily": "monospace",
                "letter-spacing": "5px",
                "text-align": "center",
                "font-weight": "light"
            }
        )
    ),
    html.Div([
        dcc.Input(id = "art_link", 
        placeholder = "enter wikipedia article link",
        value = "https://en.wikipedia.org/wiki/MissingNo.",
        style={
                "font-size": "18px",
                "fontFamily": "Lucida Console",
                "margin": "0 auto",
                "display": "center",
                'width': '100%',
                'text-align': 'center',
                # 'padding-left':'10%', 'padding-right':'10%',
                "color": "black"
                }),

    ]),
    html.Div([
        html.Div(
            dcc.Graph(id = "forwards"),
            style = {
                "width": "50%",
                "display": "inline-block"
            }
        ),
        html.Div(
            dcc.Graph(id = "backwards"),
            style = {
                "width": "50%",
                "display": "inline-block"
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
    print(article_name)
    art = art_from_origin(prop_params = "links", article_name = article_name)
    print(art)
    forwards = create_random_populated_sphere(radius=100, points=art, plot_flag=False, show_lines_with_origin=True)

    art = art_from_origin(prop_params = "linkshere", article_name = article_name)
    backwards = create_random_populated_sphere(radius=100, points=art, plot_flag=False, show_lines_with_origin=True)

    return (forwards, backwards)


if __name__ == '__main__':
  app.run_server(debug=True)
