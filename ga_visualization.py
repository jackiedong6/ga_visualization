import sys
from blotto import Blotto
from Cribbage.policy import CompositePolicy, RandomThrower, RandomPegger, GreedyThrower, GreedyPegger
from Cribbage.cribbage import Game, evaluate_policies
from Cribbage.my_policy import MyPolicy


if __name__ == "__main__":
    if sys.argv[1] == "--Blotto":
        tolerance = 10 ** -6
        units = int(sys.argv[2])
        scoring_distribution = []
        for i in range(3, len(sys.argv)):
            scoring_distribution.append(int(sys.argv[i]))

        game = Blotto(units, scoring_distribution)
        game.generate_individual()

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
