from langchain.agents import Tool
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class TransactionSheetTools:
    def __init__(self, transaction_service):
        self.transaction_service = transaction_service
        self.tools = self._initialize_tools()

    def _initialize_tools(self):

        # Tool 1: Read all transactions (no input required)
        def list_all_transactions(_=None) -> str:
            """Return all transactions as a string list."""
            txs = self.transaction_service.transactions.read_all()
            return txs.to_string()

        read_all_tool = Tool(
            name="read_all_transactions",
            func=list_all_transactions,
            description="Read all transactions from the sheet. (No input required)"
        )

        # Tool 2: Find a transaction by N° Movimiento
        def find_transaction_by_number(movement_number: int) -> str:
            """Find and return a transaction by its N° Movimiento."""
            result = self.transaction_service.transactions.find(movement_number)
            return result.to_string() if result else f"Transaction {movement_number} not found."

        find_transaction_tool = Tool(
            name="find_transaction",
            func=find_transaction_by_number,
            description="Find a transaction by its N° Movimiento. Input is the transaction ID to look up."
        )

        # Tool 3: Add a new transaction (structured input with multiple fields)
        class AddTransactionInput(BaseModel):
            date: str = Field("", description="Transaction date (DD-MM-YYYY).")
            concept: str = Field("", description="Concept of the transaction.")
            movement_number: int = Field(0, description="Unique transaction ID (N° Movimiento).")
            reference: str = Field("", description="Reference of the transaction.")
            amount: float = Field(0, description="Transaction amount.")
            query: str = Field("", description="Query of the transaction.")
            email: str = Field("", description="Email of owner of the transaction.")
            cellphone: str = Field("", description="Cellphone of owner of the transaction. (format: +573178965432)")
            sender: str = Field("", description="Sender of the transaction.")
            state: str = Field("", description="Initial ESTADO DE REMEDIACION (remediation status).")
            email_id: str = Field("", description="EMAIL ID for related client conversation (if any).")
            wp_id: str = Field("", description="WP ID for related client conversation (if any).")
            file_path: str = Field("", description="File path of the transaction.")

        def add_transaction_func(input: AddTransactionInput) -> str:
            """Add a new transaction record to the sheet."""
            new_tx = {
                'Fecha': input.date,
                'Concepto': input.concept,
                'N° Movimiento': input.movement_number,
                'Referencia': input.reference,
                'Monto': input.amount,
                'QUERY': input.query,
                'CORREO': input.email,
                'TELEFONO': input.cellphone,
                'REMITENTE': input.sender,
                'ESTADO DE REMEDIACION': input.state,
                'EMAIL ID': input.email_id,
                'WP ID': input.wp_id,
                'ARCHIVO': input.file_path
            }
            added = self.transaction_service.transactions.add(new_tx)
            return f"Transaction {input.movement_number} added successfully." if added else f"Transaction {input.movement_number} not added."

        add_transaction_tool = StructuredTool.from_function(add_transaction_func)
        # Optionally override the tool name/description for clarity
        add_transaction_tool.name = "add_transaction"
        add_transaction_tool.description = "Add a new transaction. Provide movement_number, date, concept, reference, amount, query, email, cellphone, sender, state, email_id, wp_id, and file_path."

        # Tool 4: Update an existing transaction (structured input for partial updates)
        class UpdateTransactionInput(BaseModel):
            column_to_search: str = Field("", description="Column to search for the transaction to update.")
            value_to_search: str = Field("", description="Value to search in the column_to_search column for the transaction to update.")
            date: str = Field("", description="New transaction date (DD-MM-YYYY).")
            concept: str = Field("", description="New concept of the transaction.")
            movement_number: int = Field(0, description="Unique transaction ID (N° Movimiento).")
            reference: str = Field("", description="New reference of the transaction.")
            amount: float = Field(0, description="New transaction amount.")
            query: str = Field("", description="New query of the transaction.")
            email: str = Field("", description="New email of owner of the transaction.")
            cellphone: str = Field("", description="New cellphone of owner of the transaction. (format: +573178965432)")
            sender: str = Field("", description="New sender of the transaction.")
            state: str = Field("", description="New remediation status.")
            email_id: str = Field("", description="New EMAIL ID for related client conversation (if any).")
            wp_id: str = Field("", description="New WP ID for related client conversation (if any).")
            file_path: str = Field("", description="New file path of the transaction.")

        def update_transaction_func(input: UpdateTransactionInput) -> str:
            """Update fields of an existing transaction by column_to_search and value_to_search."""
            updates = {}
            column_to_search = input.column_to_search
            value_to_search = input.value_to_search

            if input.date != "":
                updates["Date"] = input.date
            if input.concept != "":
                updates["Concepto"] = input.concept
            if isinstance(input.movement_number, int):
                updates["N° Movimiento"] = input.movement_number
            if input.reference != "":
                updates["Referencia"] = input.reference
            if isinstance(input.amount, float):
                updates["Monto"] = input.amount
            if input.query != "":
                updates["QUERY"] = input.query
            if input.email != "":
                updates["CORREO"] = input.email
            if input.cellphone != "":
                updates["TELEFONO"] = input.cellphone
            if input.sender != "":
                updates["REMITENTE"] = input.sender
            if input.state != "":
                updates["ESTADO DE REMEDIACION"] = input.state
            if input.email_id != "":
                updates["EMAIL ID"] = input.email_id
            if input.wp_id != "":
                updates["WP ID"] = input.wp_id
            if input.file_path != "":
                updates["ARCHIVO"] = input.file_path
            
            success = False
            if(column_to_search and value_to_search):
                success = self.transaction_service.transactions.update(column_to_search, value_to_search, updates)
            return f"Transaction {input.movement_number} updated successfully." if success else f"Transaction {input.movement_number} not found."

        update_transaction_tool = StructuredTool.from_function(update_transaction_func)
        update_transaction_tool.name = "update_transaction"
        update_transaction_tool.description = "Update an existing transaction's fields. Provide column_to_search, value_to_search, and any fields (date, concept, movement_number, reference, amount, query, email, cellphone, sender, state, email_id, wp_id, file_path) to update."

        # Tool 5: Update the remediation status of a transaction
        class UpdateStateInput(BaseModel):
            movement_number: int = Field(..., description="N° Movimiento of the transaction.")
            new_status: str = Field(..., description="New ESTADO DE REMEDIACION value [No Procesado, En Proceso, Respuesta Invalida 1, Respuesta Invalida 2, Procesamiento Manual, Completado].")

        def update_state_func(input: UpdateStateInput) -> str:
            """Update the remediation status of a transaction."""
            success = self.transaction_service.transactions.update_state(input.movement_number, input.new_status)
            return f"Transaction {input.movement_number} status updated to '{input.new_status}'." if success else f"Transaction {input.movement_number} not found."

        update_state_tool = StructuredTool.from_function(update_state_func)
        update_state_tool.name = "update_transaction_status"
        update_state_tool.description = "Update a transaction's ESTADO DE REMEDIACION (remediation status). Provide movement_number and new_status [No Procesado, En Proceso, Respuesta Invalida 1, Respuesta Invalida 2, Procesamiento Manual, Completado]."

        # Tool 6: Save changes to the sheet (no input)
        def save_changes_func(_=None) -> str:
            """Save all changes to the Google Sheet."""
            self.transaction_service.transactions.save_changes()
            return "All changes have been saved to the Google Sheet."

        save_tool = Tool(
            name="save_transactions",
            func=save_changes_func,
            description="Save any changes made from other tools to the Google Sheet. (No input required)"
        )

        # Tool 7: Reload data from the sheet (no input)
        def reload_data_func(_=None) -> str:
            """Reload data from the Google Sheet."""
            self.transaction_service.transactions.reload_data()
            return "Data has been reloaded from the Google Sheet."
        
        reload_data_tool = Tool(
            name="reload_data",
            func=reload_data_func,
            description="Reload data from the Google Sheet. (No input required)"
        )

        # Collect all tools into a list for the agent
        tools = [
            read_all_tool,
            find_transaction_tool,
            add_transaction_tool,
            update_transaction_tool,
            update_state_tool,
            save_tool,
            reload_data_tool
        ]

        return tools
            

