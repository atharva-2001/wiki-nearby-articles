import math
import re
import sys

import numpy as np
import plotly.graph_objects as go
import requests


def random_points_in_a_sphere(h=0, g=0, f=0, num=0, radius=5):
    """
    creates random points in a sphere
    h,g,f are the coordinates of the center
    num is the number of points
    radius is the radius of the sphere

    returns a list having three lists inside of it
    having x,y,z values respectively
    """
    coor = [[], [], []]
    index = 0
    print("finding random points...")
    while True:
        if index > num - 1:
            break

        x = np.round(np.random.uniform(h + radius, h - radius, (1,))[0], 3)
        y = np.round(np.random.uniform(g + radius, g - radius, (1,))[0], 3)
        z = np.round(np.random.uniform(f + radius, f - radius, (1,))[0], 3)

        if (
            math.sqrt((x - h) ** 2 + (y - g) ** 2 + (z - f) ** 2) <= radius
        ):  # checking if the point is in the circle
            if (x != 0) and (y != 0) and (z != 0):
                coor[0].append(np.round(x, 2))
                coor[1].append(np.round(y, 2))
                coor[2].append(np.round(z, 2))
                index += 1
    return coor


def extend_points(tip=[[0], [0], [0]], end=[[0], [0], [0]], factor=2):
    """
    returns new coordinates of the points to extend
    in a list
    the default value of tip is the origin
    end is also a list
    """
    print("extending coords...")
    xnew = factor * (end[0][0] - tip[0][0]) + tip[0][0]
    ynew = factor * (end[1][0] - tip[1][0]) + tip[1][0]
    znew = factor * (end[2][0] - tip[2][0]) + tip[2][0]

    return [[xnew], [ynew], [znew]]


def find_hover_text(str):
    lst = re.split(" ", str)
    lst = [" ".join(lst[i : i + 3]) for i in range(0, len(lst), 3)]
    str = "<br>".join(["".join(item) for item in lst])
    return str


def get_calls(article_name, number_of_lines=7):
    """
    returns hover data in raw format
    this is used in app callbacks to display hover summary data in a text box
    just enter article name like "Atom" or "Proton"
    """
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
    return DATA


