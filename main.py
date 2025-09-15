import os
import fetch
import click
import serpapi

@click.group()
@click.pass_context
def cli(ctx: click.Context):

    client = serpapi.Client(api_key=os.getenv("API_KEY"))

    ctx.ensure_object(dict)
    ctx.obj = {
        'client': client
    }

cli.add_command(fetch.fetch)

if __name__ == "__main__":
    cli()