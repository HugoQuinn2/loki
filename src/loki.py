import os

import click
import json as jzon
import csv as czv

from converters.csv_converter import CsvConverter, csv_convert
from converters.json_converter import JsonConversion, json_convert
from utils.file_utils import create_output_file_name

@click.group()
def cli():
    pass

@cli.command(help="Convert file [.csv, .xml & .yaml] to JSON")
@click.argument('input_file', required=False, type=click.Path(exists=True))
@click.option('--type', '-t', 'conversion_type', type=click.Choice([t.value for t in JsonConversion], case_sensitive=False), default=JsonConversion.LIST.value)
@click.option('--output', '-o', help="If the file is exported, define name file.")
@click.option('--export', '-e',is_flag=True, help="If set, exports the JSON to a file instead of printing it.")
def json(input_file: str, conversion_type: str, output: str, export:bool):
    try:
        conversion_type = JsonConversion(conversion_type)
        parse = json_convert(input_file=input_file, conversion_type=conversion_type)

        if export:
            if not output:
                output = create_output_file_name(input_file, '.json')

            with open(output, 'w', encoding='utf-8') as f:
                jzon.dump(parse, f, indent=4, ensure_ascii=False)

            click.echo(click.style(f"[SUCCESS] File conversion successful.", fg='green'))
            click.echo(click.style(f"[INFO] File saved in {output}.", fg='blue'))

        else:
            click.echo(jzon.dumps(parse, indent=4, ensure_ascii=False))

    except Exception as e:
        click.secho(f"[ERROR] {str(e)}", fg='red', err=True)
        raise click.Abort()


@cli.command(help="Convert file [.json, .xml & .yaml] to CSV")
@click.argument('input_file', required=False, type=click.Path(exists=True))
@click.option('--type', '-t', 'conversion_type', type=click.Choice([t.value for t in CsvConverter], case_sensitive=False), default=CsvConverter.LIST.value)
@click.option('--output', '-o', help="If the file is exported, define name file.")
@click.option('--export', '-e',is_flag=True, help="If set, exports the CSV to a file instead of printing it.")
def csv(input_file: str, conversion_type: str, output: str, export:bool):
    try:
        conversion_type = CsvConverter(conversion_type)
        parse = csv_convert(input_file=input_file, conversion_type=conversion_type)

        if export:
            if not output:
                output = create_output_file_name(input_file, '.csv')

            with open(output, mode='w', encoding='utf-8') as f:
                f.write(parse)

            click.echo(click.style(f"[SUCCESS] File conversion successful.", fg='green'))
            click.echo(click.style(f"[INFO] File saved in {output}.", fg='blue'))

        else:
            click.echo(parse)

    except Exception as e:
        click.secho(f"[ERROR] {str(e)}", fg='red', err=True)

if __name__ == "__main__":
    cli()
