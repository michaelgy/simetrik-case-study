from typing import Optional, Dict, Any
import pandas as pd
from ..google_sheets_service import GoogleSheetsService

class TransactionsWorksheet:
    # Default column definitions
    COLUMNS = [
        'Fecha', 'Concepto', 'N° Movimiento', 'Referencia', 'Monto',
        'QUERY', 'CORREO', 'TELEFONO', 'REMITENTE', 'ESTADO DE REMEDIACION',
        'EMAIL ID', 'WP ID', 'ARCHIVO'
    ]

    def __init__(self, service: GoogleSheetsService):
        """
        Initialize the Transactions Worksheet handler
        Args:
            service: GoogleSheetsService instance for the worksheet
        """
        self.service = service
        self._initialize_columns()

    def _initialize_columns(self):
        """Initialize worksheet with default columns if empty"""
        if self.service.read_all_data().empty:
            self.service._df = pd.DataFrame(columns=self.COLUMNS)
            self.service.save_changes()

    def read_all(self) -> pd.DataFrame:
        """Read all data from the worksheet"""
        return self.service.read_all_data()

    def add(self, transaction_data: Dict[str, Any]) -> bool:
        """Add a new transaction"""
        return self.service.add_row(transaction_data)

    def find(self, column_name: str, value: Any) -> Optional[pd.DataFrame]:
        """Find transactions matching the search criteria"""
        return self.service.find_row(column_name, value)
    
    def find_transaction(self, movement_number: str) -> Optional[pd.DataFrame]:
        """Find and return a transaction by its N° Movimiento."""
        return self.find('N° Movimiento', movement_number)

    def update(self, column_name: str, search_value: Any, update_data: Dict[str, Any]) -> bool:
        """Update a transaction"""
        return self.service.update_row(column_name, search_value, update_data)

    def update_state(self, movement_number: str, new_state: str) -> bool:
        """
        Update the 'ESTADO DE REMEDIACION' of a transaction
        Args:
            movement_number: The N° Movimiento to find the transaction
            new_state: The new state to set
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            transaction = self.find('N° Movimiento', movement_number)
            if transaction is None or transaction.empty:
                print(f"No transaction found with N° Movimiento: {movement_number}")
                return False

            update_data = {'ESTADO DE REMEDIACION': new_state}
            return self.update('N° Movimiento', movement_number, update_data)
        except Exception as e:
            print(f"Error updating transaction state: {e}")
            return False

    def clear(self) -> bool:
        """Clear all data from the worksheet"""
        return self.service.clear_data()

    def save_changes(self) -> bool:
        """Save changes to the worksheet"""
        return self.service.save_changes()

    def reload_data(self) -> bool:
        """Reload data from the worksheet"""
        return self.service.reload_data() 