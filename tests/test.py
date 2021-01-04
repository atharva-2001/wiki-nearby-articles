import plotly.express as px
import plotly.graph_objects as go
import math
import numpy as np
import requests 

def art_from_origin(): 
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": "Atom",
        "prop": "links",
        "pllimit": "max"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    # print(DATA)
    PAGES = DATA["query"]["pages"]

    art = []
    for k, v in PAGES.items():
        for l in v["links"]:
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
        mode = "markers"
    ))


    for x_coor,y_coor,z_coor in zip(coor[0], coor[1], coor[2]): 
        fig.add_trace(go.Scatter3d(
        x = [x_coor,0],
        y = [y_coor,0],
        z = [z_coor,0],
        text = points,
        marker=dict(
            size=0.1,
            colorscale='Viridis',   # choose a colorscale
            opacity=0.8
        ),
        mode = "lines"))

    fig.update_layout(
        height  =1300, width = 2000,
    )
    fig.update_traces(showlegend = False)   
    if plot_flag == True:
        fig.show()


    return (coor, fig)

art = art_from_origin()
_, _ = create_random_populated_sphere(radius=1000, points=art, plot_flag=True, show_lines_with_origin=True)

