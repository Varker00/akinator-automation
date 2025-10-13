from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


class AkinatorDriver(webdriver.Chrome):
    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

        super().__init__(options=chrome_options)
        self.get("https://en.akinator.com/")
        self.close_consent()
        self.click_play()

    def close_consent(self):
        try:
            WebDriverWait(self, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "appconsent_noscroll"))
            )

            try:
                iframe = WebDriverWait(self, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='Okno zgody']"))
                )
                self.switch_to.frame(iframe)
            except:
                pass

            skip_button = WebDriverWait(self, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".button__skip"))
            )
            skip_button.click()
        except TimeoutException:
            print("No consent modal displayed, skipping")
        except NoSuchElementException:
            print("No consent modal displayed, skipping")
        finally:
            self.switch_to.default_content()

    def click_play(self):
        play_btn = WebDriverWait(self, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-play > a"))
        )

        play_btn.click()

    def select_category(self, category="Characters"):
        category_btn = WebDriverWait(self, 3).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(@class, 'li-game') and contains(., '{category}')]"))
        )

        category_btn.click()

    def click_answer(self, answer_id="a_dont_know"):
        answer_btn = WebDriverWait(self, 3).until(
            EC.element_to_be_clickable((By.ID, answer_id))
        )

        answer_btn.click()

    def get_question_text(self):
        question_p = WebDriverWait(self, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".question-text"))
        )
        return question_p.text

    def get_proposition(self, timeout=0.5):
        try:
            name_proposition_element = WebDriverWait(self, timeout).until(
                EC.visibility_of_element_located((By.ID, "name_proposition"))
            )
            return name_proposition_element.text if name_proposition_element.is_displayed() else None
        except (NoSuchElementException, TimeoutException):
            return None
