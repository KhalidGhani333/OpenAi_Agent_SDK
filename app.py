from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled ,function_tool ,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os
from agents.run import RunConfig
import requests
import asyncio

load_dotenv()
set_tracing_disabled(disabled=True)
API_KEY = os.getenv("GEMINI_API_KEY")

# enable_verbose_stdout_logging()
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
# hosted tool sirf openai ki key k sath chalta hy

#  function tool
@function_tool
def substract(a:int,b:int)->int:
       """substract this two number
       first is a and second is b
       give output the sum of this two number is {answer}"""
       return a - b

@function_tool
def add(a:int,b:int)->int:
       """add this two number
       first is a and second is b
       give output the sum of this two number is {answer}"""
       return a + b

       

agent = Agent(name="Assistant",
              instructions="you are helpful assistant",
              tools=[add,substract])
async def main():
    result = await Runner.run(agent,"what is 10 - 5 ?",run_config=config)
    print(result.final_output)

if __name__ == "__main__":
      asyncio.run(main())

