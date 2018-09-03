# coding=utf-8
import click
from pathlib import Path


@click.command()
@click.argument('topic', default=None)
def cli(topic):
    """
    A command line tool for NWPC Cheat Sheet.
    """
    if topic is None:
        click.echo(click.get_current_context().get_help())

    sheets_dir = Path(Path(__file__).parent, './sheets')

    topic_file_path = Path(sheets_dir, topic)
    if topic_file_path.exists():
        with open(topic_file_path, 'r') as topic_file:
            topic_content = topic_file.read()
            print(topic_content)
    else:
        click.echo('Unknown topic.')


if __name__ == "__main__":
    cli()
