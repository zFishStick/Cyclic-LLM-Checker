
from classes.news import News
from classes.prompt import Dataset1Prompt, Dataset2Prompt
import method_checker as mc
import datasets_manager as dm
from classes.chatbot import deepseek

def main():    
    news = dm.get_random_entry_from_first_dataset()
    # news = dm.get_fake_news_from_first_dataset().sample(n=1).iloc[0]
    
    news_instance = News(
        title=news['title'],
        text=news['text'],
        fake=news['is_fake_news']
    )
    
    print("News to check:")
    print(f"Title: {news_instance.title}")
    # print(f"Text: {news_instance.text}")
    print(f"Fake: {news_instance.fake}")
    
    prompt = Dataset1Prompt(news_instance)
    
    method_checker = mc.MethodChecker()
    method_checker.start_method(prompt)
    
if __name__ == "__main__":
    main()