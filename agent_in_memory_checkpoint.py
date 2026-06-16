from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv()

checkpoint = InMemorySaver()

model = init_chat_model( "openai:gpt-5-nano")

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
)

config = RunnableConfig(configurable= {"thread_id": "1"})

print("Agent is working.")
while True:
    user_input = input("Ask anything: ")
    answer = agent.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
    print(f"Agent: {answer["messages"][-1].content}")
 