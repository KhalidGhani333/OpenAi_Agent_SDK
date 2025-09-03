from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled ,function_tool ,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os
from agents.run import RunConfig
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
    model_provider=external_client,

)


#  function tool
@function_tool
def substract(a:int,b:int)->int:
       """substract this two number
       first is a and second is b
       give output the substract of this two number is {answer}"""
       return a - b

@function_tool
def add(a:int,b:int)->int:
       """add this two number
       first is a and second is b
       give output the sum of this two number is {answer}"""
       return a + b


# Create Custom Runner
class Custom_Runner(Runner):
    async def custom(self,agent,input,run_config=None):
          
          modify_input = input
          result = await super().run(agent,modify_input,run_config=run_config)
          return result
    


agent = Agent(name="very helpful assistant",
              instructions="""you are a helpfull assistant you answer the every query of the user.
              if query is related to avaliable tool then use tool otherwise answer directly""",
              tools=[add,substract],
            )
async def main():
    custom_runner = Custom_Runner()

    result_1 = await custom_runner.run(agent,
                                "where is karachi answer in detail ?",
                                max_turns=4,
                                run_config=config
                                )
    print(result_1.final_output)
    

if __name__ == "__main__":
      asyncio.run(main())