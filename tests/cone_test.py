import plotly.graph_objects as go
import numpy as np

origin  = np.array([0,0,0])
main_point = np.array([5,4,3])
random_point = np.array([3,7,9])
a = np.array([3, 5,9])
b = np.array([4, 2,10])
c = np.array([1, 1,13])

ba = a - b
bc = c - b

cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
angle = np.arccos(cosine_angle)

print(np.degrees(angle))
angle = np.degrees(angle)
print(6.28 * (1-np.cos(angle)))
other_points = [a,b,c]
x,y,z = [origin[0], main_point[0]], [origin[1],main_point[1]], [origin[2],main_point[2]]

for item in other_points:
    # try:
    x.append(item[0])
    y.append(item[1])
    z.append(item[2])
    # except: pass
    

print(x,y,z)
import plotly.express as px
fig = go.Figure()
fig.add_trace(
    go.Scatter3d(
        x = x,
        y = y,
        z = z,
        mode = "markers"
    )
)
# fig = px.scatter_3d(x = x,y = y, z = z)
for x_coor, y_coor, z_coor in zip(
            x, y, z
        ):
        # if x_coor or y_coor or z_coor is 0:
            fig.add_trace(
                go.Scatter3d(
                    x=[x_coor, 0],
                    y=[y_coor, 0],
                    z=[z_coor, 0],
                    # text = points,
                    # name = point,
                    marker=dict(
                        size=0.1,
                        # color=line_color,
                        # colorscale='Viridis',
                        # opacity=1
                    ),
                    mode="lines",
                    hoverinfo="none"
                    # hovertemplate = f"{article_summary_for_hover(article_name=point, number_of_lines=2)}"
                )
            )
fig.update_layout(
    scene = {
        "xaxis": {
            "range": [-5, 15]
        },
        "yaxis": {
            "range": [-5,15]
        },
        "zaxis": {
            "range": [-5,15]
        }
    }

)
fig.show()

