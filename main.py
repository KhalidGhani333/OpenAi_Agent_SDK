from agents import Agent , Runner , OpenAIChatCompletionsModel ,AsyncOpenAI ,set_tracing_disabled
import os
from dotenv import load_dotenv
from agents.run import RunConfig
import chainlit as cl
from openai.types.responses import ResponseTextDeltaEvent

# Disable tracing
set_tracing_disabled(disabled=True)

# Load environment variables
load_dotenv()

# Load Gemini API key
API_KEY = os.environ.get("GEMINI_API_KEY")

# Create external client
external_client = AsyncOpenAI(
    api_key = API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define the model and configuration
model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client
)

# Create the agent
agent = Agent(name="Assistant",instructions="you are a helpful assistant")


# Chainlit message handler
@cl.on_chat_start
async def handle_start():
    # set for history store
    cl.user_session.set("history",[])
    await cl.Message(content="👋 Hello! How Can I Help You Today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    # user_input = message.content
    
    # get history and store user message
    history = cl.user_session.get("history")
    history.append({"role":"user","content":message.content})

    msg = cl.Message(content=" ")
    await msg.send()

  # Call the agent to get a response
    result = Runner.run_streamed(agent, input = history, run_config=config)


    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)
    # set the chatbot response
    history.append({"role":"assistant","content": result.final_output})
    cl.user_session.set("history",history)

 # Send the result back to the user
    # await cl.Message(content=result.final_output).send()