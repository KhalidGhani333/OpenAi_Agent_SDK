from agents import (
    Agent, 
    Runner, 
    AsyncOpenAI, 
    OpenAIChatCompletionsModel,
    SQLiteSession
    )

from dotenv import load_dotenv
from agents.run import RunConfig
import os
import asyncio
from dataclasses import dataclass
from pydantic import BaseModel

# enable_verbose_stdout_logging()
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise KeyError("Error 405: API key not found")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent = Agent(name="Assistant",
                  instructions= "",
                  tools=[],
)

session = SQLiteSession("conversation_123")

while True:

    prompt = input(" Write prompt :")

    if prompt == "exit":
        break

    
    result = Runner.run_sync(starting_agent=agent,
                              input="Hello",
                              run_config=config,
                              session=session
    )

    print(result.final_output)


