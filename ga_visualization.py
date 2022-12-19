import sys
from Blotto.blotto import Blotto
from Cribbage.policy import CompositePolicy, RandomThrower, RandomPegger, GreedyThrower, GreedyPegger
from Cribbage.cribbage import Game, evaluate_policies
from Cribbage.my_policy import MyPolicy
import QFL.nfl_strategy as nfl
import time
import QFL.qfl as qfl
from QFL.const import game_parameters
from generate_grid import Grid
import numpy as np
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

        initial_fitness = game.evaluate_fitness()
        dim = int(game.num_individuals ** (1/2))
        grid = Grid(dim, dim)
        populations.append(grid.generate_population(initial_fitness))
        for _ in range(15):
            populations.append(grid.generate_population(game.crossover()))

    if sys.argv[1] == "--Cribbage":
        games = 2
        if len(sys.argv) > 2:
            games = int(sys.argv[2])

        game = Game()
        benchmark = CompositePolicy(game, GreedyThrower(game), GreedyPegger(game))
        submission = MyPolicy(game)

        results = evaluate_policies(game, submission, benchmark, games)

        print("NET:", results[0])
        print(results)

    if sys.argv[1] == "--qfl":
        # `example: python3 ga_visualization.py --qfl 0 9 250000`
        if len(sys.argv) > 2:
            game = int(sys.argv[2])
            limit = float(sys.argv[3])
            n = int(sys.argv[4])

        model = nfl.NFLStrategy(*game_parameters[game])
        start = time.time();
        policy = qfl.q_learn(model, limit);
        t = time.time() - start
        # if t > limit:
        #     print("WARNING: Q-learning ran for", t, "seconds; allowed", limit)
        
        print(model.simulate(policy, n))
        
        sys.exit() # dk if the figure will work here

    populations = np.array(populations)

    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.01,
                        subplot_titles=("Initial Population", "Original Population"))

    fig_px = px.imshow(populations, animation_frame=0)

    sliders = fig_px.layout.sliders
    updatemenus = fig_px.layout.updatemenus

    frames = [go.Frame(data=[go.Image(z=populations[0]),
                             go.Image(z=populations[k], visible=True, name=str(k)),
                             ],
                       traces=[0, 1], name=str(k)) for k in range(populations.shape[0])]

    fig.add_trace(go.Image(z=populations[0]), row=1, col=1)
    fig.add_trace(go.Image(z=populations[1]), row=1, col=2)

    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(visible=False, showticklabels=False)

    fig.update(frames=frames)
    fig.update_layout(updatemenus=updatemenus, sliders=sliders)
    fig.update_layout(sliders=[{"currentvalue": {"prefix": "Current Generation="}}])

    fig.show()
