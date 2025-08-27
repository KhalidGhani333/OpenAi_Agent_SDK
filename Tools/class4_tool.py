from agents import (Agent,
                    Runner,
                    OpenAIChatCompletionsModel,
                    AsyncOpenAI,
                    set_tracing_disabled ,
                    function_tool ,
                    enable_verbose_stdout_logging,
                    FunctionTool,RunContextWrapper,
                    ModelSettings)

from dotenv import load_dotenv
import os ,asyncio
from agents.run import RunConfig
from agents.agent import StopAtTools
from pydantic import BaseModel
from validate_tool import tool_validate


load_dotenv()
set_tracing_disabled(disabled=True)
API_KEY = os.getenv("GEMINI_API_KEY")

# enable_verbose_stdout_logging()
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

# class Check_Premium(BaseModel):
#        isPremium:bool

# async def check_premium_tool(ctx:RunContextWrapper,args):
#        parse = Check_Premium.model_validate_json(args)
#        print("<----- Premium ----->")
#        return f"The user is Premium {parse.isPremium}"

# premium = FunctionTool(
#        name="premium_tool",
#        description="premium user function",
#        params_json_schema=Check_Premium.model_json_schema(),
#        on_invoke_tool=check_premium_tool,
#        is_enabled=tool_validate,
       
# )

# async def check_non_premium_tool(ctx:RunContextWrapper,args):
#        print("<----- Non Premium ----->")
#        obj = Check_Premium.model_validate_json(args)
#        return f"The User is Non Premium {obj.isPremium}"

# not_premium = FunctionTool(
#        name="non_premium_tool",
#        description="non premium user function",
#        params_json_schema=Check_Premium.model_json_schema(),
#        on_invoke_tool=check_non_premium_tool,
#        is_enabled=tool_validate

# )

class Tool_Schema(BaseModel):
       num1:int
       num2:int

async def substract_tool(context:RunContextWrapper,arguments):
       object = Tool_Schema.model_validate_json(arguments)
       print("Substruct Tool Fire ---->")
       return f"The Total is {object.num1 - object.num2}"

substruct = FunctionTool(
       name="substruct_tool",
       description="substruct tool funtion",
       params_json_schema=Tool_Schema.model_json_schema(),
       on_invoke_tool=substract_tool,
       is_enabled=tool_validate,

)


@function_tool(
              name_override="plus_tool",
              description_override="plus tool function",
              is_enabled=True,
              )

def add(a:int,b:int)->int:
       """add this two number
       first is a and second is b
       give output the sum of this two number is {answer}"""
       print("Add Tool Fire ---->")
       return f"The Sum of {a} and {b} is {a + b}......."

@function_tool()
def multiply(a:int,b:int)->int:
       """multiply this two number
       first is a and second is b """
       print("Multiply Tool Fire ---->")
       return a * b




agent = Agent(name="Assistant",
              instructions="you are helpful Math teacher.",
              tools=[add,substruct,multiply],
              tool_use_behavior=StopAtTools(stop_at_tool_names=["add","multiply"]),
              # tool_use_behavior="stop_on_first_tool",
              model_settings=ModelSettings(tool_choice="plus_tool"),
              # reset_tool_choice=False
              )


user = {"name":"khalid","age":19,"isPremium":"True"}

async def main():
        result = await Runner.run(agent,
              "3*10?",
              run_config=config,
              context=user,
              # max_turns=3
              )
        print(result.final_output)
        
        


if __name__ == "__main__":
      asyncio.run(main())


