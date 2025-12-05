import csv
from pathlib import Path
import glob
from datetime import datetime
import yaml
import json


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
        self, bank: str = None,
        file_starts_with: str = None,
        tx_row_col_count: int = None,
        attrs_mapping: dict = None
    ):
        self.bank: str = bank
        self.file_starts_with: str = file_starts_with
        self.tx_row_col_count: int = tx_row_col_count
        self.attrs_mapping: dict = attrs_mapping
        """Initialize the base parser with common attributes."""
        # self.encoding = "utf-8"
        self.encoding = 'utf-8-sig'
        self.transactions = []
        self.files = self.find_files()
        self.expense_mapper = self.load_expenses_mappers()

    def load_expenses_mappers(self):
        """Load expense mapping from YAML file"""
        # for ease of commenting moved to yaml
        mapping_file = Path(".") / "expense_mapper.yaml"
        if mapping_file.exists():
            with open(mapping_file, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def normalize_date(self, date_str: str):
        """Normalize different date formats to YYYY-MM-DD."""
        for fmt in ('%d-%m-%Y', '%d/%m/%Y', '%d-%b-%y', '%d/%m/%y', '%d/%m/%Y %H:%M:%S'):
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        raise ValueError(f"Unsupported date format: {date_str}")

    def read_csv(self, file_path: str, delimiter: str = ','):
        """Read a CSV file and return its rows."""
        with open(file_path, mode='r', encoding=self.encoding) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=delimiter)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                yield row

    def find_files(self):
        directory = "./data/statement"
        files = list(Path(directory).glob(f"{self.file_starts_with}*.csv"))
        if not files:
            print(f"*** No files found for {self.bank}. itshoud be *.csv sith small case")
        return files

    def write_json(self, filename: str):
        # PosixPath('csv_statements/idfc_17082024.csv')
        # self.filename.name → 'idfc_17082024.csv' (full filename with extension)
        # self.filename.stem → 'idfc_17082024' (filename without extension)
        # self.filename.suffix → '.csv' (just the extension)
        directory = Path("./data/json")
        json_filename = directory / (filename.stem + ".json")
        print(
            f"Processed {json_filename} with {len(self.transactions)}"
            " transactions"
        )
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(
                self.transactions, jsonfile, indent=2, ensure_ascii=False
            )

    def categorize_transactions(self, description: str) -> str:
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
        # In a bank statement, DR (Debit) means money has been deducted
        # or withdrawn from your account, decreasing your balance,
        # while CR (Credit) means money has been added to your account,
        # increasing your balance
        dr_amount = float(row[self.attrs_mapping["dr_amount"]].strip().strip("~").replace(",", "") or 0)
        cr_amount = float(row[self.attrs_mapping["cr_amount"]].strip().strip("~").replace(",", "") or 0)
        expense_type = "expense" if dr_amount > 0 else "deposit"
        # debug print
        # print(f"Row: {row}")
        return {
            "date": self.normalize_date(row[self.attrs_mapping["date"]].strip().strip("~")),
            "description": description,
            "dr_amount": dr_amount,
            "cr_amount": cr_amount,
            "account": self.bank,
            "category": self.categorize_transactions(description),
            "type": expense_type,
        }