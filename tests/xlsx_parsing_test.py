# python -m tests.xlsx_parsing_test


from io import BytesIO
from src.infrastructure.xlsx_parser import XLSXParser

# Path to your local Excel file
file_path_1 = './Transactions_1.xlsx'  # Replace with your actual file path
file_path_2 = './Transactions_2.xlsx'  # Replace with your actual file path

# Read the Excel files into a BytesIO object
df1 = XLSXParser.read_file(file_path_1)
df2 = XLSXParser.read_file(file_path_2)

# Display the results
print("New Transactions (present in file1 but not in file2):")
print(XLSXParser.new_rows(df1, df2, 'N° Movimiento'))
