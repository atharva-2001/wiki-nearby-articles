import numpy as np
import math
from plotly import graph_objects as go
import plotly.express as px
import pandas
# def extend_points(tip = [0,0,0], end = [10, 10, 10], distance = 10):
#     '''
#     returns new coordinates of the points to extend
#     in a list
#     the default value of tip is the origin
#     end is also a list 
#     '''
tip = [0, 0, 0]
end = [10, 10, 10]
distance = 10
u = distance
x = (1-u)*tip[0] + u*end[0]
y = (1-u)*tip[1] + u*end[1]
z = (1-u)*tip[2] + u*end[2]


fig = px.scatter(
        x = [x, tip[0], end[0]],
        y = [y, tip[1], end[2]],
        z = [z, tip[2], end[2]])
fig.show()

