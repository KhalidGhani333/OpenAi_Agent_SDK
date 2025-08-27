from agents import Agent, RunContextWrapper,Runner,OpenAIChatCompletionsModel, function_tool,set_tracing_disabled,AsyncOpenAI,handoff,enable_verbose_stdout_logging
from agents.run import RunConfig
from dotenv import load_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

load_dotenv()
set_tracing_disabled(disabled=True)
API_KEY = os.environ.get("GEMINI_API_KEY")
# enable_verbose_stdout_logging()

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

@function_tool()
def addition(a:int,b:int)->int:
       """add this two number
       first is a and second is b """
       print("Add Tool Fire ---->")
       return a + b

math_agent =Agent(
    name="Mathematician",
    instructions=""" {RECOMMENDED_PROMPT_PREFIX} You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed.""",
    handoff_description="This is a Math Teacher",
    tools=[addition]
)

general_agent =Agent(
    name="General Knowledge Assistant",
    instructions="""{RECOMMENDED_PROMPT_PREFIX} You are a highly intelligent, confident assistant capable of answering questions "
        "across all domains including science, technology, history, philosophy, math, health, and more. "
        "Respond clearly and accurately, and if you're unsure about something, state that honestly.""",
    handoff_description="This is a General Knowledge Teacher"

)

physic_agent = Agent(
    name="Physicist",
    instructions="""{RECOMMENDED_PROMPT_PREFIX} You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts.""",
    handoff_description="This is a Physic Teacher"
)


def on_handoff_electrician(ctx:RunContextWrapper[None]):
    print(" Electrician Handoff Called")


def on_handoff_mechanic(ctx:RunContextWrapper[None]):
    print("Mechanic Handoff Called")
    


electrician_customize_agent = handoff(
    agent=math_agent,
    on_handoff=on_handoff_electrician,
    tool_name_override="Electrician_agent",
    tool_description_override="you are a general Electrician agent ")


mechanic_customize_agent= handoff(
    agent=physic_agent,
    on_handoff=on_handoff_mechanic,
    tool_name_override="Mechanic_agent",
    tool_description_override="you are a Mechanical agent")


triage_agent = Agent(
    name="Triage Agent",
    instructions="""
        You are a triage assistant. Your job is to decide if a query "
        "should be handled by a specialist agent.\n"
        "- If the question is about math, handoff to Electrician_agent.\n"
        "- If the question is about physics, handoff to Mechanic_agent.\n"
        "- Do NOT answer math or physics questions yourself.""",
handoffs=[electrician_customize_agent,mechanic_customize_agent,general_agent])


# triage_agent = Agent(
#     name="triage agent",
#     instructions=("Help the user with their questions."
#         "If they ask about maths, handoff to the maths agent."
#         "If they ask about physics, handoff to the physics agent."
#         "If they ask about general knowledge, handoff to the general agent."
#         ),
#     handoffs=[math_agent,general_agent,physic_agent]
# )


result = Runner.run_sync(triage_agent, "10 + 13 ?",run_config=config)
print(f"Handoffs to ---> {result.last_agent.name}")
print(f"Handoffs Description ---> {result.last_agent.handoff_description}")
print(result.final_output)
