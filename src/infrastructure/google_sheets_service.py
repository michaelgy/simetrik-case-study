import os
from typing import Optional, List, Dict, Any
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from google.oauth2.service_account import Credentials

class GoogleSheetsService:
    def __init__(self, service_account_file: str, sheet_id: str, worksheet_name: str):
        """
        Initialize the Google Sheets Service
        Args:
            service_account_file: Path to the service account JSON file
            sheet_id: ID of the Google Sheet
            worksheet_name: Name of the worksheet to work with
        """
        self.service_account_file = service_account_file
        self.sheet_id = sheet_id
        self.worksheet_name = worksheet_name
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        self.worksheet = self._initialize_worksheet()
        # Initialize DataFrame from worksheet
        self._df = self._load_dataframe()

    def _initialize_worksheet(self):
        """
        Initialize and return the worksheet
        Returns:
            The worksheet object
        """
        credentials = Credentials.from_service_account_file(
            self.service_account_file,
            scopes=self.scopes
        )
        gc = gspread.authorize(credentials)
        spreadsheet = gc.open_by_key(self.sheet_id)
        return spreadsheet.worksheet(self.worksheet_name)

    def _load_dataframe(self) -> pd.DataFrame:
        """
        Load data from worksheet into DataFrame
        Returns:
            DataFrame containing worksheet data
        """
        return get_as_dataframe(self.worksheet)

    def read_all_data(self) -> pd.DataFrame:
        """
        Read all data from the in-memory DataFrame
        Returns:
            DataFrame containing all worksheet data
        """
        return self._df.copy()

    def add_row(self, row_data: Dict[str, Any]) -> bool:
        """
        Add a new row to the in-memory DataFrame
        Args:
            row_data: Dictionary containing column names and values
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Add new row to DataFrame
            new_df = pd.concat([self._df, pd.DataFrame([row_data])], ignore_index=True)
            self._df = new_df
            return True
        except Exception as e:
            print(f"Error adding row: {e}")
            return False

    def find_row(self, column_name: str, value: Any) -> Optional[pd.DataFrame]:
        """
        Find rows where the specified column matches the given value
        Args:
            column_name: Name of the column to search in
            value: Value to search for
        Returns:
            Optional[DataFrame]: DataFrame containing matching rows, None if not found
        """
        try:
            matches = self._df[self._df[column_name] == value]
            return matches.copy() if not matches.empty else None
        except Exception as e:
            print(f"Error finding row: {e}")
            return None

    def update_row(self, column_name: str, search_value: Any, update_data: Dict[str, Any]) -> bool:
        """
        Update a row that matches the search criteria in the in-memory DataFrame
        Args:
            column_name: Name of the column to search in
            search_value: Value to search for
            update_data: Dictionary containing column names and new values
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Find the row index
            mask = self._df[column_name] == search_value
            if not mask.any():
                print(f"No row found with {column_name} = {search_value}")
                return False
            
            # Update the row in DataFrame
            for col, val in update_data.items():
                self._df.loc[mask, col] = val
            
            return True
        except Exception as e:
            print(f"Error updating row: {e}")
            return False

    def clear_data(self) -> bool:
        """
        Clear all data from the in-memory DataFrame
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._df = pd.DataFrame(columns=self._df.columns)
            return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False

    def save_changes(self) -> bool:
        """
        Save all changes from the in-memory DataFrame to the worksheet
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            set_with_dataframe(self.worksheet, self._df)
            return True
        except Exception as e:
            print(f"Error saving changes to worksheet: {e}")
            return False

    def reload_data(self) -> bool:
        """
        Reload data from the worksheet into the in-memory DataFrame
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._df = self._load_dataframe()
            return True
        except Exception as e:
            print(f"Error reloading data: {e}")
            return False 