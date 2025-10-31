import random



def get_random_true_news(real_news: list[str]) -> str:
    index = random.randint(0, len(real_news) - 1)
    return real_news[index]

def get_random_fake_news(fake_news: list[str]) -> str:
    index = random.randint(0, len(fake_news) - 1)
    return fake_news[index]