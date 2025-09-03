from dataclasses import dataclass
from agents import (
    Agent,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled,Runner,enable_verbose_stdout_logging
)
from agents.run import RunConfig
from dotenv import load_dotenv
import os,asyncio

enable_verbose_stdout_logging()
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


helpful_agent = Agent(
    name="Assiatant",
    instructions="You are a helpful assistant",
)

science_Agent_clone = helpful_agent.clone(
    name="ScienceAgent",
    instructions="your are a Science Agent"
)

chef_Agent_clone = science_Agent_clone.clone(
    name="ChefAgent",
    instructions="your are a Chef Agent"
)

# result = Runner.run_sync(
#     starting_agent=helpful_agent,
#     input="where is karachi?",
#     run_config=config,)

# print(f"Helpful Agent:--> {result.final_output}")

# result = Runner.run_sync(
#     starting_agent=science_Agent_clone,
#     input="Explain Newton's second law in 4 lines.",
#     run_config=config,)

# print(f"Science Agent:--> {result.final_output}")

# result = Runner.run_sync(
#     starting_agent=chef_Agent_clone,
#     input="tell me about kitchen hygine in 5 lines",
#     run_config=config,)

# print(f"Chef Agent:--> {result.final_output}")


# ---------- Dynamic Cloning ----------


base_agent = Agent(
    name="BaseAgent",
    instructions="You are a helpful base agent. You can be cloned into different roles dynamically."
)

# Function for Dynamic Cloning

def create_dynamic_clone(user_role: str):
    """you make clone based on user prompt"""
    return base_agent.clone(
        name=f"{user_role} Agent",
        instructions =f"You are acting as a {user_role}. Answer queries as an expert {user_role}."
    )

while True:
    prompt = input("Enter role for agent (or type exit or quit): ")

    if prompt.lower() in ["exit","quit"]:
        break

    query = input(f"Enter your question for {prompt}: ")

    result = Runner.run_sync(
    starting_agent=create_dynamic_clone(prompt),
    input=query,
    run_config=config,)

    print(f"Agent:--> {result.final_output}")
    print(f"Last Agent Name:--> {result.last_agent.name}")