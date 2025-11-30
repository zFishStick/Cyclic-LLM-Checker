
class Step:
    def __init__(self):
        self.chatbot_name = ""
        self.step_num = 0
        # New separated evaluations
        # Whether the chatbot evaluates the news as true (True) or fake (False)
        self.step_evaluation_news = None  # type: bool | None
        # Whether the chatbot agrees with the other chatbot's previous output
        self.step_evaluation_chatbot = None  # type: bool | None

    def next_step(self):
        self.step_num += 1

    # Backward-compatibility: old code may call evaluate_step for news judgment
    def evaluate_step(self, evaluation: bool):
        self.step_evaluation_news = evaluation

    # Explicit setters for clarity
    def set_news_evaluation(self, evaluation: bool | None):
        self.step_evaluation_news = evaluation

    def set_chatbot_agreement(self, agreement: bool | None):
        self.step_evaluation_chatbot = agreement