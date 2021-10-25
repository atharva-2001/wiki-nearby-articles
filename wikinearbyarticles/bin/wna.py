"""Main class to run wiki-nearby-articles"""
import plotly.graph_objects as go
import requests
from .util import *
import json

class WNA:
    """WNA class."""
    
    def __init__(
        self, link, prop_params, points_in_one_shot=36, points={}, plot_all_points=None
    ):
        """
        WNA class.

        Parameters
        ----------
        iterations : int
            iteration number
        **kwargs : dict, optional
            Additional keyword arguments. These arguments are defined in the Other Parameters section.

        Other Parameters
        ----------------
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

        Notes
        -----
        structure of points
        {
            "article name": {
                "cluster_origin": "some string, name of the article directly connected before expanding"
                "center_coords": [[0], [0], [0]],
                "point_names": ["string 1", "string 2"],
                "coords": [[x coords list], [y coords list], [z coords list]]
            }
            # other sections will be added like this
            "some article as center": {
                "cluster_origin": "some string as before"
                "center_coords": [[x], [y], [z]],
                "point_names": ["string 1", "string 2"],
                "coords": [[x coords list], [y coords list], [z coords list]]
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
        self.fig = go.FigureWidget()
        # if the link is updated, the points sent as arguments are already empty dictionaries
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
            # S = requests.Session()
            # URL = "https://en.wikipedia.org/w/api.php"

            # PARAMS = {
            #     "action": "query",
            #     "format": "json",
            #     "titles": self.article_name,
            #     "prop": self.prop_params,
            #     "pllimit": "max",
            # }

            # R = S.get(url=URL, params=PARAMS)
            # DATA = R.json()
            
            DATA = call_mediawiki_api(
                titles=self.article_name,
                prop=self.prop_params
            )
            PAGES = DATA["query"]["pages"][0]
            points = []
            
            # for k, v in PAGES.items():
            #     print(k, v)
            for l in PAGES[self.prop_params]: # TODO: better variable names here
                points.append(l["title"])
            # print(json.dumps(points, sort_keys=True, indent=4))
            # TODO: what does this do?
            if not self.plot_all_points:
                points = [
                    points[i : i + self.points_in_one_plot]
                    for i in range(0, len(points), self.points_in_one_plot)
                ]
                self.sections = len(points)
                if plot_index is None:
                    plot_index = 0
                points = points[plot_index]

            # center is origin
            coords = random_points_in_a_sphere(
                num=len(points), radius=5
            )
            orgin_cluster_coords = random_points_in_a_sphere(
                num=len(points), radius=5
            )

            self.points[self.article_name] = {
                "cluster_origin": self.article_name,
                "center_coords": {
                        "x":0,
                        "y":0,
                        "z":0,
                    },
                "point_names": points,
                "coords": orgin_cluster_coords,
            }
            
        # TODO: what does this do
        center_coords = []
        cluster_origin = ""
        if_break = False
        
        if center != "" and center is not None:
            for key in self.points.keys():
                for name in self.points[key]["point_names"]:
                    if name == center:
                        idx = self.points[key]["point_names"].index(name)
                        center_coords = {
                            "x":self.points[key]["coords"]["x"][idx],
                            "y":self.points[key]["coords"]["y"][idx],
                            "z":self.points[key]["coords"]["z"][idx],                         
                        }

                        cluster_origin_coords = {
                            "x":self.points[key]["center_coords"]["x"],
                            "y":self.points[key]["center_coords"]["y"],
                            "z":self.points[key]["center_coords"]["z"],
                                                        
                        }
                        center_coords = extend_points(
                            tip=cluster_origin_coords, end=center_coords, factor=4.5
                        )

                        self.points[key]["coords"]["x"][idx] = center_coords["x"]
                        self.points[key]["coords"]["y"][idx] = center_coords["y"]
                        self.points[key]["coords"]["z"][idx] = center_coords["z"]

                        cluster_origin = key
                        if_break = True # TODO: can this be avoided?
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

            if not self.plot_all_points:
                points = [
                    points[i : i + self.points_in_one_plot]
                    for i in range(0, len(points), self.points_in_one_plot)
                ][plot_index]

            coords = random_points_in_a_sphere(
                num=len(points),
                radius=5,
                h=center_coords["x"],
                g=center_coords["y"],
                f=center_coords["z"],
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
            # print(f"trying to get hover text for {self.article_name}")
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

        # plotting the central point
        for cluster_name in self.points.keys():
            # adds the center cluster itself
            # though I am not so proud of the code I have written
            # and there is probably a better way to do this, here is the explanation for the traces
            # the first trace added just below adds the clusters to the diagram.
            # the trace after that adds the points corresponding to the cluster.
            # points corresponding to that particular cluster, none else.

            # this adds the cluster center point
            trace_names = [item.name for item in self.fig.data]
            if cluster_name == self.article_name:
                dot_color_main = "#525BCB"
                dot_size_main = 17
                opacity_main = 0.6
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
                        marker=dict(size=dot_size_main, color=dot_color_main, opacity=opacity_main),
                        mode="markers+text",
                        hoverinfo="text",  # what did this do?
                    )
                )
            # this adds the points corresponding to the cluster
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

        # this below adds the lines in plot.
        # this is a tough job, and adds a lot of traces to the graph, which consumes a lot of resources.
        # again, maybe there is a better way
        # I did ask this question on plotly community forum, and am yet to recieve a response.
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

        # this is pretty simple
        # this fixes the layout. However, I am adding 
        # this again to the plot, or redefining the layout in the callback, 
        # and thats causing a little trouble too
        # and I will fix it soon too
        self.fig.update_layout(
            height=1200,
            width=800,
            transition= {
                'duration': 500,
                'easing': 'cubic-in-out'
            }, 
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
