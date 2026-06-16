from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model( "openai:gpt-5-nano")

agent = create_agent( #inherits from runnable!
    model=model,
    system_prompt=(
        "You are a helpful assistant. For questions requiring real-time, current, "
        "or live information (such as current weather), you MUST use your tools "
        "immediately to find the answer. Do not ask the user for permission to use tools."
        "If you don't know the answer even after researching, just say you don't know."
    ), tools=[TavilySearch()]
)

# input = "What is the capital of Aruba?"
# answer = agent.invoke({"messages": [{"role": "user", "content": input}]})

# print(answer)
# print(answer["messages"][-1].content)

# second_input = "What is the current weather in Oranjestad, Aruba?"

# second_answer = agent.invoke({"messages": [{"role": "user", "content": second_input}]})
# print(second_answer["messages"][-1].content)
