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
       give output the sum of this two number is {answer}"""
       return a - b

@function_tool
def add(a:int,b:int)->int:
       """add this two number
       first is a and second is b
       give output the sum of this two number is {answer}"""
       return a + b

       

agent = Agent(name="physic agent",
              instructions="Tum ek Physic solving agent ho, calculation karke jawab do.",
              tools=[add,substract],
            )
async def main():
    result_1 = await Runner.run(agent,
                                "2+2+2",
                                run_config=config,
                                max_turns=3)
    print(result_1.final_output)
    
    context = [result_1.final_output]

    result_2 = await Runner.run(agent,
                                "Agar mass=10 aur acceleration=2 ho to force kitna hoga?",
                                run_config=config,
                                max_turns=3,
                                previous_response_id=result_1.last_response_id,
                                context=context)
    print(result_2.final_output)
    print(result_2.context_wrapper.context)
    print(result_2.last_response_id)

if __name__ == "__main__":
      asyncio.run(main())