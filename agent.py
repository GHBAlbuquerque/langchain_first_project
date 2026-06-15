from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model( "openai:gpt-5-nano")

agent = create_agent( #inherits from runnable!
    model=model,
    system_prompt="You're an assistant that answers question about what the user wants to know. If you don't know the answer, politely say so."
)

input = "What is the capital of Aruba?"
answer = agent.invoke({"messages": [{"role": "user", "content": input}]})

print(answer)
print(answer["messages"][-1].content)

second_input = "What is the current weather in Oranjestad?"

second_answer = agent.invoke({"messages": [{"role": "user", "content": second_input}]})
print(second_answer["messages"][-1].content)
