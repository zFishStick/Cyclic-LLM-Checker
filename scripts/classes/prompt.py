
from scripts.classes import news

class prompt:
    def __init__(self):
        self.input = ""
        self.bot_output = ""
        self.real_output = news.news()