import datetime as dt
import enum
import logging
import operator
import pathlib
import shutil
import zoneinfo

import typer
from rich.progress import track

from enerbitdso import enerbit, formats

logger = logging.getLogger(__name__)

DATE_PARTS_TO_START_DAY = {"hour": 0, "minute": 0, "second": 0, "microsecond": 0}

cli = typer.Typer(pretty_exceptions_show_locals=False)
usages = typer.Typer()
cli.add_typer(usages, name="usages")


class OutputFormat(str, enum.Enum):
    csv = "csv"
    json = "json"
    jsonl = "jsonl"


def yesterday():
    return None


def today():
    return None


@usages.command()
def fetch(
    api_base_url: str = typer.Option(..., envvar="ENERBIT_API_BASE_URL"),
    api_username: str = typer.Option(..., envvar="ENERBIT_API_USERNAME"),
    api_password: str = typer.Option(..., envvar="ENERBIT_API_PASSWORD"),
    since: dt.datetime = typer.Option(
        yesterday,
        formats=["%Y-%m-%d", "%Y%m%d"],
        show_default="yesterday",
    ),
    until: dt.datetime = typer.Option(
        today,
        formats=["%Y-%m-%d", "%Y%m%d"],
        show_default="today",
    ),
    timezone: str = typer.Option("America/Bogota"),
    out_format: OutputFormat = typer.Option(
        "json", help="Output file format", case_sensitive=False
    ),
    frts_file: pathlib.Path = typer.Option(
        None, help="Path file with one frt code per line"
    ),
    out: pathlib.Path = typer.Option("./data", help="Output folder"),
    frts: list[str] = typer.Argument(None, help="List of frt codes separated by ' '"),
):
    ebclient = enerbit.get_client(api_base_url, api_username, api_password)
    TZ_INFO = zoneinfo.ZoneInfo(timezone)
    today = dt.datetime.now(TZ_INFO).replace(**DATE_PARTS_TO_START_DAY)
    if since is None:
        since = today - dt.timedelta(days=1)
    if until is None:
        until = today

    if not operator.xor(frts_file is not None, frts is not None):
        typer.echo("Can't use '--FRTS_FILE' and 'FRTS' on the same call")
        raise typer.Exit(code=1)

    typer.echo(f"Fetching usages for {len(frts)} frts since={since} until={until}")

    if frts_file is not None:
        with open(frts_file, "r") as frts_src:
            frts = frts_src.read().splitlines()

    typer.echo("Total number of meter serials: ")
    for f in track(frts):
        try:
            usage_records = enerbit.get_schedule_usage_records(
                ebclient, f, since=since, until=until
            )
        except Exception:
            typer.echo(f"Failed to fetch usage records for frt code '{f}'")
            continue

        match out_format:
            case OutputFormat.json:
                content = formats.as_json(usage_records)
            case OutputFormat.csv:
                content = formats.as_csv(usage_records)

        f_name = f"{f}_{since}_{until}.{out_format}"

        with open(out / f_name, "w") as dst:
            content.seek(0)
            shutil.copyfileobj(content, dst)


if __name__ == "__main__":
    cli()
