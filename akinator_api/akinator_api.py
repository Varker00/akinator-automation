from akinator import Akinator, InvalidChoiceError
from pathlib import Path
from datetime import datetime
from enum import Enum
import json


class AkiCategories(Enum):
    CHARACTERS = "c"
    OBJECTS = "o"
    ANIMALS = "a"


class AkinatorGame:
    def __init__(self, category: AkiCategories, answer_func, debug_print=False):
        self.aki = Akinator()
        self.category = category.value
        self.debug_print = debug_print
        self.questions_and_answers = {}
        self.guesses = {}
        self.answer_func = answer_func

    @property
    def aki_response(self):
        return str(self.aki)

    @property
    def game_finished(self):
        return self.aki.finished

    def start_game(self, answer_func=None, debug_print=None):
        if debug_print is not None:
            self.debug_print = debug_print
        if answer_func is not None:
            self.answer_func = answer_func

        self.aki.start_game(language='en', theme=self.category)
        i = 1

        while not self.game_finished:
            akinator_response = self.aki_response
            if self.debug_print:
                print(akinator_response)
            answer = ""
            answer_ok = False

            while not answer_ok:
                try:
                    answer = self.answer_func(answer)
                    self.aki.answer(answer)
                    answer_ok = True
                except InvalidChoiceError as e:
                    print(e)

            if "think of" in akinator_response:
                self.guesses[f"q{i}"] = {
                    "guess": akinator_response,
                    "correct": self.game_finished
                }

            self.questions_and_answers[f"q{i}"] = {
                "question": akinator_response,
                "answer": answer,
            }
            i = i + 1

        if self.debug_print:
            print(self.aki_response)
        self.save_results()

    def save_results(self):
        now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        results_path = Path.cwd() / "results" / f"{now_str}.json"

        try:
            results_path.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f"Permission denied: cannot create directory {results_path.parent}")
            return
        except OSError as e:
            print(f"Failed to create directory {results_path.parent}: {e}")
            return

        results = {
            "akinator_guesses": self.guesses,
            "qna": self.questions_and_answers
        }

        try:
            with open(results_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4)
            print(f"Saved results to {results_path}")
        except PermissionError:
            print(f"Permission denied: cannot write to {results_path}")
        except OSError as e:
            print(f"Failed to write to {results_path}: {e}")
