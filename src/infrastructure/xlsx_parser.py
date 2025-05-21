from io import BytesIO
import pandas as pd

class XLSXParser:
    @staticmethod
    def read_file(file: BytesIO) -> pd.DataFrame:
        # Read the Excel file and return a DataFrame
        df = pd.read_excel(file)
        
        return df
    
    @staticmethod
    def new_rows(new_df: pd.DataFrame, current_df: pd.DataFrame, key_column: str) -> pd.DataFrame:
        # Return the rows that are in the new DataFrame but not in the current DataFrame
        return new_df[~new_df[key_column].isin(current_df[key_column])]