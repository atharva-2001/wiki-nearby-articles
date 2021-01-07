import requests
import re
import math
import numpy




class helpers():
    def __init__(
            self,
            article_name,
            prop_params,
            radius = 5,
            plot_flag = False,
            show_lines_with_origin = True,
            line_color =  "#5c5c5c",
            dot_color = "#525BCB",
            points_in_one_plot = 15
        ):
        self.article_name = article_name
        self.radius = radius
        self.prop_params = prop_params
        self.plot_flag = plot_flag
        self.dot_color = dot_color
        self.line_color = line_color
        self.show_lines_with_origin = show_lines_with_origin
        self.points_in_one_plot = points_in_one_plot
        
        S = requests.Session()

        URL = "https://en.wikipedia.org/w/api.php"

        PARAMS = {
            "action": "query",
            "format": "json",
            "titles": self.article_name,
            "prop": self.prop_params,
            "pllimit": "max"
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        PAGES = DATA["query"]["pages"]

        points = []
        for k, v in PAGES.items():
            for l in v[prop_params]:
                points.append(l["title"])


        points = [points[i:i+points_in_one_plot] for i in range(0, len(points), points_in_one_plot)]
        
        # * the total number of articles connected to the main article
        # should I call all points at once or is it possible to call them a few at at time?
        self.points = points





