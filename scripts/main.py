
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

        #news_instance = News(
            #title="Trump Lashes Out At CEOs, Suggests He’ll Replace Them With Ones Who Support His Racism",
            #text="Donald Trump attacked the CEOs who are leaving his Manufacturing Council over his failure to condemn Nazis.In the days since his weak reaction to the violence in Charlottesville, Virginia in which he blamed both sides, three CEOs of major companies did the right thing by calling Trump out and stepping down from the council.Merck CEO Kenneth Frazier was the first to leave the council, drawing an attack from Trump. What made this particular situation worse is that Frazier is black and Trump attacked him just after refusing to condemn white nationalists.Under Armour CEO Kevin Plank was the next to resign, followed by Intel CEO Brian Krzanich.Of course, Trump feels personally insulted because he thinks anyone who works for him or with him should show him complete loyalty, even it that means supporting his racism and hate.And so, Trump accused the three CEOs of  grandstanding  and suggested he will replace them with CEOs who will be blindly loyal.For every CEO that drops out of the Manufacturing Council, I have many to take their place. Grandstanders should not have gone on. JOBS!  Donald J. Trump (@realDonaldTrump) August 15, 2017Trump s accusation of grandstanding was immediately trashed by Twitter users, who noted that Trump wrote the book on it.You are the grandstander, Mr. President. Bragging about your performance instead of condemning white nationalist terrorism.  Adam Best (@adamcbest) August 15, 2017Who will be the replacements? David Duke and his buddies?  Impeach Donald Trump (@Impeach_D_Trump) August 15, 2017Read: I know CEOs who are fine with white supremacy to step in!  Jules Suzdaltsev (@jules_su) August 15, 2017Are you serious? You are the king of grandstanders! You are the mother of all grandstanders! #MOAG You wrote the Manual!  Bishop Talbert Swan (@TalbertSwan) August 15, 2017 I don t care that the popular kids left my birthday party! I have more popular friends! You don t know them! They re from another school!  Jon Bershad (@JonBershad) August 15, 2017why does every tweet sound like its written by a 10yo https://t.co/iR9NouFEe1  Bryson Masse (@Bryson_M) August 15, 2017Trump has been rage tweeting about these CEOs, but has not shown similar anger toward the white nationalists who murdered a woman in Charlottesville. That s truly pathetic and that s why every CEO who is still on Trump s Manufacturing Council should step down as well.Featured Image: Sean Rayford/Getty Images",
            #fake=True
        #)
        print("News to check:")
        print(f"Title: {news_instance.title}")
        print(f"Text: {news_instance.text}")
        print(f"Fake: {news_instance.fake}")
    
        prompt = Dataset1Prompt(news_instance)
    
        method_checker = mc.MethodChecker()
        method_checker.start_method(prompt)
        return True
    except Exception as e:
        msg = str(e)
        if "429 RESOURCE_EXHAUSTED" in msg:
            raise
        print(f"[Skip] Error: {msg}")
        return False

def main(runs: int = 10):
    successes = 0
    attempts = 0
    while successes < runs:
        attempts += 1
        try:
            ok = run_one()
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
    