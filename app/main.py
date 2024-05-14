from src.data_loader import DataLoader
from src.tournament import Tournament
from src.generate_synthetic_data import TournamentMatrix
from src.generating_image_tt import TournamentTableGenerator

import pandas as pd
import random
from tqdm import tqdm
from itertools import permutations

def random_distribution(players, total_positions):
    all_positions = list(range(total_positions))
    random_count = random.randint(1, len(players))
    chosen_positions = random.sample(all_positions, random_count)
    random.shuffle(players)
    distributed_players = dict(zip(chosen_positions, players[:random_count]))
    remaining_players = players[random_count:]
    return distributed_players, remaining_players

def calculate_win_probability(player_name, position, data):
    players = data.columns
    position_counts = 0
    total_simulations = 0
    
    for perm in permutations(players):
        simulate_order = list(perm)
        simulate_order[position] = player_name
        tournament = Tournament(data)
        _, winner = tournament.simulate_tournament(simulate_order)
        
        if winner == player_name:
            position_counts += 1
        total_simulations += 1
        
    probability = position_counts / total_simulations if total_simulations > 0 else 0
    return probability

def normalize_probabilities(player_probabilities):
    total_probability = sum(player_probabilities.values())
    for player in player_probabilities:
        player_probabilities[player] /= total_probability
    return player_probabilities

def main():
    choice = input("Вы хотите использовать собственные данные? (да/нет): ").strip().lower()
    if choice == 'да':
        path = input("Введите путь до файла: ").strip()
        data = DataLoader.load_data(path)
        print(data)
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

    optimal_positions = {}
    print("\nПоиск оптимальных позиций для оставшихся игроков:")
    for player in tqdm(remaining_players, desc="Обработка игроков"):
        best_position, reason = tournament.find_best_position_for_player(player, distributed_players)
        distributed_players[best_position] = player
        optimal_positions[player] = (best_position, reason)

    print("\nИгроки, для которых выбраны оптимальные места:")
    for player, (position, reason) in optimal_positions.items():
        print(f"Игрок: {player}, Оптимальная позиция: {position + 1}, Причина: {reason}")

    player_probabilities = {}
    for position in sorted(distributed_players.keys()):
        player = distributed_players[position]
        probability = calculate_win_probability(player, position, data)
        player_probabilities[player] = probability

    normalized_probabilities = normalize_probabilities(player_probabilities)

    print("\nИтоговое распределение игроков по позициям:")
    for player, probability in normalized_probabilities.items():
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
