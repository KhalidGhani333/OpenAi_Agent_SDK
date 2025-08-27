
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
import os

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_tracing_disabled(disabled=True)

async def main():
    agent = Agent(
        name= "Assistant",
        instructions="You are a helpful assistant",
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash",openai_client=client)
    )
    prompt = input("Enter your Prompt :")
    result = await Runner.run(agent,prompt)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())