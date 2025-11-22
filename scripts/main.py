
from classes.chatbot import Chatbot
from classes.news import News
from classes.prompt import Dataset1Prompt, Dataset2Prompt
import method_checker as mc
import datasets_manager as dm

def main():
    gemini = Chatbot(name="Gemini")
    deepseek = Chatbot(name="Deepseek")
    
    news = dm.get_random_entry_from_first_dataset()
    
    news_instance = News(
        title=news['title'],
        text=news['text'],
        fake=news['is_fake_news']
    )
    
    print("News to check:")
    print(f"Title: {news_instance.title}")
    print(f"Text: {news_instance.text}")
    print(f"Fake: {news_instance.fake}")
    
    prompt = Dataset1Prompt(news_instance)
    
    method_checker = mc.MethodChecker()
    is_true, response_text = method_checker.ask_to_bot(gemini, prompt)
    
    print(f"Gemini response indicates the news is {'True' if is_true else 'Fake'}")
    print(f"Response text: {response_text}")
    
    
    

if __name__ == "__main__":
    main()
    
    