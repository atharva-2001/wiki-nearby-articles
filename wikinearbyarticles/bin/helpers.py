from numpy.core.arrayprint import set_string_function
import requests
import re
import math
import numpy as np
import plotly.graph_objects as go


def find_hover_text(str):
    lst = re.split(" ", str)
    lst = [" ".join(lst[i : i + 3]) for i in range(0, len(lst), 3)]
    str = "<br>".join(["".join(item) for item in lst])
    return str


class helpers:
    def __init__(
        self,
        link,
        prop_params,
        points_in_one_plot=15,
    ):
        self.link = link
        self.article_name = link.split("/")[-1]
        self.prop_params = prop_params
        self.points_in_one_plot = points_in_one_plot

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
            for l in v[prop_params]:
                # print(f"appending {l['title']} to lst ")
                points.append(l["title"])

        points = [
            points[i : i + points_in_one_plot]
            for i in range(0, len(points), points_in_one_plot)
        ]

        # * the total number of articles connected to the main article
        # should I call all points at once or is it possible to call them a few at at time?
        # the get points funtion wont be used I guess
        self.points = points
        print("got points")

    def article_summary_for_hover(self, number_of_lines=2, plot_index=0):
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

    def plot_points(
        self,
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

        coor = [[], [], []]
        index = 0
        while True:
            if index > len(self.points) - 1:
                break

            x = (-1) ** np.random.randint(5, size=1)[0] * radius * np.random.rand(1)[0]
            y = (-1) ** np.random.randint(5, size=1)[0] * radius * np.random.rand(1)[0]
            z = (-1) ** np.random.randint(5, size=1)[0] * radius * np.random.rand(1)[0]

            if math.sqrt(x ** 2 + y ** 2 + z ** 2) <= radius:
                coor[0].append(x)
                coor[1].append(y)
                coor[2].append(z)
                index += 1

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
                hoverinfo="text",
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
            },
        )
        fig.update_traces(showlegend=False)
        if plot_flag == True:
            fig.show()

        # self.fig = fig

        return fig
