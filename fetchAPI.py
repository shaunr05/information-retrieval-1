import os
import sys
import time
import re
import serpapi

from dotenv import load_dotenv
from serpapi import HTTPError

_client = None

def get_client() -> serpapi.Client:
    global _client
    if _client is None:
        load_dotenv()
        _client = serpapi.Client(api_key=os.getenv(key='API_KEY'))

    return _client


def get_search_results(author: str) -> dict:
    client = get_client()

    max_results = 100
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
        results = safe_search(client, params)
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


def safe_search(client: serpapi.Client, params: dict) -> dict:
    max_retries = 5
    backoff = 1

    for attempt in range(max_retries):
        try:
            results = client.search(params)
            return results

        except serpapi.HTTPError as e:
            if "429" in str(e):
                print(f"Search failed due to too many requests. Retrying in {backoff} seconds.")
                time.sleep(backoff)
                backoff *= 2

            elif "401" in str(e):
                print("API key is not provided.")
                sys.exit(1)

            elif re.search(r"\b(5\d{2})\b", str(e)): # for 500/503 error codes
                print("SerpAPI servers are not responding. Please try again later.")
                sys.exit(1)


    else:
        raise Exception(f"Failed to get results after {max_retries} retries")