import chatbot, dataset

def is_true_or_fake(response: str) -> str:
    if "true" in response.lower():
        return "true"
    elif "fake" in response.lower():
        return "fake"
    else:
        return "unknown"

def main() -> None:
    news = dataset.get_random_fake_news()
    print(f"Random News Title: {news}")

    response = chatbot.chat_with_gemini(news)
    print(f"Gemini Response: {response}")

    truth_value = is_true_or_fake(response)
    print(f"Truth Value: {truth_value}")
    
    deepseek_response = chatbot.chat_with_deepseek(news, truth_value)
    print(f"DeepSeek Response: {deepseek_response}")

main()

