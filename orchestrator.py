from agents import Agent,Runner,OpenAIChatCompletionsModel, function_tool,set_tracing_disabled,AsyncOpenAI,enable_verbose_stdout_logging
from agents.run import RunConfig
from dotenv import load_dotenv
import os , asyncio


# enable_verbose_stdout_logging()
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

@function_tool
def add(a:int,b:int)->int:
       """add this two number
       first is a and second is b
       give output the sum of this two number is {answer}"""
       return a + b

math_agent = Agent(
    name="Mathematician",
    instructions="You're an expert in mathematics. Solve math problems with step-by-step explanations.",
    tools=[add]
)

physic_agent = Agent(
    name="Physicist",
    instructions="You're an expert in physics. Answer physics questions clearly and accurately."
)

general_agent = Agent(
    name="General Knowledge Assistant",
    instructions=(
        "You're a generalist assistant. You can handle a wide range of queries including science, history, tech, health."
    )
)


orchestrator_agent = Agent(
    name="OrchestratorAgent",
    instructions=("""
        "You are the central coordinator. First, analyze the user's query."
        If the user asks about math → call math_agent.
        If the user asks about physic → call physic_agent.
        If the user asks about General Quries → call general_agent.
        
        """
    ),
    handoffs=[math_agent, physic_agent, general_agent,general_agent]
)

async def main():
    prompt = "what is 10 + 20 ?"

    if prompt == math_agent:
        result = await Runner.run(math_agent,prompt,run_config=config)
    elif prompt == physic_agent:
        result = await Runner.run(physic_agent,prompt,run_config=config)
    elif prompt == general_agent:
        result = await Runner.run(general_agent,prompt,run_config=config)
    else :
         result = await Runner.run(orchestrator_agent,prompt,run_config=config)
    
    print(result.final_output)
    print(result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())