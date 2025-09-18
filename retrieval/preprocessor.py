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
            'authors': get_author(article.get('publication_info', {})),
            'year': get_year(article.get('publication_info', {}).get('summary', ''), article.get('title')),
            'citations': article.get('inline_links', {}).get('cited_by', {}).get('total', 0),
            'terms': set(tokens)
        }

        processed_docs.append(processed_doc)

    return processed_docs

def preprocess_query(query: str) -> str:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(query)
    processed_tokens = []
    for token in doc:
        if token.is_alpha:
            lemma = token.lemma_.lower()
            if lemma not in STOP_WORDS:
                processed_tokens.append(lemma)
            else:
                processed_tokens.append(token.text.lower())  # keep stopwords in lowercase
    return " ".join(processed_tokens)


def get_year(summary: str, title: str) -> int:

    year = extract_year(summary)
    if year is None:
        year = extract_year(title)

    return year if year is not None else 2025


def extract_year(string: str) -> int | None:
    years = re.findall(r"\b(19|20)\d{2}\b", string)
    if not years:
        return None
    # re.findall returns only the prefix (19|20), so we need full matches:
    years = re.findall(r"\b(?:19|20)\d{2}\b", string)
    return max(map(int, years)) if years else None


def get_author(publication_info: dict) -> str:
    authors: list = publication_info.get('authors', [])
    summary: str = publication_info.get('summary', '')

    final_authors_str = ""

    if not authors and not summary:
        return "Unknown"

    if authors:
        authors_list = [author.get('name', '') for author in authors]
        final_authors_str = join_authors_list(authors_list)

    if final_authors_str == "":
        authors_com = summary.split(' - ')[0].strip()
        authors_list_sum = [a.strip() for a in authors_com.split(",") if a.strip() != ""]
        final_authors_str = join_authors_list(authors_list_sum)

    return final_authors_str


def join_authors_list(authors_list: list) -> str:
    return ", ".join(authors_list)

