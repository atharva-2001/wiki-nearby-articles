from numpy.core.arrayprint import set_string_function
import requests
import re
import math
import numpy as np
import plotly.graph_objects as go
from time import sleep
import sys
import os


def find_hover_text(str):
    lst = re.split(" ", str)
    lst = [" ".join(lst[i: i + 3]) for i in range(0, len(lst), 3)]
    str = "<br>".join(["".join(item) for item in lst])
    return str


def random_points_in_a_sphere(h=0, g=0, f=0, num=0, radius=5):
    coor = [[], [], []]
    index = 0
    while True:
        if index > num - 1:
            break

        x = (-1) ** np.random.randint(5, size=1)[0] * radius * np.random.rand(1)[0]
        y = (-1) ** np.random.randint(5, size=1)[0] * radius * np.random.rand(1)[0]
        z = (-1) ** np.random.randint(5, size=1)[0] * radius * np.random.rand(1)[0]

        if math.sqrt((x - h) ** 2 + (y - g) ** 2 + (z - f) ** 2) <= radius:  # checking if the point is in the circle
            coor[0].append(x)
            coor[1].append(y)
            coor[2].append(z)
            index += 1
    return coor


def spinning_cursor():
    while True:
        for cursor in '\\|/-':
            sleep(0.1)
            # Use '\r' to move cursor back to line beginning
            # Or use '\b' to erase the last character
            sys.stdout.write('\r{}'.format(cursor))
            # Force Python to write data into terminal.
            sys.stdout.flush()


def get_calls(article_name, number_of_lines=7):
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
            points_in_one_plot=15,
    ):
        self.link = link
        if "wiki" not in link:
            self.article_name = link
        else:
            self.article_name = link.split("/")[-1]
        self.prop_params = prop_params
        self.points_in_one_plot = points_in_one_plot
        self.points = []

    def collect_points(self):
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
        print("getting points...")
        for k, v in PAGES.items():
            for l in v[self.prop_params]:
                # print(f"appending {l['title']} to lst ")
                points.append(l["title"])

        points = [
            points[i: i + self.points_in_one_plot]
            for i in range(0, len(points), self.points_in_one_plot)
        ]

        # * the total number of articles connected to the main article
        # should I call all points at once or is it possible to call them a few at at time?
        # the get points funtion wont be used I guess
        self.points = points
        print("got points")

    def return_points(self, plot_index=0):
        if not self.points:
            self.collect_points()
        return self.points[plot_index]

    def article_summary_for_hover(self, number_of_lines=2, plot_index=0, display_all_summaries=False,
                                  collect_points=True):
        if collect_points:  # TODO fix this
            self.collect_points()
            self.points = self.points[plot_index]
        if display_all_summaries:
            S = requests.Session()
            URL = "https://en.wikipedia.org/w/api.php"

            hover_text = []

            self.points = self.points[plot_index]

            print("getting summary...")
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

            # ! do you want summary of the article selected?
            self.hover_text = hover_text
            print("got summary")
        else:
            print(f"trying to get hover text for {self.article_name}")
            return get_calls(article_name=self.article_name)

    def plot_points(
            self,
            dis_to_external_point=10,
            external_points=[],
            center="",
            radius=5,
            plot_flag=False,
            show_lines_with_origin=True,
            line_color="#5c5c5c",
            dot_color="#525BCB",
            plot_index=0,
            number_of_lines=2,
    ):
        # collect summary data and plot points
        self.article_summary_for_hover(
            plot_index=plot_index, number_of_lines=number_of_lines
        )

        coor = random_points_in_a_sphere(num=len(self.points), radius=5)

        # print(len(coor[0]), len(points))
        fig = go.Figure()
        fig.add_trace(
            go.Scatter3d(
                x=coor[0],
                y=coor[1],
                z=coor[2],
                text=self.points,
                marker=dict(size=5, color=dot_color, opacity=0.5),
                mode="markers+text",
                hovertext=self.points,
                hoverinfo="text"
            )
        )

        for x_coor, y_coor, z_coor, point in zip(
                coor[0], coor[1], coor[2], self.points
        ):
            fig.add_trace(
                go.Scatter3d(
                    x=[x_coor, 0],
                    y=[y_coor, 0],
                    z=[z_coor, 0],
                    # text = points,
                    # name = point,
                    marker=dict(
                        size=0.1,
                        color=line_color,
                        # colorscale='Viridis',
                        # opacity=1
                    ),
                    mode="lines",
                    hoverinfo="none"
                    # hovertemplate = f"{article_summary_for_hover(article_name=point, number_of_lines=2)}"
                )
            )

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
            }
        )
        fig.update_traces(showlegend=False)
        if plot_flag:
            fig.show()

        # self.fig = fig
        return fig
