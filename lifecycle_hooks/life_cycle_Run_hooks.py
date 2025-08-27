from typing import Any
from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI, function_tool,set_tracing_disabled,RunHooks,RunContextWrapper,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os ,asyncio
from agents.run import RunConfig
from pydantic import BaseModel


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

class Company_data_Type(BaseModel):
    company_name:str
    service:str
    since:int
    
class Employers_type(BaseModel):
    strenght:int

# Composite Context (Sab data ek model me merge karke)
class Full_Context(BaseModel):
     company:Company_data_Type
     employer:Employers_type

# data nestesd hogaya hooks may access change hoga
class MyRunHooks(RunHooks):
    async def on_agent_start(self, ctx: RunContextWrapper[Full_Context], agent: Agent) -> None:
        print(f"🔵 Agent '{agent.name}' started.")
        print(f"The {ctx.context.company.company_name} provide {ctx.context.company.service} services in market since {ctx.context.company.since}\n")
    
    async def on_agent_end(self, context: RunContextWrapper[Full_Context], agent: Agent, final_output: Any) -> None:
        print(f"✅ Agent '{agent.name}' finished. Output: {final_output}")
        print(f"The Total Employers work in company is {context.context.employer.strenght}\n")

    async def on_tool_start(self, context: RunContextWrapper, tool_name: str, agent:Agent) -> None:
        print(f"🛠️ Tool '{tool_name.name}' started with Agent: {agent.name}\n")

    async def on_tool_end(self, context: RunContextWrapper, tool_name: str, agent:Agent,result:str) -> None:
        print(f"✅ Tool '{tool_name.name}' Ended with Result: {result}\n")

    async def on_handoff(self, context: RunContextWrapper,from_agent:Agent ,to_agent:Agent) -> None:
        print(f"✅ Handoff! Agent {from_agent.name} transfer to the {to_agent.name} agent\n")

set_hooks = MyRunHooks()

@function_tool
def math_operation(num1:int,num2:int)->int:
          """ first number is a and second number is b
          sum both, substract both, multiply both, divide both
          give output of this two number is {answer}"""
          return num1 + num2 , num1- num2 ,num1 * num2 ,num1 / num2
          
    

company_data = Company_data_Type(company_name="Mecatron Solutions",service="Electrical",since=2013)
employer_strenght = Employers_type(strenght= 12)
full_context = Full_Context(company=company_data,employer=employer_strenght)

General_Agent = Agent(name="Helpful Assistant",
instructions="you are a helpful Assistant",
)

agent = Agent(name="Intelligent_agent ",
instructions=f"""You can do basic math calculations.Always use the tool for doing calculations and transfer general knowledge to general agent""",
model = model,
tools=[math_operation],
handoffs=[General_Agent])



async def main():
    result = await Runner.run(
        agent,
        hooks=set_hooks,
        input=f"what is 2 + 3?",
        run_config=config,
        context=full_context
        )
    print(f"Final Answer :{result.final_output}")

if __name__ == "__main__":
      asyncio.run(main())





# class TestHooks(RunHooks):
#      def __init__(self):
#           self.event_number = 0
#           self.name = "TestHooks"
#      async def on_agent_start(self,context:RunContextWrapper,agent:Agent) -> None:
#           self.event_number += 1
#           print(f"{self.name} {self.on_agent_start}:Agent {agent.name} started: Usage: {context.usage}")

# set_hooks = TestHooks()

# class TestHooks(RunHooks):
#     def __init__(self):
#         self.event_counter = 0

#     async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
#         self.event_counter += 1
#         print(f"*** Agent {agent.name} started. Usage: {context.usage}***")

# set_hooks = TestHooks()