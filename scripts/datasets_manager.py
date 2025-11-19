
import subprocess
import os

def push_to_repo(df, repo_path, name):
    
    df.to_csv(os.path.join(repo_path, f"{name}.csv"), index=False)

    subprocess.run(["git", "add", "."], cwd=repo_path)

    subprocess.run(["git", "commit", "-m", f"Update {name} cleaned dataset"], cwd=repo_path)
    subprocess.run(["git", "push"], cwd=repo_path)