import numpy as np
import pandas as pd


class TournamentMatrix:
    def __init__(self):
        self.fighters = [
            "Hatsumi Sen",
            "Tokita Ohma",
            "Nakata Ichiro",
            "Komada Shigeru",
            "Julius Reinhold",
            "Masaki Meguro",
            "Masaki Hayami",
            "Nikaido Ren",
        ]
        self.matrix = self._generate_matrix()

    def _generate_matrix(self):
        n = len(self.fighters)
        prob_matrix = np.zeros((n, n), dtype=object)

        for i in range(n):
            for j in range(i + 1, n):
                prob = round(np.random.rand(), 3)
                prob_matrix[i][j] = prob
                prob_matrix[j][i] = 1 - prob

            prob_matrix[i][i] = "-"

        return prob_matrix

    def get_matrix_df(self):
        return pd.DataFrame(self.matrix, index=self.fighters, columns=self.fighters)
