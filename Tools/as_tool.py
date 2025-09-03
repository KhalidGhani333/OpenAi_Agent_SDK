from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os
from agents.run import RunConfig


load_dotenv()
# set_tracing_disabled(disabled=True)
API_KEY = os.getenv("GEMINI_API_KEY")
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

# Define a shopping assistant agent
# shopping_agent = Agent(
#     name="Shopping Assistant",
#     instructions="You assist users in finding products and making purchase decisions."
# )

# # Define a support agent
# support_agent = Agent(
#     name="Support Agent",
#     instructions="You help users with post-purchase support and returns."
# )

# shopping_tool = shopping_agent.as_tool(
#     tool_name="shopping_tool",
#     tool_description="Assists users in finding products and making purchase decisions."
# )
# support_tool = support_agent.as_tool(
#     tool_name="support_tool",
#     tool_description="Helps users with post-purchase support and returns."
# )

triage_agent = Agent(
     name="Triage Agent",
     instructions="You route user queries to the appropriate department.",
    #  tools=[shopping_agent,support_agent]
)

spanish_agent = Agent(
       name= "spanish agent",
       instructions="you translate the user input to spanish",
       model=model
)

french_agent = Agent(
       name="french agent",
       instructions="you translate the user input to french",
       model=model
)


orchestrator_agent = Agent(
    name="Orchestrator agent",
    instructions=(
        "you are a translator tool.you use the tool given to you to translate"
        "if ask for multiple translations,you call the relevent tool"
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate any input into Spanish only. Do not explain, just translate.",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate any input into French only.Do not explain, just translate."
        ),
    ],
   
)

def prompt()-> str :
    return "hello how are you? translate in spanish"


# agent = Agent(name="Assistant",instructions="you are helpful Assistant. i give you some tool if any prompt related to tool topic you must use that tool otherwise you answer the prompt according to prompt")

# Run the triage agent with a sample input
result = Runner.run_sync(starting_agent=orchestrator_agent, input= prompt() ,run_config=config)
print(result.final_output)
  



