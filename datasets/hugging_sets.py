from datasets import load_dataset
from typing import cast

import pandas as pd

ds = load_dataset("Pulk17/Fake-News-Detection-dataset", split="train")
# 0 -> Fake News
# 1 -> Real News

# https://huggingface.co/datasets/Pulk17/Fake-News-Detection-dataset

def explore_dataset():
    df = pd.read_csv("hf://datasets/Pulk17/Fake-News-Detection-dataset/train.tsv", sep="\t")
    print(df.head())
    
explore_dataset()

def retrieve_real_news() -> list[str]:
    real_news = ds.filter(lambda x: x["label"] == 1)
    return cast(list[str], real_news["title"])

def retrieve_fake_news() -> list[str]:
    fake_news = ds.filter(lambda x: x["label"] == 0)
    return cast(list[str], fake_news["title"])

# real_news = retrieve_real_news()
# fake_news = retrieve_fake_news()