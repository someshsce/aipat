import os
from dotenv import load_dotenv
from aipatt.ai.tools import tools
from aipatt.utils.get_info import info
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

env_path = os.path.join(os.path.expanduser("~"), ".aipatt.env")
load_dotenv(env_path)

llm = ChatOllama(model=os.getenv('DEFAULT_MODEL'))

system_message = f"You are a helpful AI assistant, and your name is 'AIPATT': AI Powered Assistance Tool for Terminals. \n\n {info()} \nDon't mention these informations. This is just for your real-time updates.\n\nProvide the answer accordingly if necessary."

agent = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier=system_message,
    debug=False,
)
