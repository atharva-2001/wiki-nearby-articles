"""General functions called in the WNA class."""
import math
import re
import sys
import requests
import numpy as np
from collections import defaultdict


def random_points_in_a_sphere(h=0, g=0, f=0, num=0, radius=5):
    """
    Generate random points in a sphere.

    Parameters
    ----------
    h,g,f : int
        The center of the sphere.
    num : int
        The number of points to be generated.
    radius : int
        The radius of the sphere.

    Returns
    -------
    coor: defaultdict(list)
        Dictionary having the coordinates of the points.
    """
    coor = [[], [], []]
    coor = defaultdict(list)
    index = 0

    while True:
        if index > num - 1:
            break

        x = np.random.uniform(h + radius, h - radius)
        y = np.random.uniform(g + radius, g - radius)
        z = np.random.uniform(f + radius, f - radius)

        if math.sqrt((x - h) ** 2 + (y - g) ** 2 + (z - f) ** 2) <= radius:
            if (x != 0) and (y != 0) and (z != 0):
                coor["x"].append(np.round(x, 2))
                coor["y"].append(np.round(y, 2))
                coor["z"].append(np.round(z, 2))
                index += 1

    return coor


def extend_points(tip={"x": 0, "y": 0, "z": 0}, end={"x": 0, "y": 0, "z": 0}, factor=2):
    """
    Generate random points in a sphere.

    Parameters
    ----------
    tip : list
        Coordinates of the starting point. Default [0,0,0]
    end : list
        Coordinates of the ending point.
    factor : int
        The factor by which the points are to be extended.

    Returns
    -------
    new_coords: list
        Extended coordinates of the ending point.
    """
    xnew = factor * (end["x"] - tip["x"]) + tip["x"]
    ynew = factor * (end["y"] - tip["y"]) + tip["y"]
    znew = factor * (end["z"] - tip["z"]) + tip["z"]
    new_coords = [xnew, ynew, znew]

    new_coords = {"x": xnew, "y": ynew, "z": znew}
    return new_coords


def find_hover_text(output_data):
    """
    Parse the hover text from the API output.

    Parameters
    ----------
    output_data : str
        Raw API output.

    Returns
    -------
    hover_data: str
        Parsed hover data.
    """
    output_lst = re.split(" ", output_data)
    output_lst = [" ".join(output_lst[i : i + 3]) for i in range(0, len(output_lst), 3)]
    hover_data = "<br>".join(["".join(item) for item in output_lst])
    return hover_data


def call_mediawiki_api(
    titles,
    action="query",
    format_="json",
    prop="extracts",
    exsentences="7",
    exlimit="1",
    explaintext="1",
    formatversion="2",
    pllimit="max",
):
    """
    Call MediaWiki API.

    Parameters
    ----------
    article_name : str
        Name of the wikipedia article.
    number_of_lines : int
        Number of exsentences to be returned from the API. Default: 7.

    Returns
    -------
    data: str
        Output of the API call.
    """

    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": action,
        "format": format_,
        "titles": titles,
        "prop": prop,
        "exsentences": exsentences,
        "exlimit": exlimit,
        "explaintext": explaintext,
        "formatversion": formatversion,
        "pllimit": pllimit,
    }
    R = S.get(url=URL, params=PARAMS)
    data = R.json()
    S.close()
    return data
