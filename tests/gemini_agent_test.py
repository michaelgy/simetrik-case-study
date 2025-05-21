# python -m tests.gemini_agent_test

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv

load_dotenv("./env/.env")

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
tools = []

agent_executor = create_react_agent(model, tools)

memory = MemorySaver()
agent_executor = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

m = ""
while True:
    m = input("[query]<< ")
    if m == "exit":
        break
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=m)]}, config
    ):
        response = "\n".join([ch.content for ch in chunk["agent"]["messages"]])
        print("[response chunk]>>", response)
        print("----")