import serpapi
import json


def get_search_results(client: serpapi.Client, author: str) -> dict:
    params = {
        'engine': 'google_scholar',
        'q': f'author: {author}',
        'num': 20,
        'json_restrictor': 'organic_results[].{position, title, snippet, publication_info.{summary, authors[].{name, link}}, inline_links.cited_by.total}'
    }

    results = client.search(params)

    results = results.as_dict()

    with open('tester.json', 'w') as f:
        json.dump(results, f, indent=4)

    return results