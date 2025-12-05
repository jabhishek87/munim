from parser.base import BaseParser


class SbiParser(BaseParser):
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
            attrs_mapping=self.attrs_mapping
        )
        # headers for axis bank CSV
        # [Txn Date, Value Date, Description, Ref No./Cheque No.,Debit,Credit, Balance]

    def normalize_data(self):
        """Parse Axis bank statement CSV files."""
        if not self.files:
            print(f"*** No files found for {self.bank}.")
            return
        for file in self.files:
            print(f"Parsing {self.bank} transactions from {file}")
            csv_reader = self.read_csv(file)
            for row in csv_reader:
                if row[len(row)-1].strip() == '' or row[0] == self.header_indentifier:
                    # print(f"### Malformed row: {row}")
                    continue
                # print(len(row), row)
                self.transactions.append(self.parse(row))
            self.write_json(file)