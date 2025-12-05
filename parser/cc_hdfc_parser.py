from parser.base import BaseParser


class CcHdfcParser(BaseParser):
    def __init__(self):
        self.bank: str = "Hdfc-CC"
        self.file_starts_with: str = "cc_hdfc_"
        self.tx_row_col_count: int = 7
        self.header_indentifier: str = "Transaction type~"
        self.attrs_mapping: dict = {
            "date": 2,
            "description": 3,
            "dr_amount": 4,
            "cr_amount": 5,
        }
        super().__init__(
            bank=self.bank,
            file_starts_with=self.file_starts_with,
            tx_row_col_count=self.tx_row_col_count,
            attrs_mapping=self.attrs_mapping
        )
        # headers
        # Transaction type~|~Primary / Addon Customer Name~|~DATE~|~Description~|~AMT~|~Debit /Credit~|~Base NeuCoins*

    def normalize_data(self):
        """Parse Axis bank statement CSV files."""
        if not self.files:
            print(f"*** No files found for {self.bank}.")
            return
        for file in self.files:
            print(f"Parsing {self.bank} transactions from {file}")
            csv_reader = self.read_csv(file, "|")
            for row in csv_reader:
                if len(row) != self.tx_row_col_count or row[0].strip() == self.header_indentifier or row[0].strip() == 'Opening NeuCoins with Bank~' or row[0].strip() == '399~':
                    # print(f"### Malformed row: {row}")
                    continue
                # print(len(row), row)
                # special handling for Credit cloumn
                if row[self.attrs_mapping["cr_amount"]].strip().strip("~") != 'Cr':
                    self.transactions.append(self.parse(row))
            self.write_json(file)