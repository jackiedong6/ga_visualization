import time
import random
import math

gamma = 1
epsilon = 0.2

row_cutoffs = [1.9, 3.75]
ROWS = len(row_cutoffs) + 1
col_cutoffs = [0.9, 2.49, 2.51, 5.5]
COLS = len(col_cutoffs) + 1

def q_learn(model, limit):
    """ Takes an NFLStrategy object and a time limit and returns
    a function that takes a non-terminal position and returns
    the index of the selected offensive play. """

    # initialize q-values to 0 and alpha-values to 0.2
    q_vals = {(row, col, play): 0 for row in range(ROWS) for col in range(COLS) for play in range(3)}
    alphas = {(row, col, play): 0.2 for row in range(ROWS) for col in range(COLS) for play in range(3)}

    q_vals = q_train(model, limit - 0.0003, q_vals, alphas)

    def fxn(pos):
        move = pick(q_vals, pos)
        return move

    return fxn

def pick(q_vals, pos):
    """ Selects the action leading to the highest q_value
    from the given position """
    row, col = get_bucket(pos)
    max_q = -math.inf
    max_play = -1
    for play in range(3):
        if q_vals[(row, col, play)] > max_q:
            max_play = play
            max_q = q_vals[(row, col, play)]
    return max_play

def get_bucket(pos):
    """ Takes in a position as a (yards-to-score, downs-left,
    distance, ticks) tuple and returns a pair row, col of
    the bucket it's in """

    fieldPosition, downsLeft, distance, timeLeft = pos
    x = fieldPosition / timeLeft
    y = distance / downsLeft

    # identify row
    row = 0
    for i in row_cutoffs:
        if x > i:
            row += 1
        else:
            break

    # identify col
    col = 0
    for j in col_cutoffs:
        if y > j:
            col += 1
        else:
            break

    return row, col

def q_train(model, limit, q_vals, alphas):
    """ Returns a dictionary of trained q-values """

    start_time = time.time()
    while time.time() - start_time < limit:
        pos = model.initial_position()

        # while s is not terminal
        while not model.game_over(pos):
            row, col = get_bucket(pos)

            # choose an action a from that state s with e-greedy
            if random.uniform(0, 1) < epsilon: # EXPLORE
                play = random.choice(range(3))
            else: # EXPLOIT
                play = pick(q_vals, pos)

            # observe the transition (s, a, s', r)
            result = model.result(pos, play)[0]

            # update the relevant q-value
            # check if terminal
            if model.game_over(result):
                r = -1 # loss
                if model.win(result):
                    r = 1 # win
                first = r
            else:
                row2, col2 = get_bucket(result)
                max_play2 = pick(q_vals, result)
                first = gamma*q_vals[(row2, col2, max_play2)]

            q_vals[(row, col, play)] += alphas[(row, col, play)]*(first - q_vals[(row, col, play)])

            # update values
            alphas[(row, col, play)] *= 0.9999
            pos = result

    return q_vals