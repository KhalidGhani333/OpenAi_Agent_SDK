import os
import chainlit as cl
from dotenv import load_dotenv
from agents.run import RunConfig
from agents import Agent ,Runner ,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()
set_tracing_disabled(disabled=True)
API_KEY = os.getenv("GEMINI_API_KEY")


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

agent = Agent(name="Assistant",instructions="you are helpful Assistant")



@cl.on_chat_start
async def welcome_message():
    await cl.Message(content="Welcome! How can I help you today?").send()


@cl.on_message
async def message_handler(message: cl.Message):
    # Placeholder message (bot is thinking)
    msg = cl.Message(content="")
    await msg.send()

    # Run the agent with only current user message as context (no memory)
    result = await Runner.run(agent, input=message.content, run_config=config)

    await cl.Message(content=result.final_output).send()

            