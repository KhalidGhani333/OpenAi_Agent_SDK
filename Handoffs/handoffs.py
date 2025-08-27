from agents import Agent,Runner,OpenAIChatCompletionsModel,set_tracing_disabled,AsyncOpenAI,handoff
from agents.run import RunConfig
from dotenv import load_dotenv
import os



load_dotenv()
set_tracing_disabled(disabled=False)
API_KEY = os.environ.get("GEMINI_API_KEY")

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

math_agent =Agent(
    name="Mathematician",
    instructions="You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed.",
    handoff_description="This is a Math Teacher"
)

general_agent =Agent(
    name="General Knowledge Assistant",
    instructions="You are a highly intelligent, confident assistant capable of answering questions "
        "across all domains including science, technology, history, philosophy, math, health, and more. "
        "Respond clearly and accurately, and if you're unsure about something, state that honestly.",
    handoff_description="This is a General Knowledge Teacher"

)

physic_agent = Agent(
    name="Physicist",
    instructions="You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts.",
    handoff_description="This is a Physic Teacher"
)

triage_agent = Agent(
    name="triage agent",
    instructions=("Help the user with their questions."
        "If they ask about maths, handoff to the maths agent."
        "If they ask about physics, handoff to the physics agent."
        "If they ask about general knowledge, handoff to the general agent."
        ),
    handoffs=[math_agent,general_agent,physic_agent]
)


result = Runner.run_sync(triage_agent, "what is 2+ 10?",run_config=config)
print(f"Handoffs to ---> {result.last_agent.name}")
print(f"Handoffs to ---> {result.last_agent.handoff_description}")
print(result.final_output)