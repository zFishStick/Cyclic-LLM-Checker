from datasets import load_dataset
from typing import cast
import random

ds = load_dataset("Pulk17/Fake-News-Detection-dataset", split="train")

# 0 -> Fake News
# 1 -> Real News

def retrieve_real_news() -> list[str]:
    real_news = ds.filter(lambda x: x["label"] == 1)
    return cast(list[str], real_news["title"])

def retrieve_fake_news() -> list[str]:
    fake_news = ds.filter(lambda x: x["label"] == 0)
    return cast(list[str], fake_news["title"])

real_news = retrieve_real_news()
fake_news = retrieve_fake_news()

def get_random_true_news() -> str:
    index = random.randint(0, len(real_news) - 1)
    return real_news[index]

def get_random_fake_news() -> str:
    index = random.randint(0, len(fake_news) - 1)
    return fake_news[index]