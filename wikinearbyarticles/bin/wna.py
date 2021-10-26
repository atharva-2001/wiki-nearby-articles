"""Main class to run wiki-nearby-articles."""
import plotly.graph_objects as go
from .util import *


class WNA:
    """WNA class."""

    def __init__(
        self, link, prop_params, points_in_one_shot=36, points={}, plot_all_points=None
    ):
        """
        WNA class.

        Parameters
        ----------
        link : str
            Name of the Wikipedia article or it's link
        prop_params : str
            Should either be `links` or `linkhere`.
        points_in_one_shot : int
            Points to be plotted for one cluster.
        points : dict
            Points plotted in the figure.
        plot_all_points : bool
            Whether or not to plot all points.

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
        self.fig = go.FigureWidget()

        if points != {}:
            self.points = points
        else:
            self.points = {}

    def collect_points(self, center="", plot_index=0):
        """
        Collect points and add them to the points dictionary.

        Parameters
        ----------
        center : string
            Name of the article at the center of the cluster. Default: "".
            If center is "", it means the center is at origin.
        plot_index : int
        """
        if self.points != {}:
            self.points = self.points[0]

        if self.article_name not in self.points.keys():
            DATA = call_mediawiki_api(titles=self.article_name, prop=self.prop_params)
            PAGES = DATA["query"]["pages"][0]
            new_cluster_point_names = []

            for item in PAGES[self.prop_params]:
                new_cluster_point_names.append(item["title"])

            if not self.plot_all_points:
                new_cluster_point_names = [
                    new_cluster_point_names[i : i + self.points_in_one_plot]
                    for i in range(
                        0, len(new_cluster_point_names), self.points_in_one_plot
                    )
                ]
                self.sections = len(new_cluster_point_names)
                if plot_index is None:
                    plot_index = 0
                new_cluster_point_names = new_cluster_point_names[plot_index]

            # center is origin
            new_cluster_point_coords = random_points_in_a_sphere(
                num=len(new_cluster_point_names), radius=5
            )
            orgin_cluster_coords = random_points_in_a_sphere(
                num=len(new_cluster_point_names), radius=5
            )

            self.points[self.article_name] = {
                "cluster_origin": self.article_name,
                "center_coords": {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                },
                "point_names": new_cluster_point_names,
                "coords": orgin_cluster_coords,
            }

        center_coords = []
        cluster_origin = ""
        if_break = False

        if center != "" and center is not None:
            for key in self.points.keys():
                for name in self.points[key]["point_names"]:
                    if name == center:
                        idx = self.points[key]["point_names"].index(name)
                        center_coords = {
                            "x": self.points[key]["coords"]["x"][idx],
                            "y": self.points[key]["coords"]["y"][idx],
                            "z": self.points[key]["coords"]["z"][idx],
                        }

                        cluster_origin_coords = {
                            "x": self.points[key]["center_coords"]["x"],
                            "y": self.points[key]["center_coords"]["y"],
                            "z": self.points[key]["center_coords"]["z"],
                        }

                        center_coords = extend_points(
                            tip=cluster_origin_coords, end=center_coords, factor=4.5
                        )

                        self.points[key]["coords"]["x"][idx] = center_coords["x"]
                        self.points[key]["coords"]["y"][idx] = center_coords["y"]
                        self.points[key]["coords"]["z"][idx] = center_coords["z"]

                        cluster_origin = key
                        if_break = True  # TODO: can this be avoided?
                        break
                if if_break:
                    break

            new_cluster_point_names_raw = call_mediawiki_api(
                titles=center, prop=self.prop_params
            )["query"]["pages"][0]

            new_cluster_point_names = []

            for l in new_cluster_point_names_raw[self.prop_params]:
                new_cluster_point_names.append(l["title"])

            if not self.plot_all_points:
                new_cluster_point_names = [
                    new_cluster_point_names[i : i + self.points_in_one_plot]
                    for i in range(
                        0, len(new_cluster_point_names), self.points_in_one_plot
                    )
                ][plot_index]

            new_cluster_point_coords = random_points_in_a_sphere(
                num=len(new_cluster_point_names),
                radius=5,
                h=center_coords["x"],
                g=center_coords["y"],
                f=center_coords["z"],
            )

            self.points[center] = {
                "center_coords": center_coords,
                "cluster_origin": cluster_origin,
                "point_names": new_cluster_point_names,
                "coords": new_cluster_point_coords,
            }

    def return_points(self, drop=True):
        """
        Return all points except cluster centers.

        Parameters
        ----------
        drop : bool
            If True, return names of points alongwith length of clusters.
            If False, return `self.points` and alongwith length of clusters.

        Returns
        -------
        points_lst: list
            List of point names. Only returned when the parameter drop is True.
        self.points: dict
            The points dictionary. Only returned when the parameter drop is False.
        self.sections: int
            Length of points belonging to a cluster.
        """
        if drop:
            points_lst = []
            for key in self.points.keys():
                points_lst += self.points[key]["point_names"]
                if key in points_lst:
                    points_lst = [item for item in points_lst if item != key]
            return points_lst, self.sections
        else:
            return self.points, self.sections

    def article_summary_for_hover(
        self,
        number_of_lines=2,
        plot_index=0,
        display_all_summaries=False,
        collect_points=True,
    ):
        """
        Return hover data.

        Parameters
        ----------
        number_of_lines : int
            Number of lines of hover text. Default: 2
        plot_index : int
            Default: 2.
        display_all_summaries : bool
            Default: False.
        collect_points : bool
            Default: True.


        Returns
        -------
        hover_data: str
            Parsed hover data.
        """
        if collect_points:
            self.collect_points()
            if not self.plot_all_points:
                self.points = self.points[plot_index]

        if display_all_summaries:
            hover_text = []
            for point in self.points:
                DATA = call_mediawiki_api(
                    titles=point,
                    exsentences=number_of_lines,
                )
                hover_text_for_one_point = find_hover_text(
                    DATA["query"]["pages"][0]["extract"]
                )
                hover_text.append(hover_text_for_one_point)

            self.hover_text = hover_text
            return self.hover_text
        else:
            # print(f"trying to get hover text for {self.article_name}")
            return call_mediawiki_api(titles=self.article_name)

    def plot(
        self,
        line_color="#d4d4d4",
        dot_color="#525BCB",
    ):
        """
        Plot/update the figure.

        Parameters
        ----------
        line_color : str
            Color of the lines. Default: "#d4d4d4"
        dot_color : str
            Color of the surrounding dots. Default: "#525BCB"

        Returns
        -------
        fig: go.FigureWidget
            Plotly figure.
        """
        with self.fig.batch_update():
            for cluster_name in self.points.keys():
                # add the cluster center point
                trace_names = [item.name for item in self.fig.data]
                if cluster_name == self.article_name:
                    dot_color_main = "#ffac12"
                    dot_size_main = 17
                    opacity_main = 0.9
                else:
                    dot_color_main = dot_color
                    dot_size_main = 9
                    opacity_main = 0.6

                if cluster_name not in trace_names:
                    self.fig.add_trace(
                        go.Scatter3d(
                            x=[self.points[cluster_name]["center_coords"]["x"]],
                            y=[self.points[cluster_name]["center_coords"]["y"]],
                            z=[self.points[cluster_name]["center_coords"]["z"]],
                            name=cluster_name,
                            text=[cluster_name],
                            marker=dict(
                                size=dot_size_main,
                                color=dot_color_main,
                                opacity=opacity_main,
                                symbol="diamond-open",
                            ),
                            mode="markers+text",
                            hoverinfo="text",
                        )
                    )
                # add the points corresponding to the cluster
                if cluster_name + "!points" not in trace_names:
                    self.fig.add_trace(
                        go.Scatter3d(
                            x=self.points[cluster_name]["coords"]["x"],
                            y=self.points[cluster_name]["coords"]["y"],
                            z=self.points[cluster_name]["coords"]["z"],
                            hovertext=self.points[cluster_name]["point_names"],
                            marker=dict(size=4, color=dot_color, opacity=0.5),
                            name=cluster_name + "!points",
                            mode="markers+text",
                            hoverinfo="text",
                        )
                    )

            # plot lines to connect plots
            if cluster_name + "!lines" not in trace_names:
                for cluster_name in self.points.keys():
                    idx = 0
                    while idx < len(self.points[cluster_name]["point_names"]):
                        self.fig.add_trace(
                            go.Scatter3d(
                                x=[
                                    self.points[cluster_name]["coords"]["x"][idx],
                                    self.points[cluster_name]["center_coords"]["x"],
                                ],
                                y=[
                                    self.points[cluster_name]["coords"]["y"][idx],
                                    self.points[cluster_name]["center_coords"]["y"],
                                ],
                                z=[
                                    self.points[cluster_name]["coords"]["z"][idx],
                                    self.points[cluster_name]["center_coords"]["z"],
                                ],
                                name=cluster_name + "!lines",
                                marker=dict(size=0.1, color=line_color),
                                mode="lines",
                                hoverinfo="none",
                            )
                        ),
                        idx += 1

            self.fig.update_layout(
                height=1200,
                width=800,
                transition={"duration": 500, "easing": "cubic-in-out"},
                hoverlabel={
                    "font": {"family": "monospace"},
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
            self.fig.update_traces(showlegend=False)
        return self.fig
