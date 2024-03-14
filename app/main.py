from src.data_loader import DataLoader
from src.tournament import Tournament
from src.generate_synthetic_data import TournamentMatrix
from src.generating_image_tt import TournamentTableGenerator

import pandas as pd

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
    print("Идеальные позиции и вероятности победы для каждого игрока:")
    for hero in heroes:
        probabilities = tournament.find_best_position_for_player(hero)
        print(f"{hero}: {probabilities}")

    print("\nВыберите игрока по номеру:")
    for index, hero in enumerate(heroes, start=1):
        print(f"{index}: {hero}")
    player_index = int(input()) - 1
    if player_index < 0 or player_index >= len(heroes):
        print("Неверный выбор игрока.")
        return

    player_name = heroes[player_index]

    print("Выберите новую позицию игрока:")
    position = int(input())
    if position < 1 or position > len(heroes):
        print("Неверная позиция.")
        return

    players = heroes[:]
    players.remove(player_name)
    players.insert(position - 1, player_name)

    tournament_details, winner = tournament.simulate_tournament(players)

    for round_details in tournament_details:
        print(f"\nРаунд {round_details[0]['round']}:")
        for match in round_details:
            print(f"  {match['player1']} против {match['player2']} -> Победитель: {match['winner']}")
    print(f"\nПобедитель турнира: {winner}")

    generator = TournamentTableGenerator(tournament_details, winner)
    tournament_image = generator.generate()
    tournament_image.show()
    tournament_image.save("images/tournament.png")

if __name__ == "__main__":
    main()
