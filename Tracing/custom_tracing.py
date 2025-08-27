# TracingProcessor sa hum custom class banata ha or TracingProcessor ek abstract class
# ha jis ki wala ja hama us ka sara method banana hu ga warna error aaya ga
#  

# import asyncio
# from agents import Agent, OpenAIChatCompletionsModel,Runner,trace,TracingProcessor,set_default_openai_api,set_trace_processors,enable_verbose_stdout_logging
# from dotenv import load_dotenv
# from openai import AsyncOpenAI
# import rich 
# import os

# load_dotenv()
# # enable_verbose_stdout_logging()
# set_default_openai_api("chat_completions") # Response ka upper chalta ha
# #-------------------
# my_model=OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=AsyncOpenAI(
#         api_key=os.getenv("GEMINI_API_KEY"),
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
#     )
# )
# #-------------------
# class MyTraceClass(TracingProcessor):
#     #jhot moot ka Database ha
#     def __init__(self):
#         self.traces = []
#         self.spans = []

#     def on_trace_start(self, trace):
#         # pass yaha main pass bhi likho do na to koi issue nahi ha q ka sirf hama method banana ha
#         self.traces.append(trace)
#         print(f"Trace started: {trace.trace_id}")

#     def on_trace_end(self, trace):
#         print(f"Trace Ended: {trace.export()}")

#     def on_span_start(self, span):
#         self.spans.append(span)
#         print(f"Span Started: {span.span_id}")
#         print(f"Span Details: ")
#         rich.print(span.export())

#     def on_span_end(self, span):
#         print(f"Span End: {span.span_id}")
#         print(f"Span Details: ")
#         rich.print(span.export())
    
#     def force_flush(self):
#         print("Forcing flush of trace data")

#     def shutdown(self):
#         print("========= Shutting down trace processor =========")
#         # Print all collected trace and span data
#         print("Collected Traces:")
#         for trace in self.traces:
#             print(trace.export())
#         print("Collected Spans:")
#         for span in self.spans:
#             print(span.export())

# #instance
# local_processor = MyTraceClass()
# set_trace_processors([local_processor])
# #-------------------

# agent = Agent(
#     name = "triage_agent",
#     instructions="you are a helpfull assistant",
#     model= my_model
# )


# async def main():
#     with trace("taha workflow"):
#         result = await Runner.run(agent,input="Hi, how is the weather of karachi?")
#         print(result.final_output)

# asyncio.run(main())


import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, Runner, trace, TracingProcessor, set_default_openai_api, set_trace_processors
from openai import AsyncOpenAI
import rich

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

# ------------------- Tracing -------------------
class MyTraceClass(TracingProcessor):
    def __init__(self):
        self.traces = []
        self.spans = []

    def on_trace_start(self, trace):
        self.traces.append(trace)
        print(f"[green]Trace started:[/green] {trace.trace_id}")

    def on_trace_end(self, trace):
        print(f"[red]Trace ended:[/red] {trace.export()}")

    def on_span_start(self, span):
        self.spans.append(span)
        print(f"[yellow]Span started:[/yellow] {span.span_id}")
        rich.print(span.export())

    def on_span_end(self, span):
        print(f"[blue]Span ended:[/blue] {span.span_id}")
        rich.print(span.export())

    def force_flush(self):
        print("[cyan]Forcing flush of trace data[/cyan]")

    def shutdown(self):
        print("========= Shutting down trace processor =========")
        print("Collected Traces:")
        for trace in self.traces:
            print(trace.export())
        print("Collected Spans:")
        for span in self.spans:
            print(span.export())

# Register processor
set_trace_processors([MyTraceClass()])

# ------------------- Agents -------------------
# Triage agent
triage_agent = Agent(
    name="triage_agent",
    instructions="You are a triage assistant. Decide whether the query is about weather or general chit-chat.",
    model=my_model
)

# Weather agent
weather_agent = Agent(
    name="weather_agent",
    instructions="You are a weather expert. Answer weather-related queries in detail with tips.",
    model=my_model
)

# Chit-chat agent
chat_agent = Agent(
    name="chat_agent",
    instructions="You are a friendly conversational assistant.",
    model=my_model
)

# ------------------- Input Guardrail -------------------
def input_filter(user_input: str) -> str:
    if "badword" in user_input.lower():
        return "Input rejected due to inappropriate language."
    return user_input

# ------------------- Runner -------------------
async def main():
    user_input = "Tell me about weather in Karachi"
    filtered_input = input_filter(user_input)

    with trace("main_workflow"):
        # First triage agent
        triage_result = await Runner.run(triage_agent, input=filtered_input)
        print("\n[bold green]Triage Result:[/bold green]", triage_result.final_output)

        # Route based on triage
        if "weather" in triage_result.final_output.lower():
            result = await Runner.run(weather_agent, input=filtered_input)
        else:
            result = await Runner.run(chat_agent, input=filtered_input)

        print("\n[bold cyan]Final Output:[/bold cyan]", result.final_output)

asyncio.run(main())
