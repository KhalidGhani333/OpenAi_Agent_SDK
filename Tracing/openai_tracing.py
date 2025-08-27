from agents import (Agent, 
                    Runner, 
                    RunContextWrapper, 
                    AsyncOpenAI, 
                    OpenAIChatCompletionsModel, 
                    RunConfig,
                    function_tool, 
                    enable_verbose_stdout_logging)
import os
from dotenv import load_dotenv


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
# enable_verbose_stdout_logging()

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please define it in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)


config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True)


@function_tool
def get_current_location(ctx: RunContextWrapper[None]) -> str:
    """Returns the user's current location."""
    # Dummy location for demonstration
    return "New York, USA"


@function_tool
def get_breaking_news(ctx: RunContextWrapper[None]) -> list[str]:
    """Returns a list of breaking news headlines."""
    return [
        "Global markets rally amid economic optimism.",
        "Major breakthrough in renewable energy announced.",
]

@function_tool
def explain_photosynthesis(ctx: RunContextWrapper[None]) -> str:
    """Explains the process of photosynthesis."""
    return "Photosynthesis is the process by which green plants use sunlight to synthesize foods from carbon dioxide and water."

@function_tool()
def multiply(a:int,b:int)->int:
       """multiply this two number
       first is a and second is b """
       print("Multiply Tool Fire ---->")
       return a * b

agent = Agent[None](
    name="multi_query_agent",
    instructions="Answer each query using the appropriate tools. MUST call TOOLS",
    tools=[get_current_location, get_breaking_news, explain_photosynthesis,multiply],
)


result = Runner.run_sync(
    agent,
    """
   give some breaking news
    """,
    run_config=config,
)

print("=" * 50)
print("Result: ", result.last_agent.name)
# print(result.new_items)
print("Result: ", result.final_output)