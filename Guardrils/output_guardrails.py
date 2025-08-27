from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    set_tracing_disabled,
    RunConfig,
    output_guardrail,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    TResponseInputItem,
    RunContextWrapper,
    set_tracing_disabled
    
)
import os,asyncio
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

class Message_output(BaseModel):
    response :str

class Maths_Agent(BaseModel):
    is_math_question :bool
    response :str
    

maths_guardrails_agent = Agent(
    name="guardrails agent",
    instructions="Check user input if they ask about math related question answer them otherwise through sorry message",
    output_type=Maths_Agent,
    model=model
)

@output_guardrail
async def maths_guardrails(
    ctx:RunContextWrapper,agent:Agent,output:Message_output)-> GuardrailFunctionOutput:
    result = await Runner.run(maths_guardrails_agent,output.response,context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= not result.final_output.is_math_question
    )
main_agent = Agent(
    name="Maths Agent",
    instructions="You only answer Math related queries.",
    output_guardrails=[maths_guardrails],
    output_type=Message_output,
    model=model
)

async def main():
    try:
        response = await Runner.run(main_agent, "what is the capital of japan?")
        print("Guardrail didn't trip ")
        print(response.final_output)

    except OutputGuardrailTripwireTriggered as e:
        print("Math output guardrail tripped :", e)

if __name__=="__main__":
    asyncio.run(main())