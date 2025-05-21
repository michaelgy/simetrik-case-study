from typing import Optional, Dict, Any
import pandas as pd
from datetime import datetime
from ..google_sheets_service import GoogleSheetsService

class WhatsAppHistoryWorksheet:
    # Default column definitions
    COLUMNS = [
        'Fecha', 'N° Movimiento', 'WP ID', 'Mensaje'
    ]

    # Constants
    DATE_FORMAT = '%d/%m/%Y %H:%M:%S'

    def __init__(self, service: GoogleSheetsService):
        """
        Initialize the WhatsApp History Worksheet handler
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

    def add(self, whatsapp_data: Dict[str, Any]) -> bool:
        """Add a new WhatsApp record"""
        return self.service.add_row(whatsapp_data)

    def find(self, column_name: str, value: Any) -> Optional[pd.DataFrame]:
        """Find WhatsApp records matching the search criteria"""
        return self.service.find_row(column_name, value)

    def update(self, column_name: str, search_value: Any, update_data: Dict[str, Any]) -> bool:
        """Update a WhatsApp record"""
        return self.service.update_row(column_name, search_value, update_data)

    def add_message(self, wp_id: str, message: str, movement_number: int) -> bool:
        """
        Add a new message to the WhatsApp history
        Args:
            wp_id: The WP ID
            message: The message to add
            movement_number: The N° Movimiento to link the message
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            whatsapp_data = {
                'Fecha': datetime.now().strftime(self.DATE_FORMAT),
                'N° Movimiento': movement_number,
                'WP ID': wp_id,
                'Mensaje': message
            }
            return self.add(whatsapp_data)
        except Exception as e:
            print(f"Error adding WhatsApp message: {e}")
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