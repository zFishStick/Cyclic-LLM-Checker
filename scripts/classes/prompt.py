
from classes.news import News

class Prompt:
    def __init__(self, input: str = "", context: str = "", bot_output: str = ""):
        self.input = ""
        self.context = ""
        self.bot_output = ""

class Dataset1Prompt(Prompt):
    def __init__(self, news: News):
        super().__init__()
        self.input = (
            f"I read this news: '{news.title}'. "
            f"The description of this article is the following: {news.text} "
            f"Is this true or fake? Explain briefly why."
        )

class Dataset2Prompt(Prompt):
    def __init__(self, news: News):
        super().__init__()
        self.input = (
            f"I read this news: '{news.title}'. "
            f"The url of this article is the following: {news.url} "
            f"Is this true or fake? Explain briefly why."
        )
        
        
def check_prompt_type(news: News) -> Prompt:
    if news.url:
        return Dataset2Prompt(news)
    elif news.text:
        return Dataset1Prompt(news)
    else:
        return Prompt()

    
        