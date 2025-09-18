import click

from fetchAPI import *
from result import *
from utils.fileUtils import write_to_json
from retrieval.preprocessor import *


@click.group()
@click.pass_context
def fetch(ctx: click.Context):
    pass

fetch: click.Group

@fetch.command()
@click.argument('author')
@click.option('-d', '--debug', is_flag=True)
def search(author: str, debug): #TODO: move the logic to another file

    results = get_search_results(author)
    deduped_results = deduplicate(results)
    processed_docs = preprocess(deduped_results)

    if debug:
        write_to_json(results, 'jsonDocs/tester.json')
        write_to_json(deduped_results, 'jsonDocs/dedup.json')
        write_to_json(processed_docs, 'jsonDocs/processed.json')
        click.echo("Saved to file!")


    matrix, vocab, term_to_row, doc_to_col = build_incidence_matrix(processed_docs)
    click.echo("Processing done!")

    query = input("Enter query: ")
    matching = retrieve_docs(query, processed_docs, matrix, term_to_row)

    save_to_csv("results.csv", matching)
    click.echo(f"Saved {len(matching)} matching docs to results.csv")