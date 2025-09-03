from typing import List, Optional
from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled ,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os , asyncio
from agents.run import RunConfig
from pydantic import BaseModel
from typing import Optional, List

load_dotenv()
set_tracing_disabled(disabled=False)
API_KEY = os.getenv("GEMINI_API_KEY")

enable_verbose_stdout_logging()
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client
)

# class ProductInfo(BaseModel):
#     name: str                           # Text
#     price: float                        # Decimal number
#     in_stock: bool                      # True/False
#     categories: List[str]               # List of text items
#     discount_percent: Optional[int] = 0 # Optional number, default 0
#     reviews_count: int                  # Whole number

# # Create product info extractor
# agent = Agent(
#     name="ProductExtractor",
#     instructions="Extract product information from product descriptions.",
#     output_type=ProductInfo
# )

# async def main():
#     # Test with product description
#     result = await Runner.run(
#         agent,
#         "The iPhone 15 Pro costs $999.99, it's available in electronics and smartphones categories, currently in stock with 1,247 reviews.",
#         run_config=config
#     )

#     print("Product:", result.final_output.name)         # "iPhone 15 Pro"
#     print("Price:", result.final_output.price)          # 999.99
#     print("In Stock:", result.final_output.in_stock)    # True
#     print("Categories:", result.final_output.categories) # ["electronics", "smartphones"]
#     print("Reviews:", result.final_output.reviews_count) # 1247
#     print("Discount:", result.final_output.discount_percent) # 1247


# if __name__ == "__main__":
#       asyncio.run(main())



class Ingredient(BaseModel):
    name: str
    amount: str
    unit: str

class NutritionInfo(BaseModel):
    calories_per_serving: Optional[int] = None
    prep_time_minutes: int
    cook_time_minutes: int
    
class Recipe(BaseModel):
    title: str
    description: str
    servings: int
    ingredients: List[Ingredient]
    instructions: List[str]
    nutrition: NutritionInfo
    cuisine_type: str
    dietary_tags: List[str]  # vegetarian, vegan, gluten-free, etc.


# Create recipe analyzer
recipe_analyzer = Agent(
    name="RecipeAnalyzer",
    instructions="Extract detailed recipe information from recipe text.",
    output_type=Recipe
)

# Test with recipe
recipe_text = """
Spaghetti Carbonara
A classic Italian pasta dish with eggs, cheese, and pancetta.
Serves 4 people. Prep time: 15 minutes, Cook time: 20 minutes. 

Ingredients:
- 400g spaghetti pasta
- 150g pancetta, diced
- 3 large eggs
- 100g Parmesan cheese, grated
- 2 cloves garlic, minced
- Black pepper to taste
- Salt for pasta water

Instructions:
1. Boil salted water and cook spaghetti according to package directions
2. Fry pancetta in a large pan until crispy
3. Beat eggs with Parmesan cheese in a bowl
4. Drain pasta and add to pancetta pan
5. Remove from heat and quickly mix in egg mixture
6. Serve immediately with extra Parmesan

Cuisine: Italian
Dietary notes: Contains gluten, dairy, and eggs
Approximate calories: 650 per serving
"""

result = Runner.run_sync(recipe_analyzer, recipe_text,run_config=config)

print(f"Over All: {result.final_output}\n")

print("=== Recipe Analysis ===")
print(f"Title:{result.final_output.title}")
print(f"Description:{result.final_output.description}")
print(f"Servings:{result.final_output.servings}")
print(f"Cuisine:{result.final_output.cuisine_type}")
print(f"Total Time:{result.final_output.nutrition.prep_time_minutes + result.final_output.nutrition.cook_time_minutes} minutes")


print("\nIngredients:")
for ing in result.final_output.ingredients:
    print(f"• {ing.amount}-{ing.unit} {ing.name}")

print("\nInstructions:")
for i, step in enumerate(result.final_output.instructions, 1):
    print(f"{i}. {step}")

print(f"\nDietary Tags: {', '.join(result.final_output.dietary_tags)}")
if result.final_output.nutrition.calories_per_serving:
    print(f"Calories per serving: {result.final_output.nutrition.calories_per_serving}")
