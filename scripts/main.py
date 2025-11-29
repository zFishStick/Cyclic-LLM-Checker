
from classes.news import News
from classes.prompt import Dataset1Prompt, Dataset2Prompt
import method_checker as mc
import datasets_manager as dm
import metrics


def run_one() -> bool:
    """Run a single method iteration. Return True on success, False if exception raised."""
    try:
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
        method_checker.start_method(prompt)
        return True
    except Exception as e:
        print(f"[Skip] Error: {e}")
        return False

def main(runs: int = 1):
    successes = 0
    attempts = 0
    while successes < runs:
        attempts += 1
        ok = run_one()
        if ok:
            successes += 1
            if successes % 10 == 0:
                print(f"[Progress] {successes}/{runs} successful runs (attempts: {attempts})")
    print(f"Done. Successful runs: {successes}. Attempts (including skips): {attempts}")
    
    # Display evaluation metrics for each chatbot
    metrics.display_metrics()
    

if __name__ == "__main__":
    main()
    