from typing import Optional, Dict, Any
import pandas as pd
from ..google_sheets_service import GoogleSheetsService

class StatesWorksheet:
    # Default column definitions
    COLUMNS = [
        'Estado', 'Descripción'
    ]

    # Possible transaction states
    NO_PROCESADO = 'No Procesado'
    EN_PROCESO = 'En Proceso'
    RESPUESTA_INVALIDA_1 = 'Respuesta Invalida 1'
    RESPUESTA_INVALIDA_2 = 'Respuesta Invalida 2'
    PROCESAMIENTO_MANUAL = 'Procesamiento Manual'
    COMPLETADO = 'Completado'

    def __init__(self, service: GoogleSheetsService):
        """
        Initialize the States Worksheet handler
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

    def add(self, state_data: Dict[str, Any]) -> bool:
        """Add a new state"""
        return self.service.add_row(state_data)

    def find(self, column_name: str, value: Any) -> Optional[pd.DataFrame]:
        """Find states matching the search criteria"""
        return self.service.find_row(column_name, value)

    def update(self, column_name: str, search_value: Any, update_data: Dict[str, Any]) -> bool:
        """Update a state"""
        return self.service.update_row(column_name, search_value, update_data)

    def clear(self) -> bool:
        """Clear all data from the worksheet"""
        return self.service.clear_data()

    def save_changes(self) -> bool:
        """Save changes to the worksheet"""
        return self.service.save_changes()

    def reload_data(self) -> bool:
        """Reload data from the worksheet"""
        return self.service.reload_data() 