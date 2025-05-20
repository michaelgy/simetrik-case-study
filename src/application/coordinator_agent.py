from src.domain.entities import Transaction, AgentType

class CoordinatorAgent:
    def __init__(self, google_sheet_id):
        self.google_sheet_id = google_sheet_id

    def process_transactions(self, transactions):
        for transaction in transactions:
            if self.is_transaction_processed(transaction):
                continue
            if transaction.concepto == 'cobro':
                self.call_agent(transaction, AgentType.REMEDIATION_3C)
            else:
                self.call_agent(transaction, AgentType.REMEDIATION_2B)

    def is_transaction_processed(self, transaction):
        # Logic to check if the transaction is already processed in Google Sheets
        pass

    def call_agent(self, transaction, agent_type):
        # Logic to call the appropriate agent
        pass 