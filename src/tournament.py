import numpy as np
from itertools import permutations
from collections import Counter


class Tournament:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def collect_heroes(data):
        heroes_from_columns = data.columns.tolist()
        heroes_from_rows = data.index.tolist()

        Tournament._compare_heroes(heroes_from_columns, heroes_from_rows)
        Tournament._check_heroes_count(heroes_from_columns)
        Tournament._check_heroes_empty_names(heroes_from_columns)
        Tournament._check_for_unique_heroes(heroes_from_columns)

        return heroes_from_columns

    def _compare_heroes(heroes_from_columns, heroes_from_rows):
        if set(heroes_from_columns) != set(heroes_from_rows):
            raise ValueError("Имена героев в строках и столбцах не совпадают")

    def _check_heroes_count(heroes):
        heroes_count = len(heroes)
        if heroes_count == 0 or (heroes_count & (heroes_count - 1)) != 0:
            raise ValueError("Количество героев должно быть степенью двойки")

    def _check_heroes_empty_names(heroes):
        for hero in heroes:
            if hero.strip() == "":
                raise ValueError("Имя героя не может быть пустым")

    def _check_for_unique_heroes(heroes):
        if len(heroes) != len(set(heroes)):
            raise ValueError("Имена героев должны быть уникальными")

    def simulate_tournament(self, players):
        round_number = 1

        while len(players) > 1:
            next_round = []
            for i in range(0, len(players), 2):
                p1, p2 = players[i], players[i + 1]
                prob_p1_wins = self.data.loc[p1, p2]
                prob_p2_wins = self.data.loc[p2, p1]
                next_round.append(p1 if prob_p2_wins < prob_p1_wins else p2)

            players = next_round
            round_number += 1

        return players[0]

    def find_best_position_for_player(self, player_name):
        players = list(self.data.columns)
        position_counts = Counter()
        position_simulations = Counter()
        total_simulations = 0

        for perm in permutations(players):
            simulate_order = list(perm)
            winner = self.simulate_tournament(simulate_order)
            position = simulate_order.index(player_name) + 1
            position_simulations[position] += 1

            if winner == player_name:
                position_counts[position] += 1
            total_simulations += 1

        position_probabilities = {
            position: position_counts[position] / position_simulations[position]
            for position in position_simulations
        }

        return position_probabilities
