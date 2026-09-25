"""
CLI entry point for Offline-First AI Tool.
"""

from pathlib import Path
import typer
from app import process_text_summarization

app = typer.Typer(
    help=" Offline-First Note Summarizer & Key Point Extractor",
    add_completion=False,
)


@app.command()
def summarize(
    file_path: Path = typer.Argument(
        ...,
        help="Path to the text file to summarize",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    remote: bool = typer.Option(
        False,
        "--remote",
        "-r",
        help="Switch to hosted OpenAI API instead of default local model",
    ),
):
    """
    Summarize text notes locally (default) or remotely using the --remote flag.
    """
    try:
        text_content = file_path.read_text(encoding="utf-8").strip()
        if not text_content:
            typer.secho(" Error: File is empty!", fg=typer.colors.YELLOW, bold=True)
            raise typer.Exit(code=1)

        mode_name = "Cloud (OpenAI)" if remote else "Offline Local (Ollama)"
        typer.echo(f"\n Processing using {mode_name} mode...")

        result = process_text_summarization(text_content, use_remote=remote)

        # Output Summary
        typer.secho("\n === Executive Summary ===", fg=typer.colors.GREEN, bold=True)
        typer.echo(result["summary"])

        # Output Benchmark Metrics
        typer.secho("\n === Benchmark Metrics ===", fg=typer.colors.CYAN, bold=True)
        typer.echo(f"• Model Used     : {result['model']}")
        typer.echo(f"• Execution Mode : {result['mode']}")
        typer.echo(f"• Total Latency  : {result['elapsed_time']} seconds")
        typer.echo(f"• Generation Speed: ~{result['tokens_per_sec']} tokens/sec")
        typer.echo("-" * 40 + "\n")

    except Exception as e:
        typer.secho(f"\n Execution Error: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()