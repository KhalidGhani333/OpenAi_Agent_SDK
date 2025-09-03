from agents import (
      Agent, ModelSettings,Runner,OpenAIChatCompletionsModel,
      AsyncOpenAI,set_tracing_disabled ,function_tool,enable_verbose_stdout_logging)
from dotenv import load_dotenv
import os
from agents.run import RunConfig
import asyncio

# enable_verbose_stdout_logging()
load_dotenv()
set_tracing_disabled(disabled=True)
API_KEY = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client
)
@function_tool
def add(a:int,b:int)->int:
       """add this two number
       first is a and second is b
       give output the sum of this two number is {answer}"""
       return a + b - 1

@function_tool()
def substract(a:int,b:int)->int:
       """substract this two number
       first is a and second is b
       give output the sum of this two number is {answer}"""
       return a - b

agent = Agent(
            name="Creative Assistant",
            instructions="you are a creative assistant.you perfectly answer the every quries of user",
            tools=[substract,add],
            model_settings=ModelSettings(
            temperature=0.3, # 0.1,  # Very focused , 0.8, Very creative
            top_p=0.2,
            tool_choice=("auto"), # "required" tool lazmi call hoga.substract tool ho or query add ki ho pir bhi substract hoga.
            # max_tokens=500000,  # Enough for detailed steps , 300 Short but creative
            # parallel_tool_calls=True,  # Use multiple tools simultaneously gemini support nae kar raha.
            # parallel_tool_calls=False,  # Use tools one by one
            # frequency_penalty=0,  # 0 say ziada hoga word repeat nae karay ga
            # presence_penalty=0,   # 0 say ziada hoga new ideas aur alag lafz introduce karay ga
            # top_k = 50,        # randomness ko control karna by restricting choice.
            truncation="auto", # auto hoga to automatically purani baaten cut karke nayi rakhega. model limit 200k
            
    ))
async def main():
    result = await Runner.run(agent,"write short note on pakistan.",run_config=config)
    print(result.final_output)

    # result = await Runner.run(agent,"write 20 lines essay on AI",run_config=config)
    # print(result.final_output)

if __name__ == "__main__":
      asyncio.run(main())
