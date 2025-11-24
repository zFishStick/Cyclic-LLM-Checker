

def evaluate_response(response: str) -> bool:
    text = response.strip().lower()

    if text.startswith("true") or text.startswith("real"):
        return True

    if text.startswith("false") or text.startswith("fake"):
        return False
    
    raise ValueError("Response could not be evaluated as True or Fake. Response: " + response)