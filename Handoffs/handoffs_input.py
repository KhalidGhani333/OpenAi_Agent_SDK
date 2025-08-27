from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, AsyncOpenAI, handoff, RunContextWrapper,function_tool
from agents.run import RunConfig
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from agents.extensions import handoff_filters


load_dotenv()
set_tracing_disabled(disabled=True)
API_KEY = os.environ.get("GEMINI_API_KEY")

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

@function_tool
def weather_tool(city:str) -> str:
    print("Weather tool Fire -- >")
    return f"{city} is Sunny 35℃"

# Input type for Cook Agent 
class CookAgentInput(BaseModel):
    reason: str
     # model_config = ConfigDict(strict=True) # Pydantic ka strict mode

# Callback jab handoff hota hai
async def cook_agent_callback(context: RunContextWrapper, input_data: CookAgentInput):
    print(f"Cook Agent handoff triggered with reason: {input_data.reason}")


# Math Agent (used as Cook Agent in this example)
math_agent = Agent(
    name="Mathematician",
    instructions="You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed.",
    handoff_description="This is a Math Teacher",
)

handoff_cook_agent = handoff(
    agent=math_agent,
    tool_name_override="cook_agent",
    tool_description_override="You are a cook agent",
    on_handoff=cook_agent_callback,
    input_type=CookAgentInput,
    input_filter=handoff_filters.remove_all_tools,
    is_enabled = True
)

# General Agent
general_agent = Agent(
    name="General Knowledge Assistant",
    instructions="You are a highly intelligent assistant capable of answering questions across all domains.",
    handoff_description="This is a General Knowledge Teacher",
)

# Physics Agent (used as Spanish Translator in this example)
physic_agent = Agent(
    name="Physicist",
    instructions="You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts.",
    handoff_description="This is a Physic Teacher"
)

handoff_spanish_agent = handoff(
    agent=physic_agent,
    tool_name_override="spanish_agent",
    tool_description_override="You are a Spanish translator agent",
    
)


triage_agent = Agent(
    name="triage agent",
    instructions=(
        "Help the user with their questions.\n"
        "- If they ask about maths, handoff to the cook agent.\n"
        "- If they ask about physics, handoff to the Spanish agent.\n"
        "- If they ask about general knowledge, answer yourself."
    ),
    handoffs=[handoff_cook_agent, handoff_spanish_agent],
    tools=[weather_tool]
)


result = Runner.run_sync(
    triage_agent, 
    "Calculate 453 + 947 and explain your steps.", 
    run_config=config)

print(f"\nLast Agent --->  {result.last_agent.name}")
print(f"Description ---> {result.last_agent.handoff_description}")
print(f"Final Output:\n{result.final_output}")
