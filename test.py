# from typing import TypeVar, Generic

# T = TypeVar("T")

# class Generic_Type(Generic[T]):
#     def __init__(self,item:T):
#         self.item = item

#     def get_item(self)->T:
#         return self.item
    
# str_Box = Generic_Type("Ali")
# int_Box = Generic_Type(123)

# print(str_Box.get_item())
# print(int_Box.get_item())

# from pydantic import BaseModel

# class My_class(BaseModel):
#     name:str
#     age:int
#     is_on_job:bool


# s= My_class(name="khalid",age=25,is_on_job=True)
# print(s)              # Answer name='khalid' age=25 is_on_job=True

# import asyncio

# async def say_hello():
#     await asyncio.sleep(2)
#     print("Hello")

# async def main():
#     await say_hello()
#     print("Done")

# asyncio.run(main())

# import asyncio
# from dataclasses import dataclass
# from agents import Agent, RunContextWrapper , Runner , OpenAIChatCompletionsModel ,AsyncOpenAI, function_tool ,set_tracing_disabled,enable_verbose_stdout_logging
# import os
# from dotenv import load_dotenv
# from agents.run import RunConfig



# # Disable tracing
# set_tracing_disabled(disabled=True)

# # Load environment variables
# load_dotenv()

# # Load Gemini API key
# API_KEY = os.environ.get("GEMINI_API_KEY")

# if not API_KEY:
#     raise ValueError("API Key Missing")

# # Create external client
# external_client = AsyncOpenAI(
#     api_key = API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# # Define the model and configuration
# model = OpenAIChatCompletionsModel(
#     model = "gemini-2.0-flash",
#     openai_client = external_client
# )

# config = RunConfig(
#     model=model,
#     model_provider=external_client
# )

# @dataclass
# class User_Info:
#     userName:str
#     uID:int
#     Location:str = "Pakistan"

# @function_tool
# async def fetch_user_age(wrapper: RunContextWrapper[User_Info]) -> str:
#     '''Returns the name and age of the user.'''
#     return f"User {wrapper.context.userName} is 30 years old"

# @function_tool
# async def fetch_user_location(wrapper: RunContextWrapper[User_Info]) -> str:
#     '''Returns the location of the user.'''
#     return f"User {wrapper.context.userName} is from {wrapper.context.Location}"



# async def main():
#     data = User_Info(userName="Khalid",uID=1001,Location="Pakistan")

#     agent = Agent[User_Info](
#         name="Assistant",
#         tools=[fetch_user_age,fetch_user_location],
#         model=model

#     )

#     result = await Runner.run(agent,"What is the name,age of the user? current location of his/her?",context=data,run_config=config)
#     print(result.final_output)


# if __name__ == "__main__":
#     asyncio.run(main())


# ----------------- Custon tool ----------------
# from pydantic import BaseModel
# from agents import FunctionTool ,RunContextWrapper


# class run_Class(BaseModel):
#     username :str
#     age :int


# async def custom_tool(ctx:RunContextWrapper,args:str)->str:
#     data = run_Class.model_validate_json(args)
#     return f"The name is {data.username} and the age is {data.age}"

# tool = FunctionTool(
#     name="user_info",
#     description="Get user info",
#     params_json_schema=run_Class.model_json_schema(),
#     on_invoke_tool=custom_tool
# )

import os
from agents import Agent, OpenAIChatCompletionsModel, RunConfig, Runner, function_tool, set_tracing_disabled,enable_verbose_stdout_logging
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
set_tracing_disabled(disabled=True)
API_KEY = os.environ.get("GEMINI_API_KEY")
enable_verbose_stdout_logging()

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client
)

@function_tool()
def usd_to_pkr() -> str:
    return 'USD 280'

agent = Agent(
    name='An Agent',
    instructions='You are a helpful assistant. your task is to help the user with their queries',
    tools=[usd_to_pkr]
)

result = Runner.run_sync(agent,
                         "what is USD TO PKR today? multiply it by 10",
                         run_config=config)

print(result.final_output)
