import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from PIL import Image, ImageDraw, ImageFont


class TournamentTableGenerator:
    def __init__(self, details, winner):
        self.details = details
        self.winner = winner
        self.rounds = len(details)
        self.image = Image.new("RGB", self.calculate_image_size(), "black")
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        self.text_color = "black"
        self.box_color = "white"

    def calculate_image_size(self):
        width = 200 * (self.rounds + 1)
        height = 100 * (2**self.rounds)

        return (width, height)

    def generate(self):
        for round_index, round_matches in enumerate(self.details, start=1):
            match_height = 100 * (2 ** (round_index - 1))
            for match_index, match in enumerate(round_matches):
                y = (2 * match_index + 1) * match_height / 2
                x = 200 * round_index
                self.draw_match((x, y), match, round_index, match_index)

        return self.image

    def draw_match(self, position, match, round_index, match_index):
        x, y = position
        y += 200

        self.draw.rectangle(
            [x - 50, y - 20, x + 50, y], fill=self.box_color, outline=self.text_color
        )
        self.draw.text(
            (x - 45, y - 15), match["player1"], fill=self.text_color, font=self.font
        )
        self.draw.rectangle(
            [x - 50, y, x + 50, y + 20], fill=self.box_color, outline=self.text_color
        )
        self.draw.text(
            (x - 45, y + 5), match["player2"], fill=self.text_color, font=self.font
        )

        if round_index < self.rounds:
            next_y = self.calculate_next_y(match_index, round_index)
            next_y += 50
            self.draw.line(
                (x + 50, y + 10, x + 150, next_y), fill=self.text_color, width=2
            )

    def calculate_next_y(self, match_index, round_index):
        next_match_height = 100 * (2**round_index)

        return (2 * match_index // 2 + 1) * next_match_height / 2 + 50
