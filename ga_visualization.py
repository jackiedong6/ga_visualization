import sys
from Blotto.blotto import Blotto
from Cribbage.policy import CompositePolicy, RandomThrower, RandomPegger, GreedyThrower, GreedyPegger
from Cribbage.cribbage import Game, evaluate_policies
from Cribbage.my_policy import MyPolicy
from Cribbage.cribbage_ga import Cribbage_GA
import QFL.nfl_strategy as nfl
import time
import QFL.qfl as qfl
from QFL.const import game_parameters
from generate_grid import Grid
import numpy as np
import pandas
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


if __name__ == "__main__":

    populations = []
    if sys.argv[1] == "--Blotto":
        tolerance = 10 ** -6
        units = int(sys.argv[2])
        scoring_distribution = []
        for i in range(3, len(sys.argv)):
            scoring_distribution.append(int(sys.argv[i]))

        game = Blotto(units, scoring_distribution)

        # generate initial grid            
        initial_fitness = game.evaluate_fitness()
        dim = int(game.num_individuals ** (1/2))
        x = np.array(initial_fitness).reshape(dim, dim)
        grid = Grid(dim, dim)
        populations.append(grid.generate_population(initial_fitness))
        
        prev = sum(initial_fitness)
        
        while True: 
            new_fitness = game.crossover()
            if sum(new_fitness) < prev: 
                break
            populations.append(grid.generate_population(new_fitness))
            prev = sum(new_fitness)
        
        print(game.population)

    if sys.argv[1] == "--Cribbage":
        game  = Cribbage_GA()
        initial_fitness = game.evaluate_fitness()
        dim = int(game.num_individuals ** (1/2))
        grid = Grid(dim, dim)
        populations.append(grid.generate_population(initial_fitness))
        for _ in range(5):
            populations.append(grid.generate_population(game.crossover()))

    legend = grid.generate_legend()
    populations = np.array(populations)

    fig = make_subplots(rows=1, cols = 3, horizontal_spacing=0.05,
                        subplot_titles=("Initial Population", "Current Population", "Fitness Function"),  column_widths=[0.5, 0.5, 0.09])

    fig_px = px.imshow(populations, animation_frame=0)
    sliders = fig_px.layout.sliders
    updatemenus = fig_px.layout.updatemenus


    frames  = [go.Frame(data=[go.Image(z=populations[0]),
                             go.Image(z=populations[k], visible=True, name=str(k)),
                             go.Image(z=legend),
                             ],
                       traces=[0, 1, 2], name=str(k)) for k in range(populations.shape[0])]

    fig.add_trace(go.Image(z=populations[0]), row=1, col=1)
    fig.add_trace(go.Image(z=populations[1]), row=1, col=2)
    fig.add_trace(go.Image(z = legend), row = 1, col = 3)
#     fig.add_trace(go.Image(z=legend), row = 1, col = 3)

    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(visible=False, showticklabels=False)

    fig.update(frames=frames)
    fig.update_layout(updatemenus=updatemenus, sliders=sliders)
    fig.update_layout(sliders=[{"currentvalue": {"prefix": "Current Generation=","font_size":14}}])
    fig.update_layout(
        title = "Genetic Algorithm Visualization for " + sys.argv[1].replace("--", ""),
        title_font_color = "black",
        font_size = 24,
        font_family ="Courier New",
        font_color = "black")

    fig.show()
