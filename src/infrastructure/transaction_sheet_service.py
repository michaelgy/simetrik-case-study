import os
from typing import Optional, Dict, Any
import pandas as pd
from .google_sheets_service import GoogleSheetsService
from .worksheets.transactions_worksheet import TransactionsWorksheet
from .worksheets.email_history_worksheet import EmailHistoryWorksheet
from .worksheets.whatsapp_history_worksheet import WhatsAppHistoryWorksheet
from .worksheets.states_worksheet import StatesWorksheet
from src.domain.types import TransactionsConverters, TransactionsTypes, TransactionsConvertersPreSave, EmailHistoryConverters, EmailHistoryConvertersPreSave,EmailHistoryTypes, WPHistoryTypes, WPHistoryConverters, WPHistoryConvertersPreSave
import logging


class TransactionSheetService:
    # Default column definitions
    CONVERTERS = TransactionsConverters.copy()
    TYPES = TransactionsTypes.copy()
    CONVERTERS_PRE_SAVE = TransactionsConvertersPreSave.copy()
    
    EMAILHISTORY_CONVERTERS = EmailHistoryConverters
    EMAILHISTORY_TYPES = EmailHistoryTypes
    EMAILHISTORY_CONVERTERS_PRE_SAVE = EmailHistoryConvertersPreSave
    
    WP_CONVERTERS = WPHistoryConverters
    WP_TYPES = WPHistoryTypes
    WP_CONVERTERS_PRE_SAVE = WPHistoryConvertersPreSave

    # Constants
    DATE_FORMAT = '%d/%m/%Y %H:%M:%S'

    def __init__(self, service_account_file: str, sheet_id: str):
        """
        Initialize the Transaction Sheet Service with multiple worksheets
        Args:
            service_account_file: Path to the service account JSON file
            sheet_id: ID of the Google Sheet
        """
        self.service_account_file = service_account_file
        self.sheet_id = sheet_id
        
        # Initialize services for each worksheet
        self.transactions = TransactionsWorksheet(
            GoogleSheetsService(
                service_account_file=service_account_file,
                sheet_id=sheet_id,
                worksheet_name='Transacciones',
                converters=self.CONVERTERS,
                types=self.TYPES,
                converters_pre_save=self.CONVERTERS_PRE_SAVE
            )
        )
        
        self.email_history = EmailHistoryWorksheet(
            GoogleSheetsService(
                service_account_file=service_account_file,
                sheet_id=sheet_id,
                worksheet_name='Historial_Correos',
                converters=self.EMAILHISTORY_CONVERTERS,
                types=self.EMAILHISTORY_TYPES,
                converters_pre_save=self.EMAILHISTORY_CONVERTERS_PRE_SAVE
            )
        )
        
        self.whatsapp_history = WhatsAppHistoryWorksheet(
            GoogleSheetsService(
                service_account_file=service_account_file,
                sheet_id=sheet_id,
                worksheet_name='Historial_WP',
                converters=self.WP_CONVERTERS,
                types=self.WP_TYPES,
                converters_pre_save=self.WP_CONVERTERS_PRE_SAVE
            )
        )
        
        self.states = StatesWorksheet(
            GoogleSheetsService(
                service_account_file=service_account_file,
                sheet_id=sheet_id,
                worksheet_name='Estados'
            )
        )

    def add_email_message(self, email_id: str, message: str) -> bool:
        """
        Add a new message to the email history
        Args:
            email_id: The EMAIL ID to find the transaction
            message: The message to add
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Find the transaction by EMAIL ID
            transaction = self.transactions.find('EMAIL ID', email_id)
            if transaction is None or transaction.empty:
                logging.warning(f"No transaction found with EMAIL ID: {email_id}")
                return False

            # Get the movement number
            movement_number = transaction.iloc[0]['N° Movimiento']

            # Add the message
            return self.email_history.add_message(email_id, message, movement_number)
        except Exception as e:
            logging.error(f"Error adding email message: {e}")
            return False

    def add_whatsapp_message(self, wp_id: str, message: str) -> bool:
        """
        Add a new message to the WhatsApp history
        Args:
            wp_id: The WP ID to find the transaction
            message: The message to add
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Find the transaction by WP ID
            transaction = self.transactions.find('WP ID', wp_id)
            if transaction is None or transaction.empty:
                logging.warning(f"No transaction found with WP ID: {wp_id}")
                return False

            # Get the movement number
            movement_number = transaction.iloc[0]['N° Movimiento']

            # Add the message
            return self.whatsapp_history.add_message(wp_id, message, movement_number)
        except Exception as e:
            logging.error(f"Error adding WhatsApp message: {e}")
            return False

    def save_all_changes(self) -> bool:
        """
        Save all changes from all worksheets
        Returns:
            bool: True if all saves were successful, False otherwise
        """
        try:
            transactions_saved = self.transactions.save_changes()
            email_history_saved = self.email_history.save_changes()
            whatsapp_history_saved = self.whatsapp_history.save_changes()
            states_saved = self.states.save_changes()
            
            return all([
                transactions_saved,
                email_history_saved,
                whatsapp_history_saved,
                states_saved
            ])
        except Exception as e:
            logging.error(f"Error saving changes: {e}")
            return False

    def reload_all_data(self) -> bool:
        """
        Reload all data from all worksheets
        Returns:
            bool: True if all reloads were successful, False otherwise
        """
        try:
            transactions_reloaded = self.transactions.reload_data()
            email_history_reloaded = self.email_history.reload_data()
            whatsapp_history_reloaded = self.whatsapp_history.reload_data()
            states_reloaded = self.states.reload_data()
            
            return all([
                transactions_reloaded,
                email_history_reloaded,
                whatsapp_history_reloaded,
                states_reloaded
            ])
        except Exception as e:
            logging.error(f"Error reloading data: {e}")
            return False
