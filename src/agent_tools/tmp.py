# Mock implementation of Google Sheets service.
class GoogleSheetsService:
    def __init__(self, sheet_id: str):
        self.sheet_id = sheet_id
        # Using an in-memory list to simulate Google Sheet data (including header row).
        self.data = [
            ["N° Movimiento", "Date", "Amount", "Description", "EMAIL ID", "WP ID", "ESTADO DE REMEDIACION"],
            ["1001", "2025-01-01", 100.0, "Payment from client A", "email-123", "wp-456", "Pending"],
            ["1002", "2025-01-02", 250.5, "Refund to client B", "email-789", "", "Completed"],
            ["1003", "2025-01-03", 75.0, "Chargeback from client C", "", "wp-999", "In Progress"]
        ]
    
    def read_sheet(self):
        """Simulate reading all rows from the Google Sheet (excluding header)."""
        return [row.copy() for row in self.data[1:]]  # skip header row
    
    def append_row(self, row):
        """Simulate appending a new row to the Google Sheet."""
        self.data.append(row.copy())
    
    def update_row(self, row_index, new_row):
        """Simulate updating a row at the given index (1-indexed for data rows)."""
        if 1 <= row_index < len(self.data):
            self.data[row_index] = new_row.copy()
            return True
        return False

# TransactionsWorksheet wraps the GoogleSheetsService and provides transaction operations.
class TransactionsWorksheet:
    def __init__(self, sheet_service: GoogleSheetsService):
        self.sheet_service = sheet_service
        raw_data = self.sheet_service.read_sheet()  # read initial data
        header = ["N° Movimiento", "Date", "Amount", "Description", "EMAIL ID", "WP ID", "ESTADO DE REMEDIACION"]
        # Convert each row (list) into a dict for easier handling.
        self.transactions = [dict(zip(header, row)) for row in raw_data]
    
    def get_all_transactions(self):
        """Return all transactions as a list of dicts."""
        return self.transactions
    
    def find_transaction(self, movement_number: str):
        """Find a transaction by 'N° Movimiento'. Return the transaction dict if found, else None."""
        for tx in self.transactions:
            if tx.get("N° Movimiento") == movement_number:
                return tx
        return None
    
    def add_transaction(self, transaction: dict):
        """Add a new transaction (provided as a dict) to the sheet and local store."""
        self.transactions.append(transaction)
        # Append to Google Sheet (simulate persistent storage)
        row = [
            transaction.get("N° Movimiento"), transaction.get("Date"), transaction.get("Amount"),
            transaction.get("Description"), transaction.get("EMAIL ID"), transaction.get("WP ID"),
            transaction.get("ESTADO DE REMEDIACION")
        ]
        self.sheet_service.append_row(row)
        return True
    
    def update_transaction(self, movement_number: str, updates: dict):
        """Update fields of a transaction identified by 'N° Movimiento'. Updates is a dict of fields to change."""
        for idx, tx in enumerate(self.transactions):
            if tx.get("N° Movimiento") == movement_number:
                # Apply updates to local record
                for key, value in updates.items():
                    tx[key] = value
                # Reflect changes in the Google Sheet (if this were a real sheet, use API call)
                row_index = idx + 1  # account for header row at index 0
                new_row = [
                    tx.get("N° Movimiento"), tx.get("Date"), tx.get("Amount"),
                    tx.get("Description"), tx.get("EMAIL ID"), tx.get("WP ID"),
                    tx.get("ESTADO DE REMEDIACION")
                ]
                self.sheet_service.update_row(row_index, new_row)
                return True
        return False
    
    def update_status(self, movement_number: str, new_status: str):
        """Update the remediation status ('ESTADO DE REMEDIACION') of a transaction."""
        return self.update_transaction(movement_number, {"ESTADO DE REMEDIACION": new_status})
    
    def save(self):
        """Persist any changes to the Google Sheet (no-op for mock, just confirmation)."""
        # In a real implementation, this would push local changes to the remote Google Sheet.
        print("All changes have been saved to the Google Sheet.")
        return True

