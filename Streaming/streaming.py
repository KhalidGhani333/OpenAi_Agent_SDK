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

agent = Agent(name="Joker",instructions="you are helpful Assistant")


@cl.on_chat_start
async def welcome_message():
    cl.user_session.set("History",[])
    await cl.Message(content="Welcome! How can i help you today.").send()


@cl.on_message
async def message_handler(message:cl.Message):
    history = cl.user_session.get("History")
    history.append({"role":"user","content":message.content})

    msg = cl.Message(content = "")
    await msg.send()

    result = Runner.run_streamed(agent,input=history,run_config=config)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)

    history.append({"role":"assistant","content":result.final_output})
    cl.user_session.set("history",history)

    