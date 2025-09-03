import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, ToolCallOutputItem, function_tool
from agents.run import RunConfig, RunResult
from openai import RateLimitError

#  Setup & Configuration

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in environment variables!")

# Gemini client (OpenAI-compatible endpoint)
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model configuration
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
)

#  Sub Agents

spanish_agent = Agent(
    name="Spanish Translator",
    instructions="Translate the user input into Spanish.",
    model=model
)

french_agent = Agent(
    name="French Translator",
    instructions="Translate the user input into French.",
    model=model
)

proofreader = Agent(
    name="Proofreader",
    instructions="Fix grammar and punctuation. Keep the meaning intact. "
                 "Reply only with the corrected text."
)

#  Tools

async def extract_json_payload(run_result: RunResult) -> str:
    """Extract JSON payload from agent output, fallback to {} if not found."""
    for item in reversed(run_result.new_items):
        if isinstance(item, ToolCallOutputItem) and item.output.strip().startswith("{"):
            return item.output.strip()
    return "{}"


@function_tool
async def proofread_text(text: str) -> str:
    """Fix grammar and punctuation; return corrected text."""
    result = await Runner.run(proofreader, text, max_turns=3)
    return str(result.final_output)



#  Main Agent (Orchestrator)

teacher_agent = Agent(
    name="Teacher",
    instructions=("Help students write clearly. Use tools when needed."
                  "If the input is unrelated to tools, answer normally as a helpful teacher."),
    tools=[
        proofread_text,
        spanish_agent.as_tool(
            tool_name="spanish_json",
            tool_description="Translate text to Spanish and return JSON payload only.",
            custom_output_extractor=extract_json_payload
        ),
        french_agent.as_tool(
            tool_name="french_json",
            tool_description="Translate text to French and return structured list payload."
        ),
    ],
    model=model
)

#  Runner with Retry Logic

def prompt() -> str:
    return "What is 2 + 2?"


async def safe_run():
    try:
            result = await Runner.run(
                starting_agent=teacher_agent,
                input=prompt(),
                run_config=config,
                max_turns=5   
            )
            return result
    except ValueError as e:
            print(f"Enter valid Input : {e}")

#  Entry Point

if __name__ == "__main__":
    final_result = asyncio.run(safe_run())
    print("\n✅ Final Output:", final_result.final_output)
    print("👤 Last Agent:", final_result.last_agent.name)
