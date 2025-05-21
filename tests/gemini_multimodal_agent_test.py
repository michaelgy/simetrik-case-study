# python -m tests.gemini_multimodal_agent_test

import os
import base64
import mimetypes
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv("./env/.env")

# Initialize the Gemini 2.5 Pro model
model = ChatGoogleGenerativeAI(model="gemini-2.5-pro-preview-05-06")

# Define tools if any (empty in this example)
tools = []

# Initialize memory for conversation history
memory = MemorySaver()

# Create the agent executor with memory
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Configuration with a unique thread ID
config = {"configurable": {"thread_id": "abc123"}}

# Helper function to encode image to base64
def encode_image_to_base64(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return {"mime_type": mime_type, "data": encoded_string}

# Interactive loop
while True:
    m = input("[query]<< ")
    if m.strip().lower() == "exit":
        break
    elif m.startswith("image:"):
        image_path = m.replace("image:", "").strip()
        if not os.path.isfile(image_path):
            print(f"[error]>> File not found: {image_path}")
            continue
        try:
            image_data = encode_image_to_base64(image_path)
            message = HumanMessage(
                content=[
                    {"type": "text", "text": "Describe the image, give me a table with all the data (if any) and me the most common color in the image in rgb format."},
                    {
                        "type": "image_url",
                        "image_url": f"data:{image_data['mime_type']};base64,{image_data['data']}"
                    }
                ]
            )
            for chunk in agent_executor.stream({"messages": [message]}, config):
                response = "\n".join([ch.content for ch in chunk["agent"]["messages"]])
                print("[response chunk]>>", response)
                print("----")
        except Exception as e:
            print("[error]>>", e)
    else:
        try:
            for chunk in agent_executor.stream({"messages": [HumanMessage(content=m)]}, config):
                response = "\n".join([ch.content for ch in chunk["agent"]["messages"]])
                print("[response chunk]>>", response)
                print("----")
        except Exception as e:
            print("[error]>>", e)
