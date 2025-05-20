import pandas as pd
from src.domain.entities import Transaction

class FileIO:
    @staticmethod
    def read_excel(file_path):
        # Read the Excel file and return a list of Transaction objects
        df = pd.read_excel(file_path)
        transactions = []
        for _, row in df.iterrows():
            transaction = Transaction(
                transaction_id=row['N° Movimiento'],
                concepto=row['Concepto'],
                data=row.to_dict()
            )
            transactions.append(transaction)
        return transactions 