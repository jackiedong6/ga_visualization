import numpy as np

gradient = [(250, 250, 110),
(181, 232, 119),
(119, 209, 131),
(63, 183, 141),
(0, 156, 143),
(0, 127, 134),
(28, 99, 115),
(42, 72, 88)]
MAX_VALUE = float('-infinity')
MIN_VALUE = float('infinity')


class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns
    def generate_population(self, population):
        global MAX_VALUE, MIN_VALUE

        population_2d = np.array(population).reshape(self.rows, self.cols)
        # population_2d = population_2d * 1001
        
        MIN_VALUE = min(np.min(population_2d), MIN_VALUE)
        MAX_VALUE = max(np.max(population_2d), MAX_VALUE)
        if MAX_VALUE - MIN_VALUE < len(gradient):
            # scale all values up so that MAX_VALUE maps to len(gradient) - 1
            x = np.array([[list(gradient[int(population_2d[i][j] * (len(gradient) - 1) / MAX_VALUE)])
                for i in range(self.rows)] for j in range(self.cols)], dtype=np.uint8)
        else:
            # scale values down
            x = np.array(
                [[list(gradient[round((len(gradient) - 1) * ((population_2d[i][j]) - MIN_VALUE) / (MAX_VALUE - MIN_VALUE))])
                for i in range(self.rows)] for j in range(self.cols)],
                dtype=np.uint8)

        return x

    def generate_legend(self):
        x = np.array([[gradient[i]] for i in range(len(gradient))], dtype = np.uint8)
        return x
