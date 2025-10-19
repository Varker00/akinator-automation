import random

from player import Player
from akinator_driver import AkinatorDriver
from akinator_api import AkinatorGame, AkiCategories

if __name__ == "__main__":
    # for i in range(5):
    #     category = "Characters"
    #     category_map = {
    #         "1": "Characters",
    #         "2": "Objects",
    #         "3": "Animals",
    #     }
    #     while category is None:
    #         print("Select category:")
    #         for key, item in category_map.items():
    #             print(f"{key}. {item}")
    #         category = category_map.get(input(), None)
    #
    #     driver = AkinatorDriver()
    #     player = Player(driver)
    #
    #     driver.select_category(category)
    #     player.play_until_the_end()
    #
    #     driver.quit()

    game = AkinatorGame(AkiCategories.CHARACTERS, lambda _: random.choice(["y", "n", "i", "p", "n"]), True)
    game.start_game()
