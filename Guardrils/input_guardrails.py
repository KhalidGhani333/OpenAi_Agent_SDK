from pydantic import BaseModel
from agents import (
    Agent, 
    Runner, 
    AsyncOpenAI, 
    OpenAIChatCompletionsModel,
    GuardrailFunctionOutput,
    input_guardrail,
    RunContextWrapper,
    TResponseInputItem,
    InputGuardrailTripwireTriggered,
    set_tracing_disabled
    )
from dotenv import load_dotenv
from agents.run import RunConfig
import os ,asyncio

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/" )

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client )

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True )

# Define allowed input structure
class Maths_Agent(BaseModel):
    is_math_question :bool
    reasoning:str
    answer:str

maths_guardrail_agent = Agent(
    name="Math Guardrail Agent",
    instructions="Check user input if they ask about math related question answer them otherwise through sorry message",
    output_type=Maths_Agent,
    model=model )

@input_guardrail
async def maths_guardrail(
    ctx:RunContextWrapper[None],agent:Agent,input:str | list[TResponseInputItem])-> GuardrailFunctionOutput:
    result = await Runner.run(maths_guardrail_agent,input,context=ctx.context,run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= not result.final_output.is_math_question )


Mathamathical_agent = Agent("Mathamathical",
              instructions="You only answer Math related queries.",
              input_guardrails=[maths_guardrail],
              model=model )

async def main():
    try:
        response = await Runner.run(Mathamathical_agent, "what is the capital of pakistan?")
        print("Guardrails didn't trip ")
        print(response.final_output)
    except InputGuardrailTripwireTriggered as e :
        print("Math homework guardrail tripped :" , e)

if __name__ == "__main__":
    asyncio.run(main())