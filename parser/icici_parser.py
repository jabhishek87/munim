"""ICICI bank statement parser."""

import logging
from parser.base import BaseParser

logger = logging.getLogger("munim")


class IciciParser(BaseParser):
    """Parser for ICICI bank statements."""

    def __init__(self):
        self.bank: str = "Icici"
        self.file_starts_with: str = "icici_"
        self.tx_row_col_count: int = 6
        self.header_indentifier: str = "DATE"
        self.attrs_mapping: dict = {
            "date": 0,
            "description": 2,
            # WITHDRAWALS DR
            "dr_amount": 4,
            # DEPOSITS CR
            "cr_amount": 3,
        }
        super().__init__(
            bank=self.bank,
            file_starts_with=self.file_starts_with,
            tx_row_col_count=self.tx_row_col_count,
            attrs_mapping=self.attrs_mapping,
        )
        # headers
        # DATE,MODE,PARTICULARS,DEPOSITS,WITHDRAWALS,BALANCE

    def normalize_data(self):
        """Parse ICICI bank statement CSV files."""
        for file in self.files:
            logger.info("Parsing %s transactions from %s", self.bank, file)
            csv_reader = self.read_csv(file)
            for row in csv_reader:
                if (
                    len(row) < self.tx_row_col_count
                    or row[0].strip() == self.header_indentifier
                    or row[0].strip() == "ACCOUNT TYPE"
                    or row[0].strip() == "Savings"
                ):
                    continue
                self.transactions.append(self.parse(row))
            self.write_json(file)
