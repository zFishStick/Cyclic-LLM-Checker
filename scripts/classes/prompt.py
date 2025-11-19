
import scripts.classes.news as news

class Prompt:
    def __init__(self):
        self.input = ""
        self.context = ""
        self.bot_output = ""

class Dataset1Prompt(Prompt):
    def __init__(self, news: news.news):
        super().__init__()
        self.input = (
            f"I read this news: '{news.title}'. "
            f"The description of this article is the following: {news.text} "
            f"Is this true or fake? Explain briefly why."
        )

class Dataset2Prompt(Prompt):
    def __init__(self, news: news.news):
        super().__init__()
        self.input = (
            f"I read this news: '{news.title}'. "
            f"The url of this article is the following: {news.url} "
            f"Is this true or fake? Explain briefly why."
        )
        
        
def check_prompt_type(news: news.news) -> Prompt:
    if news.url:
        return Dataset2Prompt(news)
    elif news.text:
        return Dataset1Prompt(news)
    else:
        return Prompt()

    
        