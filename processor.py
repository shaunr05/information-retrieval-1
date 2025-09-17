import spacy
import re
import string

from spacy.lang.en.stop_words import STOP_WORDS


def normalize_text(text: str) -> str:
    text = text.lower()
    title = re.sub(rf"[{string.punctuation}]", "", text)
    title = re.sub(r"\s+", " ", title).strip()
    return title

def deduplicate(search_results: dict) -> list:
    # deduplication
    seen = {}

    for article in search_results.get('organic_results', []):
        title = article.get('title', '')
        norm_title = normalize_text(title)
        if norm_title not in seen:
            seen[norm_title] = article

    deduplicated_papers = list(seen.values())
    return deduplicated_papers

def preprocess(deduped_results: list) -> list:

    nlp = spacy.load("en_core_web_sm")

    """processed format: { 
        'id': id,
        'title': title,
        'authors': authors,
        'year': 2025,
        'citations': int,
        'terms': set{}
    }
    """
    processed_docs = []

    for article in deduped_results:
        # combine text and snippet
        body_text = article.get('title', '') + article.get('snippet', '')

        # actual preprocessing; tokenizing, lowercasing, stopword removal, lemmatizing
        doc = nlp(body_text)
        tokens = []
        for token in doc:
            if token.is_alpha:
                lemma = token.lemma_.lower()
                if lemma not in STOP_WORDS:
                    tokens.append(lemma)

        processed_doc = {
            'id': article.get('position'),
            'title': article.get('title'),
            'authors': article.get('publication_info', {}).get('authors', "Unknown"),
            'year': 1, #this will come soon,
            'citations': article.get('inline_links', {}).get('cited_by', {}).get('total', 0),
            'terms': set(tokens)
        }

        processed_docs.append(processed_doc)
        return processed_docs