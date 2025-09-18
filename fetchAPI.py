import serpapi
import os

from dotenv import load_dotenv

_client = None

def get_client() -> serpapi.Client:
    global _client
    if _client is None:
        load_dotenv()
        _client = serpapi.Client(api_key=os.getenv(key='API_KEY'))

    return _client


def get_search_results(author: str) -> dict: #TODO: make api backoff and retry functions here
    client = get_client()

    max_results = 20
    all_results = []
    start = 0

    params = {
        'engine': 'google_scholar',
        'q': f'author: {author}',
        'num': 20,
        'json_restrictor': 'organic_results[].{position, title, snippet, publication_info.{summary, authors[].{name, author_id}}, inline_links.cited_by.total}'
    }

    while len(all_results) < max_results:
        params['start'] = start

        results = client.search(params).as_dict()
        organic = results.get('organic_results', [])
        if not organic:
            break

        for article in organic:
            article['position'] += start

        all_results.extend(organic)
        start += 20

    all_results.sort(
        key=lambda x: x.get('inline_links', {}).get('cited_by', {}).get('total', 0),
        reverse=True
    )
    final_results = {
        'organic_results': all_results
    }

    return final_results