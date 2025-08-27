
from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI, function_tool,set_tracing_disabled,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os
from agents.run import RunConfig


load_dotenv()
set_tracing_disabled(disabled=True)
API_KEY = os.getenv("GEMINI_API_KEY")
enable_verbose_stdout_logging()

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
    # temperature=0.2,        
    # top_p=0.95,
    # max_output_tokens=800,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
)


@function_tool()
def multiply(a:int,b:int) -> int:
       """multiply this two number
       first is a and second is b """
       print("Multiply Tool Fire ---->")
       return a * b

@function_tool()
def calculate_cbm(length_cm: float, width_cm: float, height_cm: float):
    """Calculate CBM (Cubic Meter) from dimensions in cm."""
    cbm = (length_cm * width_cm * height_cm) / 1_000_000
    return {"CBM": round(cbm, 4)}


# 2) Model configuration: yahan hum temperature/top_p set kar rahe hain.
#    Factual tasks me low temperature; creative tasks me high.
# model = OpenAIChatCompletionsModel(
#     model=model,    
#     temperature=0.2,        
#     top_p=0.95,
#     max_tokens=800,
# )

# 3) Agent instructions (system + role + few-shot + CoT prompt)
instructions = """
You are a Prompt Engineering Tutor (role). 
Goal: For any user query about prompts, explain the concept in Roman Urdu with:
1) short definition,
2) a clear example prompt (one-shot or few-shot as relevant),
3) a step-by-step explanation (Chain-of-Thought style),
4) one practical tip and one common mistake.

Always return output with these 4 labeled sections.
Be concise but clear.
"""

# 4) Few-shot examples to teach the pattern (few-shot prompting)
#    We pass them via the "examples" key in the agent's instructions area or embed in the instruction.
few_shot_examples = """
EXAMPLE 1:
Q: How to ask an LLM to summarise an article?
A:
1) Definition: ...
2) Example Prompt: "Summarize the following article in 3 bullet points: <article_text>"
3) Step-by-step: ...
4) Tip & Mistake: ...

EXAMPLE 2:
Q: How to get code explanation?
A:
1) Definition: ...
2) Example Prompt: "Explain this Python function line-by-line: <code>"
3) Step-by-step: ...
4) Tip & Mistake: ...
"""

# Combine instruction + few-shot so the agent sees pattern to follow
full_instructions = instructions + "\n\n" + few_shot_examples

# 5) Create Agent
prompt_agent = Agent(
    name="PromptEngTutorAgent",
    instructions=full_instructions,
    model=model,
    tools=[multiply,calculate_cbm],
    # optional: other control fields (like safety, max turns) -- leave default or configure as needed
)
user_query = (
    "Mujhe 'Chain-of-Thought' (CoT) samjhao roman urdu me. "
    "Example do jisme model ko maths ka simple sawal solve karwana ho "
    "(dono: short prompt & few-shot prompt), aur ek common mistake batao."
)
# 6) Runner to execute the agent
runner = Runner.run_sync(starting_agent=prompt_agent,input=user_query,run_config=config)

print(runner.final_output)


