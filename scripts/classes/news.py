
class News:
    def __init__(self, title: str = "", text: str = "", url: str = "", fake: bool = False):
        self.title = title
        self.text = text
        self.url = url
        self.fake = fake
        
    def __str__(self):
        return f"Title: {self.title}\nText: {self.text}\nURL: {self.url}\nFake: {self.fake}"
