from agents import (
    Agent, 
    Runner, 
    AsyncOpenAI, 
    OpenAIChatCompletionsModel,
    function_tool,
    RunContextWrapper,
    enable_verbose_stdout_logging
    )

from dotenv import load_dotenv
from agents.run import RunConfig
import os
import asyncio
from dataclasses import dataclass
from pydantic import BaseModel


# enable_verbose_stdout_logging()
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise KeyError("Error 405: API key not found")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# @dataclass
# class UserInfo:
#     name:str
#     age:int

# @function_tool
# def fetch_user_data(wrapper:RunContextWrapper[UserInfo]) -> str:
#     """Returns the age and name of the user."""
#     return f"Name:{wrapper.context.name} Age:{wrapper.context.age} years old"

# async def main():
#     user_info = UserInfo(name ="khalid ghani", age=123)
#     agent= Agent[UserInfo](name="Assistant",tools=[fetch_user_data])
#     result = await Runner.run(starting_agent=agent,input="What is the name and age of the user?",run_config=config, context=user_info)
#     print(result.final_output)

gernal_agent = Agent(
    name="General knowledge agent",
    instructions="you are a gerneral agent answer the every question of the user"
)



class User_Info(BaseModel):
    name :str
    age:int
    gender:str

@function_tool
def get_user_data(wrapper: RunContextWrapper[User_Info])-> str:
    """Returns the name ,age and gender of the user."""
    return f"user Name: {wrapper.context.name} Age:{wrapper.context.age} Gender:{wrapper.context.gender}"

async def main():
    user_detail = User_Info(name="Khalid ghani",age=25,gender="male")
    agent = Agent[User_Info](name="Assistant",instructions="You are a helpful AI assistant. Your job is to respond to user questions with accurate and helpful answers."
    "\nIf the user asks for specific user information and you already have it, respond directly.you have also a general knowledge answer the every type of questions from user.",tools=[get_user_data],handoffs=[gernal_agent])

    result = await Runner.run(starting_agent=agent,input="what is the user name?",run_config=config,context=user_detail)

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
