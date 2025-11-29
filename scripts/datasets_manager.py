
import pandas as pd
import subprocess
import os

def push_to_repo(df, repo_path, name):
    df.to_csv(os.path.join(repo_path, f"{name}.csv"), index=False)
    subprocess.run(["git", "add", "."], cwd=repo_path)
    subprocess.run(["git", "commit", "-m", f"Update {name} cleaned dataset"], cwd=repo_path)
    subprocess.run(["git", "push"], cwd=repo_path)
    
def get_first_dataset() -> pd.DataFrame:
    url = 'https://media.githubusercontent.com/media/zFishStick/LLM-Checker-dataset/refs/heads/main/cleaned_ds/FakeDetectionNews.csv'
    df = pd.read_csv(url, sep=',')
    return df

def get_second_dataset() -> pd.DataFrame:
    url = 'https://raw.githubusercontent.com/zFishStick/LLM-Checker-dataset/refs/heads/main/cleaned_ds/FakeNewsNet.csv'
    df = pd.read_csv(url, sep=',')
    return df

def get_random_entry_from_first_dataset() -> dict:
    df = get_first_dataset()
    random_entry = df.sample(n=1).iloc[0]
    return random_entry.to_dict()


# Debug
def get_fake_news_from_first_dataset() -> pd.DataFrame:
    df = get_first_dataset()
    fake_news_df = df[df['is_fake_news'] == True]
    return fake_news_df