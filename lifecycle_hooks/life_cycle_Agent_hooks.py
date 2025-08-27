
from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI, function_tool,set_tracing_disabled,RunContextWrapper,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os ,asyncio
from agents.run import RunConfig
from agents import AgentHooks
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

@function_tool
def add(a:int,b:int)->int:
       """add this two number
       first is a and second is b
       give output the sum of this two number is {answer}"""
       return a + b

class MyAgentHooks(AgentHooks):
    async def on_start(self, context: RunContextWrapper,agent:Agent ) -> None:
        print(f"🟡 Agent started: {agent.name}")

    async def on_end(self, context, agent, output)->None:
         print(f"🔵 Agent Stoped :{agent.name}")
         
    async def on_tool_start(self, context, agent, tool)->None:
         print(f"🟡 Tool Invoked: {agent.name} Tool_Name: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result)->None:
         print(f"🟡 Tool Stoped :{agent.name} Tool_Name: {tool.name} Result:{result}")
    
    async def on_handoff(self, context, agent, source)-> None:
         print(f"Handoffs_from: {agent.name} To Handoffs_To: {source.name}")
         


company_data = Company_data_Type(company_name="Envision",service="Duct Cleaning",since=2017)
employers_data = Employers_type(strenght=52)

full_data = Full_Context(company=company_data,employer=employers_data)

General_Agent = Agent(name="Helpful Assistant",
instructions="you are a helpful Assistant",
)

agent = Agent(name="helpfull Assistant",
instructions="you are helpfull assistant.also you can use add tool if the user input according to tool if the question about general knowledge use general agent ",
model = model,
hooks=MyAgentHooks(),
tools=[add],
handoffs=[General_Agent])


async def main():
    result = await Runner.run(
        agent,
        input="2 + 2",
        run_config=config,
        context=full_data
        )
    print(result.final_output)

if __name__ == "__main__":
      asyncio.run(main())



# class TestHooks(RunHooks):
#     def __init__(self):
#         self.event_counter = 0

#     async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
#         self.event_counter += 1
#         print(f"*** Agent {agent.name} started. Usage: {context.usage}***")

# set_hooks = TestHooks()