import random
from akinator_api import AkinatorGame, AkiCategories

if __name__ == "__main__":
    game = AkinatorGame(AkiCategories.CHARACTERS, lambda _: random.choice(["y", "n", "i", "p", "n"]), True)
    game.start_game()
