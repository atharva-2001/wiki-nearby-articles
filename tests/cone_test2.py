import numpy as np
import math
import plotly.graph_objects as go
def plot_points(
        radius=5,
        plot_flag=False,
        show_lines_with_origin=True,
        line_color="#5c5c5c",
        dot_color="#525BCB",
        plot_index=0,
        number_of_lines=2,
    ):
        # collect summary data and plot points

        coor = [[], [], []]
        index = 0
        while True:
            if index > 20:
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

                marker=dict(size=5, color=dot_color, opacity=0.5),
                mode="markers+text",
                hoverinfo="text",
            )
        )
        return fig

fig = plot_points()
fig.show()


# def check_in_cone(
#     tip = np.array([0,0,0]),
#     base_center = np.array([5,5,5]),
#     h = 10,
#     r = 5,
#     p = np.array(1,1,1)
#     ):
