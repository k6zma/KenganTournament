from src.data_loader import DataLoader
from src.tournament import Tournament
from src.generate_synthetic_data import TournamentMatrix
from src.generating_image_tt import TournamentTableGenerator

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

    print("\nИтоговое распределение игроков по позициям:")
    for position in sorted(distributed_players.keys()):
        print(f"Позиция {position + 1}: {distributed_players[position]}")

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
