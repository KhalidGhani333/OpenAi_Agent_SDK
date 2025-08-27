

from agents import Agent,Runner, AsyncOpenAI, set_default_openai_api, set_default_openai_client,set_tracing_disabled
import os

API_KEY = os.environ.get("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_default_openai_client(external_client)

agent = Agent(name="Assistant",instructions="You are a helpful assistant", model = "gemini-2.0-flash")
prompt = input("Enter your Prompt :")
result = Runner.run_sync(agent,prompt)
print(result.final_output)