from typing import List, Any, Dict
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import logging

class GeminiTextAgent:
    def __init__(self, tools: List[Any] = None, max_iterations: int = 15, max_execution_time: int = 60):
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
            checkpointer=self.memory,
        )
        self.max_iterations = max_iterations
        self.max_execution_time = max_execution_time
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
        
        # Create config with recursion limit (controls reasoning steps)
        config = self.config.copy()
        config["recursion_limit"] = self.max_iterations

        response_chunks = []
        for chunk in self.agent_executor.stream(
            {"messages": [HumanMessage(content=message)]}, 
            config
        ):
            logging.info(f"chunk: {chunk}")
            if "agent" in chunk:
                response = "\n".join([ch.content for ch in chunk["agent"]["messages"]])
                response_chunks.append(response)
        
        return "\n".join(response_chunks)

    def interactive_session(self):
        """
        Start an interactive session with the agent
        """
        logging.info("Starting interactive session. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
            
            response = self.process_message(user_input)
            logging.info(f"[response]>> {response}")
            logging.info("----") 