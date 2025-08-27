from agents import (Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel,
                    input_guardrail,GuardrailFunctionOutput,RunContextWrapper,
                    TResponseInputItem,InputGuardrailTripwireTriggered,output_guardrail,
                    OutputGuardrailTripwireTriggered,enable_verbose_stdout_logging
                    )
from agents.run import RunConfig
from dotenv import load_dotenv
import os , asyncio
from pydantic import BaseModel


# enable_verbose_stdout_logging()
load_dotenv()
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
    model_provider=external_client,
    tracing_disabled=False
)

#input Guardrils
class Hotel_agent_type(BaseModel):
    is_irrelevant_query :bool
    reason:str

hotel_input_guardrils_agent = Agent(
    name="Hotel Customer Care Agent",
    instructions="""

Task:
    Check if the user query is related to Mughal Hotel or their owner,rooms, services, and guest care .
    If yes → return is_irrelevant_query = False.
    Otherwise return is_irrelevant_query = True.""",
    output_type=Hotel_agent_type,
    model=model
)

@input_guardrail
async def hotel_guardrils(
    ctx:RunContextWrapper[None],agent:Agent,input:str|list[TResponseInputItem])-> GuardrailFunctionOutput:
    result = await Runner.run(hotel_input_guardrils_agent,input,context=ctx.context,run_config=config)
    print(f"Hotel Guardrials Input -- >{result.final_output}")
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.is_irrelevant_query
    )

#Output Guardrails
class Hotel_Output_Type(BaseModel):
    is_output_not_related_to_hotel : bool
    reason :str

hotel_output_guardrils_agent = Agent(
    name="output Guardrails",
    instructions="""Check if the assistant's answer is appropriate and safe to show the user. 
    check if the output related to Mughal hotel """,
    output_type=Hotel_Output_Type,
    model=model
)

@output_guardrail
async def hotel_output_guardrials(ctx:RunContextWrapper[None],agent:Agent,output:Hotel_Output_Type)->GuardrailFunctionOutput:
    result = await Runner.run(hotel_output_guardrils_agent,output,context=ctx.context)
    print(f"Hotel Guardrials Output -- >{result.final_output}")
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.is_output_not_related_to_hotel
    )


main_agent = Agent(
    name="helpful Assistant",
    instructions="""you are a helpful customer care mughal hotel agent.
    Mughal Hotel is located in Karachi.
    The owner of Mughal Hotel is Khalid Ghani.
    Mughal Hotel provides rooms, services, and guest care.
""",
     input_guardrails=[hotel_guardrils],
     output_guardrails=[hotel_output_guardrials]
)

async def main():
    try:
        result = await Runner.run(main_agent,"i book 1 room in mughal hotel?",run_config=config)
        print(result.final_output)
        print(result.last_agent.name)
    except InputGuardrailTripwireTriggered as e:
        print(f"🚨 Guardrail tripped: irrelevant query detected! : {e}")
    except OutputGuardrailTripwireTriggered as e :
        print(f"🚨 Guardrail tripped: irrelevant response detected! : {e}")



if __name__ == "__main__":
    asyncio.run(main())