
# # Agent Level
# from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled
# from dotenv import load_dotenv
# import os,asyncio
# from agents.run import RunConfig


# load_dotenv()
# API_KEY = os.getenv("GEMINI_API_KEY")
# set_tracing_disabled(disabled=True)

# external_client = AsyncOpenAI(
#     api_key=API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )


# agent = Agent(name="Assistant",instructions="You are helpful assistant",
#               model=OpenAIChatCompletionsModel(model="gemini-2.0-flash",openai_client=external_client)
#        )
# async def main():
#     result = await Runner.run(agent,"what is 10 - 5 ?")
#     print(result.final_output)

# if __name__ == "__main__":
#       asyncio.run(main())

#------------------------------------------------------------
# Run Level 

# from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI
# from dotenv import load_dotenv
# import os,asyncio
# from agents.run import RunConfig

# load_dotenv()
# API_KEY = os.getenv("GEMINI_API_KEY")

# external_client = AsyncOpenAI(
#     api_key=API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#      model="gemini-2.0-flash",
#      openai_client=external_client
# )

# config = RunConfig(
#      model=model,
#      model_provider=external_client,
#      tracing_disabled=True
# )

# agent = Agent(name="Assistant",instructions="You are helpful assistant")

# async def main():
#     result = await Runner.run(agent,"what is 10 - 5 ?",run_config=config)
#     print(result.final_output)

# if __name__ == "__main__":
#       asyncio.run(main())

#------------------------------------------------------------
# Globel Level 

from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_default_openai_api,set_default_openai_client
from dotenv import load_dotenv
import os,asyncio
from agents.run import RunConfig

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_default_openai_client(external_client)

agent = Agent(name="Assistant",instructions="You are helpful assistant",model="gemini-2.0-flash")

async def main():
    result = await Runner.run(agent,"what is 10 - 5 ?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

#-------------------------------------------------------
# Gemini + OpenAI multi-agent example

# import asyncio
# import os
# from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
# from agents.run import RunConfig
# from dotenv import load_dotenv

# load_dotenv()
# API_KEY = os.getenv("GEMINI_API_KEY")


# openai_client = AsyncOpenAI()

# gemini_client = AsyncOpenAI(
#     api_key=API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# openai_agent = Agent(
#     name="openai Agent",
#     instructions="You are a helpful assistant using OpenAI GPT-4.",
#     model=OpenAIChatCompletionsModel(model="gpt-4o",openai_client=openai_client)
# )

# gemini_agent = Agent(
#     name="gemini Agent",
#     instructions="You are a helpful assistant using Google Gemini.",
#     model=OpenAIChatCompletionsModel(model="gemini-2.0-flash",openai_client=gemini_client)
# )

# gemini_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash",openai_client=gemini_client)

# gemini_config = RunConfig(model=gemini_model,model_provider=gemini_client)

# async def main():
#     print("\n--- Agent Level Execution ---\n")

#     result_1 = await Runner.run(openai_agent,"Explain recursion in 3 lines.")
#     print(f"🤖 OpenAI Agent Response:\n{result_1.final_output}\n")

#     result_2 = await Runner.run(gemini_agent,"Explain recursion in 3 lines.")
#     print(f"🤖 Gemini Agent Response:\n{result_2.final_output}\n")

#     print("\n--- Run Level Execution (Force Gemini for ALL Agents) ---\n")

#     # Now even OpenAI agent will respond with Gemini
#     result_3 = await Runner.run(openai_agent,"Explain recursion in 3 lines.",run_config=gemini_config)
#     print(f"🤖 OpenAI Agent (Forced Gemini) Response\n{result_3.final_output}\n")

# if __name__ == "__main__":
#     asyncio.run(main())