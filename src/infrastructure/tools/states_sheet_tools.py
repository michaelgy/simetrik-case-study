from langchain.agents import Tool

class StatesSheetTools:
    def __init__(self, transaction_service):
        self.transaction_service = transaction_service
        self.tools = self._initialize_tools()

    def _initialize_tools(self):
        # Tool 1: Read all states (no input required)
        def list_all_states(_=None) -> str:
            """Return all states as a string list."""
            self.transaction_service.states.reload_data()
            states = self.transaction_service.states.read_all()
            return states.to_string()

        read_all_tool = Tool(
            name="read_all_states",
            func=list_all_states,
            description="Read all states from the sheet. (No input required)"
        )

        # Tool 2: Find a state by name
        def find_state_by_name(state_name: str) -> str:
            """Find and return a state by its name."""
            result = self.transaction_service.states.find('Estado', state_name)
            return result.to_string() if result is not None and not result.empty else f"State {state_name} not found."

        find_state_tool = Tool(
            name="find_state",
            func=find_state_by_name,
            description="Find a state by its name. Input is the state name to look up."
        )

        # Collect all tools into a list
        tools = [
            read_all_tool,
            find_state_tool,
        ]

        return tools 