import datetime
import click
import os
import json

from euring.config import API_DIR
from euring.codes.fetch import (
    fetch_schemes,
    fetch_species,
    fetch_countries,
    fetch_circumstances,
)
from euring import __version__


@click.group()
@click.option("--verbose", is_flag=True, help="Will print verbose messages.")
@click.pass_context
def euring_cli(ctx, verbose):
    """EURING command Line Interface."""

    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose
    click.echo(
        f"EURING Command Line Tool version {__version__}. Copyright Dylan Verheul 2019."
    )


@euring_cli.command()
@click.pass_context
def update(ctx):
    click.echo("Updating EURING schemes ...")
    data = fetch_schemes()
    write_json_file("ringing_scheme.json", data)
    click.echo("Done.")
    click.echo("Updating EURING species ...")
    data = fetch_species()
    write_json_file("species.json", data)
    click.echo("Done.")
    click.echo("Updating EURING countries ...")
    data = fetch_countries()
    write_json_file("countries.json", data)
    click.echo("Done.")
    click.echo("Updating EURING circumstances ...")
    data = fetch_circumstances()
    write_json_file("circumstances.json", data)
    click.echo("Done.")


def write_json_file(name, data):
    json_file = open(os.path.join(API_DIR, name), "w")
    json.dump(data, json_file, default=json_formatter)


def json_formatter(value):
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
