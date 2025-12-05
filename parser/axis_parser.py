from parser.base import BaseParser


class AxisParser(BaseParser):
    def __init__(self):
        self.bank: str = "Axis"
        self.file_starts_with: str = "axis_"
        self.tx_row_col_count: int = 7
        self.header_indentifier: str = "Tran Date"
        self.attrs_mapping: dict = {
            "date": 0,
            "description": 2,
            "dr_amount": 3,
            "cr_amount": 4,
        }
        super().__init__(
            bank=self.bank,
            file_starts_with=self.file_starts_with,
            tx_row_col_count=self.tx_row_col_count,
            attrs_mapping=self.attrs_mapping
        )
        # headers for axis bank CSV
        # ['Tran Date', 'CHQNO', 'PARTICULARS', 'DR', 'CR', 'BAL', 'SOL']

    def normalize_data(self):
        """Parse Axis bank statement CSV files."""
        if not self.files:
            print(f"*** No files found for {self.bank}.")
            return
        for file in self.files:
            print(f"Parsing {self.bank} transactions from {file}")
            csv_reader = self.read_csv(file)
            for row in csv_reader:
                if len(row) < self.tx_row_col_count or row[0] == self.header_indentifier:
                    # print(f"### Malformed row: {row}")
                    continue
                self.transactions.append(self.parse(row))
            self.write_json(file)