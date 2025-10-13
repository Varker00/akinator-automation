from selenium import webdriver
from pathlib import Path
import random
import time
from datetime import datetime
import json
from answer_mapper import AkinatorAnswerMapper


class Player:
    def __init__(self, driver: webdriver):
        self.driver = driver
        self.questions_and_answers = {}

    def get_question(self):
        return self.driver.get_question_text()

    def select_answer(self, question):
        choice = random.choice(["yes", "no", "don't know", "probably", "probably not"])
        answer_id = AkinatorAnswerMapper.map_response(
            choice
        )
        self.driver.click_answer(answer_id)
        return AkinatorAnswerMapper.id_to_text(answer_id)

    def play_game(self):
        question = self.get_question()
        answer = self.select_answer(question)
        self.questions_and_answers[f"q{len(self.questions_and_answers) + 1}"] = {
            "question": question,
            "answer": answer
        }

    def akinators_guess(self):
        return self.driver.get_proposition()

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
            "guess": self.akinators_guess(),
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

    def play_until_the_end(self):
        while True:
            time.sleep(0.5)
            if self.akinators_guess():
                break
            self.play_game()

        print("Game over!")

        self.save_results()

        return self.akinators_guess()
