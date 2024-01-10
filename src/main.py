import typer
from typing_extensions import Annotated

from quartz import Quartz

app = typer.Typer()


@app.command()
def playlist(
    url: str,
    out_dir: Annotated[
        str, typer.Option(help='Directory to download files to')
    ] = './out/',
):
    quartz = Quartz(out_dir)
    quartz.process_playlist(url)


@app.command()
def song(
    url: str,
    out_dir: Annotated[
        str, typer.Option(help='Directory to download file to')
    ] = './out/',
):
    quartz = Quartz(out_dir)
    quartz.process_song(url)


if __name__ == '__main__':
    app()
