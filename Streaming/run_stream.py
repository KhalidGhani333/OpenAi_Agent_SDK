import os
import chainlit as cl
from dotenv import load_dotenv
from agents.run import RunConfig
from agents import Agent ,Runner ,AsyncOpenAI,OpenAIChatCompletionsModel, function_tool,set_tracing_disabled,enable_verbose_stdout_logging
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
load_dotenv()
set_tracing_disabled(disabled=True)
API_KEY = os.getenv("GEMINI_API_KEY")
enable_verbose_stdout_logging()


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
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool
def add(a:int,b:int)->int:
       """add this two number
       first is a and second is b
       give output the sum of this two number is {answer}"""
       return a + b

math_agent = Agent(
    name="helpful math teacher",
    instructions="""you are a helpful math teacher""",
    handoff_description="i am math teacher",
    model=model,
    tools=[add])


main_agent = Agent(
    name="helpful Assistant",
    instructions="""you are a helpful Assistant""",
    handoffs=[math_agent],
    tools=[])

async def main():
    result = Runner.run_streamed(main_agent,"what is 2+2?",run_config=config)
    
    # async for event in result.stream_events():
    #     if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
    #         print(event.data.delta,end="",flush=True)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
            print(event.data.delta,end="")
            continue
        elif event.type == "agent_updated_stream_event":
            print(event.new_agent.name)
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "handoff_output_item":
                print(f"-----> {event.item.target_agent.name}")
            

if __name__ == "__main__":
    asyncio.run(main())


# async for event in result.stream_events():
#         if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
#             print(event.data.delta,end="")
#             continue
#         elif event.type == "agent_updated_stream_event":
#             print(event.new_agent.name)
#             continue
#         elif event.type == "run_item_stream_event":
#             if event.item.type == "tool_call_item":
#                 print("-- Tool was called")
#             elif event.item.type == "tool_call_output_item":
#                 print("-- Tool output Item")
#             elif event.item.type == "handoff_call_item":
#                 print("-- handoff_call_item --")
#             elif event.item.type == "handoff_output_item":
#                 print("-- handoff_output_item --")
#             elif event.item.type == "message_output_item":
#                 print("-- message_output_item --")
#             elif event.item.type == "reasoning_item":
#                 print("-- reasoning_item --")