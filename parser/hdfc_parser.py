"""HDFC bank statement parser."""

import logging
from parser.base import BaseParser

logger = logging.getLogger("munim")


class HdfcParser(BaseParser):
    """Parser for HDFC bank statements."""

    def __init__(self):
        self.bank: str = "Hdfc"
        self.file_starts_with: str = "hdfc_"
        self.tx_row_col_count: int = 7
        self.header_indentifier: str = "Date"
        self.attrs_mapping: dict = {
            "date": 0,
            "description": 1,
            "dr_amount": 3,
            "cr_amount": 4,
        }
        super().__init__(
            bank=self.bank,
            file_starts_with=self.file_starts_with,
            tx_row_col_count=self.tx_row_col_count,
            attrs_mapping=self.attrs_mapping,
        )
        # headers
        # Date,Narration,Value Date,Debit Amount,Credit Amount,Chq/Ref Number,Closing Balance

    def normalize_data(self):
        """Parse HDFC bank statement CSV files."""
        if not self.files:
            logger.warning("No files found for %s", self.bank)
            return
        for file in self.files:
            logger.info("Parsing %s transactions from %s", self.bank, file)
            csv_reader = self.read_csv(file)
            for row in csv_reader:
                if (
                    len(row) < self.tx_row_col_count
                    or row[0].strip() == self.header_indentifier
                ):
                    continue
                self.transactions.append(self.parse(row))
            self.write_json(file)
