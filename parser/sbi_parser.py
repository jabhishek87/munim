"""SBI bank statement parser."""

import logging
from parser.base import BaseParser

logger = logging.getLogger("munim")


class SbiParser(BaseParser):
    """Parser for SBI bank statements."""

    def __init__(self):
        self.bank: str = "Sbi"
        self.file_starts_with: str = "sbi_"
        self.tx_row_col_count: int = 7
        self.header_indentifier: str = "Txn Date"
        self.attrs_mapping: dict = {
            "date": 0,
            "description": 2,
            "dr_amount": 4,
            "cr_amount": 5,
        }
        super().__init__(
            bank=self.bank,
            file_starts_with=self.file_starts_with,
            tx_row_col_count=self.tx_row_col_count,
            attrs_mapping=self.attrs_mapping,
        )
        # headers for axis bank CSV
        # [Txn Date, Value Date, Description, Ref No./Cheque No.,Debit,Credit, Balance]

    def normalize_data(self):
        """Parse SBI bank statement CSV files."""
        if not self.files:
            logger.warning("No files found for %s", self.bank)
            return
        for file in self.files:
            logger.info("Parsing %s transactions from %s", self.bank, file)
            csv_reader = self.read_csv(file)
            for row in csv_reader:
                if row[len(row) - 1].strip() == "" or row[0] == self.header_indentifier:
                    continue
                self.transactions.append(self.parse(row))
            self.write_json(file)