# Initialize the TransactionsWorksheet with a mock GoogleSheetsService.
sheet_service = GoogleSheetsService(sheet_id="dummy_sheet_id")
transactions_worksheet = TransactionsWorksheet(sheet_service)

# Define LangChain tools (or structured tools) for transaction operations.
from langchain.agents import Tool
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

# Tool 1: Read all transactions (no input required)
def list_all_transactions(_=None) -> str:
    """Return all transactions as a string list."""
    txs = transactions_worksheet.get_all_transactions()
    return "\n".join(str(tx) for tx in txs)

read_all_tool = Tool(
    name="read_all_transactions",
    func=list_all_transactions,
    description="Read all transactions from the sheet. (No input required)"
)

# Tool 2: Find a transaction by N° Movimiento
def find_transaction_by_number(movement_number: str) -> str:
    """Find and return a transaction by its N° Movimiento."""
    result = transactions_worksheet.find_transaction(movement_number)
    return str(result) if result else f"Transaction {movement_number} not found."

find_transaction_tool = Tool(
    name="find_transaction",
    func=find_transaction_by_number,
    description="Find a transaction by its N° Movimiento. Input is the transaction ID to look up."
)

# Tool 3: Add a new transaction (structured input with multiple fields)
class AddTransactionInput(BaseModel):
    movement_number: str = Field(..., description="Unique transaction ID (N° Movimiento).")
    date: str = Field(..., description="Transaction date (YYYY-MM-DD).")
    amount: float = Field(..., description="Transaction amount.")
    description: str = Field(..., description="Description of the transaction.")
    email_id: str = Field("", description="EMAIL ID for related client conversation (if any).")
    wp_id: str = Field("", description="WP ID for related client conversation (if any).")
    state: str = Field(..., description="Initial ESTADO DE REMEDIACION (remediation status).")

def add_transaction_func(input: AddTransactionInput) -> str:
    """Add a new transaction record to the sheet."""
    new_tx = {
        "N° Movimiento": input.movement_number,
        "Date": input.date,
        "Amount": input.amount,
        "Description": input.description,
        "EMAIL ID": input.email_id or "",
        "WP ID": input.wp_id or "",
        "ESTADO DE REMEDIACION": input.state
    }
    transactions_worksheet.add_transaction(new_tx)
    return f"Transaction {input.movement_number} added successfully."

add_transaction_tool = StructuredTool.from_function(add_transaction_func)
# Optionally override the tool name/description for clarity
add_transaction_tool.name = "add_transaction"
add_transaction_tool.description = "Add a new transaction. Provide movement_number, date, amount, description, email_id, wp_id, and state."

# Tool 4: Update an existing transaction (structured input for partial updates)
class UpdateTransactionInput(BaseModel):
    movement_number: str = Field(..., description="N° Movimiento of the transaction to update.")
    date: str = Field(None, description="New date (if updating).")
    amount: float = Field(None, description="New amount (if updating).")
    description: str = Field(None, description="New description (if updating).")
    email_id: str = Field(None, description="New EMAIL ID (if updating).")
    wp_id: str = Field(None, description="New WP ID (if updating).")
    state: str = Field(None, description="New ESTADO DE REMEDIACION (if updating).")

def update_transaction_func(input: UpdateTransactionInput) -> str:
    """Update fields of an existing transaction by N° Movimiento."""
    updates = {}
    if input.date is not None:
        updates["Date"] = input.date
    if input.amount is not None:
        updates["Amount"] = input.amount
    if input.description is not None:
        updates["Description"] = input.description
    if input.email_id is not None:
        updates["EMAIL ID"] = input.email_id
    if input.wp_id is not None:
        updates["WP ID"] = input.wp_id
    if input.state is not None:
        updates["ESTADO DE REMEDIACION"] = input.state
    success = transactions_worksheet.update_transaction(input.movement_number, updates)
    return f"Transaction {input.movement_number} updated successfully." if success else f"Transaction {input.movement_number} not found."

