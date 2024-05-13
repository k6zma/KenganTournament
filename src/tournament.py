from itertools import permutations
from collections import Counter
from math import factorial

import numpy as np
from tqdm import tqdm

class Tournament:
    def __init__(self, data):
        self.data = data

    def collect_heroes(self):
        heroes_from_columns = self.data.columns.tolist()
        heroes_from_rows = self.data.index.tolist()

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
        tournament_details = []

        round_number = 1
        while len(players) > 1:
            round_info = []
            next_round = []
            for i in range(0, len(players), 2):
                match = {
                    "round": round_number,
                    "player1": players[i],
                    "player2": players[i + 1],
                    "winner": None,
                }

                prob_p1_wins = self.data.loc[players[i], players[i + 1]]
                prob_p2_wins = self.data.loc[players[i + 1], players[i]]

                winner = players[i] if prob_p2_wins < prob_p1_wins else players[i + 1]
                match["winner"] = winner

                round_info.append(match)
                next_round.append(winner)

            tournament_details.append(round_info)
            players = next_round
            round_number += 1

        return tournament_details, players[0]

    def find_best_position_for_player(self, player_name, distributed_players):
        players = list(self.data.columns)
        free_positions = [pos for pos in range(len(players)) if pos not in distributed_players]
        total_permutations = factorial(len(players))

        best_position = None
        best_probability = -1
        reasons = []

        for position in free_positions:
            position_counts = Counter()
            position_simulations = Counter()
            total_simulations = 0

            for perm in permutations(players):
                simulate_order = list(perm)
                simulate_order[position] = player_name
                _, winner = self.simulate_tournament(simulate_order)
                current_position = simulate_order.index(player_name)
                position_simulations[current_position] += 1

                if winner == player_name:
                    position_counts[current_position] += 1
                total_simulations += 1

            position_probability = (
                position_counts[position] / position_simulations[position]
                if position_simulations[position] > 0
                else 0
            )

            reasons.append(
                f"Позиция {position + 1}: {position_probability:.2%} вероятность победы"
            )

            if position_probability > best_probability:
                best_probability = position_probability
                best_position = position

        reason = "\n".join(reasons)
        return best_position, reason
