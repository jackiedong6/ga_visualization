import numpy as np

gradient = [(250, 250, 110),
(224, 241, 111),
(199, 232, 113),
(176, 223, 115),
(154, 212, 118),
(134, 202, 120),
(115, 191, 121),
(98, 180, 122),
(82, 168, 122),
(69, 156, 121),
(58, 145, 119),
(50, 133, 115),
(44, 121, 110),
(42, 109, 104),
(41, 98, 97),
(42, 86, 88)]
MAX_VALUE = float('-infinity')
MIN_VALUE = float('infinity')


class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns
    def generate_population(self, population):
        global MAX_VALUE, MIN_VALUE

        population_2d = np.array(population).reshape(self.rows, self.cols)
        MIN_VALUE = min(np.min(population_2d), MIN_VALUE)
        MAX_VALUE = max(np.max(population_2d), MAX_VALUE)

        x = np.array(
            [[list(gradient[round((len(gradient) - 1) * ((population_2d[i][j]) - MIN_VALUE) / (MAX_VALUE - MIN_VALUE))])
              for i in range(self.rows)] for j in range(self.cols)],
            dtype=np.uint8)

        return x

    def generate_legend(self):
        x = np.array([[gradient[i]] for i in range(len(gradient))], dtype = np.uint8)
        return x
