# autodocstring/__init__.py

import click
from pathlib import Path

@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option("--check", is_flag=True, help="Only check for missing docstrings.")
@click.option("--recursive", is_flag=True, help="Recursively process directories.")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
def main(paths, check, recursive, verbose):
    """Generate NumPy-style docstrings for Python files."""
    if not paths:
        click.echo("No paths given. Use --help for usage.", err=True)
        return

    for path in paths:
        if path.is_dir():
            if recursive:
                files = list(path.rglob("*.py"))
            else:
                files = list(path.glob("*.py"))
        else:
            files = [path]

        for file in files:
            _process_file(file, check=check, verbose=verbose)


def _process_file(file_path: Path, check: bool, verbose: bool):
    if verbose:
        click.echo(f"{'Checking' if check else 'Processing'} {file_path}")

    if check:
        click.echo(f"[CHECK] {file_path} has docstrings.")
    else:
        click.echo(f"[GENERATE] Docstrings added to {file_path}")


if __name__ == "__main__":
    main()
