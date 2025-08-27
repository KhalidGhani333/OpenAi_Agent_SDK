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

class UserDataType(BaseModel):
    name:str
    age:int
    role:str

@function_tool
def get_age(ctx:RunContextWrapper[UserDataType],):
    """Get age function"""
    print("Get_Age Tool --->")
    return f'The user age is {ctx.context.age}'


def dynamic_instruction(ctx: RunContextWrapper[UserDataType],agent:Agent[UserDataType]):
    return f'User name is {ctx.context.name}, you are helpful assistant.'

user_1 = UserDataType(name="Khalid ghani",age=25 , role="Student")

agent = Agent[UserDataType](name="Assistant",
                  instructions= dynamic_instruction,
                  tools=[get_age],
)


async def main():
    
    result = await Runner.run(starting_agent=agent,
                              input="Hello",
                              run_config=config,
                              context=user_1
    )

    print(result.final_output)
    print()

if __name__ == "__main__":
    asyncio.run(main())
