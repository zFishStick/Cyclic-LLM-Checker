
import json
import re

def evaluate_response(response: str) -> bool:

    if not response:
        raise ValueError("Empty response received")

    text = response.strip()

    json_pattern = r"```(?:json)?\s*(.*?)\s*```"
    match = re.search(json_pattern, text, re.DOTALL)
    
    json_str = match.group(1) if match else text

    try:
        data = json.loads(json_str)
        
        if isinstance(data, dict):
            val = data.get("classification") or data.get("agreement") or data.get("label")
            
            # Se il valore è già booleano
            if isinstance(val, bool):
                return val
            
            # Se il valore è stringa
            if isinstance(val, str):
                val_lower = val.lower().strip()
                if val_lower in ["true", "real", "accept", "yes"]:
                    return True
                if val_lower in ["false", "fake", "reject", "no"]:
                    return False
                    
    except (json.JSONDecodeError, TypeError):
        pass
    
    clean_text = text.lower().replace("```json", "").replace("```", "").strip()
    
    first_line = clean_text.splitlines()[0] if clean_text else ""
    
    first_word = re.sub(r'[^\w\s]', '', first_line).strip()

    if first_word.startswith(("true", "real", "accept")):
        return True
    if first_word.startswith(("false", "fake", "reject")):
        return False

    raise ValueError(f"Response could not be evaluated. Preview: {text[:50]}...")


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def text_similarity(a: str, b: str) -> float:
    vec = TfidfVectorizer().fit_transform([a, b])
    return cosine_similarity(vec[0:1], vec[1:2])[0][0] # type: ignore
