import pandas as pd

def parse_number(value):
    if isinstance(value, str):
        # Remove thousands separator and replace decimal comma with dot
        value = value.replace('.', '').replace(',', '.')
    try:
        return float(value)
    except ValueError:
        return None 
    
def parse_phone_number(value):
    if isinstance(value, str) and value != '':
        value = value.replace("'", '')
        if not value.startswith('+'):
            value = f"+{value}"
    return value

TransactionsTypes = {
        'Fecha': pd.StringDtype(),
        'Concepto': pd.StringDtype(),
        'N° Movimiento': pd.StringDtype(),
        'Referencia': pd.StringDtype(),
        'Monto': pd.Float64Dtype(),
        'QUERY': pd.StringDtype(),
        'CORREO': pd.StringDtype(),
        'TELEFONO': pd.StringDtype(),
        'REMITENTE': pd.StringDtype(),
        'ESTADO DE REMEDIACION': pd.StringDtype(),
        'EMAIL ID': pd.StringDtype(),
        'WP ID': pd.StringDtype(),
        'ARCHIVO': pd.StringDtype()
    }

TransactionsConverters = {
        'Fecha': str,
        'Concepto': str,
        'N° Movimiento': str,
        'Referencia': str,
        'Monto': parse_number,
        'QUERY': str,
        'CORREO': str,
        'TELEFONO': parse_phone_number,
        'REMITENTE': str,
        'ESTADO DE REMEDIACION': str,
        'EMAIL ID': str,
        'WP ID': str,
        'ARCHIVO': str
    }

TransactionsConvertersPreSave = {
    'TELEFONO': lambda x: f"'{x}" if pd.notnull(x) else x,
}

EmailHistoryTypes = {
    'Fecha': pd.StringDtype(),
    'N° Movimiento': pd.StringDtype(),
    'EMAIL ID': pd.StringDtype(),
    'Mensaje': pd.StringDtype(),
}

EmailHistoryConverters = {
    'Fecha': str,
    'N° Movimiento': str,
    'EMAIL ID': str,
    'Mensaje': str,
}

EmailHistoryConvertersPreSave = {}

WPHistoryTypes = {
    'Fecha': pd.StringDtype(),
    'N° Movimiento': pd.StringDtype(),
    'WP ID': pd.StringDtype(),
    'Mensaje': pd.StringDtype(),
}

WPHistoryConverters = {
    'Fecha': str,
    'N° Movimiento': str,
    'WP ID': str,
    'Mensaje': str,
}

WPHistoryConvertersPreSave = {}

