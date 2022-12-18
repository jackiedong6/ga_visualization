import numpy as np

gradient = [(250, 250, 110), (237, 247, 111), (224, 244, 112), (212, 241, 113), (200, 237, 115), (188, 234, 117),
            (176, 230, 120), (165, 226, 122), (153, 222, 124), (142, 218, 127), (131, 214, 129), (121, 210, 131),
            (110, 205, 133), (100, 201, 135), (90, 196, 137), (80, 191, 139), (70, 187, 140), (60, 182, 141),
            (50, 177, 142), (40, 172, 143), (30, 167, 143), (18, 162, 143), (3, 157, 143), (0, 152, 142), (0, 147, 141),
            (0, 142, 140), (0, 137, 138), (0, 132, 136), (0, 126, 134), (0, 121, 131), (5, 116, 128), (14, 111, 125),
            (21, 106, 121), (26, 101, 117), (30, 96, 113), (34, 91, 108), (37, 86, 103), (39, 81, 99), (41, 77, 93),
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
        MIN_VALUE = min(np.min(population_2d), MIN_VALUE)
        MAX_VALUE = max(np.max(population_2d), MAX_VALUE)
        for i in range(self.rows):
            for j in range(self.cols):
                print(round((len(gradient) - 1) * ((population_2d[i][j]) - MIN_VALUE) / (MAX_VALUE - MIN_VALUE)))
        x = np.array(
            [[list(gradient[round((len(gradient) - 1) * ((population_2d[i][j]) - MIN_VALUE) / (MAX_VALUE - MIN_VALUE))])
              for i in range(self.rows)] for j in range(self.cols)],
            dtype=np.uint8)

        return x
