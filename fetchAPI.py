import serpapi

def get_search_results(client: serpapi.Client, author: str) -> dict:
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

    final_results = {
        'organic_results': all_results
    }

    return final_results


