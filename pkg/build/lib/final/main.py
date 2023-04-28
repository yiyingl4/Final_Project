# pylint: disable=E0401
"""main"""
import click
from .works import Works


@click.command
@click.option("--bibtex", is_flag=True, help="Get the Bibtex citation")
@click.option("--ris", is_flag=True, help="Get the RIS citation")
@click.argument("website", nargs=1)
def main(website, bibtex, ris):
    """main"""
    w_work = Works(website)
    if ris:
        w_work.ris()
    if bibtex:
        w_work.bibtex()
