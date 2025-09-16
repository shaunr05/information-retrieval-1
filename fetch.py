import os

import click
import serpapi
import json

from fetchAPI import get_search_results
from textUtils import normalize_text


@click.group()
@click.pass_context
def fetch(ctx: click.Context):
    pass

fetch: click.Group

@fetch.command()
@click.argument('author')
@click.pass_context
def search(ctx: click.Context, author: str):

    client: serpapi.Client = ctx.obj['client']

    results = get_search_results(client, author)

    #deduplication
    seen = {}

    for article in results.get('organic_results', []):
        title = article.get('title', '')
        norm_title = normalize_text(title)
        if norm_title not in seen:
            seen[norm_title] = article

    deduplicated_papers = list(seen.values())

    click.echo("Saved to file!")


