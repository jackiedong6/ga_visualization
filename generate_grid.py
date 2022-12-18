from random import randint
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns

    def generate_starting_population(self):
        x = np.array([[[randint(0, 255), randint(0, 255), randint(0,255)] for i in range(self.rows)] for j in range(self.cols)], dtype = np.uint8)

        return x

if __name__ == "__main__":

    populations = []
    grid = Grid(16, 16)

    for i in range(16):
        populations.append(grid.generate_starting_population())


    populations = np.array(populations)

    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.01, subplot_titles = ("Initial Population", "Original Population"))

    fig_px = px.imshow(populations, animation_frame=0)

    sliders = fig_px.layout.sliders
    updatemenus = fig_px.layout.updatemenus


    frames =[go.Frame(data=[go.Image(z=populations[0]),
                            go.Image(z=populations[k], visible=True, name=str(k)),
                            ],
                      traces=[0,1], name=str(k)) for k in range(populations.shape[0])]

    fig.add_trace(go.Image(z=populations[0]), row=1, col=1)
    fig.add_trace(go.Image(z=populations[1]), row=1, col=2)

    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(visible=False, showticklabels=False)

    fig.update(frames=frames)
    fig.update_layout(updatemenus=updatemenus, sliders=sliders)
    fig.update_layout(sliders=[{"currentvalue": {"prefix": "Current Generation="}}])

fig.show()