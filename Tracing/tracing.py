import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel,Runner,trace,set_default_openai_api,set_default_openai_client,set_trace_processors
from agents.tracing.processor_interface import TracingProcessor # Base class jisko extend karke hum apna custom trace processor banaenge.
from pprint import pprint  # Pretty-printing for span detail output.

# ------------------- Setup -------------------
load_dotenv()
set_default_openai_api("chat_completions")

# Model
my_model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

class LocalTraceProcessor(TracingProcessor):
    def __init__(self):
        self.traces = []
        self.spans = []

# Trace ki trace_id print karta hai aur usay list mein add karta hai.
    def on_trace_start(self, trace):
        self.traces.append(trace)
        print(f"Trace started:---> {trace.trace_id}")

# Jab trace end hoti hai, woh export (JSON form) mein print hoti hai.
    def on_trace_end(self, trace):
        print(f"Trace ended:---> {trace.name}")

# Jab bhi koi action (jaise agent run) hota hai, toh span create hota hai.
    def on_span_start(self, span):
        self.spans.append(span)
        print(f"Span started:---> {span.span_id}")
        print(f"Span Details:--->")
        print(span.export())

# Jab woh span complete hota hai (e.g. tool ya agent ne reply de diya), toh end log hoti hai.
    def on_span_end(self, span):
        print(f"Span end:---> {span.span_id}")
        print(f"Span Details:--->")
        print(span.export())

# Jab app ya tracing band hoti hai toh yeh method call hota hai. Yeh sab stored data (traces + spans) ko print kar deta hai.
    def force_flush(self):
        print("----- Force Flush of Trace Data -----")

    def shutdown(self):
        print("=======Shutting down trace processor========")



# Gemini ka client banaya gaya hai. SDK ko bataya gaya ke tracing ke liye bhi isi client ka istemal ho.

set_default_openai_api("chat_completions")

# Apna custom tracing logic SDK ko de diya. Ab jitni bhi trace() ya Runner.run() calls hongi, yeh processor trigger hoga.
Local_Processor = LocalTraceProcessor()
set_trace_processors([Local_Processor])

# Example function to run an agent and collect traces
async def main():
    agent = Agent(name="Example Agent", instructions="Perform example tasks.", model=my_model)

    with trace("Khalid Workflow"):
        first_agent = await Runner.run(agent ,"what is sulfuric acid?")
        second_agent = await Runner.run(agent,f"Rate this result: {first_agent.final_output}")
        print(f"Result: {first_agent.final_output}")
        print(f"Rating: {second_agent.final_output}")

# Run the main function
import asyncio
asyncio.run(main())