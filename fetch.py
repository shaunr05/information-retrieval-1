import click
import serpapi
import json

@click.group()
@click.pass_context
def fetch(ctx: click.Context):
    pass

fetch: click.Group

@fetch.command()
@click.pass_context
def search(ctx: click.Context):

    client: serpapi.Client = ctx.obj['client']

    results = client.search({
        'engine': 'google_scholar',
        'q': 'coffee',
        'json_restrictor': 'organic_results[].{position, title, link, snippet, publication_info.authors[].{name, link}}'
    })

    results = dict(results)

    with open('tester.json', 'w') as f:
        json.dump(results, f, indent=4)

    click.echo("Saved to file!")