update_transaction_tool = StructuredTool.from_function(update_transaction_func)
update_transaction_tool.name = "update_transaction"
update_transaction_tool.description = "Update an existing transaction's fields. Provide movement_number and any fields (date, amount, description, email_id, wp_id, state) to update."

# Tool 5: Update the remediation status of a transaction
class UpdateStateInput(BaseModel):
    movement_number: str = Field(..., description="N° Movimiento of the transaction.")
    new_status: str = Field(..., description="New ESTADO DE REMEDIACION value.")

def update_state_func(input: UpdateStateInput) -> str:
    """Update the remediation status of a transaction."""
    success = transactions_worksheet.update_status(input.movement_number, input.new_status)
    return f"Transaction {input.movement_number} status updated to '{input.new_status}'." if success else f"Transaction {input.movement_number} not found."

update_state_tool = StructuredTool.from_function(update_state_func)
update_state_tool.name = "update_transaction_status"
update_state_tool.description = "Update a transaction's ESTADO DE REMEDIACION (remediation status). Provide movement_number and new_status."

# Tool 6: Save changes to the sheet (no input)
def save_changes_func(_=None) -> str:
    """Save all changes to the Google Sheet."""
    transactions_worksheet.save()
    return "All changes have been saved to the Google Sheet."

save_tool = Tool(
    name="save_transactions",
    func=save_changes_func,
    description="Save any changes to the Google Sheet. (No input required)"
)

# Collect all tools into a list for the agent
tools = [
    read_all_tool,
    find_transaction_tool,
    add_transaction_tool,
    update_transaction_tool,
    update_state_tool,
    save_tool
]

# Configure the GeminiTextAgent with the LLM and tools.
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

class GeminiTextAgent:
    def __init__(self, llm, tools, transactions_ws: TransactionsWorksheet):
        """
        Initialize the agent with a language model, a set of tools, and the transactions worksheet.
        The agent will use the tools to fulfill user requests.
        """
        self.transactions_ws = transactions_ws
        # Prepare a set of allowed keywords (transaction IDs and conversation IDs) for filtering queries.
        self.allowed_keywords = set()
        for tx in transactions_ws.transactions:
            if tx.get("N° Movimiento"):
                self.allowed_keywords.add(str(tx["N° Movimiento"]).lower())
            if tx.get("EMAIL ID"):
                self.allowed_keywords.add(str(tx["EMAIL ID"]).lower())
            if tx.get("WP ID"):
                self.allowed_keywords.add(str(tx["WP ID"]).lower())
        # Initialize the LangChain agent with provided tools and LLM.
        self.agent_chain = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
    
    def is_transaction_related(self, query: str) -> bool:
        """Check if the query is related to transactions or associated client conversations."""
        q = query.lower()
        if "transaction" in q or "movimiento" in q:
            return True
        return any(keyword in q for keyword in self.allowed_keywords)
    
    def run(self, query: str) -> str:
        """Run the agent on the query, refusing if the query is out of scope."""
        if not self.is_transaction_related(query):
            # Refuse questions that are not about transactions or related conversations
            return "I'm sorry, but I can only assist with transaction-related queries and linked client conversations."
        # If the query is in scope, use the agent chain to process it
        return self.agent_chain.run(query)

# Example of setting up the agent with tools:
# llm = OpenAI(temperature=0)  # Using OpenAI as a placeholder for the Gemini model
# agent = GeminiTextAgent(llm=llm, tools=tools, transactions_ws=transactions_worksheet)
# 
# # Using the agent:
# response1 = agent.run("Read all transactions")
# response2 = agent.run("Find transaction 1002")
# response3 = agent.run("What's the weather tomorrow?")
# print(response1)  # Should list all transactions
# print(response2)  # Should show details of transaction 1002
# print(response3)  # Should refuse, as it's not related to transactions
