class Transaction:
    def __init__(self, transaction_id, concepto, data):
        self.transaction_id = transaction_id
        self.concepto = concepto
        self.data = data


class AgentType:
    REMEDIATION_3C = 'Remediation Agent 3C'
    REMEDIATION_2B = 'Remediation Agent 2B'


class EmailNotification:
    def __init__(self, transaction_id, email):
        self.transaction_id = transaction_id
        self.email = email


class WhatsAppNotification:
    def __init__(self, transaction_id, phone_number):
        self.transaction_id = transaction_id
        self.phone_number = phone_number 