from scripts.classes import chatbot, news

# Test (run with command "pytest")
def test_methodology():
    gemini = chatbot.chatbot()
    gemini.name = "Gemini"
    
    deep_seek = chatbot.chatbot()
    deep_seek.name = "DeepSeek"
    
    news1 = news.news()
    