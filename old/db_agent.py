from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit

import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH=os.path.abspath("./db/store.sqlite")
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

model = init_chat_model("openai:gpt-5.4-mini", temperature=0)

toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()

system_prompt = """You are an expert assistant in SQL queries.

Mandatory rules:
- Always inspect the available tables and the schema BEFORE generating any query.
- Limit results to a maximum of 10 records (use LIMIT 10).
- NEVER execute DML commands (INSERT, UPDATE, DELETE, DROP). Only SELECT.
- If you do not find the information, say that the data was not found.
"""

agent = create_agent(
    model=model,
    system_prompt=(system_prompt),
    tools=tools
)

