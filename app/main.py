from src.data_loader import DataLoader
from src.tournament import Tournament
from src.generate_synthetic_data import TournamentMatrix
from src.generating_image_tt import TournamentTableGenerator
from itertools import permutations
from math import factorial

import pandas as pd
import random
from tqdm import tqdm

def random_distribution(players, total_positions):
    all_positions = list(range(total_positions))
    random_count = random.randint(1, len(players))
    chosen_positions = random.sample(all_positions, random_count)
    random.shuffle(players)
    distributed_players = dict(zip(chosen_positions, players[:random_count]))
    remaining_players = players[random_count:]
    return distributed_players, remaining_players

def calculate_win_probabilities(data):
    players = data.columns
    total_permutations = factorial(len(players))
    win_counts = {player: 0 for player in players}

    for perm in permutations(players):
        simulate_order = list(perm)
        tournament = Tournament(data)
        _, winner = tournament.simulate_tournament(simulate_order)
        win_counts[winner] += 1

    probabilities = {player: win_counts[player] / total_permutations for player in players}
    return probabilities

def main():
    choice = input("Вы хотите использовать собственные данные? (да/нет): ").strip().lower()
    if choice == 'да':
        path = input("Введите путь до файла: ").strip()
        data = DataLoader.load_data(path)
    else:
        print("Генерируем данные...")
        tm = TournamentMatrix()
        data = tm.get_matrix_df()

    print(data)
    tournament = Tournament(data)
    heroes = tournament.collect_heroes()
    total_positions = len(heroes)
    distributed_players, remaining_players = random_distribution(heroes, total_positions)

    print("Случайно распределенные игроки по позициям:")
    for position, player in distributed_players.items():
        print(f"Позиция {position + 1}: {player}")

    print("\nПоиск оптимальных позиций для оставшихся игроков:")
    for player in tqdm(remaining_players, desc="Обработка игроков"):
        best_position, reason = tournament.find_best_position_for_player(player, distributed_players)
        distributed_players[best_position] = player

    probabilities = calculate_win_probabilities(data)

    print("\nИтоговое распределение игроков по позициям:")
    for player, probability in probabilities.items():
        print(f"Игрок {player} (Вероятность победы: {probability:.2%})")

    final_players_order = [distributed_players[i] for i in range(total_positions)]
    tournament_details, winner = tournament.simulate_tournament(final_players_order)
    for round_details in tournament_details:
        print(f"\nРаунд {round_details[0]['round']}:")
        for match in round_details:
            print(f"  {match['player1']} против {match['player2']} -> Победитель: {match['winner']}")

    print(f"\nПобедитель турнира: {winner}")

    generator = TournamentTableGenerator(tournament_details, winner)
    tournament_image = generator.generate()
    tournament_image.show()
    tournament_image.save("imgs/tournament.png")

if __name__ == "__main__":
    main()
