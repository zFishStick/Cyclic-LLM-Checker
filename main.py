
from scripts.classes.news import News
from scripts.classes.prompt import Prompt, Dataset1Prompt, Dataset2Prompt, check_prompt_type
import scripts.method_checker as mc
import scripts.datasets_manager as dm
import scripts.metrics as metrics
import sys

def run_one(dataset: int = 1) -> bool:
    """Run a single method iteration. Return True on success, False if exception raised.
    
    Args:
        dataset: 1 for text-based dataset, 2 for URL-based dataset
    """
    try:
        if dataset == 2:
            news = dm.get_random_entry_from_second_dataset()
            news_instance = News(
                title=news['title'],
                url=news['news_url'],
                fake=news['is_fake_news']
            )
        else:
            news = dm.get_random_entry_from_first_dataset()
            news_instance = News(
                title=news['title'],
                text=news['text'],
                fake=news['is_fake_news']
            )
        
        # Wait a bit between runs to avoid rate limits
        import time
        time.sleep(5) # Sleep 5 seconds between runs
        
        print("Waiting 5 seconds before continuing...")

        print(f"News to check (Dataset {dataset}):")
        print(f"Title: {news_instance.title}")
        print(f"Fake: {news_instance.fake}")
        if dataset == 2:
            print(f"URL: {news_instance.url}")
    
        prompt = check_prompt_type(news_instance)
    
        method_checker = mc.MethodChecker()
        method_checker.start_method(prompt)
        return True
    except Exception as e:
        msg = str(e)
        if "429 RESOURCE_EXHAUSTED" in msg:
            raise
        print(f"[Skip] Error: {msg}")
        return False

def main(runs: int = 50, dataset: int = 1): # Number of runs to perform
    print(f"Starting with Dataset {dataset}\n")
    successes = 0
    attempts = 0
    while successes < runs:
        attempts += 1
        try:
            ok = run_one(dataset=dataset)
        except Exception as e:
            if "429 RESOURCE_EXHAUSTED" in str(e):
                print("[Quota] 429 RESOURCE_EXHAUSTED detected. Stopping runs and showing metrics.")
                break
            else:
                print(f"[Error] Unexpected exception: {e}")
                ok = False
        print("\n-----------------------\n")
        if ok:
            successes += 1
            if successes % 10 == 0:
                print(f"[Progress] {successes}/{runs} successful runs (attempts: {attempts})")
    print(f"Done. Successful runs: {successes}. Attempts (including skips): {attempts}")
    
    # Display evaluation metrics for each chatbot
    metrics.display_metrics()
    

if __name__ == "__main__":
    main()
    