from typing import List, Any, Dict
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

class GeminiTextAgent:
    def __init__(self, tools: List[Any] = None):
        """
        Initialize the Gemini Text Agent
        Args:
            tools: List of tools that the agent can use
        """
        self.model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
        self.tools = tools or []
        self.memory = MemorySaver()
        self.agent_executor = create_react_agent(
            self.model, 
            self.tools, 
            checkpointer=self.memory
        )
        self.config = {"configurable": {"thread_id": "default"}}

    def set_thread_id(self, thread_id: str):
        """
        Set a custom thread ID for the conversation
        Args:
            thread_id: Unique identifier for the conversation thread
        """
        self.config["configurable"]["thread_id"] = thread_id

    def process_message(self, message: str) -> str:
        """
        Process a single message and return the response
        Args:
            message: The message to process
        Returns:
            str: The agent's response
        """
        response_chunks = []
        for chunk in self.agent_executor.stream(
            {"messages": [HumanMessage(content=message)]}, 
            self.config
        ):
            response = "\n".join([ch.content for ch in chunk["agent"]["messages"]])
            response_chunks.append(response)
        
        return "\n".join(response_chunks)

    def interactive_session(self):
        """
        Start an interactive session with the agent
        """
        print("Starting interactive session. Type 'exit' to quit.")
        while True:
            message = input("[query]<< ")
            if message.lower() == "exit":
                break
            
            response = self.process_message(message)
            print("[response]>>", response)
            print("----") 