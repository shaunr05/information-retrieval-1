import fetch
import click


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    ctx.ensure_object(dict)
    ctx.obj = {
        'filename': 'jsonDocs/tester.json'
    }

cli.add_command(fetch.fetch)

if __name__ == "__main__":
    cli()