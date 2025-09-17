import click

from fetchAPI import *
from utils.fileUtils import write_to_json
from processor import *


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
    write_to_json(results, ctx.obj['filename'])

    deduped_results = deduplicate(results)
    write_to_json(deduped_results, 'jsonDocs/dedup.json')

    processed_docs = preprocess(deduped_results)
    write_to_json(processed_docs, 'jsonDocs/processed.json')

    click.echo("processing done!")
    click.echo("Saved to file!")


