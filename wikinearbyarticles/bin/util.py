import math
import re
import sys
import requests
import numpy as np

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
    # print("finding random points...")
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
    # print("extending coords...")
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
