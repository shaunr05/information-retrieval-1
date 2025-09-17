import os
import fetch
import click
import serpapi
from dotenv import load_dotenv

@click.group()
@click.pass_context
def cli(ctx: click.Context):

    load_dotenv()
    client = serpapi.Client(api_key=os.getenv(key='API_KEY'))

    ctx.ensure_object(dict)
    ctx.obj = {
        'client': client,
        'filename': 'jsonDocs/tester.json'
    }

cli.add_command(fetch.fetch)

if __name__ == "__main__":
    cli()