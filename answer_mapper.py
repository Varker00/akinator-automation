import string


class AkinatorAnswerMapper:
    AKINATOR_ANSWERS = ["yes", "no", "don't know", "probably", "probably not"]

    # ANSWER_KEYWORDS = {
    #     "a_yes": ["yes", "they are", "yeah", "yep", "affirmative", "correct"],
    #     "a_no": ["no", "not", "nah", "negative", "never"],
    #     "a_dont_know": ["don't know", "idk", "maybe", "not sure", "unsure", "unknown"],
    #     "a_probably": ["probably", "likely", "maybe yes", "most likely"],
    #     "a_probably_not": ["probably not", "unlikely", "maybe no", "doubtful"]
    # }

    ANSWER_KEYWORDS = {
        "a_yes": ["yes"],
        "a_no": ["no"],
        "a_dont_know": ["don't know"],
        "a_probably": ["probably"],
        "a_probably_not": ["probably not"]
    }

    ID_TO_TEXT_MAP = {
        "a_yes": "Yes",
        "a_no": "No",
        "a_dont_know": "Don't know",
        "a_probably": "Probably",
        "a_probably_not": "Probably not",
    }

    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower().strip()
        text = text.translate(str.maketrans("", "", string.punctuation))
        return text

    @classmethod
    def map_response(cls, ai_response: str) -> str:
        text = cls.normalize(ai_response)
        words = text.split()

        for answer, keywords in cls.ANSWER_KEYWORDS.items():
            for keyword in keywords:
                if text == keyword:
                    return answer
                if keyword in words:
                    return answer

        for answer, keywords in cls.ANSWER_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return answer

        return "don't know"

    @classmethod
    def id_to_text(cls, answer_id):
        return cls.ID_TO_TEXT_MAP.get(answer_id, None)
