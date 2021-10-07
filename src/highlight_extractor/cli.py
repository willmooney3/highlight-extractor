from glob import iglob
import os

from .db import SQLiteDatabaseManager
from .libs.highlights import KoboElipsaHighlightExtractor

import click


@click.group()
@click.option("--directory", help="The directory containing annotated PDFs")
@click.pass_context
def main(context, directory: str):
    """Main launcher function for the CLI.

    Args:
        context (): The context for the command
    """
    db_manager = SQLiteDatabaseManager()
    db_manager.create_database()
    for pdf in iglob(os.path.join(directory, "*.pdf")):
        pdf_annotations = KoboElipsaHighlightExtractor(pdf)
        for annotation in pdf_annotations:
            db_manager.add_highlight(
                pdf,
                annotation["pageNumber"],
                annotation["imgPath"],
                annotation["content"],
            )


def start():
    main(obj={})
