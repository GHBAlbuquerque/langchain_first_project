import sqlite3
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from langchain_tavily import TavilySearch
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.agents.middleware import SummarizationMiddleware
from dotenv import load_dotenv

load_dotenv()

conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
checkpoint= SqliteSaver(conn)

model = init_chat_model("openai:gpt-5.4-mini")

agent = create_agent( #inherits from runnable!
    model=model,
    system_prompt=(
        "You are a helpful assistant. For questions requiring real-time, current, "
        "or live information (such as current weather), you MUST use your tools "
        "immediately to find the answer. Do not ask the user for permission to use tools."
        "If you don't know the answer even after researching, just say you don't know."
    ), 
    tools=[TavilySearch()],
    checkpointer=checkpoint,
    middleware=[SummarizationMiddleware(
            model=model, #does not have to be the same as the agent model
            trigger=("messages", 6), #decides the qt of token, messages or contexts windows to trigger a summarization (token is the best but fpr the example we use message)
            keep=("messages", 2) #how much recent conversation history is preserved exactly as it was written, while the older messages get compressed into a summary
        )],
)

config = RunnableConfig(configurable= {"thread_id": "2"})

print("Agent is working.")
while True:
    user_input = input("Ask anything: ")
    answer = agent.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
    print(f"Agent: {answer["messages"][-1].content}")
 