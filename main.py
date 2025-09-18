import fetch
import click


@click.group()
def cli():
    pass

# lazy add in command group
cli.add_command(fetch.fetch)

if __name__ == "__main__":
    cli()