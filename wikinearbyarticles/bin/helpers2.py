from numpy.core.arrayprint import set_string_function
import requests
import re
import math
import numpy as np
import plotly.graph_objects as go
from time import sleep
import sys
import os

def random_points_in_a_sphere(h = 0, g = 0, f = 0, num = 0, radius = 5):
    '''
    creates random points in a sphere
    h,g,f are the coordinates of the center
    num is the number of points
    radius is the radius of the sphere

    returns a list having three lists inside of it
    having x,y,z values respectively
    '''
    coor = [[], [], []]
    index = 0
    while True:
        if index > num - 1:
            break

        x = (-1) ** np.random.randint(5, size=1)[0] * radius * np.random.rand(1)[0]
        y = (-1) ** np.random.randint(5, size=1)[0] * radius * np.random.rand(1)[0]
        z = (-1) ** np.random.randint(5, size=1)[0] * radius * np.random.rand(1)[0]

        if math.sqrt((x-h) ** 2 + (y-g) ** 2 + (z-f) ** 2) <= radius: # checking if the point is in the circle
            coor[0].append(x)
            coor[1].append(y)
            coor[2].append(z)
            index += 1
    return coor

def get_calls(article_name, number_of_lines=7):
    '''
    returns hover data in raw format
    this is used in app callbacks to display hover summary data in a text box
    just enter article name like "Atom" or "Proton"
    '''
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
                "action": "query",
                "format": "json",
                "titles": article_name,
                "prop": "extracts",
                "exsentences": number_of_lines,
                "exlimit": "1",
                "explaintext": "1",
                "formatversion": "2",
                }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    sys.stdout.flush()
    # print(DATA)
    # os._exit(0)
    return DATA



class wna: 
    def __init__(
        self,
        link,
        prop_params,
        points_in_one_shot = 15
    ):
        '''
        this is the main class
        link can have the website link and the article name as well
        prop params are parameters that can be links or linkshere etc

        structure of points
        {
            "main point": {
                "name": ["name of main article searched for"]
                "coords": [[0], [0], [0]]
            }
            "main section": {
                "center coords": [[0], [0], [0]],
                "names of other points": ["string 1", "string 2"],
                "coords": [[x coords llist], [y coords llist], [z coords llist]] 
            }
            # other sections will be added like this
            "some article as center": {
                "center coords": [[x], [y], [z]],
                "names of other points": ["string 1", "string 2"],
                "coords": [[x coords llist], [y coords llist], [z coords llist]] 
            }
        }
        '''
        self.link = link
        if "wiki" not in link:
            self.article_name = link
        else:
            self.article_name = link.split("/")[-1]
        self.prop_params = prop_params
        self.points_in_one_plot = points_in_one_shot
        self.points = {
            self.article_name: {
                "name": [self.article_name],
                "coords": [[0], [0], [0]]
            }
        } 


    def collect_points(self, center = ""):
        '''
        this function will collect points and will add them to the points dictionary
        the center is the point around which the points will be sourrounded 
        if center is "" then center is the orgin, at which is the main article

        else center will be the name of the article which has to be expanded. 

        '''
        if "main section" not in self.points.keys():
            S = requests.Session()
            URL = "https://en.wikipedia.org/w/api.php"

            PARAMS = {
                "action": "query",
                "format": "json",
                "titles": self.article_name,
                "prop": self.prop_params,
                "pllimit": "max",
            }

            R = S.get(url=URL, params=PARAMS)
            DATA = R.json()
            PAGES = DATA["query"]["pages"]
            points = []
            for k, v in PAGES.items():
                for l in v[self.prop_params]:
                    # print(f"appending {l['title']} to lst ")
                    points.append(l["title"])

            points = [
                points[i : i + self.points_in_one_plot]
                for i in range(0, len(points), self.points_in_one_plot)
            ]

            coords = random_points_in_a_sphere(num = len(points), radius = 5) # center is origin 

            self.points["main_section"] = {
                "center_coords": [[0], [0], [0]],
                "point_names": points,
                "coords": coords
            }

        # * now consider the center has a value
        # * searching for its coords

        center_coords = []

        for key in self.points.keys():
            if key != self.article_name:
                for name in key["point_names"]:
                    if name == center:
                        idx = key["point_names"].index("name")
                        center_coords = [key["coords"][0][idx], key["coords"][0][idx], key["coords"][0][idx]]
                        break
        
        S = requests.Session()
        URL = "https://en.wikipedia.org/w/api.php"

        PARAMS = {
            "action": "query",
            "format": "json",
            "titles": center,
            "prop": self.prop_params,
            "pllimit": "max",
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        PAGES = DATA["query"]["pages"]
        points = []
        for k, v in PAGES.items():
            for l in v[self.prop_params]:
                # print(f"appending {l['title']} to lst ")
                points.append(l["title"])

        points = [
            points[i : i + self.points_in_one_plot]
            for i in range(0, len(points), self.points_in_one_plot)
        ]

        coords = random_points_in_a_sphere(num = len(points), radius = 5) # center is origin 

        self.points[center] = {
            "center_coords":center_coords, 
            "point_names": points,
            "coords": coords
        }

            




