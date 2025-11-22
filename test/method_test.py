from scripts.classes import Chatbot, News

# Test (run with command "pytest")
def test_methodology():
    gemini = Chatbot(
        name="Gemini"
    )
    
    deep_seek = Chatbot(
        name="DeepSeek"
    )
    
    news1 = News()
    