class wna:
    def __init__(
        self, link, prop_params, points_in_one_shot=36, points={}, plot_all_points=None
    ):
        """
        this is the main class
        link can have the website link and the article name as well
        prop params are parameters that can be links or linkshere etc

        structure of points
        {
            "article name": {
                "cluster_origin": "some string, name of the article directly connected before expanding"
                "center_coords": [[0], [0], [0]],
                "point_names": ["string 1", "string 2"],
                "coords": [[x coords llist], [y coords llist], [z coords llist]]
            }
            # other sections will be added like this
            "some article as center": {
                "cluster_origin": "some string as before"
                "center_coords": [[x], [y], [z]],
                "point_names": ["string 1", "string 2"],
                "coords": [[x coords list], [y coords list], [z coords llist]]
            }
        }
        """

        self.link = link
        if "wiki" not in link:
            self.article_name = link
        else:
            self.article_name = link.split("/")[-1]
        self.prop_params = prop_params
        self.points_in_one_plot = points_in_one_shot
        self.plot_all_points = plot_all_points
        self.sections = 0
        # if the link is updated, the points sent as arguments are already empty distionaries
        if points != {}:
            self.points = points
        else:
            self.points = {}

    def collect_points(self, center="", plot_index=0):
        """
        this function will collect points and will add them to the points dictionary
        the center is the point around which the points will be surrounded
        if center is "" then center is the origin, at which is the main article

        else center will be the name of the article which has to be expanded.

        """

        if self.points != {}:
            self.points = self.points[0]
        if self.article_name not in self.points.keys():
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
                    points.append(l["title"])

            if self.plot_all_points == False:
                points = [
                    points[i : i + self.points_in_one_plot]
                    for i in range(0, len(points), self.points_in_one_plot)
                ]
                self.sections = len(points)
                if plot_index is None:
                    plot_index = 0
                points = points[plot_index]

            coords = random_points_in_a_sphere(
                num=len(points), radius=5
            )  # center is origin

            self.points[self.article_name] = {
                "cluster_origin": self.article_name,
                "center_coords": [[0], [0], [0]],
                "point_names": points,
                "coords": coords,
            }
        # * now consider the center has a value
        # * searching for its coords

        center_coords = []
        cluster_origin = ""
        if_break = False
        if center != "" and center is not None:
            for key in self.points.keys():
                for name in self.points[key]["point_names"]:
                    if name == center:
                        idx = self.points[key]["point_names"].index(name)
                        center_coords = [
                            [self.points[key]["coords"][0][idx]],
                            [self.points[key]["coords"][1][idx]],
                            [self.points[key]["coords"][2][idx]],
                        ]
                        cluster_origin_coords = [
                            [self.points[key]["center_coords"][0][0]],
                            [self.points[key]["center_coords"][1][0]],
                            [self.points[key]["center_coords"][2][0]],
                        ]
                        center_coords = extend_points(
                            tip=cluster_origin_coords, end=center_coords, factor=4.5
                        )

                        self.points[key]["coords"][0][idx] = center_coords[0][0]
                        self.points[key]["coords"][1][idx] = center_coords[1][0]
                        self.points[key]["coords"][2][idx] = center_coords[2][0]

                        cluster_origin = key
                        if_break = True
                        break
                if if_break:
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
                    points.append(l["title"])

            if self.plot_all_points == False:
                points = [
                    points[i : i + self.points_in_one_plot]
                    for i in range(0, len(points), self.points_in_one_plot)
                ][plot_index]

            coords = random_points_in_a_sphere(
                num=len(points),
                radius=5,
                h=center_coords[0][0],
                g=center_coords[1][0],
                f=center_coords[2][0],
            )

            self.points[center] = {
                "center_coords": center_coords,
                "cluster_origin": cluster_origin,
                "point_names": points,
                "coords": coords,
            }
        # return self.points

    def return_points(self, drop=True):
        """
        returns all points except cluster centers
        """
        if drop:
            points = []
            for key in self.points.keys():
                points += self.points[key]["point_names"]
                if key in points:
                    points = [item for item in points if item != key]
            return points, self.sections
        else:
            return self.points, self.sections

    def article_summary_for_hover(
        self,
        number_of_lines=2,
        plot_index=0,
        display_all_summaries=False,
        collect_points=True,
    ):

        if collect_points:
            self.collect_points()
            if self.plot_all_points == False:
                self.points = self.points[plot_index]

        if display_all_summaries:
            S = requests.Session()
            URL = "https://en.wikipedia.org/w/api.php"

            hover_text = []

            for point in self.points:
                PARAMS = {
                    "action": "query",
                    "format": "json",
                    "titles": point,
                    "prop": "extracts",
                    "exsentences": number_of_lines,
                    "exlimit": "1",
                    "explaintext": "1",
                    "formatversion": "2",
                }

                R = S.get(url=URL, params=PARAMS)
                DATA = R.json()
                hover_text_for_one_point = find_hover_text(
                    DATA["query"]["pages"][0]["extract"]
                )
                hover_text.append(hover_text_for_one_point)

            # ! do you want summary of the article selected?s
            self.hover_text = hover_text
        else:
            print(f"trying to get hover text for {self.article_name}")
            return get_calls(article_name=self.article_name)

    def plot(
        self,
        dis_to_external_point=10,  # distance between clusters
        radius=5,
        plot_flag=False,  # whether or not to plot the graph separately
        show_lines_with_origin=True,
        line_color="#d4d4d4",
        dot_color="#525BCB",
        plot_index=0,
    ):
        # * plotting main cluster

        fig = go.Figure()

        # plotting the central point

        for cluster_name in self.points.keys():
            fig.add_trace(
                go.Scatter3d(
                    x=self.points[cluster_name]["center_coords"][0],
                    y=self.points[cluster_name]["center_coords"][1],
                    z=self.points[cluster_name]["center_coords"][2],
                    text=[cluster_name],
                    marker=dict(
                        size=5, color=dot_color, opacity=0.5
                    ),  # change the marker color of the central marker
                    mode="markers",
                    # hoverinfo="text",  # what did this do?
                )
            )
            fig.add_trace(
                go.Scatter3d(
                    x=self.points[cluster_name]["coords"][0],
                    y=self.points[cluster_name]["coords"][1],
                    z=self.points[cluster_name]["coords"][2],
                    hovertext=self.points[cluster_name]["point_names"],
                    marker=dict(size=2, color=dot_color, opacity=0.5),
                    # change the marker color of the central marker
                    mode="markers+text",
                    hoverinfo="text",  # what did this do?
                )
            )

        for cluster_name in self.points.keys():
            idx = 0
            while idx < len(self.points[cluster_name]["point_names"]):
                fig.add_trace(
                    go.Scatter3d(
                        x=[
                            self.points[cluster_name]["coords"][0][idx],
                            self.points[cluster_name]["center_coords"][0][0],
                        ],
                        y=[
                            self.points[cluster_name]["coords"][1][idx],
                            self.points[cluster_name]["center_coords"][1][0],
                        ],
                        z=[
                            self.points[cluster_name]["coords"][2][idx],
                            self.points[cluster_name]["center_coords"][2][0],
                        ],
                        marker=dict(size=0.1, color=line_color),
                        mode="lines",
                        hoverinfo="none",
                    )
                ),
                idx += 1

        fig.update_layout(
            height=1200,
            width=800,
            hoverlabel={
                "font": {"family": "monospace"},
                # "hover"
            },
            # template = "plotly_dark",
            font={"family": "monospace", "size": 18},
            scene={
                "xaxis": {"visible": False, "showticklabels": False},
                "yaxis": {"visible": False, "showticklabels": False},
                "zaxis": {"visible": False, "showticklabels": False},
            },
            margin={
                "pad": 0,
                "t": 0,
                "r": 0,
                "l": 0,
                "b": 0,
            },
        )
        fig.update_traces(showlegend=False)
        # fig.show()
        return fig
