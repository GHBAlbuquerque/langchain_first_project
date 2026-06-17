from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
import requests
from dotenv import load_dotenv

load_dotenv()
    
@tool
def search_zipcode(cep: str) -> str:
    """
    Gets information of a brazilian zipcode.
    
    Args:
        cep: Brazilian zipcode that takes only numbers
    
    Returns:
        str: Zipcode information
    """
    
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    data = response.json()
    
    return data


model = init_chat_model("openai:gpt-5.4-mini")

agent = create_agent( #inherits from runnable!
    model=model,
    system_prompt=(
        "You are a helpful assistant. For questions requiring real-time, current, "
        "or live information (such as current weather), you MUST use your tools "
        "immediately to find the answer. Do not ask the user for permission to use tools."
        "If you don't know the answer even after researching, just say you don't know."
    ), 
    tools=(search_zipcode,)
)