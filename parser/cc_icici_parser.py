"""ICICI credit card statement parser."""

import logging
from parser.base import BaseParser

logger = logging.getLogger("munim")


class CcIciciParser(BaseParser):
    """Parser for ICICI credit card statements."""

    def __init__(self):
        self.bank: str = "Icici-CC"
        self.file_starts_with: str = "cc_icici_"
        self.tx_row_col_count: int = 7
        self.header_indentifier: str = "Date"
        self.attrs_mapping: dict = {
            "date": 0,
            "description": 2,
            # WITHDRAWALS DR
            "dr_amount": 5,
            # DEPOSITS CR
            "cr_amount": 4,
        }
        super().__init__(
            bank=self.bank,
            file_starts_with=self.file_starts_with,
            tx_row_col_count=self.tx_row_col_count,
            attrs_mapping=self.attrs_mapping,
        )
        # headers
        # "Date",
        # "Sr.No.",
        # "Transaction Details",
        # "Reward Point Header",
        # "Intl.Amount",
        # "Amount(in Rs)",
        # "BillingAmountSign"

    def normalize_data(self):
        """Parse ICICI credit card statement CSV files."""
        for file in self.files:
            logger.info("Parsing %s transactions from %s", self.bank, file)
            csv_reader = self.read_csv(file)
            for row in csv_reader:
                if (
                    len(row) < self.tx_row_col_count
                    or row[0].strip() == self.header_indentifier
                ):
                    continue
                dr_amount = float(
                    row[self.attrs_mapping["dr_amount"]].strip().replace(",", "") or 0
                )
                if dr_amount > 0:
                    self.transactions.append(self.parse(row))
            self.write_json(file)
