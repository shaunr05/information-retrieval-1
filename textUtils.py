import re
import string

def normalize_text(text: str) -> str:
    text = text.lower()
    title = re.sub(rf"[{string.punctuation}]", "", text)
    title = re.sub(r"\s+", " ", title).strip()
    return title