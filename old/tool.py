from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

# example tool

@tool
def delivery_fee_calculator(weight_kg: float, distance_km: float) -> float: #typehint
    #docstrings
    """ 
    Calculares delivery fee based on the distance and weight of the package.
    Use it when user wants to know the delivery fee.
    
    Args:
        weight_kg: Weight of the delivery package in kg
        distance_km: Distance of the delivery in km
    
    Returns:
        float: delivery fee
    
    """
    
    basic_fee = 6.0
    return basic_fee + (weight_kg * distance_km)
    
@tool
def temperature_conversion(celsius: float) -> float:
    """
    Converts temperature from celsius to farenheit.
    
    Args:
        celsius: Temperature in celsius
    
    Returns:
        float: Temperature in farenheit
    
    """
    
    return (celsius * 9/5) + 32

model = init_chat_model("openai:gpt-5.4-mini")

agent = create_agent( #inherits from runnable!
    model=model,
    system_prompt=(
        "You are a helpful assistant. For questions requiring real-time, current, "
        "or live information (such as current weather), you MUST use your tools "
        "immediately to find the answer. Do not ask the user for permission to use tools."
        "If you don't know the answer even after researching, just say you don't know."
    ), 
    tools=(delivery_fee_calculator, temperature_conversion)
)