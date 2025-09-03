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


# hosted tool sirf openai ki key k sath chalta hy

#  function tool
@function_tool
def get_weather(city:str)->str:
        result=requests.get(f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}")
        # data=result.json()
        # return f"The current weather in {city} is {data}."
        if result.status_code == 200:
                data = result.json()
                return f"The weather in {city} is {data}"
        else:
            return "Sorry, I couldn't fetch the weather data."
@function_tool
def get_jokes(joke:str)-> str:
      url = "https://official-joke-api.appspot.com/random_joke"
      result = requests.get(url)
      data = result.json()
      return data


@function_tool
def add(a:int,b:int)->int:
       """add this two number
       first is a and second is b
       give output the sum of this two number is {answer}"""
       return a + b - 1

def my_failure_handler(agent,error,context):
       print(f"[ERROR] agent {agent.name} is failed with {error}")
       return {"output": "Sorry, kuch masla ho gaya. Please try again."}



agent = Agent(name="Assistant",
              instructions="you are helpful Assistant. i give you some tool if any prompt related to tool topic you must use that tool otherwise you answer the prompt according to prompt",
              tools=[get_weather,add],
              tool_use_behavior="stop_on_first_tool",
              on_error=my_failure_handler 
              )



async def main():
    while True:
        prompt = input("Enter prompt :")
        if prompt.lower() in ['exit',"quit"]:
            break
        result = await Runner.run(agent,prompt, run_config=config)
        print(result.final_output)
  



if __name__ == "__main__":
      asyncio.run(main())