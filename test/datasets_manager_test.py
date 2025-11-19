
from scripts.datasets_manager import push_to_repo

import os
import pandas as pd


def test_push_to_repo():
    url = 'https://raw.githubusercontent.com/zFishStick/LLM-Checker-dataset/refs/heads/main/train.tsv'
    df = pd.read_csv(url, sep='\t')
    
    path = 'C:\\Projects\\Other\\LLM-Checker-dataset\\cleaned_ds'
    name = 'FakeDetectionNews'
    
    assert not df.empty, "DataFrame should not be empty after loading data."
    assert os.path.exists(path), f"Repository path {path} does not exist."
    assert name.strip() != "", "Dataset name should not be empty."
    push_to_repo(df, path, name)