from agents import Agent,Runner,OpenAIChatCompletionsModel,set_tracing_disabled,enable_verbose_stdout_logging
from agents.run import RunConfig
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import litellm
from openai import OpenAI

 
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()

external_client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# config = RunConfig(
#     model=model,
#     model_provider=external_client
# )

def main():
    print("Asking Gemini a question...\n")

    response = external_client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role":"system","content": "You are a helpful assistant."},
            {"role":"user" ,"content": "Explain the human body in 10 lines"}
        ]
    )

    message = response.choices[0].message.content
    print("💡 Gemini's Response:\n")
    print(message)

if __name__ == "__main__":
    main()