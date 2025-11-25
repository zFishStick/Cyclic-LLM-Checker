
from typing import Tuple
from classes.news import News

class Prompt:
    def __init__(self, news: News, input: str = ""):
        self.input = input
        self.bot_output_text = ""
        self.bot_evaluation = False
        self.response = ""
        self.news = news
        
class Dataset1Prompt(Prompt):
    def __init__(self, news: News):
        super().__init__(news=news)
        self.input = (
            f"I read this news: '{news.title}'. "
            f"The description of this article is the following: {news.text} "
            f"Is this true or fake? Explain briefly and in a human way why."
        ),
        self.response = (
            f"A friend talked me about this news: '{news.title}'  "
            f"with the following description: {news.text}. "
            f"He replied with this statement: '{self.bot_output_text}'. "
            f"Is his statement true or fake? Explain briefly why."
        )

class Dataset2Prompt(Prompt):
    def __init__(self, news: News):
        super().__init__(news=news)
        self.input = (
            f"I read this news: '{news.title}'. "
            f"The url of this article is the following: {news.url} "
            f"Is this true or fake? Explain briefly and in a human way why."
        )
        
        
def check_prompt_type(news: News) -> Prompt:
    if news.url:
        return Dataset2Prompt(news)
    elif news.text:
        return Dataset1Prompt(news)
    else:
        return Prompt(news=news)

    
        