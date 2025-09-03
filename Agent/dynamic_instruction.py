from dataclasses import dataclass
from agents import (
    Agent,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled,Runner,RunContextWrapper
)
from agents.run import RunConfig
from dotenv import load_dotenv
import os,asyncio


load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

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

@dataclass
class UserInfo:
    name:str
    age:int
    ispremium:bool

def dynamic_instruction(context:RunContextWrapper[UserInfo],agent:Agent[UserInfo]) :
    # yaha database sy data lao or use karo
    return f"The user name is {context.context}.if the user is premium you also warm greet him.if user is not premium say him sir"
    
data = UserInfo(name="khalid",age=25,ispremium="no premium")

agent = Agent[UserInfo](
    name="Assiatant",
    instructions=dynamic_instruction,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="what is the user name?",
    run_config=config,
    context=data

)

print(result.final_output)