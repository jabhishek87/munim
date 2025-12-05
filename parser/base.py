"""Base parser module for bank statement parsing."""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path

import yaml

logger = logging.getLogger("munim")


class SingletonMeta(type):
    """A metaclass for singleton pattern implementation."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Ensure only one instance of the class is created."""
        # print(f"Creating instance of {cls}")
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseParser(metaclass=SingletonMeta):
    """Base class for bank statement parsers."""

    def __init__(
        self,
        bank: str = None,
        file_starts_with: str = None,
        tx_row_col_count: int = None,
        attrs_mapping: dict = None,
    ):
        """Initialize the base parser with common attributes."""
        self.bank: str = bank
        self.file_starts_with: str = file_starts_with
        self.tx_row_col_count: int = tx_row_col_count
        self.attrs_mapping: dict = attrs_mapping
        self.encoding = "utf-8-sig"
        self.transactions = []
        self.files = self.find_files()
        self.expense_mapper = self.load_expenses_mappers()

    def load_expenses_mappers(self):
        """Load expense mapping from YAML file."""
        mapping_file = Path(".") / "expense_mapper.yaml"
        if mapping_file.exists():
            with open(mapping_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def normalize_date(self, date_str: str):
        """Normalize different date formats to YYYY-MM-DD."""
        for fmt in (
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%d-%b-%y",
            "%d/%m/%y",
            "%d/%m/%Y %H:%M:%S",
        ):
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        raise ValueError(f"Unsupported date format: {date_str}")

    def read_csv(self, file_path: str, delimiter: str = ","):
        """Read a CSV file and return its rows."""
        with open(file_path, mode="r", encoding=self.encoding) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=delimiter)
            next(csv_reader, None)  # Skip header
            yield from csv_reader

    def find_files(self):
        """Find statement files for the bank."""
        directory = "./data/statement"
        files = list(Path(directory).glob(f"{self.file_starts_with}*.csv"))
        if not files:
            logger.warning("No files found for %s", self.bank)
        return files

    def write_json(self, filename: str):
        """Write transactions to JSON file."""
        directory = Path("./data/json")
        json_filename = directory / (filename.stem + ".json")
        logger.debug(
            "Writing %d transactions to %s", len(self.transactions), json_filename
        )
        with open(json_filename, "w", encoding="utf-8") as jsonfile:
            json.dump(self.transactions, jsonfile, indent=2, ensure_ascii=False)

    def categorize_transactions(self, description: str) -> str:
        """Categorize transaction based on description."""
        ret_category = "uncategorized"
        desc_lower = description.lower()
        for category, keywords in self.expense_mapper.items():
            for keyword in keywords:
                if keyword.lower() in desc_lower:
                    ret_category = category
        return ret_category

    def parse(self, row):
        """Parse a transaction row and return a normalized transaction dict."""
        description = row[self.attrs_mapping["description"]].strip().strip("~")
        dr_amount = float(
            row[self.attrs_mapping["dr_amount"]].strip().strip("~").replace(",", "")
            or 0
        )
        cr_amount = float(
            row[self.attrs_mapping["cr_amount"]].strip().strip("~").replace(",", "")
            or 0
        )
        expense_type = "expense" if dr_amount > 0 else "deposit"
        return {
            "date": self.normalize_date(
                row[self.attrs_mapping["date"]].strip().strip("~")
            ),
            "description": description,
            "dr_amount": dr_amount,
            "cr_amount": cr_amount,
            "account": self.bank,
            "category": self.categorize_transactions(description),
            "type": expense_type,
        }
