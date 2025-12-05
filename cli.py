"""CLI module for Munim bank statement parser."""

import logging
import sys
from parser.axis_parser import AxisParser
from parser.cc_hdfc_parser import CcHdfcParser
from parser.cc_icici_parser import CcIciciParser
from parser.hdfc_parser import HdfcParser
from parser.icici_parser import IciciParser
from parser.sbi_parser import SbiParser

import click

PARSERS = {
    "hdfc": HdfcParser,
    "icici": IciciParser,
    "sbi": SbiParser,
    "axis": AxisParser,
    "cc_hdfc": CcHdfcParser,
    "cc_icici": CcIciciParser,
}


def setup_logging(verbose, log_file="munim.log"):
    """Setup logging with file and stderr output."""
    log_level = logging.DEBUG if verbose else logging.INFO

    # Create logger
    logger = logging.getLogger("munim")
    logger.setLevel(log_level)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    # Stderr handler (only if verbose)
    if verbose:
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(log_level)
        logger.addHandler(stderr_handler)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


@click.group()
@click.option(
    "--verbose", "-v", is_flag=True, help="Enable verbose output with stderr logging."
)
@click.option("--log-file", default="munim.log", help="Log file path.")
@click.pass_context
def cli(ctx, verbose, log_file):
    """Munim - Bank statement parser and expense categorizer for Indian banks."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["log_file"] = log_file


@cli.command()
@click.argument("bank", type=click.Choice(list(PARSERS.keys()), case_sensitive=False))
@click.pass_context
def parse(ctx, bank):
    """Parse bank statements for a specific bank."""
    verbose = ctx.obj["verbose"]
    log_file = ctx.obj["log_file"]
    logger = setup_logging(verbose, log_file)

    try:
        bank_lower = bank.lower()
        logger.info("Starting parse for bank: %s", bank_lower)

        parser_class = PARSERS[bank_lower]
        parser = parser_class()

        if not parser.files:
            logger.warning("No files found for %s", bank_lower)
            return

        for file_path in parser.files:
            logger.info("Processing file: %s", file_path)
            parser.transactions = []

            for row in parser.read_csv(str(file_path)):
                if len(row) == parser.tx_row_col_count:
                    transaction = parser.parse(row)
                    parser.transactions.append(transaction)

            parser.write_json(file_path)
            logger.info(
                "✅ Parsed %s - %d transactions",
                file_path.name,
                len(parser.transactions),
            )

        logger.info("✅ All files processed for %s", bank)

    except (FileNotFoundError, KeyError, ValueError) as e:
        logger.error("❌ Error during parsing: %s", str(e), exc_info=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def parse_all(ctx):
    """Parse statements for all supported banks."""
    verbose = ctx.obj["verbose"]
    log_file = ctx.obj["log_file"]
    logger = setup_logging(verbose, log_file)

    try:
        logger.info("Starting parse for all banks")

        for bank_name, parser_class in PARSERS.items():
            logger.info("Processing bank: %s", bank_name)
            parser = parser_class()

            if not parser.files:
                logger.warning("No files found for %s", bank_name)
                continue

            for file_path in parser.files:
                logger.info("Processing file: %s", file_path)
                parser.transactions = []

                for row in parser.read_csv(str(file_path)):
                    if len(row) == parser.tx_row_col_count:
                        transaction = parser.parse(row)
                        parser.transactions.append(transaction)

                parser.write_json(file_path)
                logger.info(
                    "✅ Parsed %s - %d transactions",
                    file_path.name,
                    len(parser.transactions),
                )

        logger.info("✅ All banks processed")

    except (FileNotFoundError, KeyError, ValueError) as e:
        logger.error("❌ Error during parsing: %s", str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
